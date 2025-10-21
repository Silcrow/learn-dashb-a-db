# Quick Start Guide

## What You Built
A **Dash dashboard** connected to **PostgreSQL** (running in Docker) that visualizes e-commerce data:
- 4 tables: User, Product, Order, OrderItem
- Charts: KPIs, bestsellers, top spenders, order tables

## First-Time Setup

### 1. Configure Environment Variables
Edit `.env` file and add:
```ini
SECRET_KEY=my-super-secret-key-123
DB_URL=postgresql://user:password@localhost:5433/mydatabase
```

### 2. Start Database
```bash
# Open Docker Desktop first!
docker-compose up -d

# Verify it's running
docker ps  # Should show 'postgres_db' container
```

### 3. Initialize Database
```bash
# Create tables
alembic upgrade head

# Add sample data
python -m database.populate populate_fake_products
python -m database.populate populate_db
```

### 4. Run Dashboard
```bash
python app.py
```
Open browser to: **http://127.0.0.1:8050**

---

## Daily Usage

```bash
# Start database (if not running)
docker-compose up -d

# Run dashboard
python app.py
```

---

## Common Commands

### Database Management
```bash
# Stop database
docker-compose down

# Wipe all data
python -m database.populate wipe_db

# Re-populate data
python -m database.populate populate_fake_products
python -m database.populate populate_db

# View database logs
docker logs postgres_db
```

### Troubleshooting
```bash
# Check if Docker is running
docker ps

# Check database connection
docker exec -it postgres_db psql -U user -d mydatabase

# Restart everything
docker-compose down
docker-compose up -d
alembic upgrade head
```

---

## Project Structure
```
app.py              # Entry point - runs Dash dashboard
├── database/       # Database layer
│   ├── models.py   # SQLAlchemy models (User, Product, Order, OrderItem)
│   ├── crud.py     # Create, Read, Update, Delete operations
│   ├── dao.py      # Data Access Objects
│   └── populate.py # Sample data generation
└── dashboard/      # Visualization layer
    ├── dashboard.py # Dash app setup
    ├── charts.py    # Chart components
    └── queries.py   # Database queries for charts
```
