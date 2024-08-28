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
                    echo "Checking out the repository from branch: ${env.BRANCH_NAME}"
                    git credentialsId: GIT_CREDENTIALS_ID, url: GIT_REPO_URL, branch: env.BRANCH_NAME
                    // Build the Docker image
                    withCredentials([usernamePassword(credentialsId: DOCKER_CREDENTIALS_ID, usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                        sh "docker login -u $DOCKER_USER -p $DOCKER_PASS"
                        sh "docker build -t $DOCKER_IMAGE:build-${env.BUILD_NUMBER} ."
                        sh "docker push $DOCKER_IMAGE:build-${env.BUILD_NUMBER}"
                    }
                }
            }
        }

        stage('Test') {
            steps {
                script {
                    // Pull the Docker image for testing
                    sh "docker pull $DOCKER_IMAGE:build-${env.BUILD_NUMBER}"
                    // Run tests inside the Docker container
                    sh "docker run --rm $DOCKER_IMAGE:build-${env.BUILD_NUMBER} pytest"
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
                    // Tag the tested image as 'latest' and push it to Docker Hub
                    sh "docker tag $DOCKER_IMAGE:build-${env.BUILD_NUMBER} $DOCKER_IMAGE:latest"
                    sh "docker push $DOCKER_IMAGE:latest"
                    
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
        script {
            withCredentials([string(credentialsId: 'email-address-id', variable: 'SECURE_EMAIL_ADDR')]) {
                mail to: SECURE_EMAIL_ADDR,
                     subject: "Build Success: ${env.JOB_NAME} for branch: ${env.BRANCH_NAME}",
                     body: "The build for ${env.JOB_NAME} succeeded!"
            }
        }
    }
    failure {
        script {
            withCredentials([string(credentialsId: 'email-address-id', variable: 'SECURE_EMAIL_ADDR')]) {
                mail to: SECURE_EMAIL_ADDR,
                     subject: "Build Failure: ${env.JOB_NAME} for branch: ${env.BRANCH_NAME}",
                     body: "The build for ${env.JOB_NAME} failed. Please check Jenkins for details."
            }
        }
    }
}
