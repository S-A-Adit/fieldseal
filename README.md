# esense

esense is a private, worker-first assignment and work-planning system for
professional organizations, schools, task providers, reviewers and assigned
workers.

[Live synthetic demonstration](https://esense.no/en/demo-report) | [Midnight receipt pilot](midnight/README.md)

This repository is the public hackathon snapshot. It contains synthetic demo
content only. Runtime databases, uploaded documents, credentials, private
state and generated contract artifacts are intentionally excluded.

The current production generation focuses on:

- organization membership with explicit roles;
- professional assignment briefs;
- private worker planning drafts;
- deterministic electro and ekom source considerations;
- deliberate, versioned planning submissions;
- a separate execution and final-inspection record with private drafts;
- independent review gates for both planning and completed work;
- encrypted documentation packages built from accepted plan and completion evidence;
- owner handover and purpose-bound recipient access;
- a protected report view for authorized recipients;
- selective recipient revocation and full package revocation;
- local integrity receipts with an explicit Midnight anchoring status.

The interface and professional source guidance can be shown in Norwegian or
English. Norwegian remains the default, the user's choice persists across the
sign-in and application screens, and user-entered assignment and report text is
never machine-translated. The central translation layer is designed to accept
reviewed Polish, Lithuanian and Latvian dictionaries later without duplicating
the application. Google and tenant-restricted Microsoft Entra ID can be enabled
independently. See `docs/microsoft-entra-oppsett.md` for the school IT setup.

Assignment does not imply competence, authorization, supervision or
professional responsibility. The source prompts are planning aids, not legal
decisions. A qualified person remains responsible for the final assessment.

The documentation helper currently uses deterministic policy and workflow
rules. It does not send assignment content to an external AI service. Private
package manifests are protected with AES-256-GCM. Only a salted commitment is
eligible for the separate Midnight pilot; the application reports
`not_submitted` until an independently verifiable transaction exists.

Production must keep `SECRET_KEY`, `ESENSE_RECEIPT_SECRET`, and
`ESENSE_DOCUMENT_SECRET` stable and outside the application directory. Losing
the document secret makes existing encrypted packages unreadable.

## Local verification

Create a virtual environment, install `requirements.txt`, copy `.env.example`
to `.env`, provide local development secrets, and run:

```text
python workflow_smoke.py
```

The smoke workflow covers the complete provider, worker, reviewer and outsider
lifecycle: assignment, private planning, plan approval, private execution
record, final-inspection approval, protected owner package, access grants,
Midnight receipt processing and revocation.

## Local visual QA

The public demonstration can be rendered locally without production access,
production data, browser extensions or live Midnight calls. Run:

```text
python visual_preview.py
```

Then open `http://127.0.0.1:5055/en/demo-report`. The preview uses the real
templates, styles and browser code with an isolated synthetic fixture that
represents a confirmed preprod anchor. It is suitable for desktop, mobile,
tooltip and accessibility review, but it is not evidence of a new network
transaction. Production truth remains available from the production health and
public demonstration API checks.

## Public English demonstration

`/en/demo-report` presents an English, synthetic example of an issued work
report. Its public API, `/api/public/midnight-demo`, returns fixed fictional
report content and only the package reference, commitment and verification
state from the matching synthetic database record. It must not return user,
recipient, organization or free-form database content.

The page uses the official dark Midnight logo from the Midnight brand hub only
at the proposed anchoring boundary and network status. It must not imply that
esense encryption or access control is provided by Midnight. The status remains
`not_submitted` and no transaction is shown until an independently verifiable
network receipt exists.

Inside the application, the same logo is intentionally used as a small
contextual mark rather than general branding. Hovering it, or focusing it with
a keyboard, explains the privacy boundary and current transaction claim.

## Production

Production runtime secrets stay outside version control, and the SQLite
database lives under the ignored `data/` directory. Neither credentials nor
production records are committed.

The legacy production system was archived before this generation was deployed.
No legacy users, jobs, uploads or records are imported automatically.
