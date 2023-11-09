# User Portal

## Setup & Run

1. Install dependencies:
```bash
pip install -r requirements.txt
```
2. Set up the .env file with your database credentials.
3. Run the application:
```bash
uvicorn app.main:app --reload
```
## API Endpoints

- POST /register/: Register a new user.
- GET /users/{user_id}: Get user details by ID.