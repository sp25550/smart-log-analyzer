pipeline {
    agent any
    environment {
        PYTHON = "C:\\Users\\User\\AppData\\Local\\Programs\\Python\\Python310\\python.exe"
    }
    stages {
        stage('Clone') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/sp25550/smart-log-analyzer.git'
            }
        }
        stage('Install Dependencies') {
            steps {
                bat """
                %PYTHON% -m pip install --upgrade pip
                %PYTHON% -m pip install -r requirements.txt
                %PYTHON% -m pip install pytest selenium requests flake8
                """
            }
        }
        stage('Run Unit Tests') {
            steps {
                bat """
                %PYTHON% -m pytest -v tests/test_app.py
                """
            }
        }
        stage('Start Flask App') {
            steps {
                bat """
                echo Starting Flask server...
                start "FlaskApp" /min %PYTHON% app.py
                """
            }
        }
        stage('Wait for Flask Server') {
            steps {
                bat '''
                powershell -Command "& { $url = 'http://127.0.0.1:5000'; for ($i = 0; $i -lt 30; $i++) { try { Invoke-WebRequest -Uri $url -UseBasicParsing -TimeoutSec 2 | Out-Null; Write-Host 'Server is up!'; exit 0 } catch { Write-Host ('Attempt ' + $i + ' failed, retrying...'); Start-Sleep -Seconds 2 } }; Write-Host 'Server did not start'; exit 1 }"
                '''
            }
        }
        stage('Run Selenium UI Tests') {
            steps {
                bat """
                %PYTHON% -m pytest -v tests/test_ui.py
                """
            }
        }
        stage('Code Quality (flake8)') {
            steps {
                bat """
                %PYTHON% -m flake8 . --ignore=W292,W293,E402 || exit /b 0
                """
            }
        }
        stage('Build') {
            steps {
                echo "Build completed successfully"
            }
        }
    }
    post {
        success {
            echo "Pipeline SUCCESS ✔"
        }
        failure {
            echo "Pipeline FAILED ❌"
        }
    }
}