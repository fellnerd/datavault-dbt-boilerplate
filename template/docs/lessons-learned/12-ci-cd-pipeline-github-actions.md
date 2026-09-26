---
title: "CI/CD Pipeline (GitHub Actions)"
tags:
  - lessons-learned
---
[Dokumentation](../README.md) › [Lessons Learned - Data Vault 2.1 mit dbt auf Azure](README.md)

# CI/CD Pipeline (GitHub Actions)

### Implementierte Workflows (2025-12-27)

| Workflow | Datei | Trigger | Funktion |
|----------|-------|---------|----------|
| **CI** | `.github/workflows/ci.yml` | PR nach main/dev + Path Filter | dbt compile + dbt test |
| **Deploy Dev** | `.github/workflows/deploy-dev.yml` | Push auf main + manual | dbt run → Vault DB |
| **Deploy Prod** | `.github/workflows/deploy-prod.yml` | Tag v* + manual + Approval | dbt run → Vault_Jira |
| **Docs** | `.github/workflows/docs.yml` | Push auf main + manual | dbt docs → GitHub Pages |

### Path Filter Konfiguration
Workflows werden **nur** bei Änderungen an folgenden Pfaden getriggert:
- `models/**`, `macros/**`, `seeds/**`, `snapshots/**`, `tests/**`
- `dbt_project.yml`, `packages.yml`

**Kein Trigger bei:** `docs/**`, `*.md`

### Wichtige Ressourcen

| Ressource | Wert |
|-----------|------|
| **Service Principal** | `sp-github-datavault-dbt` |
| **Self-hosted Runner** | `dbt-runner-vm` auf VM 10.0.0.25 |
| **GitHub Secrets** | `AZURE_CLIENT_ID`, `AZURE_CLIENT_SECRET`, `AZURE_TENANT_ID` |
| **GitHub Pages** | https://fellnerd.github.io/datavault-dbt/ |
| **Environments** | `development`, `production` (mit Approval) |

### CI/CD Lessons Learned

1. **Profile-Name muss übereinstimmen:** `profiles.yml` Profile-Name muss mit `dbt_project.yml` → `profile:` übereinstimmen (`datavault`, nicht `datavault_jira`)

2. **DBT_PROFILES_DIR beachten:** Wenn `DBT_PROFILES_DIR` gesetzt ist, muss `profiles.yml` dort erstellt werden, nicht in `~/.dbt/`

3. **GitHub Pages vorher aktivieren:** Docs-Workflow schlägt fehl, wenn GitHub Pages nicht aktiviert ist

4. **Seeds in Prod:** `ref_role` Seed existiert nur in Dev - bei Prod-Deployment müssen Seeds mit `dbt seed --target jira` geladen werden

5. **Runner Version:** Aktuelle Runner-Version dynamisch ermitteln statt hardcoden

---

◀ [Best Practices](10-best-practices-gelernt.md) · [Übersicht](README.md) · [Technische Referenz](13-technische-referenz.md) ▶
