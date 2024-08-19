pipeline {
    agent any

    stages {
        stage('Setup') {
            steps {
                echo "Setting up environment..."
                // Common setup steps for all branches
            }
        }

        stage('Production Only Steps') {
            when {
                branch 'production'
            }
            steps {
                echo "Running steps on production branch..."
                // Steps that should only run on the production branch
            }
        }

        stage('Non-Production Steps') {
            when {
                not {
                    branch 'production'
                }
            }
            steps {
                echo "Running steps on non-production branches..."
                // Steps that should run on all other branches
            }
        }

        stage('Common Steps') {
            steps {
                echo "Running common steps for all branches..."
                // Steps that should run on all branches
            }
        }
    }

    post {
        always {
            echo "Cleaning up..."
            // Post steps, if any, like cleanup
        }
    }
}