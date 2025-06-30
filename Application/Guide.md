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

## 5. Running the Applications

You need to run **two separate servers**: one for the API and one for the web app.

### a. Start the Emotion API
- In the terminal, run:
  ```
  python emotion_api.py
  ```
- This will start the backend API at `http://127.0.0.1:5001/detect`

### b. Start the Web App
- Open a **new terminal** (keep the API running in the first one):
  ```
  python app.py
  ```
- This will start the web app at `http://127.0.0.1:5000/`

### c. Open in Browser
- Go to `http://127.0.0.1:5000/` in your web browser.
- Upload a photo and see the emotion detection in action!

---

## 6. VSCode Tips
- Install the **Python extension** (search for "Python" in the Extensions sidebar).
- VSCode will prompt you to select a Python interpreter. Choose the one from your `venv` folder.
- You can set breakpoints and debug your code using the built-in debugger.

---

## 7. Troubleshooting
- If you get errors about missing packages, make sure your virtual environment is activated and you ran `pip install -r requirements.txt`.
- If you see `ModuleNotFoundError`, double-check your Python interpreter in VSCode (bottom left corner).
- For any other issues, try searching the error message online or ask your friend for help!

---

## 8. Deactivating the Virtual Environment
- When you're done, you can deactivate the virtual environment by running:
  ```
  deactivate
  ```

---

Happy coding! 🚀 
