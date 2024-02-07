# Text To Image
This project aims to provide a brief overview of how to utilize the Stable Diffusion API within the FastAPI framework, along with additional tasks such as creating base model schemas, generating and manipulating images, and deploying the application using Render cloud provider.

# Introduction
In this project, we utilized the Stable Diffusion API alongside the FastAPI framework to create a web application capable of generating and manipulating images based on specific tasks. The following sections detail the steps taken to achieve this, including the technologies used and the deployment process.

# Technologies Used
FastAPI Framework: FastAPI was chosen for its ease of use and high performance, allowing for efficient development of web applications with Python.
uvicorn Web Server: uvicorn was used as the ASGI server to run the FastAPI application.
Pythonic Libraries: Various Python libraries were utilized throughout the project, including HTTPX for making HTTP requests, Pillow for image manipulation, and imgkit for converting HTML to images.
Render Cloud Provider: Render was chosen as the cloud provider for deployment due to its simplicity and ease of use.
# Project Workflow
Initial Setup: The project began with researching and implementing the Stable Diffusion API within the FastAPI framework. This involved creating base model schemas and verifying the functionality through API testing.

Dynamic Key Generation: A key generation endpoint was implemented to allow dynamic usage of the Stable Diffusion API, following the format specified on the example page of the Stable Diffusion API documentation. This allowed users to use their own keys for accessing the API.

Task Implementation: Tasks were implemented based on specific requirements, including generating and manipulating images. The output of these tasks was provided through an API endpoint, allowing users to access the generated content.

Deployment: The application was deployed using the Render cloud provider to ensure accessibility for all users. Render's seamless deployment process facilitated the deployment of the application for multiple users.

# Usage
To run the application locally, follow these steps:

Install the necessary dependencies by running pip install -r requirements.txt.
Run the FastAPI application using uvicorn: uvicorn main:app --reload.
To access the deployed application.

# Conclusion
This project demonstrates the integration of the Stable Diffusion API within the FastAPI framework to create a web application capable of generating and manipulating images based on specific tasks. By leveraging various technologies and libraries, we were able to efficiently develop and deploy the application for widespread use.

For more details and usage instructions, please refer to the documentation and source code.
![output_image](https://github.com/tolgaboroglu/creative/assets/46046034/6beb5f8f-bbf0-41a6-a72c-d3ec09fca60b)
