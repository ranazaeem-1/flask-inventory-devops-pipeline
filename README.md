# TDS Assignment 3: DevOps Pipeline with Selenium, Jenkins, Docker, GitHub, and AWS

This project demonstrates a complete DevOps pipeline using:
- Flask web application with CRUD functionality
- Selenium automated testing
- Jenkins CI/CD pipeline
- Docker containerization
- GitHub for source control
- AWS EC2 for deployment

## Project Overview

This project is a simple inventory management system with the following features:
- User authentication (register, login, logout)
- Item management (add, edit, delete, search)
- Profile management

## Technologies Used

- **Backend**: Flask with PyMongo
- **Frontend**: Bootstrap for responsive UI
- **Database**: MongoDB Atlas (cloud-based NoSQL database)
- **Testing**: Selenium with Python
- **CI/CD**: Jenkins
- **Containerization**: Docker
- **Cloud**: AWS EC2

## Test Cases

The project includes 10 automated test cases using Selenium:

1. Check if home page redirects to login when not authenticated
2. Register a new user
3. Test login failure with wrong credentials
4. Validate successful login with correct credentials
5. Add a new inventory item
6. Edit an existing inventory item
7. Test search functionality
8. Delete an inventory item
9. Update user profile
10. Test logout functionality

## Local Setup

1. Clone the repository:
   ```
   git clone https://github.com/your-username/TDS_A3.git
   cd TDS_A3
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run the application:
   ```
   python app.py
   ```
   The application should now be running at http://localhost:5000

4. Run the tests locally:
   ```
   pytest -v tests/test_selenium.py
   ```

## Detailed Implementation Steps

### 1. Setting Up Your Development Environment

1. Install Python 3.9+ if not already installed
2. Install Chrome browser and ChromeDriver for Selenium tests
3. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
4. Install required packages:
   ```
   pip install -r requirements.txt
   ```

### 2. GitHub Repository Setup

1. Create a new repository on GitHub (e.g., TDS_A3)
2. Initialize your local repository:
   ```
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/your-username/TDS_A3.git
   git push -u origin main
   ```

### 3. AWS EC2 Instance Setup

1. Launch a t2.micro Ubuntu EC2 instance on AWS
2. Configure security groups to allow traffic on ports:
   - 22 (SSH)
   - 8080 (Jenkins)
   - 5000 (Application)
3. Connect to your instance via SSH:
   ```
   ssh -i your-key.pem ubuntu@your-instance-ip
   ```

### 4. Setting Up Jenkins on EC2

1. Update packages and install Java:
   ```
   sudo apt update
   sudo apt install openjdk-11-jdk -y
   ```

2. Install Jenkins:
   ```
   wget -q -O - https://pkg.jenkins.io/debian-stable/jenkins.io.key | sudo apt-key add -
   sudo sh -c 'echo deb https://pkg.jenkins.io/debian-stable binary/ > /etc/apt/sources.list.d/jenkins.list'
   sudo apt update
   sudo apt install jenkins -y
   ```

3. Start Jenkins service:
   ```
   sudo systemctl start jenkins
   sudo systemctl enable jenkins
   ```

4. Get the initial admin password:
   ```
   sudo cat /var/lib/jenkins/secrets/initialAdminPassword
   ```

5. Access Jenkins in your browser at http://your-instance-ip:8080
   - Enter the admin password
   - Install suggested plugins
   - Create an admin user when prompted

6. Install additional Jenkins plugins:
   - Go to "Manage Jenkins" > "Manage Plugins" > "Available"
   - Install: Docker Pipeline, GitHub Integration, Email Extension

### 5. Setting Up Docker on EC2

1. Install Docker:
   ```
   sudo apt update
   sudo apt install docker.io -y
   ```

2. Add the Jenkins user to the Docker group:
   ```
   sudo usermod -aG docker jenkins
   ```

3. Restart Jenkins and Docker:
   ```
   sudo systemctl restart docker
   sudo systemctl restart jenkins
   ```

### 6. Creating the Jenkins Pipeline

1. In Jenkins, click "New Item"
2. Enter a name for your pipeline and select "Pipeline"
3. Configure the pipeline:
   - Under "Pipeline", select "Pipeline script from SCM"
   - Select "Git" as the SCM
   - Enter your GitHub repository URL
   - Specify the branch to build (e.g., "main")
   - Script Path: "Jenkinsfile" (this should match the name of your Jenkinsfile)
4. Save the pipeline configuration

### 7. Setting Up GitHub Webhook

1. In your GitHub repository, go to "Settings" > "Webhooks" > "Add webhook"
2. Set Payload URL to: `http://your-instance-ip:8080/github-webhook/`
3. Select "Content type" as "application/json"
4. Under "Which events would you like to trigger this webhook?", select "Just the push event"
5. Make sure "Active" is checked and click "Add webhook"

### 8. Running the Full CI/CD Pipeline

1. Push changes to your GitHub repository:
   ```
   git add .
   git commit -m "Update application code"
   git push
   ```

2. This will automatically trigger the Jenkins pipeline, which will:
   - Clone your repository
   - Build a Docker image
   - Run your application in a container
   - Execute Selenium tests
   - Send email notifications with results

3. Monitor the pipeline execution in Jenkins at http://your-instance-ip:8080

### 9. Troubleshooting

If you encounter issues with Selenium tests in the Docker environment:
1. Make sure you're using headless Chrome in your Selenium tests
2. Verify ChromeDriver version matches your Chrome version
3. Check Docker logs for any errors:
   ```
   docker logs <container_id>
   ```

### 10. Documentation

Document your implementation with screenshots of:
1. Jenkins pipeline execution
2. GitHub webhook configuration
3. EC2 instance details
4. Successful test execution results

## Docker Setup

1. Build the Docker image:
   ```
   docker build -t tds_flask_app .
   ```

2. Run the application in a container:
   ```
   docker run -p 5000:5000 tds_flask_app
   ```

## CI/CD Pipeline

The pipeline performs the following steps:
1. Checkout code from GitHub
2. Build Docker image
3. Run the application in a container
4. Execute Selenium tests
5. Send email notifications based on test results

## GitHub Integration

1. Set up a webhook in your GitHub repository
2. Configure the webhook to trigger your Jenkins pipeline on push events
3. URL format: `http://<EC2-IP>:8080/github-webhook/`

## AWS Deployment

1. Launch an EC2 t2.micro Ubuntu instance
2. Install Jenkins, Docker, and required plugins
3. Configure security groups to allow traffic on ports:
   - 22 (SSH)
   - 8080 (Jenkins)
   - 5000 (Application)

## Screenshots

Include screenshots of:
- Jenkins pipeline setup
- Successful test execution
- GitHub webhook configuration
- EC2 instance running the application
