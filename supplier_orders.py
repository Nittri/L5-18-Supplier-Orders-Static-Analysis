
"""Track supplier purchase orders using SQLite."""

import logging
import sqlite3
from typing import Optional

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s",
)
LOGGER = logging.getLogger(__name__)


def create_connection() -> sqlite3.Connection:
    """Create an in-memory database and its orders table."""
    connection = sqlite3.connect(":memory:")
    connection.execute(
        """
        CREATE TABLE orders (
            id INTEGER PRIMARY KEY,
            supplier TEXT NOT NULL,
            item TEXT NOT NULL,
            quantity INTEGER NOT NULL CHECK (quantity > 0),
            received INTEGER NOT NULL DEFAULT 0 CHECK (received IN (0, 1))
        )
        """
    )
    return connection


def place_order(
    connection: sqlite3.Connection,
    supplier: str,
    item: str,
    quantity: int,
) -> int:
    """Insert an order safely and return its database-generated ID."""
    if not isinstance(supplier, str) or not supplier.strip():
        raise ValueError("Supplier must be a non-empty string.")
    if not isinstance(item, str) or not item.strip():
        raise ValueError("Item must be a non-empty string.")

    if (
        isinstance(quantity, bool)
        or not isinstance(quantity, int)
        or quantity <= 0
    ):
        raise ValueError(
            "Quantity must be a positive integer."
        )

    cursor = connection.execute(
        "INSERT INTO orders (supplier, item, quantity, received) "
        "VALUES (?, ?, ?, 0)",
        (supplier.strip(), item.strip(), quantity),
    )
    return int(cursor.lastrowid)


def mark_received(
    connection: sqlite3.Connection,
    order_id: int,
    remarks: Optional[str] = None,
) -> None:
    """Mark an existing order as received."""
    if (
        isinstance(order_id, bool)
        or not isinstance(order_id, int)
        or order_id <= 0
    ):
        raise ValueError("Order ID must be a positive integer.")

    cursor = connection.execute(
        "UPDATE orders SET received = 1 WHERE id = ?",
        (order_id,),
    )
    if cursor.rowcount == 0:
        raise ValueError(
            f"No order exists with ID {order_id}."
        )

    if remarks:
        LOGGER.info("Order %s received: %s", order_id, remarks)


def notify_warehouse(supplier: str) -> None:
    """Log a warehouse notification without invoking a system shell."""
    if not isinstance(supplier, str) or not supplier.strip():
        raise ValueError("Supplier must be a non-empty string.")

    LOGGER.info(
        "Notifying warehouse about supplier %s",
        supplier.strip(),
    )


def cleanup(connection: sqlite3.Connection) -> int:
    """Delete received orders and return the number deleted."""
    try:
        cursor = connection.execute(
            "DELETE FROM orders WHERE received = 1"
        )
        connection.commit()
        return cursor.rowcount
    except sqlite3.Error:
        connection.rollback()
        LOGGER.exception("Could not clean up received orders.")
        raise


def pending_count(connection: sqlite3.Connection) -> int:
    """Return the number of orders that have not been received."""
    row = connection.execute(
        "SELECT COUNT(*) FROM orders WHERE received = 0"
    ).fetchone()
    return int(row[0])


def main() -> None:
    """Run a short demonstration of the order tracker."""
    connection = create_connection()
    try:
        first_order = place_order(
            connection, "Acme Steel", "rods", 40
        )
        place_order(connection, "Bolt Co", "bolts", 500)
        mark_received(
            connection,
            first_order,
            "Delivered successfully",
        )
        notify_warehouse("Acme Steel")
        LOGGER.info("Pending orders: %d", pending_count(connection))
        LOGGER.info(
            "Received orders removed: %d",
            cleanup(connection),
        )
    finally:
        connection.close()


if __name__ == "__main__":
    main()
