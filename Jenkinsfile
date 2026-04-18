pipeline {
    agent any

    environment {
        PYTHON = "C:\\Users\\User\\AppData\\Local\\Programs\\Python\\Python310\\python.exe"
        IMAGE = "xxxxxyyyy/smart-log-analyzer"
        CONTAINER = "smart-log-analyzer-container"
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
                bat "%PYTHON% -m pytest -v tests/test_app.py"
            }
        }

        stage('Code Quality Check') {
            steps {
                bat "%PYTHON% -m flake8 . --ignore=W292,W293,E402 || exit /b 0"
            }
        }

        stage('Docker Build') {
            steps {
                bat "docker build -t %IMAGE%:latest ."
            }
        }

        stage('Run Container') {
            steps {
                bat "docker rm -f %CONTAINER% || exit /b 0"
                bat "docker run -d -p 5000:5000 --name %CONTAINER% %IMAGE%:latest"
            }
        }

        stage('Wait for App') {
            steps {
                bat '''
                powershell -Command "& {
                    $url='http://127.0.0.1:5000';
                    for ($i=0; $i -lt 30; $i++) {
                        try {
                            Invoke-WebRequest $url -UseBasicParsing -TimeoutSec 2 | Out-Null;
                            Write-Host 'Server UP';
                            exit 0;
                        } catch {
                            Write-Host ('Retry ' + $i);
                            Start-Sleep 2;
                        }
                    }
                    exit 1
                }"
                '''
            }
        }

        stage('UI Tests') {
            steps {
                bat "%PYTHON% -m pytest -v tests/test_ui.py"
            }
        }

        stage('Docker Login + Push') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-credentials',
                    usernameVariable: 'USER',
                    passwordVariable: 'PASS'
                )]) {
                    bat "echo %PASS% | docker login -u %USER% --password-stdin"
                    bat "docker push %IMAGE%:latest"
                    bat "docker logout"
                }
            }
        }
    }

    post {
        success {
            echo "PIPELINE SUCCESS: Image built, tested, and pushed"
        }

        failure {
            bat "docker rm -f %CONTAINER% || exit /b 0"
            echo "PIPELINE FAILED"
        }
    }
}