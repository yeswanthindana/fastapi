# Simple Web UI for API Testing

This is a simple HTML/CSS/JS frontend to test the APIs.

## How to specificy the API URL
The API URL is pre-filled as `http://127.0.0.1:8000`. If your API is running somewhere else, just update the "Base URL" input field at the top of the page.

## How to Run it
1. Ensure your backend API is running (e.g., `uvicorn web_api.main:app --reload`).
2. Simply open `index.html` in your browser.
3. You should see "API Tester".
4. Use the forms to Create, Read, Update, and Delete data for Users, Roles, and Organizations.

## Notes
- CORS is enabled in the backend (`web_api/main.py`) to allow this page to communicate with the API.
- All errors are logged to the console (F12) and also displayed in the output boxes.
