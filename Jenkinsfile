pipeline {
    agent any

    environment {
        DOCKER_REGISTRY = 'https://hub.docker.com/'
        DOCKER_CREDENTIALS = credentials('DockerHubCred')
        S3_BUCKET = 'healthcarechatbot1'
    }

    stages {
        stage('Checkout') {
            steps {
                git 'https://github.com/veertp10/SPE_final.git'
            }
        }

        stage('Train Model') {
            steps {
                script {
                    docker.build('train-model', '-f training/Dockerfile .').push("${DOCKER_REGISTRY}/train-model:${env.BUILD_NUMBER}")
                    withAWS(credentials: 'aws-s3-creds') {
                        sh """
                            docker run --rm -v ${pwd()}/training:/app ${DOCKER_REGISTRY}/train-model:${env.BUILD_NUMBER}
                            aws s3 cp training/model.pkl s3://${S3_BUCKET}/model.pkl
                        """
                    }
                }
             }
        }

        stage('Build and Push Docker Images') {
            steps {
                script {
                    docker.withRegistry("${DOCKER_REGISTRY}", "${DOCKER_CREDENTIALS}") {
                        def backendImage = docker.build("${DOCKER_REGISTRY}/backend:${env.BUILD_NUMBER}", './backend')
                        def frontendImage = docker.build("${DOCKER_REGISTRY}/frontend:${env.BUILD_NUMBER}", './frontend')
                        backendImage.push()
                        frontendImage.push()
                    }
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                script {
                    sh """
                        kubectl apply -f backend.yaml
                        kubectl apply -f frontend.yaml
                    """
                }
            }
        }
    }
}