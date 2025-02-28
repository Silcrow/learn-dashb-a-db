# learn-dashb-a-db
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

## Dev Guide
- Whenever you make schema changes, don't forget to modify the DAO (Data Access Object) and CRUD (Create, Read, Update, Delete) operations accordingly.
- The key technologies used here are: **PostgreSQL, SQLAlchemy, Alembic, and Dash**.

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

## Installation
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

## To run scripts inside packages
> The builtin CLI input system would be just running the package functions.

To run each `populate.py`'s functions:
- `python -m database.populate wipe_db`
- `python -m database.populate populate_fake_products`
- `python -m database.populate populate_db`

# Ongoing Dashboard design

## Notes
- [ ] Ideally I should get a hierarchical table where it only lists usernames. When I click, then the user's order appears.
When I click an order, then its items appears. The current table does it lazily by listing every product ordered.
You can work with that for bare functionality, by filtering each column. GPT says need `dash_ag_grid`, DBC, Dash callbacks, if I'll do it that way.
- 

## questions
- `dash_table` (1) what's the Aa button in the filter bar, what does it do? What can the select button do?
- [ ] You can run a script from the CLI as a package, so maybe no need Typer CLI.
Just make a "control panel" script package.