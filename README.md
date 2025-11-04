# Personal Task Manager

A beautiful, full-stack web application for managing your daily tasks. Built with Flask (Python) backend and vanilla HTML/CSS/JavaScript frontend.

## 🚀 Live Demo

**Try it now**: [https://nexatask-pro.onrender.com/](https://nexatask-pro.onrender.com/)

> Note: Free tier may take ~30 seconds to wake up from sleep mode on first request.

## Features

- ✅ Add new tasks
- ✅ Mark tasks as complete/incomplete
- ✅ Delete tasks
- ✅ View task statistics
- ✅ Persistent storage with SQLite
- ✅ Beautiful, responsive UI
- ✅ XSS protection

## Tech Stack

- **Backend**: Python 3, Flask
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Database**: SQLite
- **OS**: Linux (Parrot OS / Any Linux distribution)

## Project Structure

```
taskmanager/
├── app.py                 # Flask backend with REST API
├── templates/
│   └── index.html        # Main HTML template
├── static/
│   ├── style.css         # CSS styling
│   └── script.js         # Frontend JavaScript
├── tasks.db              # SQLite database (auto-generated)
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## Installation & Setup

### 1. Install System Dependencies

```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv
```

### 2. Create Virtual Environment

```bash
cd /home/t470s/Desktop/task
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Python Dependencies

```bash
pip install -r requirements.txt
```

## Running the Application

### 1. Activate Virtual Environment (if not already activated)

```bash
source venv/bin/activate
```

### 2. Start the Flask Server

```bash
python3 app.py
```

### 3. Access the Application

Open your web browser and navigate to:
```
http://localhost:5000
```

## Usage

1. **Add a Task**: Type your task in the input field and click "Add Task" or press Enter
2. **Complete a Task**: Click the checkbox next to a task to mark it as complete
3. **Delete a Task**: Click the "Delete" button to remove a task
4. **View Statistics**: See total and completed task counts at the bottom

## API Endpoints

- `GET /api/tasks` - Get all tasks
- `POST /api/tasks` - Create a new task
- `PUT /api/tasks/<id>` - Update a task (toggle completion)
- `DELETE /api/tasks/<id>` - Delete a task

## Future Enhancements

- [ ] User authentication
- [ ] Task categories
- [ ] Due dates
- [ ] Task priorities
- [ ] Search and filter
- [ ] Dark mode
- [ ] Mobile app

## Troubleshooting

**Port 5000 already in use:**
```bash
# Find and kill the process
sudo lsof -t -i tcp:5000 | xargs kill -9

# Or change the port in app.py
app.run(debug=True, host='0.0.0.0', port=8000)
```

**Module not found:**
```bash
# Ensure virtual environment is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

## Security Features

- XSS protection with HTML escaping
- Input validation
- SQL injection prevention with parameterized queries

## License

MIT License - Feel free to use this project for learning!

## Author

Built as a full-stack learning project for Parrot OS users.
