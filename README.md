# learn-dashb-a-db

## Quickstart: Installation
> To copy this scaffold and extend as another project.

1. **Clone this repo:**
```bash
git clone https://github.com/your-username/wild-rift-dashboard.git
cd wild-rift-dashboard
```
2. Create and activate a virtual environment:

```shell
python3 -m venv venv
source venv/bin/activate # on Mac
```
3. Install dependencies:
```shell
pip install -r requirements.txt
```
Create a `.env` file with:
```ini
SECRET_KEY=<your-secret-key>
DB_URL=<your-database-url>
```
Run the app:
```shell
python app.py
```

- [ ] I also got the issue where my app has 2 entry points (on commented out). Do I make readme instructions on that, or edit the code? (editing the code complicates the codebase), but if I write instructions, it has to be obvious to a zero-day.

## To run scripts inside packages
> The builtin CLI input system would be just running the package functions.

To run each `populate.py`'s functions:
- `python -m database.populate wipe_db`
- `python -m database.populate populate_fake_products`
- `python -m database.populate populate_db`

## Alternative Quickstart
> I don't know if cloning and using the scaffold works yet, so I'm noting this coz WindSurf suggested it.

If you want to use this scaffold as the base for a brand new project (not a fork), follow these steps:

1. **Clone this repo to a new directory:**
   ```bash
   git clone https://github.com/Silcrow/learn-dashb-a-db.git my-new-project
   cd my-new-project
   ```
2. **Remove the old git history:**
   ```bash
   rm -rf .git
   ```
3. **Initialize a new git repository:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit: scaffold from learn-dashb-a-db"
   ```
4. **Create a new remote repository (e.g. on GitHub), then add it as your origin:**
   ```bash
   git remote add origin <your-new-repo-url>
   git push -u origin main
   ```
5. **Update project details:**
   - Change the project name and description in the README and any metadata files.
   - Update configuration files as needed (e.g., `.env.example`).

You now have a clean, independent project based on this scaffold!

## Dev Guide

### Important Notes to the Dev
- Whenever you make schema changes, don't forget to modify the DAO (Data Access Object) and CRUD (Create, Read, Update, Delete) operations accordingly.
- The key technologies used here are: **PostgreSQL, SQLAlchemy, Alembic, and Dash**.

There are 2 entry points in `app.py`. The canonical entry point is `main()` in `app.py`, but it's commented out so the app launch `run_dash()`instead.
**To use `main()`**:
1. Uncomment the dashboard entry point and comment in `main()`.
2. Open Docker. Make sure the docker container is running.
3. Run `python app.py`. You will see a list of database entries displayed in the terminal when `main()` was triggered.

### Git Timeline: How the Scaffold Was Built
This section briefly outlines the chronological evolution of the codebase, to help you understand the rationale behind its structure and how to extend it.

1. **Initial Setup:**
   - Set up PostgreSQL in Docker using `docker-compose.yml`.
   - Created `models.py` to define the initial DB schema and connection logic.
2. **Refactoring for Separation of Concerns:**
   - Moved DB connection logic from `models.py` to `database.py`.
   - Introduced `dao.py` and `crud.py` to abstract database operations.
3. **ORM and Migrations:**
   - Integrated Alembic for schema migrations.
   - Updated DAOs and CRUD whenever the schema changed.
4. **Extras:**
   - Added `populate.py` for generating fake/sample data (placeholder for ETL or CLI).
   - Added `dashboard/` for data visualization (optional, not core to backend/data infra).

### File Structure Explained
This project consists of **three main components**:

1. **`app.py` (Main Entry Point)**
   - Initializes the **Dash web application**.
   - Starts the **data-fetching logic**.
   - Uses **multi-threading** to keep the dashboard running while executing database queries.

2. **`dashboard/` (Dash App & Visualizations)**
   - `dashboard.py` → The main **Dash application** logic.
   - `charts.py` → Defines **graphs and visual elements**.
   - `queries.py` → Handles **data queries** from the database.
   - This modular approach keeps `dashboard.py` clean and efficient.

3. **`database/` (Database Management)**
   - `database.py` → Sets up the **SQLAlchemy engine & session**.
   - `models.py` → Defines **database models**.
   - `dao.py` → Contains **Data Access Objects (DAO)** for structured queries.
   - `crud.py` → Implements **basic CRUD operations**.
   - `populate.py` → Populates the database with **sample data**.

### **How They Work Together**

- `app.py` imports `database/` for querying and `dashboard/` for visualization.
- `dashboard/` dash app fetches data from `database/` via DAO queries.
- `database/` handles data CRUD.

```sh
app.py
 │
 ├──▶ database/    # Handles queries, updates
 │       └──▶ DAO Queries → Data
 │
 └──▶ dashboard/   # Dash App for visualization
         └──▶ Fetches data from database/
