# Your Happiness - Arabic Sentiment Analysis Web Application

**Author:** Gaith Hani Swaidan  
**Supervisor:** Eng. Mohammed al-heileh  

## Description
A web application that processes Arabic text sentences written by the user and determines their emotional state (Happy, Sad, or Neutral) using set-based string matching and emotion word ratios. The application tracks each user's history of analyses and displays it securely on their personal dashboard.

## Features
- **User Authentication:** Secure user registration and login utilizing JSON Web Tokens (JWT). Includes strong password enforcement and email validation.
- **Sentiment Analysis Engine:** Real-time Arabic text evaluation based on predefined categories of emotion-based keywords.
- **Personalized History:** Logged-in users can browse their past text inputs alongside calculated sentiment percentages.
- **Responsive UI:** Clean, vanilla frontend utilizing modern HTML/CSS with JavaScript API integrations.

## Technologies
- **Frontend:** HTML5, CSS3, Vanilla JavaScript
- **Backend:** Python 3, Flask REST API
- **Database:** PostgreSQL
- **ORM & Migrations:** SQLAlchemy Core, Alembic
- **Security:** Password Hashing, JWT Token Protection, CORS enabled

## Setup Instructions

### Prerequisites
- Python 3.8+ installed
- PostgreSQL installed and running locally

### 1. Database Setup
Ensure your local PostgreSQL server is running. Create a new database named `happiness_db`.
```sql
CREATE DATABASE happiness_db;
```
*(Note: If you are using different credentials than the defaults, update the `DATABASE_URL` in `app/db.py` or export it as an environment variable).*

### 2. Environment Setup
Navigate to the project directory and set up a Python virtual environment:
```bash
# Navigate to the project directory
cd happy_web

# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install required dependencies
pip install flask flask-cors sqlalchemy psycopg2-binary alembic pyjwt bcrypt
```

### 3. Run Database Migrations
Initialize the database tables (`users`, `sentiments`, `words`) using Alembic:
```bash
alembic upgrade head
```

### 4. Seed the Database
Seed the dictionary of Arabic words used for the sentiment analysis engine:
```bash
python -m app.seed_words
```

### 5. Start the Backend Server
Run the Flask application backend:
```bash
python -m app.main
```
The REST API server will start on `http://localhost:5000`.

### 6. Run the Frontend
Since the frontend uses vanilla HTML/JS and relies on a REST API, you can serve it using any simple local server. For example, using Python's built-in HTTP server:
```bash
# In a new terminal, from the project root:
python -m http.server 8000
```
Then navigate to `http://localhost:8000/templates/login.html` in your web browser.

## Project Structure
- `app/` - Contains the Flask backend API (`main.py`), database connection logic (`db.py`), ORM models (`models.py`), authorization (`auth.py`), and sentiment logic (`sentiment.py`).
- `alembic/` & `alembic.ini` - Database schema migrations configuration.
- `templates/` - Frontend HTML views (`login.html`, `register.html`, `analyze.html`, `history.html`, etc.).
- `static/` - Shared frontend assets containing the API interface (`app.js`) and stylesheets (`style.css`).
- `app/words.json` - Raw JSON dictionary containing the categorized Arabic words used for initial seeding.

## How It Works
1. The user registers or logs in securely to obtain an authorization token.
2. The user inputs an Arabic text prompt on the "Analyze" page.
3. The prompt is sent to the backend, stripped, and checked against the lists of happy, sad, and neutral words in the database.
4. Sentiment ratios are calculated to dictate the overarching emotional state.
5. The result is logged into the user's history and visualized instantly in the browser.
