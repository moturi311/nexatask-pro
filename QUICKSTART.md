# Quick Start Guide

## Option 1: Automated Setup (Recommended)

```bash
cd /home/t470s/Desktop/task
chmod +x setup.sh
./setup.sh
```

## Option 2: Manual Setup

### Step 1: Install System Dependencies
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv
```

### Step 2: Create & Activate Virtual Environment
```bash
cd /home/t470s/Desktop/task
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Flask
```bash
pip install -r requirements.txt
```

### Step 4: Run the Application
```bash
python3 app.py
```

### Step 5: Open in Browser
Navigate to: **http://localhost:5000**

---

## What You'll See

- A beautiful purple gradient interface
- Input field to add tasks
- Task list with checkboxes and delete buttons
- Statistics showing total and completed tasks

## How to Use

1. **Add Task**: Type in the input field and press Enter or click "Add Task"
2. **Complete Task**: Click the checkbox next to any task
3. **Delete Task**: Click the red "Delete" button
4. **View Stats**: Check the bottom of the page for task counts

---

## File Structure Created

```
task/
├── app.py              # Backend Flask server
├── templates/
│   └── index.html      # Frontend HTML
├── static/
│   ├── style.css       # Styling
│   └── script.js       # Frontend logic
├── tasks.db            # Database (auto-created on first run)
├── requirements.txt    # Python dependencies
├── setup.sh           # Automated setup script
├── README.md          # Full documentation
└── QUICKSTART.md      # This file
```

---

## Stopping the Server

Press `Ctrl + C` in the terminal where Flask is running

---

## Troubleshooting

**Port already in use?**
```bash
sudo lsof -t -i tcp:5000 | xargs kill -9
```

**Flask not found?**
```bash
source venv/bin/activate
pip install flask
```

**Permission denied on setup.sh?**
```bash
chmod +x setup.sh
```

---

Enjoy your task manager! 🚀
