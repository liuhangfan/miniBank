# miniBank

miniBank is a simple banking application developed in Python using Flask. It supports basic banking operations such as balance checks and funds transfers between accounts.

## Features

- **User Authentication**: Secure login and token generation using JWT.
- **Account Management**: Users can check balances and transfer funds securely.
- **Security**: Implements CSRF protection and rate limiting to safeguard against common web threats.

## Installation

To set up the miniBank project, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/liuhangfan/miniBank
   ```
2. Navigate to the miniBank directory
3. Install dependencies: ```pip install -r requirements.txt```
3. Initialize the database (if needed)
4. Run the application: ```flask run```

## Configuration
Ensure that the app.config['SECRET_KEY'] is set to a secure random value.

## Usage
After starting the application, navigate to http://localhost:5000 in your web browser to start using miniBank.

## Implementation Introduction

### Technology Stack

- **Python**: The primary programming language used for backend development.
- **Flask**: A lightweight web framework for building web applications in Python.
- **JWT (JSON Web Tokens)**: Used for user authentication and session management.
- **SQLite**: The database engine for storing user account information and transaction data.

### Design Principles

- **Security**: We prioritize security in every aspect of our implementation. From user authentication to database operations, security is at the forefront of our design choices.
- **Simplicity**: We believe in keeping things simple and straightforward. Our codebase is structured in a way that promotes readability and maintainability.

### Features Overview

- **User Authentication**: Users can securely log in to their accounts using JWT authentication.
- **Account Management**: Account holders can check their balances and transfer funds between accounts seamlessly.
- **Robust Error Handling**: We've implemented robust error handling mechanisms to ensure the application remains stable and resilient in the face of unexpected issues.
- **Logging and Monitoring**: Logging is an integral part of our implementation. We log important events and errors to facilitate debugging and monitoring.
