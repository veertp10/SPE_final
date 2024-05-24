pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/veertp10/SPE_final.git'
            }
        }

        // stage('Build Docker Frontend Image') {
        //     steps {
        //         dir('healthcare_chatbot_frontend') {
        //             script {
        //                 frontendImage = docker.build("sankalp137rai/react-app:frontend")
        //             }
        //         }
        //     }
        // }

        // stage('Push Docker Frontend Image') {
        //     steps {
        //         script {
        //             withDockerRegistry([credentialsId: "DockerHubCred", url: ""]) {
        //                 frontendImage.push()
        //             }
        //         }
        //     }
        // }

        // stage('Build Docker Backend Image') {
        //     steps {
        //         dir('healthcare_chatbot_backend') {
        //             script {
        //                 backendImage = docker.build("sankalp137rai/flask-app:backend")
        //             }
        //         }
        //     }
        // }

        // stage('Push Docker Backend Image') {
        //     steps {
        //         script {
        //             withDockerRegistry([credentialsId: "DockerHubCred", url: ""]) {
        //                 backendImage.push()
        //             }
        //         }
        //     }
        // }
        stage('Run ansible playbook'){
            steps{
            
                    script {
                         ansiblePlaybook becomeUser: null, colorized: true, disableHostKeyChecking: true, installation: 'Ansible', playbook: './ansible-deploy/ansible-book.yml', sudoUser: null
                    
                        )
                    }
                
            }
        }
        // stage('Deploy frontend to Kubernetes') {
        //     steps {
        //         dir('kubernates') {
        //             script {
        //                 sh "kubectl apply -f frontend.yaml"
        //             }
        //         }
        //     }
        // }
    }
}