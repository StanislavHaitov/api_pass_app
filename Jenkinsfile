pipeline {
    agent any
    
    environment {
        DOCKER_IMAGE = "stanislavhaitov/pass_app"
        DOCKER_TAG = "v1.0" // Initial value; will be updated dynamically
        DOCKER_HUB_CREDENTIALS = 'dockerhub-credentials-id'
        GIT_REPO_URL = 'https://github.com/StanislavHaitov/api_pass_app.git'
        LATEST_TAG = "latest"
    }

    stages {
        stage('Clone Repository') {
            steps {
                // Clone the GitHub repository from the production branch
                git branch: 'production', url: "${GIT_REPO_URL}"
            }
        }
        
        stage('Test Latest Image') {
            steps {
                // Pull and run unit tests in the latest Docker image
                sh "docker pull ${DOCKER_IMAGE}:${LATEST_TAG}"
                sh "docker run --rm ${DOCKER_IMAGE}:${LATEST_TAG} sh -c \"pip install -r requirements.txt && python -m unittest discover\""
            }
        }
        
        stage('Build Docker Image') {
            steps {
                // Build the Docker image after tests pass
                sh "docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} ."
            }
        }
        
        stage('Approval') {
            steps {
                script {
                    // Timeout after 30 seconds, if no approval is given, skip the push stage
                    def userInput = false
                    try {
                        timeout(time: 30, unit: 'SECONDS') {
                            userInput = input message: 'Approve to push the new Docker image?', ok: 'Approve'
                        }
                    } catch (org.jenkinsci.plugins.workflow.steps.FlowInterruptedException e) {
                        echo "No approval received within 30 seconds. Continuing without pushing the image."
                    }

                    if (userInput) {
                        // The user approved the action, proceed with the push stage
                        echo "Approval received. Proceeding to push the Docker image."
                        
                        // Increment the Docker tag for the next release
                        DOCKER_TAG = incrementTag(DOCKER_TAG)
                        echo "Updated DOCKER_TAG to ${DOCKER_TAG}"
                    } else {
                        echo "Skipping image push due to lack of approval."
                    }
                }
            }
        }
        
        stage('Push Docker Image') {
            when {
                expression { return userInput }
            }
            steps {
                // Log in to Docker Hub
                withCredentials([usernamePassword(credentialsId: "${DOCKER_HUB_CREDENTIALS}", passwordVariable: 'DOCKER_HUB_PASS', usernameVariable: 'DOCKER_HUB_USER')]) {
                    sh "echo $DOCKER_HUB_PASS | docker login -u $DOCKER_HUB_USER --password-stdin"
                }
                // Push the new Docker image to Docker Hub
                sh "docker push ${DOCKER_IMAGE}:${DOCKER_TAG}"
                // Optionally update the latest tag
                sh "docker tag ${DOCKER_IMAGE}:${DOCKER_TAG} ${DOCKER_IMAGE}:latest"
                sh "docker push ${DOCKER_IMAGE}:latest"
            }
        }
    }
    
    post {
        always {
            // Clean up Docker images on the Jenkins server
            sh "docker rmi ${DOCKER_IMAGE}:${DOCKER_TAG} || true"
            sh "docker rmi ${DOCKER_IMAGE}:latest || true"
        }
    }
}

def incrementTag(String currentTag) {
    // Split the tag into parts using the dot as a delimiter
    def parts = currentTag.tokenize('.')
    // Increment the left side (major version)
    parts[0] = (parts[0].toInteger() + 1).toString()
    // Reset the minor version (right side) to 0
    parts[1] = '0'
    // Rejoin the parts to form the new tag
    return parts.join('.')
}

