[Dokumentation](../README.md) › [Data Vault 2.1 - Benutzer-Dokumentation](README.md)

# 2. Tägliche Operationen

Das Standard-Target ist die Entwicklungsumgebung. Alle Befehle akzeptieren `--target`, um
gezielt gegen Development, Test oder Produktion zu laufen (siehe [Verfügbare Targets](06-verfuegbare-targets.md)).

### 2.1 Development

```bash
# Alle Models bauen (Standard-Target = Development)
dbt run

# Einzelnes Model bauen
dbt run --select <concept>_<entity>      # Staging View
dbt run --select hub_<entity>
dbt run --select sat_<entity>__<quelle>

# Model mit allen Abhängigkeiten
dbt run --select +hub_<entity>+

# Tests ausführen
dbt test

# SQL generieren ohne Ausführung
dbt compile
```

### 2.2 Test und Produktion

```bash
# Test-Umgebung
dbt run --target <mandant>-test

# Produktion (regulär über die CI/CD-Pipeline, manuell nur im Ausnahmefall)
dbt run --target <mandant>
```

### 2.3 External Tables aktualisieren

```bash
# Development
dbt run-operation stage_external_sources

# Andere Umgebung
dbt run-operation stage_external_sources --target <mandant>-test
```

> Domänen mit grossen Datenmengen (z. B. Call-Detail-Records oder Zeitreihen) sind mit einem
> Tag versehen und laufen **nicht** im regulären `dbt run`, sondern über eigene Pipeline-Jobs
> bzw. `--select tag:<tag>`.

---

◀ [Erste Schritte](04-erste-schritte.md) · [Übersicht](README.md) · [Verfügbare Targets](06-verfuegbare-targets.md) ▶
