# 테스트 데이터 생성 

import random
from datetime import date
from database import get_connection, init_db

random.seed(42)

DEPARTMENTS = [
    (1, "개발팀"),
    (2, "마케팅팀"),
    (3, "인사팀"),
    (4, "재무팀"),
    (5, "교육서비스팀"),
]

EMPLOYEES = [
    (1, "김민준", 1),
    (2, "이지훈", 1),
    (3, "박서연", 2),
    (4, "최유진", 2),
    (5, "정하늘", 3),
    (6, "한지우", 3),
    (7, "오세진", 4),
    (8, "강도윤", 4),
    (9, "윤서아", 5),
    (10, "임지호", 5),
]

CATEGORIES = [
    ("교통비", 20000, 100000),
    ("숙박비", 70000, 150000),
    ("식비", 10000, 50000),
    ("사무용품", 10000, 120000),
    ("교육훈련비", 50000, 200000),
]


def seed():
    init_db()

    with get_connection() as conn:
        # 개발용 샘플 데이터를 다시 생성할 수 있도록 초기화
        conn.execute("DELETE FROM expenses")
        conn.execute("DELETE FROM budgets")
        conn.execute("DELETE FROM employees")
        conn.execute("DELETE FROM departments")

        conn.executemany(
            "INSERT INTO departments VALUES (?, ?)",
            DEPARTMENTS
        )

        conn.executemany(
            "INSERT INTO employees VALUES (?, ?, ?)",
            EMPLOYEES
        )

        budgets = []
        budget_id = 1

        for month in ["2026-09", "2026-10"]:
            for department_id, _ in DEPARTMENTS:
                budgets.append((
                    budget_id,
                    department_id,
                    month,
                    3000000
                ))
                budget_id += 1

        conn.executemany(
            "INSERT INTO budgets VALUES (?, ?, ?, ?)",
            budgets
        )

        expenses = []

        for expense_id in range(1, 151):
            employee = random.choice(EMPLOYEES)
            category, minimum, maximum = random.choice(CATEGORIES)

            month = random.choice([9, 10])
            day = random.randint(1, 20)
            expense_date = date(2026, month, day).isoformat()

            amount = random.randrange(
                minimum, maximum + 1, 1000
            )

            expenses.append((
                expense_id,
                employee[0],
                expense_date,
                category,
                f"{category} 업무 지출",
                amount
            ))

        conn.executemany(
            """
            INSERT INTO expenses (
                expense_id,
                employee_id,
                expense_date,
                category,
                description,
                amount
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            expenses
        )

    print("VIZ ERP 데이터 생성 완료")
    print(f"부서: {len(DEPARTMENTS)}개")
    print(f"직원: {len(EMPLOYEES)}명")
    print(f"지출 내역: {len(expenses)}건")


if __name__ == "__main__":
    seed()
