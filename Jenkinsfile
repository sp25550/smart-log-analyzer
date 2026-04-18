pipeline {
    agent any

    environment {
        PYTHON = "C:\\Users\\User\\AppData\\Local\\Programs\\Python\\Python310\\python.exe"
        IMAGE_NAME = "xxxxxyyyy/smart-log-analyzer"
        CONTAINER_NAME = "smart-log-analyzer-container"
    }

    stages {

        stage('Checkout') {
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

        stage('Code Quality Check') {
            steps {
                bat """
                %PYTHON% -m flake8 . --ignore=W292,W293,E402 || exit /b 0
                """
            }
        }

        stage('Docker Build') {
            steps {
                bat "docker build -t %IMAGE_NAME%:latest ."
            }
        }

        stage('Run Container') {
            steps {
                bat "docker rm -f %CONTAINER_NAME% || exit /b 0"
                bat "docker run -d -p 5000:5000 --name %CONTAINER_NAME% %IMAGE_NAME%:latest"
            }
        }

        stage('Wait for Flask App') {
            steps {
                bat """
                powershell -Command ^
                "$url='http://127.0.0.1:5000'; ^
                for ($i=0; $i -lt 30; $i++) { ^
                    try { ^
                        Invoke-WebRequest -Uri $url -UseBasicParsing -TimeoutSec 2 | Out-Null; ^
                        Write-Host 'Server is UP'; exit 0 ^
                    } catch { ^
                        Write-Host ('Retry ' + $i); Start-Sleep -Seconds 2 ^
                    } ^
                }; ^
                Write-Host 'Server did not start'; exit 1"
                """
            }
        }

        stage('UI Tests') {
            steps {
                bat """
                %PYTHON% -m pytest -v tests/test_ui.py
                """
            }
        }

        stage('Docker Push') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-credentials',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    bat """
                    echo %DOCKER_PASS% | docker login -u %DOCKER_USER% --password-stdin
                    docker push %IMAGE_NAME%:latest
                    docker logout
                    """
                }
            }
        }
    }

    post {
        success {
            echo "PIPELINE SUCCESS - Deployment complete"
        }
        failure {
            bat "docker rm -f %CONTAINER_NAME% || exit /b 0"
            echo "PIPELINE FAILED"
        }
    }
}