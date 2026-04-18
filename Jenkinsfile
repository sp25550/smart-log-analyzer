pipeline {
    agent any

    environment {
        PYTHON = "C:\\Users\\User\\AppData\\Local\\Programs\\Python\\Python310\\python.exe"
        IMAGE = "xxxxxyyyy/smart-log-analyzer:latest"
        CONTAINER = "smart-log-analyzer-container"
        APP_URL = "http://127.0.0.1:5000"
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
                docker stop %CONTAINER% || exit /b 0
                docker rm %CONTAINER% || exit /b 0
                docker rmi %IMAGE% || exit /b 0
                docker build -t %IMAGE% .
                """
            }
        }

        stage('Run Docker Container') {
            steps {
                bat """
                docker run -d -p 5000:5000 --name %CONTAINER% %IMAGE%
                """
            }
        }

        stage('Wait for Flask Server') {
            steps {
                bat '''
                powershell -Command "
                $url = 'http://127.0.0.1:5000'
                $success = $false

                for ($i = 0; $i -lt 30; $i++) {
                    try {
                        Invoke-WebRequest -Uri $url -UseBasicParsing -TimeoutSec 2 | Out-Null
                        Write-Host 'Server is up!'
                        $success = $true
                        break
                    } catch {
                        Write-Host ('Attempt ' + $i + ' failed')
                        Start-Sleep -Seconds 2
                    }
                }

                if (-not $success) { exit 1 }
                "
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
                withCredentials([usernamePassword(credentialsId: 'docker-hub-creds',
                                                 usernameVariable: 'DOCKER_USER',
                                                 passwordVariable: 'DOCKER_PASS')]) {
                    bat """
                    echo %DOCKER_PASS% | docker login -u %DOCKER_USER% --password-stdin
                    IF %ERRORLEVEL% NEQ 0 exit /b 1

                    docker push %IMAGE%
                    IF %ERRORLEVEL% NEQ 0 exit /b 1
                    """
                }
            }
        }

        stage('Build Complete') {
            steps {
                echo "Build + Test + Deploy SUCCESS ✔"
            }
        }
    }

    post {
        success {
            echo "Pipeline SUCCESS ✔ Image pushed to Docker Hub"
        }

        failure {
            bat "docker rm -f %CONTAINER% || exit /b 0"
            echo "Pipeline FAILED ❌"
        }
    }
}