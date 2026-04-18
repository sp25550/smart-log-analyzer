from flask import Flask, render_template, request, send_file
import os
from collections import Counter

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


def analyze_logs(file_path, search_query=None, filter_type=None):
    error_count = 0
    warning_count = 0
    info_count = 0

    errors = []
    timestamps = []
    critical_errors = []

    critical_keywords = ["failed", "crash", "fatal", "panic"]

    with open(file_path, 'r') as file:
        lines = file.readlines()

    for line in lines:
        line_lower = line.lower()

        # SEARCH FILTER
        if search_query and search_query.lower() not in line_lower:
            continue

        if "error" in line_lower:
            if filter_type and filter_type != "ERROR":
                continue

            error_count += 1
            errors.append(line.strip())

            parts = line.split()
            if len(parts) >= 2:
                timestamps.append(parts[1])

            for word in critical_keywords:
                if word in line_lower:
                    critical_errors.append(line.strip())
                    break

        elif "warning" in line_lower:
            if filter_type and filter_type != "WARNING":
                continue
            warning_count += 1

        elif "info" in line_lower:
            if filter_type and filter_type != "INFO":
                continue
            info_count += 1

    total = len(lines)
    error_rate = (error_count / total * 100) if total > 0 else 0

    # Most frequent error
    freq_error = None
    if errors:
        freq_error = Counter(errors).most_common(1)[0]

    return {
        "total": total,
        "errors": error_count,
        "warnings": warning_count,
        "info": info_count,
        "error_rate": round(error_rate, 2),
        "error_list": errors,
        "timestamps": timestamps,
        "critical": critical_errors,
        "freq_error": freq_error
    }


@app.route('/', methods=['GET', 'POST'])
def index():
    result = None

    if request.method == 'POST':
        file = request.files['logfile']
        search = request.form.get('search')
        filter_type = request.form.get('filter')

        if file:
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)

            result = analyze_logs(filepath, search, filter_type)

    return render_template('index.html', result=result)


@app.route('/download', methods=['POST'])
def download():
    file = request.files['logfile']
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)

    result = analyze_logs(filepath)

    report_path = os.path.join(UPLOAD_FOLDER, "report.txt")

    with open(report_path, "w") as f:
        f.write("Log Analysis Report\n")
        f.write("====================\n")
        f.write(f"Total Logs: {result['total']}\n")
        f.write(f"Errors: {result['errors']}\n")
        f.write(f"Warnings: {result['warnings']}\n")
        f.write(f"Info: {result['info']}\n")
        f.write(f"Error Rate: {result['error_rate']}%\n\n")

        f.write("Critical Errors:\n")
        for c in result['critical']:
            f.write(f"- {c}\n")

    return send_file(report_path, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)