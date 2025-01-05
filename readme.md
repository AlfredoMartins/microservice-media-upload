# Network Python-based Microservice for Media File Uploads

This microservice is designed to efficiently handle media file uploads, including audio and video files. It provides various components such as a RESTful API, task queuing, metadata storage, and a relational database. The system is containerized using Docker and orchestrated with Kubernetes for seamless scaling and deployment.

## Components

### 1. File Upload API
- A RESTful API designed for handling audio and video file uploads efficiently.
- Ensures scalability and reliability for large file transfers.

### 2. Task Queueing
- Utilizes RabbitMQ for queuing tasks related to media processing.
- Helps manage long-running tasks and decouple file upload from processing.

### 3. Metadata Repository
- Leverages MongoDB for dynamic and flexible storage of media metadata.
- Suitable for storing unstructured data, such as file details, status, and processing information.

### 4. Relational Database
- MySQL is used to manage structured data, including user permissions, logs, and relationships between media files and users.
- Ensures data integrity and efficient querying for structured information.

### 5. Containerization
- Docker is employed to containerize the application, ensuring that it can run consistently across different environments.
- Facilitates smooth deployment and testing.

### 6. Orchestration
- Kubernetes is used to deploy, scale, and maintain containerized services.
- Enables high availability and automated scaling of services based on demand.

### 7. File Storage Integration
- Processed media files are stored in either cloud or local storage solutions.
- The system updates file paths in the relational database to track the location of processed files.

## Deployment & Setup

### Prerequisites
- Docker
- Kubernetes
- RabbitMQ
- MongoDB
- MySQL

### Installation
1. Clone the repository:
   ```bash
   git clone https://your-repository-url.git

# Project Setup Documentation

## 1. Install MySQL Database

To install and initialize the MySQL database, run the following command:

```bash
mysql -uroot < init.sql
```

# Setup Instructions

## 2. Install Dependencies

### Install K9s
To install K9s, follow the instructions in the official documentation:  
[https://k9scli.io/](https://k9scli.io/)

### Install kubectl
To install kubectl, follow the instructions in the official documentation:  
[https://kubernetes.io/docs/tasks/tools/install-kubectl/](https://kubernetes.io/docs/tasks/tools/install-kubectl/)

### Install Minikube
To install Minikube, follow the instructions in the official documentation:  
[https://minikube.sigs.k8s.io/docs/](https://minikube.sigs.k8s.io/docs/)

## 3. Run the Update Script
Once the dependencies are installed, run the following script to update the environment:

```bash
./update.sh

# Expose Ports and Enable Ingress

## 4. Expose Ports

To expose the necessary services, run the following commands:

```bash
kubectl port-forward svc/rabbitmq 15672:15672
kubectl port-forward svc/gateway 8080:8080
minikube addons enable ingress