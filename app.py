from flask import Flask, render_template, request
import os
from collections import Counter

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


def get_severity(line):
    line = line.lower()

    if "fatal" in line or "crash" in line:
        return "HIGH"
    elif "error" in line:
        return "MEDIUM"
    elif "warning" in line:
        return "LOW"
    return "INFO"


def analyze_logs(file_path):
    errors = 0
    warnings = 0
    infos = 0

    structured_logs = []
    error_messages = []

    with open(file_path, "r") as file:
        lines = file.readlines()

    for line in lines:
        parts = line.strip().split()

        if len(parts) < 3:
            continue

        date = parts[0]
        time = parts[1]
        level = parts[2]

        if level not in ["INFO", "WARNING", "ERROR"]:
            continue

        message = " ".join(parts[3:])
        severity = get_severity(line)

        structured_logs.append(
            {
                "date": date,
                "time": time,
                "level": level,
                "message": message,
                "severity": severity,
            }
        )

        if level == "ERROR":
            errors += 1
            error_messages.append(message)
        elif level == "WARNING":
            warnings += 1
        elif level == "INFO":
            infos += 1

    total = len(structured_logs)
    error_rate = (errors / total * 100) if total else 0

    top_errors = Counter(error_messages).most_common(5)

    return {
        "total": total,
        "errors": errors,
        "warnings": warnings,
        "infos": infos,
        "error_rate": round(error_rate, 2),
        "logs": structured_logs,
        "top_errors": top_errors,
    }


@app.route("/", methods=["GET", "POST"])
def index():
    result = None

    if request.method == "POST":
        file = request.files["logfile"]

        if file:
            path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
            file.save(path)

            result = analyze_logs(path)

    return render_template("index.html", result=result)


if __name__ == "__main__":
    app.run(debug=True)