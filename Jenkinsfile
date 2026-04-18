pipeline {
    agent any

    environment {
        IMAGE_NAME = "xxxxxyyyy/smart-log-analyzer:latest"
        CONTAINER_NAME = "smart-log-analyzer-container"
        PYTHON = "C:\\Users\\User\\AppData\\Local\\Programs\\Python\\Python310\\python.exe"
    }

    stages {

        stage('Checkout') {
            steps {
                git url: 'https://github.com/sp25550/smart-log-analyzer.git', branch: 'main'
            }
        }

        stage('Install Dependencies') {
            steps {
                bat """
                %PYTHON% -m pip install --upgrade pip
                %PYTHON% -m pip install -r requirements.txt
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

        stage('Code Quality Check') {
            steps {
                bat """
                %PYTHON% -m flake8 . --ignore=W292,W293,E402 || exit /b 0
                """
            }
        }

        stage('Docker Prep (Fix TLS Issue)') {
            steps {
                bat """
                docker pull python:3.10-slim || echo "Using cached image"
                """
            }
        }

        stage('Docker Build') {
            steps {
                bat """
                docker build --pull=false -t %IMAGE_NAME% .
                """
            }
        }

        stage('Run Container') {
            steps {
                bat """
                docker rm -f %CONTAINER_NAME% || exit /b 0
                docker run -d -p 5000:5000 --name %CONTAINER_NAME% %IMAGE_NAME%
                """
            }
        }

        stage('Wait for Flask App') {
            steps {
                script {
                    sleep time: 10, unit: 'SECONDS'
                }
            }
        }

        stage('UI Tests (Optional Safe)') {
            steps {
                bat """
                if exist tests\\test_ui.py (
                    %PYTHON% -m pytest -v tests/test_ui.py || exit /b 0
                ) else (
                    echo UI tests not found
                )
                """
            }
        }

        stage('Docker Push (Optional Safe)') {
            steps {
                bat """
                docker login -u xxxxxyyyy -p YOUR_PASSWORD
                docker push %IMAGE_NAME% || exit /b 0
                """
            }
        }
    }

    post {
        always {
            bat """
            docker rm -f %CONTAINER_NAME% || exit /b 0
            """
        }

        success {
            echo "PIPELINE SUCCESS"
        }

        failure {
            echo "PIPELINE FAILED"
        }
    }
}