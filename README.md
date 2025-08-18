# Project Setup Guide

Follow these steps to set up and run the project on your local machine.

---

## 1. Install Python Dependencies

Make sure you have Python installed. Then run:

```bash
pip install -r requirements.txt
```

## 2. Install Node Modules

Ensure you have Node.js and npm installed. Then run:

```bash
npm install
```

## 3.Set Up a Virtual Environment

If you're using a virtual environment (recommended), activate it with:

```bash
.venv\Scripts\activate   # On Windows
# or
source .venv/bin/activate   # On macOS/Linux
```

Make sure the virtual environment is created beforehand using:

```bash
python -m venv .venv
```

## 4. Run the Development Server

Start the frontend development server with:

```bash
npm run dev
```

##  5. Launch the Python Backend

In a separate terminal (with the virtual environment activated), run:

```bash
python app.py
```

## 6. Expected Output

After running the backend, you should see something like:

```bash
WARNING: FFmpeg not found. Audio downloads will be in native format without conversion to MP3.
 * Serving Flask app 'app'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
 * Restarting with stat
WARNING: FFmpeg not found. Audio downloads will be in native format without conversion to MP3.
 * Debugger is active!
 * Debugger PIN: 797-827-461
127.0.0.1 - - [18/Aug/2025 02:44:14] "GET / HTTP/1.1" 200 -
```