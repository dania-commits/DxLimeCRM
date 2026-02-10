import sqlite3
import datetime as dt
from pathlib import Path

DB_PATH = Path("lime_demo.db")


def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS company (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            segment TEXT,
            city TEXT
        );
        """
    )

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS contact (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_id INTEGER,
            name TEXT NOT NULL,
            email TEXT,
            role TEXT,
            FOREIGN KEY(company_id) REFERENCES company(id)
        );
        """
    )

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS activity (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            contact_id INTEGER,
            kind TEXT NOT NULL,
            summary TEXT,
            created_at TEXT NOT NULL,
            due_date TEXT,
            status TEXT NOT NULL,
            FOREIGN KEY(contact_id) REFERENCES contact(id)
        );
        """
    )

    conn.commit()
    conn.close()


def prompt(msg: str) -> str:
    return input(msg).strip()


def create_company():
    print("\nNew company")
    name = prompt("Company name: ")
    segment = prompt("Segment (for example SaaS, manufacturing, public sector): ")
    city = prompt("City: ")

    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO company (name, segment, city) VALUES (?, ?, ?)",
        (name, segment or None, city or None),
    )
    conn.commit()
    conn.close()
    print("✔ Company saved.\n")


def list_companies():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM company ORDER BY name")
    rows = cur.fetchall()
    conn.close()
    if not rows:
        print("\nNo companies yet. Add one first.\n")
    else:
        print("\nCompanies:")
        for row in rows:
            print(f"[{row['id']}] {row['name']} ({row['segment'] or 'segment n/a'} - {row['city'] or 'city n/a'})")
        print()
    return rows


def create_contact():
    companies = list_companies()
    if not companies:
        return
    try:
        company_id = int(prompt("Choose company id for this contact: "))
    except ValueError:
        print("Please enter a valid id.\n")
        return
    name = prompt("Contact name: ")
    email = prompt("Email: ")
    role = prompt("Role (for example COO, CRM owner): ")

    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO contact (company_id, name, email, role) VALUES (?, ?, ?, ?)",
        (company_id, name, email or None, role or None),
    )
    conn.commit()
    conn.close()
    print("✔ Contact saved.\n")


def list_contacts():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT c.id, c.name, c.email, c.role, co.name AS company_name
        FROM contact c
        LEFT JOIN company co ON c.company_id = co.id
        ORDER BY co.name, c.name
        """
    )
    rows = cur.fetchall()
    conn.close()
    if not rows:
        print("\nNo contacts yet. Add one first.\n")
    else:
        print("\nContacts:")
        for row in rows:
            print(f"[{row['id']}] {row['name']} - {row['role'] or 'role n/a'} at {row['company_name'] or 'n/a'}")
        print()
    return rows


def create_activity():
    contacts = list_contacts()
    if not contacts:
        return
    try:
        contact_id = int(prompt("Choose contact id for this activity: "))
    except ValueError:
        print("Please enter a valid id.\n")
        return

    kind = prompt("Activity type (call, meeting, email, task): ")
    summary = prompt("Short summary: ")
    due_raw = prompt("Follow-up date (YYYY-MM-DD, optional): ")
    if due_raw:
        try:
            due_date = dt.datetime.fromisoformat(due_raw).date().isoformat()
        except ValueError:
            print("Could not parse date, storing as today.")
            due_date = dt.date.today().isoformat()
    else:
        due_date = None

    created_at = dt.datetime.now().isoformat(timespec="seconds")

    status = "open"
    if kind.lower() in {"call", "meeting"} and due_date:
        status = "follow-up scheduled"

    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO activity (contact_id, kind, summary, created_at, due_date, status)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (contact_id, kind, summary, created_at, due_date, status),
    )
    conn.commit()
    conn.close()
    print("✔ Activity saved. Trigger status:", status)
    print()


def view_pipeline():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT
            a.id,
            a.kind,
            a.summary,
            a.created_at,
            a.due_date,
            a.status,
            c.name AS contact_name,
            co.name AS company_name
        FROM activity a
        LEFT JOIN contact c ON a.contact_id = c.id
        LEFT JOIN company co ON c.company_id = co.id
        ORDER BY
            CASE
                WHEN a.status = 'follow-up needed' THEN 0
                WHEN a.status = 'follow-up scheduled' THEN 1
                ELSE 2
            END,
            a.due_date IS NULL,
            a.due_date
        """
    )
    rows = cur.fetchall()
    conn.close()

    if not rows:
        print("\nNo activities yet. Add one first.\n")
        return

    print("\nActivity overview (simple Lime-style board):")
    today = dt.date.today()

    for row in rows:
        due_info = row["due_date"] or "no due date"
        status = row["status"]
        if row["due_date"]:
            due = dt.date.fromisoformat(row["due_date"])
            if due < today and status == "follow-up scheduled":
                status = "follow-up needed"

        print(
            f"[{row['id']}] {row['kind']} with {row['contact_name'] or 'n/a'} at {row['company_name'] or 'n/a'}"
        )
        print(f"    Summary : {row['summary']}")
        print(f"    Status  : {status}")
        print(f"    Created : {row['created_at']}  |  Due: {due_info}")
    print()


def main():
    init_db()
    menu = """Lime CRM mini sandbox - built by Dania

1) Add company
2) Add contact
3) Add activity (with simple trigger logic)
4) View activity board
5) Exit

Choose an option: """
    while True:
        choice = input(menu).strip()
        if choice == "1":
            create_company()
        elif choice == "2":
            create_contact()
        elif choice == "3":
            create_activity()
        elif choice == "4":
            view_pipeline()
        elif choice == "5":
            print("Goodbye.")
            break
        else:
            print("Please choose a number between 1 and 5.\n")


if __name__ == "__main__":
    main()