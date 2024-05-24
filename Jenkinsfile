pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/veertp10/SPE_final.git'
            }
        }
        stage('Deploy with Ansible') {
            steps {
                script {
                    ansiblePlaybook becomeUser: null, colorized: true, disableHostKeyChecking: true, installation: 'Ansible', playbook: './ansible-deploy/ansible-book.yml', sudoUser: null
                }
            }
        }
    }
}