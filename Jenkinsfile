pipeline {
    agent any
    environment {
        PYTHON = "C:\\Users\\User\\AppData\\Local\\Programs\\Python\\Python310\\python.exe"
        IMAGE_NAME = "smart-log-analyzer"
        DOCKERHUB_USERNAME = "YOUR_DOCKERHUB_USERNAME"
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
        stage('Code Quality (flake8)') {
            steps {
                bat """
                %PYTHON% -m flake8 . --ignore=W292,W293,E402 || exit /b 0
                """
            }
        }
        stage('Build Docker Image') {
            steps {
                bat """
                docker stop %IMAGE_NAME%-container || exit /b 0
                docker rm %IMAGE_NAME%-container || exit /b 0
                docker rmi %DOCKERHUB_USERNAME%/%IMAGE_NAME% || exit /b 0
                docker build -t %DOCKERHUB_USERNAME%/%IMAGE_NAME% .
                """
            }
        }
        stage('Run Docker Container') {
            steps {
                bat """
                docker run -d -p 5000:5000 --name %IMAGE_NAME%-container %DOCKERHUB_USERNAME%/%IMAGE_NAME%
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
        stage('Push to Docker Hub') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-credentials',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    bat """
                    echo %DOCKER_PASS% | docker login -u %DOCKER_USER% --password-stdin
                    docker push %DOCKERHUB_USERNAME%/%IMAGE_NAME%
                    docker logout
                    """
                }
            }
        }
        stage('Build') {
            steps {
                echo "Build and Deployment completed successfully"
            }
        }
    }
    post {
        success {
            echo "Pipeline SUCCESS ✔ - Image pushed to Docker Hub"
        }
        failure {
            bat """
            docker stop %IMAGE_NAME%-container || exit /b 0
            docker rm %IMAGE_NAME%-container || exit /b 0
            """
            echo "Pipeline FAILED ❌"
        }
    }
}