<!--
  Sync Impact Report
  Version change: 0.0.0 → 1.0.0 (initial adoption)
  Added sections:
    - Principle I: Odoo Module Standards
    - Principle II: Data Integrity & Security
    - Principle III: User Experience First
    - Principle IV: Testing & Quality
    - Principle V: Maintainability & Upgrade Safety
    - Section: Technology Stack & Constraints
    - Section: Development Workflow
    - Governance
  Removed sections: none (first version)
  Templates requiring updates:
    - .specify/templates/plan-template.md — ✅ no changes needed (generic)
    - .specify/templates/spec-template.md — ✅ no changes needed (generic)
    - .specify/templates/tasks-template.md — ✅ no changes needed (generic)
  Follow-up TODOs: none
-->

# ODesk IT Helpdesk Constitution

## Core Principles

### I. Odoo Module Standards

All code MUST follow the Odoo module structure and conventions:

- The module MUST be a valid Odoo addon with `__manifest__.py`
  and `__init__.py` at the root
- Models MUST extend `models.Model` or `models.TransientModel`
  and follow Odoo ORM conventions
- Views MUST use Odoo XML view architecture (form, tree, kanban,
  search views) with proper `ir.ui.view` records
- Security MUST be defined via `ir.model.access.csv` and
  `ir.rule` record rules
- Menu items, actions, and sequences MUST be declared in XML data
  files, not created programmatically at runtime
- Python code MUST follow the Odoo coding guidelines: method
  naming (`_compute_*`, `_onchange_*`, `_check_*`), field
  definitions on the model class body, and API decorators
  (`@api.depends`, `@api.constrains`, `@api.onchange`)

**Rationale**: Odoo has strict conventions that ensure modules are
installable, upgradable, and compatible with the broader ecosystem.
Deviating breaks the upgrade path and store publication eligibility.

### II. Data Integrity & Security

Every data operation MUST respect Odoo's security and integrity
framework:

- All models MUST have explicit access rights in
  `security/ir.model.access.csv`
- Sensitive operations (ticket reassignment, SLA override,
  escalation) MUST be protected by record rules scoped to
  appropriate groups
- SQL queries MUST NOT be used unless the ORM is provably
  insufficient; any raw SQL MUST use parameterized queries
- User input rendered in views MUST be escaped; QWeb templates
  MUST use `t-esc` by default, `t-raw` only with explicit
  sanitization justification
- Passwords, tokens, and API keys MUST use `ir.config_parameter`
  or Odoo's encrypted fields — never plain-text model fields

**Rationale**: Helpdesk modules handle internal IT data (asset
inventories, credentials, employee info). A security gap here
exposes the entire organization.

### III. User Experience First

The helpdesk interface MUST prioritize clarity and efficiency for
both end-users (ticket submitters) and IT staff:

- Ticket creation MUST be achievable in ≤ 3 clicks from the main
  menu
- Kanban and list views MUST show ticket status, priority, and
  assignee at a glance
- The module MUST support the Odoo website portal so external
  users can submit and track tickets without backend access
- Email integration MUST allow ticket creation and updates via
  `mail.thread` and `mail.activity.mixin`
- Dashboard views MUST provide IT managers with SLA compliance
  and workload distribution metrics

**Rationale**: An IT helpdesk tool is only valuable if people
actually use it. Friction in ticket submission leads to
shadow-IT and unreported issues.

### IV. Testing & Quality

Code MUST be testable and tested at the boundaries:

- Critical business logic (SLA computation, auto-assignment,
  escalation rules) MUST have unit tests using
  `odoo.tests.common.TransactionCase` or `HttpCase`
- Data migrations and post-init hooks MUST be tested against a
  populated demo database
- XML views MUST be validated by installing the module in a test
  Odoo instance — broken XML MUST NOT be committed
- Linting with `pylint-odoo` MUST pass with zero errors before
  merge

**Rationale**: Odoo modules are tightly coupled to the framework.
A broken view or bad migration can render the entire instance
unusable on upgrade.

### V. Maintainability & Upgrade Safety

The module MUST be designed for long-term maintenance across Odoo
versions:

- Model inheritance MUST prefer `_inherit` (extension) over
  `_inherits` (delegation) unless a new database table is
  genuinely required
- Monkey-patching or overriding private (`_`) Odoo methods MUST
  be documented with the Odoo version and reason, as these are
  unstable APIs
- Data files MUST use `noupdate="1"` for records that users are
  expected to customize (e.g., email templates, default stages)
- The module MUST NOT depend on community modules unless
  explicitly approved; dependencies MUST be limited to Odoo CE/EE
  core modules
- Version in `__manifest__.py` MUST follow `{odoo_version}.X.Y.Z`
  format (e.g., `18.0.1.0.0`)

**Rationale**: Odoo has a major release cycle roughly every 18
months. Modules that rely on private APIs or unnecessary
dependencies become unmaintainable across upgrades.

## Technology Stack & Constraints

- **Framework**: Odoo 18.0 (Community or Enterprise edition)
- **Language**: Python 3.10+
- **Frontend**: Odoo OWL framework for custom widgets; QWeb for
  templates and reports
- **Database**: PostgreSQL (managed by Odoo ORM — no direct DDL)
- **Testing**: `odoo.tests` framework, `pylint-odoo` for static
  analysis
- **Deployment**: Standard Odoo addon path; MUST be installable
  via Apps menu
- **Localization**: All user-facing strings MUST use Odoo's `_()`
  translation mechanism
- **Dependencies**: Only Odoo core modules (`mail`, `portal`,
  `base`, `web`) unless explicitly approved

## Development Workflow

- Feature branches MUST follow `{issue_number}-feature-name`
  naming convention
- Each PR MUST include: updated `__manifest__.py` version,
  security files if new models are added, and demo data for new
  features
- Module installation MUST be tested on a clean Odoo database
  before merge
- Code review MUST verify: access rights coverage, proper use of
  API decorators, view XML validity, and translation markup
- Commits MUST be atomic — one logical change per commit
- Demo data MUST be provided in `demo/` directory for all new
  models to support testing and evaluation

## Governance

This constitution is the authoritative guide for all development
decisions on the ODesk IT Helpdesk module. It supersedes
informal conventions and ad-hoc decisions.

- **Amendments** require: (1) a written proposal describing the
  change, (2) review by at least one other contributor, and
  (3) an updated version number following SemVer rules
- **Versioning**: MAJOR for principle removals or redefinitions,
  MINOR for new principles or expanded guidance, PATCH for
  wording clarifications
- **Compliance**: Every PR review MUST include a check against
  these principles. Non-compliance MUST be flagged and resolved
  before merge
- **Exceptions**: Any deviation from these principles MUST be
  documented in the PR description with a justification and a
  plan to return to compliance

**Version**: 1.0.0 | **Ratified**: 2026-03-30 | **Last Amended**: 2026-03-30
