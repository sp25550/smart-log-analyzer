# Smart Log Analyzer

Smart Log Analyzer is a Flask web application that helps users upload log files, detect patterns in log entries, and summarize issues such as errors, warnings, and system failures.

## Features

- Upload a log file from the browser
- Parse log entries into structured data
- Detect severity levels such as INFO, WARNING, ERROR, and HIGH/MEDIUM/LOW categories
- Calculate total log count and error rate
- Highlight the most common error messages
- Simple and lightweight Flask UI for fast log review

## Tech Stack

- Python
- Flask
- HTML/CSS
- Jinja2 templates
- Docker
- Jenkins

## Project Structure

- `app.py` - Flask application and log analysis logic
- `templates/` - Front-end UI templates
- `static/` - CSS and static assets
- `tests/` - Automated tests for the app
- `uploads/` - Uploaded log files are stored here at runtime
- `sample.log` and `invalid.log` - Sample log data for testing
- `Dockerfile` - Container configuration for deployment
- `Jenkinsfile` - CI pipeline configuration
- `requirements.txt` - Python dependencies

## Setup

1. Clone the repository:

```bash
git clone https://github.com/sp25550/smart-log-analyzer.git
cd smart-log-analyzer
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate
```

On Windows:

```bash
venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Run the application:

```bash
python app.py
```

The app will run locally on:

```text
http://localhost:5000
```

## Usage

1. Open the app in your browser.
2. Upload a log file.
3. The app analyzes the file and displays:
   - total number of log entries
   - error count
   - warning count
   - info count
   - error rate
   - top repeated error messages
   - structured log list

## Environment Variables

This project does not currently require any custom environment variables for normal local use. A local `.env` file can still be used for secrets or deployment settings if needed.

## Docker

A Dockerfile is included for containerized deployment.

```bash
docker build -t smart-log-analyzer .
docker run -p 5000:5000 smart-log-analyzer
```

## CI/CD

The repository includes a Jenkins pipeline for automated builds and testing. See `Jenkinsfile` for pipeline configuration.

## Notes

- Uploaded files are stored in the `uploads/` directory at runtime.
- The `.env` file is not committed to version control.
- Sample log files are included for local testing and demonstration purposes.
