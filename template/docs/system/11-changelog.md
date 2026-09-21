[Dokumentation](../README.md) › [Data Vault 2.1 - Systemdokumentation](README.md)

# 11. Changelog

| Datum | Änderung |
|-------|----------|
| 2026-09-14 | Dokumentation kapitelweise aufgeteilt, mandantenunabhängig formuliert und gegen den Projektstand abgeglichen |
| 2026-07 | Security: OLS auf View-Grants umgestellt (`grant_select_on_views` als `on-run-end`-Hook), dimensionale RLS-Absicherung |
| 2026-06 | Energiedaten-Domäne (Zeitreihen/Lastgang) mit eigenem Schema und Tag ergänzt |
| 2026-05 | GitLab CI als primäre Pipeline (Stages validate/deploy, ADF-getriggerter Testlauf, Nightly Tests) |
| 2026-04 | Telecom-/CDR-Domäne mit PSA und eigenem Ladejob ergänzt |
| 2026-02 | Security-Fundament (`sec`-Schema, RLS/CLS-Funktionen, Rechtetabellen) eingeführt |
| 2025-12-28 | CI/CD mit GitHub Actions und Self-hosted Runner, dbt Docs via GitHub Pages |
| 2025-12-27 | DV-2.1-Optimierung: Ghost Records, PIT-Tabellen, Effectivity Satellites, `dss_is_current` + `dss_end_date` in Satellites |
| 2025-12-27 | Initial Release: Multi-Mandanten-Architektur, dbt-external-tables integriert |

> Hinweis: Der Hash-Separator wurde zwischenzeitlich auf `^^` umgestellt und ist heute wieder
> `||` (`concat_string` in `dbt_project.yml`) — massgeblich ist immer die Projektkonfiguration.

---

◀ [CI/CD Pipeline](10-ci-cd-pipeline.md) · [Übersicht](README.md) · [Wiederverwendbare Macros](12-wiederverwendbare-macros.md) ▶
