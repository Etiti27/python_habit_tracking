# Habit Tracker Application

A Flask-based habit tracker application with PostgreSQL as the database. The app allows users to create, track, and analyze habits with different frequencies (e.g., daily, weekly). Docker is used to containerize the application for consistent development and production environments.

## Table of Contents

- [Technologies Used](#technologies-used)
- [Setup](#setup)
- [Running the Application](#running-the-application)
- [Environment Variables](#environment-variables)
- [API Endpoints](#api-endpoints)


## Technologies Used

- **Flask** - Python web framework
- **PostgreSQL** - Relational database for data persistence
- **Docker & Docker Compose** - Containerization for easy deployment
- **Flask-Login** - User authentication management
- **psycopg2** - PostgreSQL adapter for Python

## Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Etiti27/python_habit_tracking.git
   
2. **Create environment variables in the project directory: **
   example ".env" file
   `````.env
   HOST=db 
   DB_NAME=python_project_second
   DB_USER=postgres
   DB_PASSWORD=Obinna27
   SECRET_KEY=your_secret_key
   DEBUG=True
   


3. **Run docker file with docker-compose**
   ```bash
   docker-compose up --build
    
4. **access point**
   ```url
   http://0.0.0.0:3002/

5. **API Endpoints**
   ````endpoints

   GET / - Homepage
   POST /login - User login
   GET /daily_habit - Display daily habits
   POST /add_daily_habit - Add a new daily habit
   GET /weekly_habit - Display weekly habits
   POST /add_weekly_habit - Add a new weekly habit
   POST /checkoff - Mark a habit as completed

6. **to run test suite**
   in the project directory, run the command
   ```bash
   python3 test_script.py

