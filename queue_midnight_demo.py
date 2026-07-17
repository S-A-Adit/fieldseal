from __future__ import annotations

import app as esense


def main() -> None:
    if not esense.MIDNIGHT_READY:
        raise SystemExit("Midnight anchoring is not configured.")
    with esense.db() as connection:
        package = connection.execute(
            """
            SELECT p.id, p.commitment
            FROM document_packages p
            JOIN assignments a ON a.id = p.assignment_id
            WHERE a.title = ? AND a.execution_context = 'training_synthetic'
            ORDER BY p.issued_at DESC, p.version DESC
            LIMIT 1
            """,
            (esense.DEMO_ASSIGNMENT_TITLE,),
        ).fetchone()
        if not package:
            raise SystemExit("The synthetic demonstration package was not found.")
        queued = esense.enqueue_midnight_anchor(
            connection,
            package["id"],
            package["commitment"],
            "register",
        )
    print("Synthetic Midnight anchor queued." if queued else "Synthetic Midnight anchor already confirmed.")


if __name__ == "__main__":
    main()
