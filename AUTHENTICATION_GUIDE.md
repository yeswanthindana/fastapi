# Octo-API Authentication & Authorization Guide

This project is a FastAPI-based backend system with a robust, enterprise-grade authentication and authorization flow. This document explains the **What**, **Why**, and **How** of the implementation, specifically for beginners.

---

## 1. The Core Components

We use three main technologies to secure this API:
1.  **Bcrypt**: For securely hashing and storing passwords.
2.  **JWT (JSON Web Tokens)**: For creating "identification cards" that users use to access protected data.
3.  **OAuth2 (Password Bearer)**: The standard "handshake" protocol that FastAPI uses to manage logins and tokens.

---

## 2. Step-by-Step Implementation Flow

### Phase A: Secure Password Storage (`hash.py`)
**The Problem**: We never store passwords in plain text. If the database is stolen, plain text passwords would be a disaster.
**The Solution**: We "hash" the password. A hash is a one-way mathematical function. You can turn "password123" into a hash, but you cannot turn the hash back into "password123".

*   **Implementation**: In `web_api/hash.py`, we use the `bcrypt` library.
*   **Code logic**: 
    1.  We SHA-256 hash the password first (to avoid bcrypt's 72-character limit).
    2.  We use `bcrypt.hashpw` with a random "salt" to generate the secure string stored in the DB.
    3.  During login, we use `bcrypt.checkpw` to see if the provided password matches the stored hash.

### Phase B: Token Generation (`jwt_token.py`)
**The Problem**: Once a user logs in, we don't want them to send their username/password with *every single request*.
**The Solution**: We give them a temporary "Access Token" (JWT).

*   **JWT Structure**: A JWT is a string (e.g., `eyJhbGci...`) that contains the user's ID and an expiration date.
*   **Security**: The token is digitally signed using a `SECRET_KEY`. If someone tries to change the email inside the token, the signature becomes invalid, and the API rejects it.

### Phase C: The Login Handshake (`routers/authentication.py`)
This is the entry point. When a user hits the `/login` endpoint:
1.  They provide their Email and Password via an `OAuth2PasswordRequestForm`.
2.  The server verifies the user exists and the password hash matches.
3.  If successful, the server calls `jwt_token.create_access_token` and returns a JSON response:
    ```json
    {
      "access_token": "...",
      "token_type": "bearer"
    }
    ```

### Phase D: Global Protection (`main.py` & `oauth2.py`)
Instead of manually checking for a token in every single function, we use **FastAPI Dependencies**.

*   **`oauth2.py`**: This file contains a function `get_current_user`. It extracts the token from the request header, verifies it, and returns the user's email.
*   **Global Enforcement**: In `web_api/main.py`, we register our routers with the dependency:
    ```python
    app.include_router(user.router, dependencies=[Depends(oauth2.get_current_user)])
    ```
    This one line ensures that **every** endpoint inside the `user` router is now locked behind a login.

---

## 3. Code-Level Directory Structure

| File | Purpose |
| :--- | :--- |
| `hash.py` | Contains the `Hash` class for encryption logic. |
| `jwt_token.py` | Logic to sign and verify the tokens. |
| `oauth2.py` | The "Security Guard" dependency used by our routes. |
| `schemas.py` | Pydantic models for `Token` and `TokenData` response formats. |
| `routers/authentication.py` | The actual `/login` endpoint logic. |
| `main.py` | The glue that connects everything and enforces security. |

---

## 4. How to Test & Use (Browser Guide)

1.  **Run the Server**: `uvicorn web_api.main:app --reload`
2.  **Open Docs**: Go to `http://localhost:8000/docs`.
3.  **The Locker Icon**: You will see a "padlock" icon next to protected routes (`/user`, `/role`, etc.).
4.  **Authorize**:
    *   Click the big **"Authorize"** button at the top.
    *   Enter a valid email and password.
    *   FastAPI will automatically send these to `/login` and store the token in your browser session.
5.  **Try it out**: Now, when you call `GET /user/all`, the browser automatically adds the header: `Authorization: Bearer <your_token>`.

---

## 5. Summary for Beginners
*   **Authentication** = "Who are you?" (The Login process).
*   **Authorization** = "Are you allowed to see this?" (The Dependency check).
*   **Bearer Token** = "I am carrying (bearing) this token to prove I was already authenticated."
