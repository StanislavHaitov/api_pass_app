pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "stanislavhaitov/pass_app"
        DOCKER_CREDENTIALS_ID = "dockerhub-credentials-id"
        KUBECONFIG = "~/.kube/config"
        EMAIL_ADDR = credentials('email-address-id')
        GIT_REPO_URL = 'git@github.com:StanislavHaitov/api_pass_app.git'
        GIT_CREDENTIALS_ID = 'github-credentials-id'
    }

    stages {
        stage('Build') {
            steps {
                script {
                    // Checkout the repository
                    echo "Checking out the repository from branch: ${BRANCH_NAME}"
                    git credentialsId: GIT_CREDENTIALS_ID, url: GIT_REPO_URL, branch: BRANCH_NAME
                    
                    echo 'Building the Python application...'
                    
                    // Create a virtual environment
                    sh 'python -m venv .passapp'
                    
                    // Activate the virtual environment and install dependencies
                    sh '. .passapp/bin/activate && pip install -r requirements.txt'

                    // Lint the code
                    sh '. passapp/bin/activate && flake8 .'
                }
            }
        }

        stage('Test') {
            steps {
                script {
                    echo 'Running Python tests...'
                    // Activate the virtual environment and run tests
                    sh '. .passapp/bin/activate && pytest test_pass_app.py'
                }
            }
        }

        stage('Deploy') {
            when {
                allOf {
                    branch 'production'
                    changeRequest target: 'production'
                }
            }
            steps {
                script {
                    echo 'Deploying to Minikube...'
                    // Dockerize the application and push to Docker Hub
                    withCredentials([usernamePassword(credentialsId: DOCKER_CREDENTIALS_ID, usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                        sh "docker login -u $DOCKER_USER -p $DOCKER_PASS"
                        sh "docker build -t $DOCKER_IMAGE:latest ."
                        sh "docker push $DOCKER_IMAGE:latest"
                    }
                    // Use kubectl to apply Kubernetes manifests
                    sh "kubectl --kubeconfig=$KUBECONFIG apply -f deployment.yml"
                    
                    // Get Minikube IP and NodePort
                    def minikubeIp = sh(script: "minikube -p project-app ip", returnStdout: true).trim()
                    def nodePort = sh(script: "kubectl --kubeconfig=$KUBECONFIG get svc passapp-service -o jsonpath='{.spec.ports[0].nodePort}'", returnStdout: true).trim()
                    
                    echo "Application is accessible at http://${minikubeIp}:${nodePort}/password/"
                }
            }
        }
    }

    post {
        always {
            echo 'Cleaning up...'
            cleanWs()
        }
        success {
            mail to: EMAIL_ADDR,
                 subject: "Build Success: ${env.JOB_NAME} for branch: ${env.BRANCH_NAME}",
                 body: "The build for ${env.JOB_NAME} succeeded!"
        }
        failure {
            mail to: EMAIL_ADDR,
                 subject: "Build Failure: ${env.JOB_NAME} for branch: ${env.BRANCH_NAME}",
                 body: "The build for ${env.JOB_NAME} failed. Please check Jenkins for details."
        }
    }
}
