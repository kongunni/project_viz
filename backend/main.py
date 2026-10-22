
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import get_connection, init_db

app = FastAPI(
    title="VIZ API",
    description="Enterprise AI Assistant",
    version="0.2.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["GET"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup():
    init_db()


@app.get("/")
def root():
    return {"message": "VIZ API Server is running"}


@app.get("/api/health")
def health():
    return {"status": "healthy"}


@app.get("/api/departments")
def get_departments():
    with get_connection() as conn:
        rows = conn.execute("""
            SELECT department_id, department_name
            FROM departments
            ORDER BY department_id
        """).fetchall()

        return [dict(row) for row in rows]


@app.get("/api/expenses/summary")
def get_expense_summary(month: str = "2026-10"):
    with get_connection() as conn:
        rows = conn.execute("""
            SELECT
                d.department_name,
                COUNT(e.expense_id) AS expense_count,
                COALESCE(SUM(e.amount), 0) AS total_amount
            FROM departments d
            LEFT JOIN employees emp
                ON d.department_id = emp.department_id
            LEFT JOIN expenses e
                ON emp.employee_id = e.employee_id
                AND substr(e.expense_date, 1, 7) = ?
            GROUP BY d.department_id, d.department_name
            ORDER BY total_amount DESC
        """, (month,)).fetchall()

        return {
            "month": month,
            "data": [dict(row) for row in rows]
        }
