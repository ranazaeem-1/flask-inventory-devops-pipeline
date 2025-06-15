pipeline {
    agent any
    
    environment {
        GITHUB_REPO = 'https://github.com/your-username/TDS_A3.git' // Replace with your GitHub repo URL
        APP_PORT = '5000'
        TEST_CONTAINER_NAME = 'tds_app_test'
    }
    
    stages {
        stage('Checkout') {
            steps {
                // Clean workspace before checkout
                cleanWs()
                
                // Checkout code from GitHub repository
                git url: "${env.GITHUB_REPO}", branch: 'main'
                
                echo 'Code checkout complete'
            }
        }
        
        stage('Build Docker Image') {
            steps {
                script {
                    // Build docker image
                    sh 'docker build -t tds_flask_app .'
                    
                    echo 'Docker image build complete'
                }
            }
        }
        
        stage('Run App Container') {
            steps {
                script {
                    // Stop and remove existing container if it exists
                    sh 'docker rm -f ${TEST_CONTAINER_NAME} || true'
                    
                    // Run the application container in background
                    sh 'docker run -d -p ${APP_PORT}:${APP_PORT} --name ${TEST_CONTAINER_NAME} tds_flask_app'
                    
                    // Wait for app to start
                    sh 'sleep 10'
                    
                    echo 'Application container started'
                }
            }
        }
        
        stage('Run Selenium Tests') {
            steps {
                script {
                    try {
                        // Run tests
                        sh 'docker exec ${TEST_CONTAINER_NAME} pytest -v tests/test_selenium.py'
                        
                        echo 'Selenium tests passed'
                    } catch (Exception e) {
                        echo 'Selenium tests failed'
                        throw e
                    }
                }
            }
        }
    }
    
    post {
        always {
            // Stop and remove the test container
            sh 'docker rm -f ${TEST_CONTAINER_NAME} || true'
        }
        
        success {
            echo 'All tests passed!'
            
            // Send success email notification
            mail to: "${env.GIT_COMMITTER_EMAIL}",
                 subject: "✅ Build Success: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                 body: """
                    Build #${env.BUILD_NUMBER} of ${env.JOB_NAME} was successful.
                    
                    Check console output at ${env.BUILD_URL}
                 """
        }
        
        failure {
            echo 'Tests failed!'
            
            // Send failure email notification
            mail to: "${env.GIT_COMMITTER_EMAIL}",
                 subject: "❌ Build Failed: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                 body: """
                    Build #${env.BUILD_NUMBER} of ${env.JOB_NAME} failed.
                    
                    Check console output at ${env.BUILD_URL}
                 """
        }
    }
}
