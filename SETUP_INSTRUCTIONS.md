# OctopiX API Setup Instructions

Follow these steps to get the API up and running on your local machine.

## Prerequisites

1.  **Python 3.8+**: Ensure Python is installed.
2.  **PostgreSQL**: Ensure PostgreSQL is installed and running on `localhost:5432`.
    - Default credentials used: `postgres` / `123`.
    - Database name: `postgres`.
    - If your credentials differ, update `web_api/database.py`.

## Setup Steps

1.  **Open Terminal** in the `oct-api-main` directory.

2.  **Create Virtual Environment** (if not already created):
    ```powershell
    python -m venv venv
    ```

3.  **Activate Virtual Environment**:
    ```powershell
    .\venv\Scripts\Activate
    ```

4.  **Install Dependencies**:
    ```powershell
    pip install -r requirements.txt
    ```

5.  **Run the API**:
    Navigate to the root directory (if not already there) and run:
    ```powershell
    uvicorn web_api.main:app --reload
    ```
    
    *Alternatively, run from inside `web_api` directory:*
    ```powershell
    cd web_api
    uvicorn main:app --reload
    ```

6.  **Verify**:
    Open your browser and navigate to: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
    You should see the Swagger UI.

## Troubleshooting

-   **Database Connection Error**: verify your PostgreSQL service is running and credentials in `web_api/database.py` match your setup.
-   **Port in Use**: If port 8000 is occupied, run on another port:
    ```powershell
    uvicorn web_api.main:app --reload --port 8001
    ```


The Solution: 
web_api/utils.py
We created a custom JSON validation step that runs before your data reaches the main API logic.

1. The Custom Hook (
_duplicate_key_checker
)
This is the core logic. When Python's 
json
 library parses a string, it creates a list of pairs like [("username", "alice"), ("username", "bob")].

We use the object_pairs_hook feature of json.loads to intercept this list.

python
def _duplicate_key_checker(ordered_pairs):
    cleaned_dict = {}
    for key, value in ordered_pairs:
        # CHECK: Have we seen this key before in this object?
        if key in cleaned_dict:
            # YES: Stop everything and raise an error!
            raise ValueError(f"Duplicate key detected: '{key}'")
        
        cleaned_dict[key] = value
    return cleaned_dict
2. The Dependency (
verify_unique_keys
)
This is a FastAPI "Dependency" function. It is designed to inspect the Request object directly.

Step A: Check Method: We only care about POST, PUT, or PATCH. GET requests usually don't have bodies.
Step B: Read Raw Body: We access await request.body(). This gives us the raw bytes (e.g., b'{"username": "alice", "username": "bob"}') before FastAPI has tried to parse it into your Pydantic schemas.
Step C: Parse with our Hook:
python
json.loads(..., object_pairs_hook=_duplicate_key_checker)
This forces the standard JSON parser to use our logic from Step 1.
Step D: Handle Errors: If Step 1 raises a ValueError, we catch it and convert it into a 422 Unprocessable Entity HTTP error, which is sent back to the client immediately.
how it is Connected: 
web_api/main.py
In 
main.py
, we added this line:

python
app.include_router(user.router, dependencies=[Depends(verify_unique_keys)])
dependencies=[...]: This tells FastAPI: "Before running any function in the user.router, run this list of functions first."
Depends(verify_unique_keys): This executes our logic.
The Flow:

Request Arrives -> POST /user
FastAPI sees Dependency -> Calls 
verify_unique_keys
verify_unique_keys -> Reads body, checks for duplicates.
If Duplicates: Raises 422 Error. Request ENDS here.
If Clean: Returns successfully.
FastAPI continues -> Parses data into schemas.User.
Path Operation -> Calls 
createuser
 in 
routers/user.py
.
