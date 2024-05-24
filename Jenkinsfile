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
                git branch: 'main', url: 'https://github.com/veertp10/SPE_final.git'
            }
        }

        stage('Train Model') {
            steps {
                script {
                    // Build the Docker image for training the model
                    def trainImage = docker.build('train-model', '-f training/Dockerfile training')
                    
                    // Push the Docker image to the Docker registry
                    docker.withRegistry("${DOCKER_REGISTRY}", "${DOCKER_CREDENTIALS}") {
                        trainImage.push("${env.BUILD_NUMBER}")
                    }
                    
                    // Run the training process inside the Docker container
                    withAWS(credentials: 'aws-s3-creds') {
                        sh """
                            docker run --rm -v ${pwd()}/training:/app ${trainImage.imageName()}:${env.BUILD_NUMBER}
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
