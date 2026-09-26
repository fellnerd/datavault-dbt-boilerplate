---
title: "Reproduzierbarkeit"
tags:
  - system
---
[Dokumentation](../../README.md) › [Data Vault 2.1 - Systemdokumentation](../README.md)

# 13. Reproduzierbarkeit

### Komplettes Deployment von Null

```bash
# 1. Repository und Umgebung
git clone <repository-url> && cd datavault-dbt
python3 -m venv .venv && source .venv/bin/activate
pip install dbt-core dbt-sqlserver

# 2. Verbindung konfigurieren (~/.dbt/profiles.yml, Profil "datavault")

# 3. dbt Packages installieren
dbt deps

# 4. Verbindung testen
dbt debug --target <mandant>-dev

# 4b. Security-Fundament deployen (einmalig pro Datenbank, VOR dbt run!)
#     security/ddl/01-03 + Service-User-Exemption + OLS
#     Anleitung: security/DEPLOYMENT.md

# 5. External Tables erstellen
dbt run-operation stage_external_sources --target <mandant>-dev

# 6. Reference Data laden
dbt seed --target <mandant>-dev

# 7. Alle Models bauen
dbt run --full-refresh --target <mandant>-dev

# 8. Ghost Records einfügen (optional)
dbt run-operation insert_ghost_records --target <mandant>-dev

# 9. Tests ausführen
dbt test --target <mandant>-dev
```

### Deployment in Test und Produktion

```bash
# Test
dbt run-operation stage_external_sources --target <mandant>-test
dbt seed --target <mandant>-test
dbt run --target <mandant>-test
dbt test --target <mandant>-test

# Produktion (regulär über die Pipeline, siehe Kapitel 10)
dbt run-operation stage_external_sources --target <mandant>
dbt seed --target <mandant>
dbt run --target <mandant>
dbt test --target <mandant>
```

> Domänen mit eigenem Tag (Massendaten wie CDR oder Zeitreihen) werden nicht vom regulären
> `dbt run` erfasst — sie laufen über die dafür vorgesehenen CI-Jobs bzw. `--select tag:<tag>`.

---

◀ [Wiederverwendbare Macros](12-wiederverwendbare-macros.md) · [Übersicht](../README.md) · [Weiterführende Dokumentation](14-weiterfuehrende-dokumentation.md) ▶
