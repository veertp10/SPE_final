pipeline {
    agent any

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

                }
            }
        }

        stage('Push Model to S3') {
            steps {
                script {
                    withAWS(credentials: 'aws-access-key-id, aws-secret-access-key', region: 'eu-north-1') {
                        sh """
                            aws s3 cp ${WORKSPACE}/ExtraTrees s3://${healthcarechatbot1}/ExtraTrees
                        """
                    }
                }
            }   
        }

        stage('Build Docker Frontend Image') {
            steps {
                dir('healthcare_chatbot_frontend') {
                    script {
                        frontendImage = docker.build("veerendragoudatp10/react-app:frontend")
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
                dir('healthcare_chatbot_backend') {
                    script {
                        backendImage = docker.build("veerendragoudatp10/flask-app:backend")
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
        stage('Run ansible playbook'){
            steps{
                script {
                    ansiblePlaybook(
                        playbook: 'playbook.yml',
                        inventory: 'inventory',
                        
                    )
                }
            }
        }
        stage('Deploy frontend to Kubernetes') {
            steps {
                dir('kubernates') {
                    script {
                        sh "kubectl apply -f frontend.yaml"
                    }
                }
            }
        }
    }
}