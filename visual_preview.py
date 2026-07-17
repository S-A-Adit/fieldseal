from __future__ import annotations

import json
import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
PREVIEW_DB = Path(os.environ.get("ESENSE_VISUAL_PREVIEW_DB", BASE_DIR / "data" / "visual-preview.db"))

# This process is intentionally isolated from production data and secrets.
os.environ["ESENSE_DB_PATH"] = str(PREVIEW_DB)
os.environ.setdefault("SECRET_KEY", "visual-preview-session-key")
os.environ.setdefault("ESENSE_RECEIPT_SECRET", "visual-preview-receipt-key")
os.environ.setdefault("ESENSE_DOCUMENT_SECRET", "visual-preview-document-key")
os.environ.setdefault("ESENSE_MIDNIGHT_ENABLED", "true")
os.environ.setdefault("ESENSE_MIDNIGHT_NETWORK", "preprod")
os.environ.setdefault(
    "ESENSE_MIDNIGHT_CONTRACT_ADDRESS",
    "e5beb257fc5c6f6a999d7c00f5541b62426cf4d716e38cc50f2481e84b96721e",
)
os.environ.setdefault("ESENSE_MIDNIGHT_WORKER_TOKEN", "visual-preview-worker-token")

import app as esense  # noqa: E402
from flask import redirect, session  # noqa: E402


TIMESTAMP = "2026-07-17T20:10:00+00:00"
USER_ID = "usr_visual_preview"
ORGANIZATION_ID = "org_visual_preview"
ASSIGNMENT_ID = "asg_visual_preview"
SUBMISSION_ID = "sub_visual_preview"
PACKAGE_ID = "pkg_dfab3cdf0a6f4c779f54977d97ac56c1"
ANCHOR_ID = "mda_visual_preview"
COMMITMENT_SALT = "11" * 32
ANCHOR_TRANSACTION = "003e5a396df50fcdc6af13667a6fa4b1ef0fec812586f72c9a92fd4c0573970729"
ANCHOR_BLOCK_HASH = "6f76e449740e00070eebf41b3cf120e8ad7040ef034f5e02c650568b17716a22"