```
`dashboard/`:
```
SQL database → `queries` → df
df → `charts` → dash charts
```

### DB Schema Explained
There are 4 tables: User, Order, OrderItem, and Product. Entries in Product are fixed and represent "organizational capability".
User represent customers. Each User has many orders and each order has many items.
Think of it as each user putting items in a basket before cashing at the cashier.
A basket and corresponding would-be receipt is the Order and the items bought listed on the receipt are OrderItem.

# Project Conceptualization
Intent: Run PostgreSQL in a Docker container and query it into a dashboard with Python.

## Conception
- **Input:** Data is inserted into the database via CLI or RPA equivalents.
- **Output:** A Dash dashboard for data visualization, with minimal to no API endpoints.

## Modular Architecture
This setup is akin to building a WarCraft or StarCraft base:

This project represents a **Level 1 resource depot**—a standalone DB unit with a built-in dashboard.  
To build more specialized or complex data depots, you can fork this project and expand upon it.

**Separate projects that can interface with the depot:**
- Typer CLI or other manual input tools
- Dedicated dashboard apps (including ones that aggregate multiple DBs)
- RPA bots or automated data-gathering workers
- API layers for online access
- Frontend (FE) that connects to any API, turning it into a full-stack setup—but links can change anytime.

## Galactic Formics Hive Metaphor
1. **Hive Queen (me):** A singular entity guiding the hive's expansion. The hive grows through replication and evolution of units.
2. **The Nest Planet:**  
   - **Pollen Depots (DB):** Stores pollen (data), with built-in honey refining (dashboard and analytics) for that depot's pollen.  
   - **Refinery (dedicated dashboard and analytics):** Refines honey more robustly, often aggregating pollen from multiple depots.  
   - **Queen Control Panels:** Extra functionality for manual management of pollen depots (admin tools, query builders, etc.).  
3. **Cyberspace Units:**  
   - **Barracks (bots):** Hatches squads of formics. They can be scouts, gatherers, web crawlers, IoT sensors, etc.  
   - **StarGates (API):** Pollen transporters floating in cyberspace, connecting different units across the hive and beyond.  
   - **Outposts (FE or CURL):** Outpost units interact with other planets (e.g. Terrans) and outposts but never the hive.

# Backlog
## Dashboard ongoing: could do / skipped
- [ ] You can run a script from the CLI as a package, so maybe no need Typer CLI.
Just make a "control panel" script package.
- [ ] make bestseller / whalers chart toggleable
- [ ] You can make a donut chart of whalers once you figure out the cutoff criteria.
Right now I can just eyeball it coz there aren't many usernames.
- [ ] maybe change both bar charts into tree bark maps (you'll see proportion of products/spenders from total revenue)
- [ ] Implement a bestsellers/spenders chart that adapts to the filtered rows in the orders overview table and 
overlaps with the all-time data for comparison purposes.
### more could do next
- [ ] dockerizing BE for production
- [ ] how to migrate this localhost DB to a cloud DB (workplace reality)

## Lessons learned from doing this project
1. Setup PostgreSQL in Docker with SQLAlchemy and initialized tables
2. Implemented Infras for the DB: DAO, CRUD, Alembic ORM for schema migration, Faker Data, and loading dot env.
3. Implemented Infras for Dashboarding. Busywork code aside, the meat to practice further are:
   1. Writing SQLAlchemy queries = learning to write those one-lines that goes into a python variable.
   This means learning raw SQL would be useless, since SQLAlchemy is pythonic like calling model objects.
   2. Trying more kinds of Dash charts, including advanced topics like callbacks and dynamic UIs.
4. Added some basic dashboard components:
   1. [KPI card](https://github.com/Silcrow/learn-dashb-a-db/commit/b5185fa5d62d967b91905c2258c1612537cf5017) (easy)
   2. [collapsible table](https://github.com/Silcrow/learn-dashb-a-db/commit/645c07726103d66b2f089ffb28e98c04a0dbfd47#diff-cdc1cbda46dc4e05f73d5131ccc477279b71c99adb92241beda2eba5652b2e20)
   3. [bestselling products chart](https://github.com/Silcrow/learn-dashb-a-db/commit/cf037787a1199e5fae6e33c6e4a708ea109e34f1)
   4. [top spenders chart](https://github.com/Silcrow/learn-dashb-a-db/commit/cb21a754b65fd43d3f99697ddbf95b07bf4eb80a)
      1. Modify query to [filter for top spenders](https://github.com/Silcrow/learn-dashb-a-db/commit/dd11b4e1f55b888d17b14c8e5c11eb3a45bf78e6)
      2. [split bar](https://github.com/Silcrow/learn-dashb-a-db/commit/a62d019de310c49089ed6b36f3c776c58132d158) (donut chart equivalent)
      3. slider mechanism with callback