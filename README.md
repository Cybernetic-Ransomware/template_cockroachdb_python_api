# Template Project: Dockerized CockroachDB + SQLAlchemy

Quick implementation of a containerized CockroachDB instance + basic API 

---
## Requirements
- Docker Desktop,
- Docker Compose,
- Python >= 3.12.

## Initialization

1. Clone the repository:
    ```bash
    git clone https://github.com/Cybernetic-Ransomware/___
    ```
2. Install dependencies:
    ```bash
    pip install poetry
    poetry install
    ```
3. Run Docker Desktop and start the db container:
    ```bash
    docker-compose up --build
    ```
4. Enter container's terminal and set an example table:
    ```bash
    cockroach sql --insecure -e "CREATE TABLE accounts (id UUID PRIMARY KEY, balance INT8);"
    ```
5. Run the demonstrating script:
    ```bash
    poetry run python app/main.py
    ```

---

## Useful Links and Documentation

- SQL Alchemy Tutorial: [cockroachlabs](https://www.cockroachlabs.com/docs/stable/build-a-python-app-with-cockroachdb-sqlalchemy)
- Docker deployment: [cockroachlabs](https://www.cockroachlabs.com/docs/stable/install-cockroachdb-windows.html)
