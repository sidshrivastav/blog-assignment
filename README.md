# 📝 Blog Assignment

A containerized blog backend API built with **FastAPI**, using **SQLite** and **Docker**. This project follows a production-grade structure to enable versioned APIs, ORM-based models, and clear separation of concerns.

---

## 📁 Project Structure

```
fastapi_app/
├── app/
│   ├── api/v1/endpoints/   # Route handlers
│   ├── core/               # Config and security
│   ├── models/             # SQLAlchemy models
│   ├── schemas/            # Pydantic schemas
│   ├── crud/               # DB logic
│   ├── db/                 # DB session/base/init
│   ├── middlewares/        # Middleware Logics
│   └── main.py             # App entry point
├── tests/                  # Unit/integration tests
├── .env                    # App environment variables
├── requirements.txt        # Python dependencies
├── promethus               # Promethus settings
├── grafana                 # Grafana Provisioning
├── docker-compose.yml      # Docker Compose config
├── Dockerfile              # App Dockerfile
└── README.md               # Project documentation
```

---

## 🚀 Quick Start (with Docker)

### 1. Clone the repo

```bash
git clone https://github.com/sidshrivastav/blog-assignment.git
cd blog-assignment
```

### 2. Create the `.env` file

```bash
cp .env.example .env
```

Edit the `.env` file if needed:

```env
ENV=development
DEBUG=true
DATABASE_URL=sqlite:///./test.db
JWT_SECRET=your-secret-key
JWT_ALGORITHM=HS256
```

### 3. Build and run

```bash
docker-compose up --build
```

> ℹ️ The app will be available at: [http://localhost:8000/docs](http://localhost:8000/docs)
> ℹ️ The app logs will be available at: [http://localhost:8000/log-dashboard](http://localhost:8000/log-dashboard)
> ℹ️ The app promethus metrics will be available at: [http://localhost:9090](http://localhost:9090)

---

## 🧪 Run Tests (Locally)

You can run tests using `pytest` (assumes you have Python + requirements installed locally):

```bash
pytest --cov=app --cov-report=html
```

---

## 🐳 Docker Services

```yaml
services:
  blog:
    build: .
    ports:
      - "8000:8000"
    env_file:
      - .env
```

SQLite is used locally. No external DB container is needed unless switching to PostgreSQL or MySQL.

---

## 🔐 Environment Variables

Key | Description
----|-------------
`DATABASE_URL`    | DB connection string (e.g. SQLite or PostgreSQL)
`JWT_SECRET`      | Secret key for JWT/OAuth
`JWT_ALGORITHM`   | Algorithm used for JWT
`ENV`             | App environment (`development`, `production`)
`DEBUG`           | Enables hot reload & debug logs

---

## 🔖 Versioning & CI/CD

This project follows **semantic versioning** powered by **Conventional Commits** and automated GitHub Actions.

### Commit Format

We follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

| Type      | Description               | Version Bump |
|-----------|---------------------------|--------------|
| `fix:`    | Bug fixes                 | Patch        |
| `feat:`   | New features              | Minor        |
| `feat!:` / `BREAKING CHANGE:` | Breaking changes         | Major        |
| `chore:`  | Maintenance changes       | None         |

**Examples:**

```bash
git commit -m "fix: correct typo in blog title"
git commit -m "feat: add tags to blog post"
git commit -m "feat!: remove author model"
```

### CI/CD Flow (GitHub Actions)

On each push to the `main` branch, the following automated steps occur:

* **Version bump detection**: Achieved by analyzing commit history using `standard-version`.
* **Semantic Git Tagging**: A new semantic Git tag (e.g., `v1.2.3`) is created and subsequently pushed to the repository.
* **Docker Image Build and Push**: A Docker image is built and then pushed to the following container registries:
    * `docker.io/<your-username>/your-image-name:v1.2.3`
    * `ghcr.io/<your-username>/your-image-name:v1.2.3`
* **(Optional) Kubernetes Deployment**: The newly built image can then be deployed to a Kubernetes cluster using `kubectl`, Helm, or Kustomize.

For a complete overview of the workflow, please refer to the `docker.yml` file.
