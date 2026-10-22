# db 연결, 테이블 생성

import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "data" / "viz.db"


def get_connection():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")

    return conn


def init_db():
    with get_connection() as conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS departments (
                department_id INTEGER PRIMARY KEY,
                department_name TEXT NOT NULL UNIQUE
            );

            CREATE TABLE IF NOT EXISTS employees (
                employee_id INTEGER PRIMARY KEY,
                employee_name TEXT NOT NULL,
                department_id INTEGER NOT NULL,
                FOREIGN KEY (department_id)
                    REFERENCES departments(department_id)
            );

            CREATE TABLE IF NOT EXISTS budgets (
                budget_id INTEGER PRIMARY KEY,
                department_id INTEGER NOT NULL,
                budget_month TEXT NOT NULL,
                budget_amount INTEGER NOT NULL
                    CHECK (budget_amount >= 0),
                FOREIGN KEY (department_id)
                    REFERENCES departments(department_id),
                UNIQUE (department_id, budget_month)
            );

            CREATE TABLE IF NOT EXISTS expenses (
                expense_id INTEGER PRIMARY KEY,
                employee_id INTEGER NOT NULL,
                expense_date TEXT NOT NULL,
                category TEXT NOT NULL,
                description TEXT,
                amount INTEGER NOT NULL CHECK (amount >= 0),
                FOREIGN KEY (employee_id)
                    REFERENCES employees(employee_id)
            );

            CREATE INDEX IF NOT EXISTS idx_expense_date
                ON expenses(expense_date);
        """)
