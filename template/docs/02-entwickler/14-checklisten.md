---
title: "Checklisten"
tags:
  - entwickler
  - typ/checkliste
---
[Dokumentation](../README.md) › [Data Vault 2.1 - Developer Guide](README.md)

# ✅ Checklisten

### Neue Entity Checkliste

```
□ External Table in sources.yml definiert
□ Staging View erstellt (<concept>_<entity>.sql)
  □ automate_dv.stage() YAML Metadata Pattern
  □ Hash Key definiert in hashed_columns
  □ Hash Diff definiert (falls Satellite)
  □ Reserved Keywords via _escape escaped
  □ Metadata-Spalten als derived_columns
□ Hub erstellt (hub_<entity>.sql)
□ Satellite erstellt (sat_<entity>.sql)
  □ Post-Hook für dss_is_current
□ Link erstellt (falls Beziehung)
□ Tests in schema.yml hinzugefügt
□ dbt run-operation stage_external_sources
□ dbt run --select +raw_vault.<concept>.hub_<entity> +raw_vault.<concept>.sat_<entity>
□ dbt test --select raw_vault.<concept>
□ Ghost Records erweitert (optional)
□ Design-Dokumentation in design/ nachgezogen
□ Dokumentation aktualisiert
```

### Attribut hinzufügen Checkliste

```
□ Spalte in sources.yml hinzugefügt
□ Spalte in Staging View hashed_columns/hashdiff hinzugefügt (falls getrackt)
□ Spalte in Satellite src_payload hinzugefügt
□ dbt run-operation stage_external_sources
□ dbt run --full-refresh --select <concept>_* sat_*
□ dbt test
```

### Pre-Deployment Checkliste

```
□ Alle Tests lokal bestanden
□ SQL kompiliert und geprüft
□ Keine hardcoded Datenbanknamen
□ +as_columnstore: false gesetzt
□ Hash-Separator ist '||' (concat_string in dbt_project.yml)
□ Bei Hash-Input-Änderungen: Full Refresh eingeplant
□ Git committed und gepusht
□ Merge Request erstellt und CI erfolgreich ✓
```

### CI/CD Troubleshooting

| Problem | Lösung |
|---------|--------|
| CI läuft nicht | Prüfen, ob Änderungen unter `models/`, `macros/`, `seeds/`, `dbt_project.yml` oder `packages.yml` liegen (Path Filter!) |
| Profile not found | `profile:` in `dbt_project.yml` muss zum generierten `profiles.yml` passen (`DBT_PROFILES_DIR`) |
| Runner offline | Runner-Dienst auf dem CI-Host neu starten (GitLab Runner bzw. Actions-Runner) |
| Tests schlagen nur in Test/Prod fehl | `dbt seed --target <mandant>-test` bzw. `--target <mandant>` ausführen |
| Login failed in der Pipeline | CI-Variablen für den DB-Zugang prüfen (Passwort abgelaufen?) |
| Job läuft in Timeout | Getaggte Massendaten-Domänen über die dafür vorgesehenen Jobs laden, nicht im Standardlauf |

---

◀ [Troubleshooting](13-troubleshooting.md) · [Übersicht](README.md) · [Weiterführende Dokumentation](15-weiterfuehrende-dokumentation.md) ▶
