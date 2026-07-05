# datavault-dbt-boilerplate

A [Copier](https://copier.readthedocs.io/) template for scaffolding new **Data
Vault 2.1** dbt projects on SQL Server / Azure SQL. Ships with generic hash-key
and satellite macros, the standard staging → hub/sat/link layering convention,
a working AdventureWorks reference implementation, and CI workflows for
`dbt build` + docs publishing.

This repository is the template itself — the actual project scaffold lives
under [`template/`](template/). `copier.yml` at the root defines the questions
asked when generating a new project.

## Create a new project from this template

Install Copier once:

```bash
pipx install copier
# or: uv tool install copier
```

Generate a new project:

```bash
copier copy gh:fellnerd/datavault-dbt-boilerplate my-customer-dbt-project
```

Copier will prompt for: project name, dbt profile name, company/author name,
GitHub org, example warehouse server / database name, schema names, hash
algorithm, and whether to include the AdventureWorks demo. Answers are
written to `.copier-answers.yml` in the new project — **do not delete this
file**, it is required for `copier update` later.

## Pull in later template improvements

From inside an already-generated project:

```bash
copier update
```

Copier re-applies your original answers (from `.copier-answers.yml`), diffs
against the current template version, and merges upstream boilerplate changes
(new macros, CI fixes, doc improvements) into your project — including
conflict markers for anything you've customized. Commit the result like any
other merge.

To change an answer after the fact (e.g. drop the AdventureWorks demo):

```bash
copier update --data include_example=false
```

## What's included

- `macros/` — 10 generic Data Vault 2.1 macros (hash keys, ghost records,
  satellite current-flag handling, schema naming, parquet/external-table
  helpers).
- `models/raw_vault/_common/{hubs,satellites,links}` — empty framework
  folders for your cross-source Data Vault objects.
- `models/raw_vault/adworks/`, `models/staging/adworks_*.sql` — optional
  AdventureWorks reference implementation (toggle via `include_example`).
- `design/` — Mermaid/Markdown design templates for hubs, links, PITs,
  bridges, and staging mappings.
- `docs/` — developer guide, architecture notes, lessons learned.
- `.github/workflows/` — generic CI (`dbt build` on PR) and docs-publishing
  workflows; `.github/workflows-examples/` has non-executing deploy pipeline
  patterns to adapt per customer.
- `scripts/setup_schemas.sql` — creates the staging/vault/mart schemas in a
  fresh target database so `dbt debug && dbt run` works right after setup.

## Template development

Test changes to the template locally before pushing:

```bash
copier copy . /tmp/smoke-test --defaults
```

## License

[MIT](LICENSE)
