FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
# Ensure .dockerignore handles excluding venv/ and __pycache__ if they exist, but COPY . . is usually fine for small projects
COPY . .

# Expose port
EXPOSE 8000

# Run the app
CMD ["uvicorn", "web_api.main:app", "--host", "0.0.0.0", "--port", "8000"]
