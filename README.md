# Personal Expense Tracker (PET)

Personal Expense Tracker (PET) is a lightweight Streamlit application backed by MySQL that helps you track expenses per user, manage user accounts, and generate useful reporting views. It features a dark-themed glassmorphism UI and is built for quick data entry and simple analytics for personal finance tracking.

---

## Table of Contents

- [Features](#features)
- [Tech stack](#tech-stack)
- [Project structure](#project-structure)
- [Quick start](#quick-start)
- [Database setup](#database-setup)
- [Database schema](#database-schema)
- [SQL views (reporting)](#sql-views-reporting)
- [Application modules](#application-modules)
- [UI / UX details](#ui--ux-details)
- [Security notes & recommended improvements](#security-notes--recommended-improvements)
- [Development & testing](#development--testing)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

---

## Features

- **User management** — create, edit, and delete user accounts with username, email, and password.
- **Expense tracking** — add, edit, and delete expenses with amount, category, date, payment method, description, and location. Filter expenses by user.
- **Pre-built reporting views** — 14 SQL views providing aggregate and time-based analytics (highest/lowest by category, totals, averages, recent entries, etc.). Reports that contain a `user_id` are joined with the `users` table to display usernames.
- **Dark glassmorphism UI** — custom CSS with animated gradient background, frosted-glass containers, sidebar branding, and hover effects.
- **MySQL-backed storage** — all data persisted in MySQL with pandas integration for seamless DataFrame display.
- **Cached database connection** — `@st.cache_resource` ensures a single connection is reused across the session.

---

## Tech stack

| Component          | Technology                |
|--------------------|---------------------------|
| Language           | Python 3.10+              |
| Web framework      | Streamlit 1.31.1          |
| Data manipulation  | pandas 2.2.0              |
| Database connector | mysql-connector-python 8.2.0 |
| Database server    | MySQL (8.0+ recommended)  |
| UI / styling       | Custom CSS (glassmorphism) |

See `requirements.txt` for exact dependency pins.

---

## Project structure

```
Personal Expense Tracker/
├─ .gitignore
├─ requirements.txt
├─ README.md
├─ .streamlit/
│  └─ secrets.toml
├─ Data Dictionary/
│  ├─ Data Dictionary (PDF ver.).pdf
│  └─ Data Dictionary (Sheet ver.).xlsx
├─ Database & ERD/
│  ├─ ERD_expense_db.mwb
│  ├─ ERD_expense_db.pdf
│  ├─ expense_tracker_report (updated).sql
│  └─ personal_expense_tracker (updated).sql
├─ database.py
├─ expenses.py
├─ main.py
├─ reports.py
└─ users.py
```

---

## Quick start

1. **Clone the repository** and navigate to the tracker folder:

   ```bash
   git clone https://github.com/Miko-Explorer/MySQL-Based-Projects.git
   cd "MySQL-Based-Projects/Personal Expenses Tracker"
   ```

2. **Create and activate a virtual environment**, then install dependencies:

   ```bash
   python -m venv .venv
   # macOS / Linux
   source .venv/bin/activate
   # Windows
   .venv\Scripts\activate

   pip install -r requirements.txt
   ```

3. **Configure Streamlit secrets**:

   Create (or edit) `.streamlit/secrets.toml` with your MySQL credentials:

   ```toml
   [mysql]
   host = "localhost"
   user = "your_db_user"
   password = "your_db_password"
   database = "expense_db"
   port = 3306
   ```

   > **Important:** `.streamlit/secrets.toml` is listed in `.gitignore` and must never be committed to version control.

4. **Set up the database** — run the SQL scripts in order (see [Database setup](#database-setup)).

5. **Launch the app**:

   ```bash
   streamlit run main.py
   ```

   Open the URL shown in the terminal (typically `http://localhost:8501`).

---

## Database setup

SQL scripts are located in the `Database & ERD/` directory. Run them against your MySQL server in this order:

1. **Create database and tables:**

   ```bash
   mysql -u your_user -p < "Database & ERD/personal_expense_tracker (updated).sql"
   ```

   This script:
   - Creates the `expense_db` database (if it does not exist).
   - Creates the `users` table.
   - Creates the `expenses` table with a foreign key referencing `users(id)` and `ON DELETE CASCADE`.

2. **Create reporting views:**

   ```bash
   mysql -u your_user -p expense_db < "Database & ERD/expense_tracker_report (updated).sql"
   ```

   This creates the 14 views that `reports.py` queries.

Alternatively, open each file in MySQL Workbench or your preferred SQL client and execute the statements sequentially.

---

## Database schema

### `expense_db` database

#### `users` table

| Column     | Type              | Constraints                        |
|------------|-------------------|------------------------------------|
| `id`       | `INT`             | `PRIMARY KEY`, `AUTO_INCREMENT`    |
| `username` | `VARCHAR(100)`    | `NOT NULL`, `UNIQUE`               |
| `email`    | `VARCHAR(255)`    | `NOT NULL`, `UNIQUE`               |
| `passwords`| `VARCHAR(255)`    | `NOT NULL`                         |
| `created_at`| `TIMESTAMP`      | `DEFAULT CURRENT_TIMESTAMP`        |

#### `expenses` table

| Column          | Type              | Constraints                        |
|-----------------|-------------------|------------------------------------|
| `id`            | `INT`             | `PRIMARY KEY`, `AUTO_INCREMENT`    |
| `user_id`       | `INT`             | `NOT NULL`, `FOREIGN KEY → users(id) ON DELETE CASCADE` |
| `amount_spent`  | `DECIMAL(12,2)`   | `NOT NULL`                         |
| `category`      | `ENUM('Food','Transport','Utilities','Subscription','Health','Work','School','Entertainment','Insurance','Miscellaneous')` | |
| `description`   | `VARCHAR(500)`    |                                    |
| `dates`         | `DATE`            | `NOT NULL`                         |
| `payment_method`| `ENUM('Debit','Credit','Cash','Online Payment')` | |
| `location`      | `VARCHAR(255)`    |                                    |
| `created_at`    | `TIMESTAMP`       | `DEFAULT CURRENT_TIMESTAMP`        |
| `updated_at`    | `TIMESTAMP`       | `NULL` on insert, `ON UPDATE CURRENT_TIMESTAMP` |

---

## SQL views (reporting)

The `expense_tracker_report (updated).sql` script creates the following 14 views, all of which are consumed by `reports.py`:

| View name                              | Display name                                    | Has `user_id` |
|----------------------------------------|-------------------------------------------------|:-------------:|
| `high_expense_based_cat`               | Highest Amount Spent per Category (by User)     | Yes           |
| `low_expense_based_cat`                | Lowest Amount Spent per Category (by User)      | Yes           |
| `high_amount_paid_based_paymethod`     | Highest Amount Paid per Payment Method (by User)| Yes           |
| `low_amount_paid_based_paymethod`      | Lowest Amount Paid per Payment Method (by User) | Yes           |
| `latest_created_expense`               | 10 Most Recent Expenses (created_at)            | No            |
| `outdated_created_expense`             | 30 Oldest Expenses (created_at)                 | No            |
| `recently_updated_expense`             | Most Recently Updated Expenses                  | No            |
| `not_updated_expense`                  | Expenses Never Updated (oldest first)           | No            |
| `total_amount_spent`                   | Total Amount Spent (by User)                    | Yes           |
| `average_amount_spent_based_cat`       | Average Amount Spent per Category (by User)     | Yes           |
| `average_amount_spent_based_paymethod` | Average Amount Paid per Payment Method (by User)| Yes           |
| `total_amount_paid_based_paymethod`    | Total Amount Paid per Payment Method (by User)  | Yes           |
| `total_amount_spent_based_cat`         | Total Amount Spent per Category (by User)       | Yes           |
| `total_entries`                        | Total Number of Expense Entries                 | No            |

Views marked with `user_id` are queried with a `LEFT JOIN` on `users` so the `username` appears alongside the data. Empty results display "No data available for this report."

---

## Application modules

| Module | File | Role |
|--------|------|------|
| **Entry point** | `main.py` | Sets page config, injects dark glassmorphism CSS (animated gradient, frosted containers, styled inputs), renders sidebar with logo and radio navigation, routes to Users/Expenses/Reports pages. |
| **Database layer** | `database.py` | `get_db_connection()` — cached connection reading from `secrets.toml`. `run_query(query, params, fetch)` — parameterized executor returning a DataFrame (fetch) or affected row count (no fetch). |
| **User management** | `users.py` | `show_users()` — displays user table, add/edit/delete with confirmation checkbox. Edits only changed fields via dynamic UPDATE; cascading delete removes expenses. |
| **Expense management** | `expenses.py` | `show_expenses()` — filters expenses by user, add/edit/delete with full form (category, amount, date, payment method, location, description). Guards against empty user table. |
| **Report viewer** | `reports.py` | `show_reports()` — queries 14 SQL views, groups them into 4-per-tab layout. Views with `user_id` are LEFT JOINed with `users` to show usernames. Empty results show "No data available." |

---

## UI / UX details

- **Dark glassmorphism theme** — animated gradient background, frosted-glass containers (`backdrop-filter: blur(8px)`, `border-radius: 20px`), semi-transparent form inputs, and subtle borders.
- **Sidebar** — dark `#1E1E24` backdrop, centered "PET" logo with glow shadow, hidden-label radio navigation (Users / Expenses / Reports).
- **Interactions** — buttons glow blue on hover; data tables render with a transparent background; mutation actions trigger `st.rerun()` for instant UI refresh.

---

## Security notes & recommended improvements

- **Plain-text passwords** — the `passwords` column stores cleartext. Before deploying, hash with bcrypt/Argon2.
- **Secrets** — `.streamlit/secrets.toml` is git-ignored. For production, use environment variables or a secrets manager.
- **SQL injection** — mitigated via parameterized queries (keep this pattern).
- **Enhancements** — add input validation, rate limiting, TLS/SSL for DB and deployment.

---

## Development & testing

- **Run locally:** ensure MySQL is running with `expense_db` created, then `streamlit run main.py`
- **Schema changes:** update `reports.py` (view names, display names, `user_id` set) if altering views
- **Testing:** no test suite yet. Consider:
  - Unit tests for `run_query()` with a mock connection
  - Integration tests with a dedicated test DB
  - `streamlit.testing` for UI tests

---

## Contributing

- Fork the repo, create a feature branch (`feat/your-feature`), make changes, and open a PR.
- Avoid committing secrets or large binaries.

---

## License

Include your chosen license here (e.g., MIT).

---

## Contact

Maintained by **Miko-Explorer** — open an issue on [GitHub](https://github.com/Miko-Explorer/MySQL-Based-Projects).