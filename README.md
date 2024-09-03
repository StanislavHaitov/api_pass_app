
# PassApp DevOps Project

## Overview
`PassApp` is a DevOps-oriented project that automates the deployment and management of a Flask application in tranc base flow. This project is part of the final project for the DevSecOps course at Bar-Ilan University. It leverages technologies such as Docker, Jenkins, Kubernetes (via Minikube), Terraform, and Ansible to implement continuous integration, delivery, and infrastructure management, focusing on security best practices.

## Key Features
- **Automated CI/CD pipeline** with Jenkins.
- **Containerization** of the Flask application using Docker.
- **Infrastructure management** using Terraform for Minikube profile creation, deployment, and service management.
- **Kubernetes deployment** with Minikube for updating the "production" environment after deployment.
- **Configuration management** and automation with Ansible for installing Minikube, kubectl, and configuring the Minikube profile for the project.

## Prerequisites
Ensure that the following tools are installed on your system:
- **Python 3.x**
- **Docker**
- **Jenkins**
- **Minikube**
- **kubectl**
- **Terraform**
- **Ansible**

## Project Structure
```
api_pass_app
├── ansible
│   └── start_minikube.yml           # Ansible playbook for Minikube setup
├── command_list                     # List of commands
│   ├── 01.command_ansible.txt
│   ├── 02.command_tf_kubernetes.txt
│   ├── 03.minikube_IP_and_nodeport_extract.txt
│   └── 04.jenkins_container_run_command.txt
├── jenkins
│   ├── Jenkinsfile                  # Jenkins pipeline configuration
│   ├── smee.io                      # Webhook service file github to Jenkins
│   ├── Jankinsfile_steps
│   │   └── Jankinsfile_minikube_running_verefication.txt
│   └── Jankins with kubectl
│       └── Dockerfile
├── kubernetes
│   ├── deployment.yaml              # Kubernetes deployment configuration
│   └── service.yaml                 # Kubernetes service configuration
├── scripts
│   └── deploy_script.sh             # Deployment script
├── terraform
│   ├── main.tf                      # Main Terraform configuration
│   └── aws_terraform_example
│       └── aws_main.tf.example      # Example Terraform configuration for AWS
├── .gitignore                       # Git ignore file
├── Dockerfile                       # Dockerfile for building the Flask app
├── LICENSE                          # License file
├── pass_app.py                      # Flask application
├── README.md                        # Project documentation
├── requirements.txt                 # Python dependencies
├── test_pass_app.py                 # Unit tests for the Flask application
```

## Getting Started

### 1. Clone the Repository
First, clone the project repository from GitHub:

```bash
git clone git@github.com:StanislavHaitov/api_pass_app.git
cd api_pass_app
```

### 2. Install Minikube, kubectl, and Project Environment with Ansible
Use Ansible to automate the installation of Minikube, kubectl, and set up the project environment, including configuring the Minikube profile:

```bash
ansible-playbook ansible/start_minikube.yml
```

### 3. Infrastructure Setup with Terraform and Kubernetes Deployment
Set up your Minikube infrastructure using Terraform and deploy the application to Kubernetes:

```bash
cd terraform
terraform init
terraform plan
terraform apply
```
Next, apply the Kubernetes deployment configuration:

```bash
kubectl apply -f kubernetes/deployment.yaml
kubectl apply -f kubernetes/service.yaml
```

### 4. Install Jenkins and Set Up the CI/CD Pipeline
- Install Jenkins on your local machine or server.
- Configure your Jenkins pipeline using the provided Jenkinsfile.
- Set up credentials for Docker Hub, GitHub, and any other necessary services.
- Configure smee.io to handle webhook events from GitHub to trigger the Jenkins pipeline for automated CI/CD.

### 5. Deploy to the Kubernetes Cluster
The deployment to the Kubernetes cluster will only occur when changes are pushed to the production branch. 

Once configured, the Jenkins pipeline will handle the continuous integration and deployment process, including running unit tests, building Docker images, pushing to Docker Hub, and updating the Kubernetes "production" environment in Minikube.


## Docker Hub
The Docker image for this project is hosted on Docker Hub. You can pull the latest version of the image using:

```bash
docker pull stanislavhaitov/pass_app:latest
```

Docker Hub repository: [stanislavhaitov/pass_app](https://hub.docker.com/r/stanislavhaitov/pass_app)

## Jenkins CI/CD Pipeline
This project uses a Jenkins pipeline to automate the following tasks:
1. Clone the GitHub repository.
2. Build the Docker image and tag it.
3. Run unit tests.
4. Push the Docker image to Docker Hub (with version management).
5. Deploy to the Kubernetes cluster when changes are pushed to the production branch.

## Ansible Automation
The Ansible playbook (`start_minikube.yml`) automates the setup of Minikube and ensures that the correct profile and nodes are configured.

## Terraform Infrastructure Management
Terraform scripts are provided to manage Minikube profiles, deployments, and services for the `PassApp` project. This approach ensures a consistent and automated setup of the local Kubernetes environment, supporting effective development and testing workflows.

## Technology Stack
- **Python & Flask**: Web application framework.
- **Docker**: Containerization of the application.
- **Jenkins**: Continuous integration and deployment pipeline.
- **Minikube & Kubernetes**: Local Kubernetes cluster for testing and deployment.
- **Terraform**: Infrastructure as code (IaC) for Minikube profile creation, deployment, and service management.
- **Ansible**: Configuration management and automation.

## Future Improvements
- Integration with a cloud CI/CD system (e.g., GitHub Actions).
- Autoscaling and monitoring with Prometheus and Grafana.
- Implementing security best practices (e.g., secrets management).
  
## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact
For any inquiries, feel free to contact Stanislav Haitov at [stanislav.haitov@gmail.com](mailto:stanislav.haitov@gmail.com).