def seed_preview() -> None:
    manifest = {
        "demonstration": True,
        "report": esense.DEMO_PUBLIC_REPORT,
        "source": "local visual QA fixture",
    }
    commitment = esense.document_commitment(manifest, COMMITMENT_SALT)
    receipt_signature = esense.document_signature(manifest, commitment)
    encrypted_manifest = esense.encrypt_document_manifest(manifest, PACKAGE_ID)

    with esense.db() as connection:
        connection.execute("DELETE FROM midnight_anchors WHERE id = ?", (ANCHOR_ID,))
        connection.execute("DELETE FROM document_packages WHERE id = ?", (PACKAGE_ID,))
        connection.execute("DELETE FROM submissions WHERE id = ?", (SUBMISSION_ID,))
        connection.execute("DELETE FROM assignments WHERE id = ?", (ASSIGNMENT_ID,))
        connection.execute("DELETE FROM organizations WHERE id = ?", (ORGANIZATION_ID,))
        connection.execute("DELETE FROM users WHERE id = ?", (USER_ID,))

        connection.execute(
            """
            INSERT INTO users
                (id, google_sub, email, display_name, profile_json, created_at, updated_at)
            VALUES (?, ?, ?, ?, '{}', ?, ?)
            """,
            (USER_ID, "identity:visual-preview", "preview@example.test", "Visual preview", TIMESTAMP, TIMESTAMP),
        )
        connection.execute(
            """
            INSERT INTO organizations
                (id, name, organization_type, created_by, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (ORGANIZATION_ID, "Synthetic training organization", "school", USER_ID, TIMESTAMP, TIMESTAMP),
        )
        connection.execute(
            """
            INSERT INTO assignments
                (id, organization_id, title, purpose, desired_result, known_scope,
                 known_constraints, location_context, execution_context, due_at,
                 expected_submission, work_families_json, provider_id,
                 professional_responsible, version, status, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                ASSIGNMENT_ID,
                ORGANIZATION_ID,
                esense.DEMO_ASSIGNMENT_TITLE,
                "Demonstrate controlled work documentation.",
                "A complete synthetic report with an integrity receipt.",
                "Hardwired 48 A Level 2 EV charger on a dedicated 60 A branch circuit.",
                "Synthetic training data only.",
                "Synthetic residence / garage, Bradenton, Florida",
                "training_synthetic",
                "2026-07-31T12:00:00+00:00",
                "Load calculation, installation plan, test results, commissioning and handover documentation.",
                json.dumps(["electrical"]),
                USER_ID,
                "Synthetic qualified supervisor",
                1,
                "accepted_plan",
                TIMESTAMP,
                TIMESTAMP,
            ),
        )
        connection.execute(
            """
            INSERT INTO memberships
                (id, organization_id, email, user_id, roles_json, status, invited_by, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, 'active', ?, ?, ?)
            """,
            ("mem_visual_preview", ORGANIZATION_ID, "preview@example.test", USER_ID, json.dumps(["admin", "task_provider", "worker", "reviewer"]), USER_ID, TIMESTAMP, TIMESTAMP),
        )
        connection.execute(
            """
            INSERT INTO assignment_roles
                (id, assignment_id, role, email, user_id, status, created_at, updated_at)
            VALUES (?, ?, 'assigned_worker', ?, ?, 'assigned', ?, ?)
            """,
            ("rol_visual_preview", ASSIGNMENT_ID, "preview@example.test", USER_ID, TIMESTAMP, TIMESTAMP),
        )
        connection.execute(
            """
            INSERT INTO planning_drafts
                (id, assignment_id, user_id, data_json, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                "drf_visual_preview",
                ASSIGNMENT_ID,
                USER_ID,
                json.dumps(
                    {
                        "work_description": "Plan a hardwired 48 A Level 2 EV charger on a dedicated 60 A, 240 V branch circuit.",
                        "building_type": "residential",
                        "construction_site": "no",
                        "energized_proximity": "yes",
                        "responsibility_check": "The synthetic electrical contractor assigns the work and records the responsible license holder.",
                        "work_method": "Verify service capacity, isolate, install the branch circuit and EV charger, torque, test, commission and document.",
                        "risk_controls": "Secure isolation, control the garage work area, protect the cable route and follow equipment instructions.",
                        "tools_materials": "Electrical tester, torque tools, approved breaker and conductors, EV charger and manufacturer documentation.",
                        "tests_and_evidence": "Record load calculation, panel schedule, electrical tests, torque verification, commissioning and photographs.",
                        "open_questions": "Confirm the final owner handover recipient before issue.",
                    }
                ),
                TIMESTAMP,
                TIMESTAMP,
            ),
        )
        connection.execute(
            """
            INSERT INTO submissions
                (id, assignment_id, submitted_by, version, snapshot_json, status, submitted_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                SUBMISSION_ID,
                ASSIGNMENT_ID,
                USER_ID,
                1,
                json.dumps({"demonstration": True}),
                "accepted",
                TIMESTAMP,
                TIMESTAMP,
            ),
        )
        connection.execute(
            """
            INSERT INTO document_packages
                (id, assignment_id, organization_id, submission_id, version, title,
                 property_reference, summary, owner_email, status, manifest_json,
                 commitment_salt, commitment, receipt_signature, signing_method,
                 midnight_status, created_by, issued_at, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                PACKAGE_ID,
                ASSIGNMENT_ID,
                ORGANIZATION_ID,
                SUBMISSION_ID,
                1,
                esense.DEMO_PUBLIC_REPORT["title"],
                esense.DEMO_PUBLIC_REPORT["property_reference"],
                esense.DEMO_PUBLIC_REPORT["summary"],
                "owner@example.test",
                "issued",
                encrypted_manifest,
                COMMITMENT_SALT,
                commitment,
                receipt_signature,
                "server_hmac_sha256",
                "confirmed",
                USER_ID,
                TIMESTAMP,
                TIMESTAMP,
                TIMESTAMP,
            ),
        )
        connection.execute(
            """
            INSERT INTO midnight_anchors
                (id, package_id, commitment, operation, network, contract_address,
                 status, transaction_id, block_hash, block_height,
                 verification_method, attempts, submitted_at, confirmed_at,
                 created_at, updated_at)
            VALUES (?, ?, ?, 'register', 'preprod', ?, 'confirmed', ?, ?, ?,
                    'finalized_transaction', 1, ?, ?, ?, ?)
            """,
            (
                ANCHOR_ID,
                PACKAGE_ID,
                commitment,
                os.environ["ESENSE_MIDNIGHT_CONTRACT_ADDRESS"],
                ANCHOR_TRANSACTION,
                ANCHOR_BLOCK_HASH,
                1680106,
                TIMESTAMP,
                TIMESTAMP,
                TIMESTAMP,
                TIMESTAMP,
            ),
        )


@esense.app.get("/visual-preview/login")
def visual_preview_login():
    session.clear()
    session.permanent = True
    session["user_id"] = USER_ID
    esense.csrf_token()
    return redirect("/")


def main() -> None:
    seed_preview()
    esense.app.config["SESSION_COOKIE_SECURE"] = False
    port = int(os.environ.get("ESENSE_VISUAL_PREVIEW_PORT", "5055"))
    print(f"esense visual preview: http://127.0.0.1:{port}/en/demo-report")
    esense.app.run(host="127.0.0.1", port=port, debug=False)


if __name__ == "__main__":
    main()
