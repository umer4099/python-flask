# 📘 Flask App with PostgreSQL - Dockerized

This project is a **Flask application** integrated with **PostgreSQL**, running inside **Docker** using a multi-stage build for optimization. The container follows **security best practices** by running as a **non-root user** and using a **minimal base image**.

## 📌 Features
- ✅ **Multi-stage Docker build** for optimized image size  
- ✅ **Flask + PostgreSQL integration**  
- ✅ **Runs as a non-root user** for security  
- ✅ **Uses Docker Compose** for easy container management  
- ✅ **Best practices applied** for efficiency and clarity  

## 🚀 Tech Stack
- **Python 3.10**
- **Flask**
- **PostgreSQL**
- **Docker & Docker Compose**

## 📂 Project Structure
```
📦 flask-postgres-app
 ┣ 📜 Dockerfile
 ┣ 📜 docker-compose.yml
 ┣ 📜 requirements.txt
 ┣ 📜 main.py
 ┣ 📜 .env (for environment variables)
 ┣ 📜 README.md
```

## 🔧 Setup Instructions

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/umer4099/python-flask.git
cd python-flask
```

### 2️⃣ Configure Environment Variables
Create a `.env` file:
```
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=demo
DB_HOST=postgres
DB_PORT=5432


```

### 3️⃣ Build & Run with Docker Compose
```bash
docker-compose up -d --build
```

### 4️⃣ Check Running Containers
```bash
docker ps
```

### 5️⃣ View Logs
```bash
docker logs flask_app
```

### 6️⃣ Stop Containers
```bash
docker-compose down
```

## 🛠 Docker & Docker Compose Configuration
### 📜 Dockerfile
- Uses **multi-stage builds** to optimize image size  
- Runs Flask as a **non-root user** for security  
- Uses **`python:3.10-slim`** for minimal image size  
- Installs `libpq5` for PostgreSQL compatibility  

### 📜 docker-compose.yml
- Defines services for **Flask App** and **PostgreSQL**  
- Uses a `.env` file for database credentials  
- Maps **port 5000** for the Flask app  

## 🔍 Troubleshooting

### 1️⃣ PostgreSQL Connection Error
- Ensure the database service is running:
  ```bash
  docker-compose ps
  ```
- Check logs:
  ```bash
  docker logs postgres
  ```

### 2️⃣ Flask App Exited with ImportError (`libpq.so.5` not found)
- Rebuild the container with:
  ```bash
  docker-compose build --no-cache
  ```
- Ensure **libpq5** is installed in the final Docker stage.

## 📜 License
This project is licensed under **MIT License**.

