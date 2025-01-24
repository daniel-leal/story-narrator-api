# 📖 Story Narrator Backend

![CI](https://github.com/daniel-leal/story-narrator-backend/actions/workflows/ci.yml/badge.svg)
[![Coverage Status](https://coveralls.io/repos/github/daniel-leal/story-narrator-backend/badge.svg?branch=main)](https://coveralls.io/github/daniel-leal/story-narrator-backend?branch=main)

This repository contains the backend implementation for the Story Narrator application, built using FastAPI and SQLAlchemy with PostgreSQL as the database. The architecture emphasizes scalability, maintainability, and adherence to modern software engineering principles.

---

## ✨ Features
- 👤 User management with unique email constraints.
- 📜 Database migrations with Alembic.
- ⚡ Asynchronous database handling using `asyncpg`.
- 🧹 **Clean architecture** implementing **SOLID principles** and **Object Calisthenics** for maintainable and readable code.
- 🌱 Environment variable configuration using `dotenv`.
- 🤖 Integration-ready for Generative AI (GenAI) features.

---

## 📋 Requirements
To run this project, you need:
- 🐍 Python >= 3.11
- 🛠️ Poetry >= 1.4.0
- 🐘 PostgreSQL >= 14
- 🐳 Docker & Docker Compose (optional, but recommended)

---

## 🚀 Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/<your-username>/story-narrator-backend.git
   cd story-narrator-backend
   ```

2. **Set up environment variables:**
   Create a `.env` file in the root directory and configure it based on .env.example:


3. **Install dependencies:**
   Use Poetry to install project dependencies:
   ```bash
   poetry install
   ```

4. **Run database migrations:**
   Apply the database migrations using Alembic:
   ```bash
   poetry run alembic upgrade head
   ```

---

## ▶️ How to Run

1. **Run with Poetry:**
   ```bash
   poetry run uvicorn main:app --reload
   ```
   This will start the FastAPI application on `http://127.0.0.1:8000`.

2. **Run with Docker Compose:**
   Ensure Docker and Docker Compose are installed, then run:
   ```bash
   make docker-up
   ```
   The application will be available on `http://localhost:8000`.

   - Debug Mode:
      ```bash
      make docker-debug
      ```

   - Stop the application:
      ```bash
      make docker-down
      ```

   - Rebuild Docker Containers:
      ```bash
      make docker-rebuild
      ```

---

## 🧪 Running Tests
To run the tests, use:
```bash
make test
```
For specific test files or directories:
```bash
poetry run pytest tests/
```

---

## 🐘 Database Migration
### Alembic Commands
- Create a new migration:
```bash
make revision MESSAGE="your migration message"
```

- Apply the latest migrations:
```bash
make upgrade
```

- Rollback the last migration:
```bash
make downgrade
```

- Check the migration status:
```bash
make show
```

---

## 🛠️ Troubleshooting
- ⚙️ **Database Connection Issues:**
  Ensure your `.env` file is correctly configured and the database is running.
- 📂  **Alembic Migration Errors:**
  Verify that your models are correctly imported in `env.py`.
- 🐳 **Docker Issues:**
  If a port conflict occurs, stop existing containers using `docker ps` and `docker stop <container_id>`

---

## 🤝 Contributing
Feel free to submit issues or pull requests. Ensure your changes pass tests and adhere to the project's style guidelines.

---

## 📜 License
This project is licensed under the MIT License. See `LICENSE` for details.

---

## 👨‍💻 Author
Developed by Daniel Leal.
