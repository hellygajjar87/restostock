  # Restaurant Inventory Management System

  A professional inventory management system for restaurants, built with Django and Tailwind CSS.

  ## Running the Project

  ### 1. Prerequisites
  Ensure you have Python installed.

  ### 2. Activate Virtual Environment
  ```bash
  # Windows
  .\venv\Scripts\activate

  # macOS/Linux
  source venv/bin/activate
  ```

  ### 3. Run the Development Server
  Navigate to the `backend` directory and start the server:
  ```bash
  cd backend
  python manage.py runserver
  ```

  ### 4. Access the Application
  Open your browser and go to: [http://127.0.0.1:8000](http://127.0.0.1:8000)

  ## Additional Commands

  ### Seed Data
  If you need to populate the database with initial restaurant data:
  ```bash
  python seed_data.py
  ```

  ### Create Admin User
  ```bash
  cd backend
  python manage.py createsuperuser
  ```