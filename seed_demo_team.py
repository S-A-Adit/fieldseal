from __future__ import annotations

import argparse
import json

import app as esense


DEMO_TEAM = (
    {
        "key": "marta-kowalska",
        "name": "Marta Kowalska (syntetisk)",
        "email": "marta.kowalska@demo.esense.invalid",
        "role_title": "Elektrotekniker",
        "primary_family": "electrical",
        "roles": ["worker"],
    },
    {
        "key": "jonas-petrauskas",
        "name": "Jonas Petrauskas (syntetisk)",
        "email": "jonas.petrauskas@demo.esense.invalid",
        "role_title": "Ekomtekniker",
        "primary_family": "ekom",
        "roles": ["worker"],
    },
    {
        "key": "elina-ozola",
        "name": "Elina Ozola (syntetisk)",
        "email": "elina.ozola@demo.esense.invalid",
        "role_title": "Lærling",
        "primary_family": "both",
        "roles": ["worker"],
    },
    {
        "key": "ingrid-solheim",
        "name": "Ingrid Solheim (syntetisk)",
        "email": "ingrid.solheim@demo.esense.invalid",
        "role_title": "Faglig kontrollør",
        "primary_family": "electrical",
        "roles": ["reviewer"],
    },
)


def seed_demo_team(organization_id: str) -> list[str]:
    timestamp = esense.now_iso()
    created: list[str] = []

    with esense.db() as connection:
        organization = connection.execute(
            "SELECT id, created_by FROM organizations WHERE id = ?",
            (organization_id,),
        ).fetchone()
        if not organization:
            raise SystemExit(f"Unknown organization: {organization_id}")

        for person in DEMO_TEAM:
            user_id = f"usr_demo_{person['key'].replace('-', '_')}"
            membership_id = f"mem_demo_{person['key'].replace('-', '_')}"
            profile = json.dumps(
                {
                    "role_title": person["role_title"],
                    "primary_family": person["primary_family"],
                    "synthetic": True,
                },
                ensure_ascii=False,
            )
            connection.execute(
                """
                INSERT INTO users
                    (id, google_sub, email, display_name, profile_json, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(email) DO UPDATE SET
                    display_name = excluded.display_name,
                    profile_json = excluded.profile_json,
                    updated_at = excluded.updated_at
                """,
                (
                    user_id,
                    f"synthetic:demo-team:{person['key']}",
                    person["email"],
                    person["name"],
                    profile,
                    timestamp,
                    timestamp,
                ),
            )
            stored_user = connection.execute(
                "SELECT id FROM users WHERE lower(email) = lower(?)",
                (person["email"],),
            ).fetchone()
            connection.execute(
                """
                INSERT INTO memberships
                    (id, organization_id, email, user_id, roles_json, status,
                     invited_by, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, 'active', ?, ?, ?)
                ON CONFLICT(organization_id, email) DO UPDATE SET
                    user_id = excluded.user_id,
                    roles_json = excluded.roles_json,
                    status = 'active',
                    updated_at = excluded.updated_at
                """,
                (
                    membership_id,
                    organization_id,
                    person["email"],
                    stored_user["id"],
                    json.dumps(person["roles"]),
                    organization["created_by"],
                    timestamp,
                    timestamp,
                ),
            )
            created.append(person["name"])

        esense.audit(
            connection,
            "demo_team.seeded",
            organization["created_by"],
            organization_id,
            detail={"members": created, "synthetic": True},
        )

    return created


def main() -> None:
    parser = argparse.ArgumentParser(description="Add the synthetic demonstration team.")
    parser.add_argument("organization_id")
    args = parser.parse_args()
    for name in seed_demo_team(args.organization_id):
        print(name)


if __name__ == "__main__":
    main()
