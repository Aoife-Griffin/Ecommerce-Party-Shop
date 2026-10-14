# Full-Stack Party E-Commerce Shop

A complete full-stack e-commerce demo store built to demonstrate proper backend engineering, secure checkout workflows, automated testing, and containerised deployments. The skeleton of the project was from a faulty ecommerce made in second year of university that I fixed up.

## Key  Features

This project was built from the ground up to follow enterprise security and development standards:

*   **Secure Checkout Snapshot Design:** When a customer checks out, the application locks in the product names and prices at the time of purchase. This keeps past order financial history completely safe, even if an admin changes a product's price in the database later.
*   **Environment-Based Security:** Application details like database keys, debug flags, and hosting boundaries are completely separate from the source code. They are safely pulled from the host system environment variables.
*   **Automated Continuous Integration (CI):** An automated testing pipeline is built using GitHub Actions. Every single time code is pushed to GitHub, a remote cloud server automatically runs a suite of tests to verify core security rules.
*   **Production Static File Asset Pipeline:** The application uses WhiteNoise middleware to compress and serve CSS, JavaScript, and user-uploaded media files efficiently, making the system fast and stable in production environments.

## Technology Stack

*   **Language:** Python 3.12+
*   **Web Framework:** Django 5.1 (utilising built-in secure PBKDF2 password hashing)
*   **Frontend Layout:** Bootstrap 5, HTML5 Templates, and jQuery AJAX
*   **Database Engine:** SQLite (Local Sandbox development) / Compatible with PostgreSQL
*   **DevOps/CI Framework:** Docker Containers, GitHub Actions CI Pipelines

## Automated Test Validation

The application contains a dedicated testing framework to catch bugs early. You can run the entire automated verification suite locally by running:

```bash
python manage.py test
```

### Main Testing Scenarios Covered:
1.  **Catalog Context Delivery:** Confirms the store front page pulls catalog data rows successfully from the database without causing crashes.
2.  **Case-Insensitive Search Queries:** Verifies that database text search lookups accurately return matching items regardless of mismatched uppercase or lowercase user inputs.
3.  **Authentication Middleware Security:** Confirms that unauthenticated visitors are blocked and gracefully redirected to the login screen when trying to access private screens like order tracking history.
4.  **Data Profile Isolation Guardrails:** Security test ensuring that logged-in users can only view their own unique personal transaction history records, strictly blocking cross-user profile data leakage.

## Local Installation & Sandbox Setup

Follow these simple steps to run this application on your local computer:

### Standard Installation
1.  Clone this repository to your computer:
    ```bash
    git clone https://github.com
    cd Ecommerce-Party-Shop
    ```
2.  Initialize a fresh Python virtual environment and install the required dependencies:
    ```bash
    python -m venv env
    # Activate on Windows:
    env\Scripts\activate
    # Activate on Mac/Linux:
    source env/bin/activate
    
    pip install -r requirements.txt
    ```
3.  Apply the relational database migrations and create your administrator login profile:
    ```bash
    python manage.py migrate
    python manage.py createsuperuser
    ```
4.  Launch the local development engine web server:
    ```bash
    python manage.py runserver
    ```
    Open `http://127.0.0` in your favorite web browser to explore the store!

---

###  Running via Docker (Containerised Deployment)
If you have Docker Desktop installed, you can build and launch the entire project instantly inside an isolated container with one simple terminal command:

```bash
docker-compose up --build
```
Once the container finishes building, navigate to `http://localhost:8000` to browse the live shop sandbox.

-
*Note: This repository is a technical project showcase. No live financial payment routing operations or physical package distributions take place inside this project.*
