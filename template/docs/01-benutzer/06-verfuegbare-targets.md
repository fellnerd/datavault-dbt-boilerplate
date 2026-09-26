---
title: "Verfügbare Targets"
tags:
  - benutzer
---
[Dokumentation](../README.md) › [Data Vault 2.1 - Benutzer-Dokumentation](README.md)

# 3. Verfügbare Targets

| Target | Umgebung | Befehl |
|--------|----------|--------|
| `<mandant>-dev` (Standard) | Entwicklung | `dbt run` |
| `<mandant>-test` | Test / Abnahme | `dbt run --target <mandant>-test` |
| `<mandant>` | Produktion | `dbt run --target <mandant>` |

Die konkreten Target- und Datenbanknamen des Mandanten stehen in `~/.dbt/profiles.yml` und in
der [Mandanten-Dokumentation](../projekt/README.md). Produktionsläufe erfolgen im
Regelfall über die Pipeline, nicht von Hand.

---

◀ [Tägliche Operationen](05-taegliche-operationen.md) · [Übersicht](README.md) · [Neue Entity hinzufügen](07-neue-entity-hinzufuegen.md) ▶
