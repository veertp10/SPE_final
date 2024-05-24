pipeline {
    agent any

    environment {
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
                    def trainImage = docker.build("veerendragoudatp10/train-model:latest", '-f training/Dockerfile training')
                    withDockerRegistry([credentialsId: "DockerHubCred", url: ""]) {
                        trainImage.push("${env.BUILD_NUMBER}")
                    }
                    sh """
                        docker run --rm -v ${pwd()}/training:/app veerendragoudatp10/train-model:${env.BUILD_NUMBER}
                    """
                }
            }
        }

        stage('Push Model to S3') {
            steps {
                script {
                    withAWS(credentials: 'aws-s3-creds') {
                        sh """
                            aws s3 cp training/model.pkl s3://${S3_BUCKET}/model.pkl
                        """
                    }
                }
            }
        }

        stage('Build Docker Frontend Image') {
            steps {
                dir('frontend') {
                    script {
                        frontendImage = docker.build("veerendragoudatp10/chat-frontend:frontend")
                    }
                }
            }
        }

        stage('Push Docker Frontend Image') {
            steps {
                script {
                    withDockerRegistry([credentialsId: "DockerHubCred", url: ""]) {
                        frontendImage.push()
                    }
                }
            }
        }

        stage('Build Docker Backend Image') {
            steps {
                dir('backend') {
                    script {
                        backendImage = docker.build("veerendragoudatp10/chat-backend:backend")
                    }
                }
            }
        }

        stage('Push Docker Backend Image') {
            steps {
                script {
                    withDockerRegistry([credentialsId: "DockerHubCred", url: ""]) {
                        backendImage.push()
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
