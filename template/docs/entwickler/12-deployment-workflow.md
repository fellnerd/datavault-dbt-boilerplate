[Dokumentation](../README.md) › [Data Vault 2.1 - Developer Guide](README.md)

# 🚢 Deployment Workflow

### CI/CD-Pipelines

Deployments laufen über die Pipeline, nicht von Hand. Es gibt zwei parallel gepflegte
Konfigurationen — Details in der [Systemdokumentation, Kapitel 10](../system/10-ci-cd-pipeline.md):

| Pipeline | Datei | Rolle |
|----------|-------|-------|
| GitLab CI | `.gitlab-ci.yml` | Primäre Pipeline (Merge-Request-Validierung, Deployments dev/test/prod, geplante Läufe) |
| GitHub Actions | `.github/workflows/` | Parallel gepflegte Workflows im Herstellerrepository |

Wird ein Deployment-Schritt geändert, muss er in **beiden** Konfigurationen nachgezogen werden.

| Auslöser | Was passiert |
|----------|--------------|
| Merge Request | `stage_external_sources` + `dbt compile` + `dbt test` gegen dev (ohne `tag:nightly` und Staging-Tests) |
| Push auf `dev` (Änderungen an `models/`, `macros/`, `seeds/`, `dbt_project.yml`, `packages.yml`) | Deployment nach dev |
| Push/manuell auf `test` | Deployment nach test; zusätzlich alle 30 Min. ein geplanter Lauf, der nur startet, wenn `vault.load_status_pending_v` einen neuen Quell-Load meldet |
| Tag `v*` bzw. manueller Job auf `main` | Deployment nach Produktion |
| Manuelle Domänen-Jobs | Getaggte Massendaten-Domänen laden (Staging → PSA → Vault → Mart) |
| Geplanter Nightly-Lauf | Langlaufende Tests (`tag:nightly`, Staging-Views auf External Tables) |

### Entwicklungs-Workflow

```bash
# 1. Änderungen entwickeln
dbt run --select <changed_models>

# 2. Tests lokal ausführen
dbt test --select <changed_models>

# 3. SQL prüfen
dbt compile --select <model>
cat target/compiled/datavault/models/path/to/model.sql

# 4. Commit & Push auf einen Feature-Branch bzw. dev
git add .
git commit -m "feat: <feature>"
git push origin <branch>

# 5. Merge Request erstellen → CI-Validierung läuft automatisch
```

Nach dem Merge nach `dev` deployt die Pipeline automatisch in die Dev-Datenbank; der Weg nach
Test und Produktion erfolgt über die entsprechenden Branches bzw. Tags.

### Manuelles Deployment (Ausnahmefall)

```bash
# 1. External Tables erstellen/aktualisieren
dbt run-operation stage_external_sources --target <mandant>-test

# 2. Seeds laden (falls geändert)
dbt seed --target <mandant>-test

# 3. Models deployen
dbt run --target <mandant>-test

# 4. Tests
dbt test --target <mandant>-test
```

### Full Refresh (Schema-Änderungen)

```bash
# Bei geänderten Hash-Inputs oder Typänderungen: Full Refresh erforderlich!
dbt run --full-refresh --select <model> --target <mandant>-test
```

> Neue Spalten allein brauchen keinen Full Refresh: `on_schema_change: append_new_columns`
> ergänzt sie, bestehende Zeilen bleiben für diese Spalte NULL. Ändert sich dagegen ein
> Hash-Input (Business Key, Hashdiff, Typ, Casing), ist ein Full Refresh nötig.

---

◀ [Tests hinzufügen](11-tests-hinzufuegen.md) · [Übersicht](README.md) · [Troubleshooting](13-troubleshooting.md) ▶
