# Docker Guide for OctopiX API

## Prerequisite: Database Connection
If your PostgreSQL database is running on your **local machine** (Windows), the container cannot access it via `localhost`.
Use `host.docker.internal` instead of `localhost` when running the container.

---

## 1. Build the Docker Image
First, build the image from the project root directory.

```bash
docker build -t octopix-api:latest .
```

---

## 2. Run Locally (Test)
To test if it works, run a container. We use `-e DATABASE_URL` to override the localhost connection string.
(Replace `postgres:123` with your actual DB credentials if different).

```bash
docker run -d -p 8000:8000 --name octopix-api \
  -e DATABASE_URL="postgresql://postgres:123@host.docker.internal:5432/postgres" \
  octopix-api:latest
```

*   `-d`: Detached mode (runs in background).
*   `-p 8000:8000`: Maps container port 8000 to host port 8000.
*   `--name`: Assigns a name to the container.

**Verify it works:**
Open `http://localhost:8000/docs` in your browser.

---

## 3. Push to Docker Registry (e.g., Docker Hub)

### Step A: Login
Login to your Docker Hub account in the terminal.
```bash
docker login
```

### Step B: Tag the Image
You must tag the image with your Docker Hub username.
Replace `yourusername` with your actual Docker Hub username.

```bash
docker tag octopix-api:latest yourusername/octopix-api:v1.0
```

### Step C: Push
Upload the image to the registry.
```bash
docker push yourusername/octopix-api:v1.0
```

---

## 4. Pull and Run (From Registry)
To simulate running on another machine (or just testing the pull), first stop/remove the old container and image if you want a clean slate.

```bash
# Stop and remove existing container
docker stop octopix-api
docker rm octopix-api

# Pull the image
docker pull yourusername/octopix-api:v1.0

# Run it
docker run -d -p 8000:8000 --name octopix-api-pulled \
  -e DATABASE_URL="postgresql://postgres:123@host.docker.internal:5432/postgres" \
  yourusername/octopix-api:v1.0
```

---

## 5. Export and Import (Offline Transfer)
If you cannot use a registry (e.g., air-gapped system), you can save the image to a file.

### Step A: Export (Save to File)
Save the image `octopix-api:latest` to a tar file.

```bash
docker save -o octopix-api.tar octopix-api:latest
```
This creates a file named `octopix-api.tar` in your current directory. You can copy this file to another machine.

### Step B: Import (Load from File)
On the target machine, load the image from the file.

```bash
docker load -i octopix-api.tar
```

### Step C: Run the Imported Image
```bash
docker run -d -p 8000:8000 --name octopix-offline \
  -e DATABASE_URL="postgresql://postgres:123@host.docker.internal:5432/postgres" \
  octopix-api:latest
```
