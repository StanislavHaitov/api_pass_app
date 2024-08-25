pipeline {
    agent any

    environment {
    }
    
    stages {
        stage('Build') {
            steps {
                echo 'Building... '
            }
        }
        stage('Test') {
            steps {
                echo 'Testing...'
            }
        }
        stage('Deploy') {
            steps {
                echo 'Deploying...'
            }
        }
    }
   
    post {
        always {
            echo 'Cleaning up...'
        }
    }           
}