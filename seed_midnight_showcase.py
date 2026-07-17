from __future__ import annotations

import json
import secrets

import app as esense


USER_ID = "usr_midnight_showcase"
ORGANIZATION_ID = "org_midnight_showcase"
MEMBERSHIP_ID = "mem_midnight_showcase"
ASSIGNMENT_ID = "asg_midnight_showcase_v2"
ROLE_ID = "rol_midnight_showcase_v2"
SUBMISSION_ID = "sub_midnight_showcase_v2"
PACKAGE_ID = "pkg_midnight_showcase_v2"
PACKAGE_VERSION = 2
DEMO_EMAIL = "midnight-showcase@esense.invalid"


def create_showcase() -> tuple[str, bool]:
    timestamp = esense.now_iso()
    manifest = {
        "demonstration": True,
        "report": esense.DEMO_PUBLIC_REPORT,
        "document_set": [item["name"] for item in esense.DEMO_PUBLIC_REPORT["documents"]],
        "privacy_boundary": "Private report in esense; document commitment registered on Midnight.",
    }

    with esense.db() as connection:
        package = connection.execute(
            "SELECT id, commitment FROM document_packages WHERE id = ?",
            (PACKAGE_ID,),
        ).fetchone()
        if not package:
            connection.execute(
                """
                INSERT OR IGNORE INTO users
                    (id, google_sub, email, display_name, profile_json, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    USER_ID,
                    "identity:midnight-showcase",
                    DEMO_EMAIL,
                    "Synthetic report issuer",
                    json.dumps({"role_title": "Synthetic qualified supervisor"}),
                    timestamp,
                    timestamp,
                ),
            )
            connection.execute(
                """
                INSERT OR IGNORE INTO organizations
                    (id, name, organization_type, created_by, created_at, updated_at)
                VALUES (?, ?, 'school', ?, ?, ?)
                """,
                (ORGANIZATION_ID, "esense synthetic showcase", USER_ID, timestamp, timestamp),
            )
            connection.execute(
                """
                INSERT OR IGNORE INTO memberships
                    (id, organization_id, email, user_id, roles_json, status, invited_by, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, 'active', ?, ?, ?)
                """,
                (
                    MEMBERSHIP_ID,
                    ORGANIZATION_ID,
                    DEMO_EMAIL,
                    USER_ID,
                    json.dumps(["admin", "task_provider", "worker", "reviewer"]),
                    USER_ID,
                    timestamp,
                    timestamp,
                ),
            )
            connection.execute(
                """
                INSERT INTO assignments
                    (id, organization_id, title, purpose, desired_result, known_scope,
                     known_constraints, location_context, execution_context, due_at,
                     expected_submission, work_families_json, provider_id,
                     professional_responsible, version, status, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'training_synthetic', ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    ASSIGNMENT_ID,
                    ORGANIZATION_ID,
                    esense.DEMO_ASSIGNMENT_TITLE,
                    "Demonstrate a complete US residential EV charger handover package with privacy-preserving verification.",
                    "A synthetic issued report whose integrity can be verified without publishing private contents.",
                    "Hardwired 48 A Level 2 EV charger on a dedicated 60 A, 240 V branch circuit.",
                    "All people, places, measurements and work are fictional.",
                    esense.DEMO_PUBLIC_REPORT["property_reference"],
                    "2026-07-15T14:36:00+00:00",
                    "Complete issued report, handover documents and verification receipt.",
                    json.dumps(["electrical"]),
                    USER_ID,
                    "Synthetic qualified supervisor",
                    PACKAGE_VERSION,
                    "accepted_plan",
                    timestamp,
                    timestamp,
                ),
            )
            connection.execute(
                """
                INSERT INTO assignment_roles
                    (id, assignment_id, role, email, user_id, status, created_at, updated_at)
                VALUES (?, ?, 'assigned_worker', ?, ?, 'assigned', ?, ?)
                """,
                (ROLE_ID, ASSIGNMENT_ID, DEMO_EMAIL, USER_ID, timestamp, timestamp),
            )
            connection.execute(
                """
                INSERT INTO submissions
                    (id, assignment_id, submitted_by, version, snapshot_json, status, submitted_at, updated_at)
                VALUES (?, ?, ?, ?, ?, 'accepted', ?, ?)
                """,
                (
                    SUBMISSION_ID,
                    ASSIGNMENT_ID,
                    USER_ID,
                    PACKAGE_VERSION,
                    json.dumps({"demonstration": True, "report": esense.DEMO_PUBLIC_REPORT}),
                    timestamp,
                    timestamp,
                ),
            )

            salt = secrets.token_hex(32)
            commitment = esense.document_commitment(manifest, salt)
            signature = esense.document_signature(manifest, commitment)
            encrypted_manifest = esense.encrypt_document_manifest(manifest, PACKAGE_ID)
            connection.execute(
                """
                INSERT INTO document_packages
                    (id, assignment_id, organization_id, submission_id, version, title,
                     property_reference, summary, owner_email, status, manifest_json,
                     commitment_salt, commitment, receipt_signature, signing_method,
                     midnight_status, created_by, issued_at, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 'issued', ?, ?, ?, ?,
                        'server_hmac_sha256', 'not_submitted', ?, ?, ?, ?)
                """,
                (
                    PACKAGE_ID,
                    ASSIGNMENT_ID,
                    ORGANIZATION_ID,
                    SUBMISSION_ID,
                    PACKAGE_VERSION,
                    esense.DEMO_PUBLIC_REPORT["title"],
                    esense.DEMO_PUBLIC_REPORT["property_reference"],
                    esense.DEMO_PUBLIC_REPORT["summary"],
                    "demo-owner@esense.invalid",
                    encrypted_manifest,
                    salt,
                    commitment,
                    signature,
                    USER_ID,
                    timestamp,
                    timestamp,
                    timestamp,
                ),
            )
            package = {"id": PACKAGE_ID, "commitment": commitment}

        queued = esense.enqueue_midnight_anchor(
            connection,
            package["id"],
            package["commitment"],
            "register",
        )
        return package["id"], queued


def main() -> None:
    package_id, queued = create_showcase()
    state = "queued for Midnight anchoring" if queued else "present; no new anchor was queued"
    print(f"{package_id}: {state}")


if __name__ == "__main__":
    main()
