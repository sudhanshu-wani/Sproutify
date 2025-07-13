# Sproutify Emotion Detection - Setup Guide

Welcome to the Sproutify Emotion Detection project! This guide will help you set up everything from scratch.

---

## 1. Prerequisites

- **Windows 10/11** (instructions are similar for Mac/Linux)
- **VSCode** (Visual Studio Code)
- **Python 3.8+**
- **Git**

---

## 2. Install Required Tools

### a. Install Git
- Download from: https://git-scm.com/downloads
- Run the installer and follow the default steps.
- To check if Git is installed, open Command Prompt or PowerShell and run:
  ```
  git --version
  ```

### b. Install Python
- Download from: https://www.python.org/downloads/
- Run the installer. **Check the box that says "Add Python to PATH"** before clicking Install.
- To check if Python is installed, run:
  ```
  python --version
  ```

### c. Install VSCode
- Download from: https://code.visualstudio.com/
- Run the installer and follow the steps.
- Open VSCode after installation.

---

## 3. Clone the Repository

1. Open VSCode.
2. Open the Command Palette (press `Ctrl+Shift+P`).
3. Type `Git: Clone` and select it.
4. Paste the repository URL (for us it is "https://github.com/sudhanshu-wani/Sproutify.git").
5. Choose a folder to save the project.
6. Open the cloned folder in VSCode when prompted.

---

## 4. Set Up Python Environment

### a. Open a Terminal in VSCode
- Go to `Terminal` > `New Terminal` (or press `` Ctrl+` ``).

### b. Create a Virtual Environment (Recommended)
- In the terminal, run:
  ```
  python -m venv venv
  ```
- Activate the virtual environment:
  - **Windows:**
    ```
    .\venv\Scripts\activate
    ```
  - **Mac/Linux:**
    ```
    source venv/bin/activate
    ```
- You should see `(venv)` at the start of your terminal line.

### c. Install Required Python Libraries
- With the virtual environment activated, run:
  ```
  pip install --upgrade pip
  pip install -r requirements.txt
  ```

---

## 5. Running the Application

The app now runs as a **single server** with both the web interface and emotion detection API integrated!

### Start the Application
- In the terminal, run:
  ```
  python app.py
  ```
- This will start the complete application at `http://127.0.0.1:5000/`

### Open in Browser
- Go to `http://127.0.0.1:5000/` in your web browser.
- You'll be redirected to the login page if not authenticated.
- **Register** a new account or **login** with existing credentials.
- After authentication, you can upload a photo and see the emotion detection in action!

---

## 6. Authentication Features

The app now includes a complete authentication system:

### Registration
- Visit `http://127.0.0.1:5000/register` to create a new account
- Username must be at least 3 characters long
- Password must be at least 6 characters long
- Passwords are securely hashed using Werkzeug

### Login
- Visit `http://127.0.0.1:5000/login` to access your account
- Use your registered username and password
- You'll be redirected to the emotion detection page after successful login

### Logout
- Click the "Logout" button in the top-right corner of the main page
- You'll be redirected back to the login page

### Security Features
- Password hashing for secure storage
- Session management with Flask-Login
- Protected routes that require authentication
- Automatic redirect to login for unauthenticated users

---

## 7. VSCode Tips
- Install the **Python extension** (search for "Python" in the Extensions sidebar).
- VSCode will prompt you to select a Python interpreter. Choose the one from your `venv` folder.
- You can set breakpoints and debug your code using the built-in debugger.

---

## 8. Troubleshooting
- If you get errors about missing packages, make sure your virtual environment is activated and you ran `pip install -r requirements.txt`.
- If you see `ModuleNotFoundError`, double-check your Python interpreter in VSCode (bottom left corner).
- For authentication issues, try clearing your browser cookies or using incognito mode.
- For any other issues, try searching the error message online or ask your friend for help!

---

## 9. Deactivating the Virtual Environment
- When you're done, you can deactivate the virtual environment by running:
  ```
  deactivate
  ```

---

Happy coding! 🚀 