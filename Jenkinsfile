pipeline {
    agent any

    environment {
        APP_NAME = 'jenkins-cicd-demo'
        APP_ENV = 'ci'
        DOCKERHUB_REPO = 'yashvikothari/jenkins-cicd-demo'
        IMAGE_TAG = "${BUILD_NUMBER}"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build') {
            steps {
                sh '''
                    echo "Compiling Python source..."
                    python3 -m compileall -q src
                '''
            }
        }

        stage('Test') {
            steps {
                sh '''
                    echo "Running automated tests..."
                    APP_NAME="$APP_NAME" APP_ENV="$APP_ENV" \
                    python3 -m unittest discover -s tests -v
                '''
            }
        }

        stage('Package') {
            steps {
                sh '''
                    rm -rf dist
                    mkdir -p dist
                    tar -czf "dist/${APP_NAME}-${BUILD_NUMBER}.tar.gz" src Dockerfile README.md
                    ls -lh dist
                '''
                archiveArtifacts artifacts: 'dist/*.tar.gz', fingerprint: true
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                    docker build \
                      -t "$DOCKERHUB_REPO:$IMAGE_TAG" \
                      -t "$DOCKERHUB_REPO:latest" .
                '''
            }
        }

        stage('Push Docker Image') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'dockerhub-credentials',
                        usernameVariable: 'DOCKERHUB_USER',
                        passwordVariable: 'DOCKERHUB_TOKEN'
                    )
                ]) {
                    sh '''
                        set +x
                        echo "$DOCKERHUB_TOKEN" | docker login -u "$DOCKERHUB_USER" --password-stdin
                        docker push "$DOCKERHUB_REPO:$IMAGE_TAG"
                        docker push "$DOCKERHUB_REPO:latest"
                        docker logout
                    '''
                }
            }
        }
    }

    post {
        success {
            echo "SUCCESS: ${DOCKERHUB_REPO}:${IMAGE_TAG} was built, tested, packaged and pushed."
        }
        failure {
            echo 'Pipeline failed. Check the stage logs above.'
        }
        always {
            deleteDir()
        }
    }
}
