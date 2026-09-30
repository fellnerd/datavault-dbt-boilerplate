---
title: "Changelog"
aliases:
  - "Changelog"
  - "Änderungsprotokoll"
tags:
  - typ/changelog
---
[Dokumentation](README.md)

# Changelog

Alle fachlich oder technisch relevanten Änderungen an Modellen, Macros, Pipeline, Security und Dokumentation — neueste zuerst. **Wird von Entwicklern und den Claude-Agents (`dv-toolkit`, Skill `dv-docs`) bei jeder Änderung fortgeschrieben**, im selben Commit wie die Änderung.

<!-- Format (nicht entfernen, Agents lesen es):
| JJJJ-MM-TT | Version | Bereich | Änderung (was + Wirkung, Objekte in `code`) | Ticket/Commit |
- Neue Zeile direkt unter dem Tabellenkopf einfügen.
- Version: leer bis zum Release, dann vX.Y.Z nachtragen.
- Bereich: staging | raw-vault | business-vault | mart | security | macros | pipeline | doku | betrieb
- Breaking Changes (Full Refresh, entfallene Objekte/Spalten) mit "BREAKING:" beginnen.
-->

| Datum | Version | Bereich | Änderung | Ticket/Commit |
|-------|---------|---------|----------|---------------|
| 2026-09-30 | | raw-vault | BREAKING: Beispiel-Satellites nach Konvention `sat_<entity>__<quelle>` umbenannt (`sat_kunde` → `sat_kunde__adworks` usw.), Hash-Diff-Spalten im Staging auf `hd_<entity>__adworks`; bestehende Beispiel-Tabellen unter altem Namen bleiben liegen und können gelöscht werden | |
| 2026-09-30 | | doku | Beispiele vereinheitlicht und neutralisiert (Vertrieb/CRM: `hub_kunde`, `hub_bestellung`, `hub_vertrag`; Sensordaten: `hub_sensor`, `sat_sensor_messung_tl__iot`), Hashdiff-Alias einheitlich `hashdiff` | |
| 2026-09-27 | | doku | Dokumentation neu gegliedert: Inhaltsverzeichnisse `00-*.md`, Base je Handbuch, Kapitel Namenskonventionen, `04-objekte-anlegen/` (Staging, Raw Vault, Business Vault, Mart), Transaction Link, SCD1/SCD2, Deployment Workflow, zentraler Changelog, `04-mandant-architektur/` | |
| 2026-09-27 | | macros | Aus dem Referenzprojekt übernommen: `surrogate_key`, `satellite_current_view`, `create_clustered_index`, `create_load_status_table`/`log_load_status`, `log_row_counts`, `measure_rls_overhead`, Security-Macros (`tenant_key`, `rls_filter`, `cls_mask`, `security_policy`, `grant_select_on_views`) und `security/ddl` | |
| 2026-09-26 | | doku | Dokumentation als Obsidian-Vault (Frontmatter, Callouts, Graph, Lesezeichen, Vorlagen, Bases) | |
