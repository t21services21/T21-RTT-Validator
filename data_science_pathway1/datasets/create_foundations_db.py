import sqlite3
from pathlib import Path

# Path: data_science_pathway1/datasets/foundations.db
BASE_PATH = Path(__file__).resolve().parent
DB_PATH = BASE_PATH / "foundations.db"


def create_database(db_path: Path) -> None:
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    # Drop tables if they already exist (for repeatable runs while developing)
    cur.executescript(
        """
        DROP TABLE IF EXISTS payments;
        DROP TABLE IF EXISTS orders;
        DROP TABLE IF EXISTS products;
        DROP TABLE IF EXISTS customers;
        """
    )

    # Customers table (UK, US and other regions)
    cur.execute(
        """
        CREATE TABLE customers (
            customer_id   INTEGER PRIMARY KEY,
            first_name    TEXT,
            last_name     TEXT,
            country       TEXT,
            segment       TEXT
        );
        """
    )

    # Products table
    cur.execute(
        """
        CREATE TABLE products (
            product_id    INTEGER PRIMARY KEY,
            name          TEXT,
            category      TEXT,
            unit_price    REAL
        );
        """
    )

    # Orders table
    cur.execute(
        """
        CREATE TABLE orders (
            order_id      INTEGER PRIMARY KEY,
            customer_id   INTEGER,
            product_id    INTEGER,
            order_date    TEXT,
            order_value   REAL,
            FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
            FOREIGN KEY (product_id)  REFERENCES products(product_id)
        );
        """
    )

    # Payments table
    cur.execute(
        """
        CREATE TABLE payments (
            payment_id    INTEGER PRIMARY KEY,
            order_id      INTEGER,
            amount        REAL,
            payment_date  TEXT,
            method        TEXT,
            FOREIGN KEY (order_id) REFERENCES orders(order_id)
        );
        """
    )

    # Seed customers
    customers = [
        (1, "Amira", "Khan", "UK", "Retail"),
        (2, "James", "Smith", "UK", "Online"),
        (3, "Olivia", "Brown", "UK", "Corporate"),
        (4, "Ethan", "Johnson", "US", "Online"),
        (5, "Sophia", "Davis", "US", "SMB"),
        (6, "Liam", "Wilson", "US", "Enterprise"),
        (7, "Amina", "Okafor", "NG", "Retail"),
        (8, "Lucas", "Martin", "FR", "Online"),
    ]
    cur.executemany(
        "INSERT INTO customers VALUES (?, ?, ?, ?, ?);",
        customers,
    )

    # Seed products
    products = [
        (1, "Analytics Starter", "Software", 49.0),
        (2, "Analytics Pro", "Software", 99.0),
        (3, "Reporting Add-on", "Service", 29.0),
        (4, "Data Audit", "Consulting", 399.0),
        (5, "Training Bundle", "Training", 199.0),
    ]
    cur.executemany(
        "INSERT INTO products VALUES (?, ?, ?, ?);",
        products,
    )

    # Seed orders
    orders = [
        (1001, 1, 1, "2024-01-05", 49.0),
        (1002, 2, 2, "2024-01-06", 99.0),
        (1003, 3, 5, "2024-01-10", 199.0),
        (1004, 4, 2, "2024-01-11", 99.0),
        (1005, 5, 3, "2024-01-12", 29.0),
        (1006, 6, 4, "2024-01-15", 399.0),
        (1007, 4, 5, "2024-01-20", 199.0),
        (1008, 1, 3, "2024-01-21", 29.0),
        (1009, 7, 1, "2024-01-22", 49.0),
        (1010, 8, 2, "2024-01-25", 99.0),
    ]
    cur.executemany(
        "INSERT INTO orders VALUES (?, ?, ?, ?, ?);",
        orders,
    )

    # Seed payments
    payments = [
        (1, 1001, 49.0, "2024-01-05", "card"),
        (2, 1002, 99.0, "2024-01-06", "card"),
        (3, 1003, 199.0, "2024-01-11", "invoice"),
        (4, 1004, 99.0, "2024-01-11", "card"),
        (5, 1005, 29.0, "2024-01-13", "paypal"),
        (6, 1006, 399.0, "2024-01-16", "invoice"),
        (7, 1007, 199.0, "2024-01-21", "card"),
        (8, 1008, 29.0, "2024-01-22", "card"),
        (9, 1009, 49.0, "2024-01-23", "mobile"),
        (10, 1010, 99.0, "2024-01-26", "card"),
    ]
    cur.executemany(
        "INSERT INTO payments VALUES (?, ?, ?, ?, ?);",
        payments,
    )

    conn.commit()
    conn.close()


if __name__ == "__main__":
    print(f"Creating database at: {DB_PATH}")
    create_database(DB_PATH)
    print("Done.")
