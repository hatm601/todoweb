# To-Do List Maker (Flask Web App)

This is a simple To-Do List web application built with Flask, SQLAlchemy, and SCSS.

## Features

- Add, edit, and delete tasks
- Tasks are stored in a local SQLite database
- Responsive UI styled with SCSS
- No internet connection required (works offline)
- Easy to run locally
- Login page to make different to-do lists

## Requirements

- Python 3.8+
- Flask
- Flask-SQLAlchemy
- Flask-Scss
- pyScss

## Setup

1. **Clone the repository:**
   ```
   git clone <your-repo-url>
   cd webproject
   ```

2. **Create a virtual environment (optional but recommended):**
   ```
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```
   pip install Flask Flask-SQLAlchemy Flask-Scss pyScss
   ```

4. **Run the app:**
   ```
   python main.py
   ```
   The app will be available at [http://localhost:5000](http://localhost:5000).

## Project Structure

```
webproject/
├── main.py
├── static/
│   ├── scss/
│   │   └── style.scss
│   └── style.css
├── templates/
│   |-- base.html
│   |-- index.html
│   |-- edit.html
|   |-- login.html
|   instances/ 
├── |--database.db
├── README.md
└── .gitignore
```

## License

MIT License