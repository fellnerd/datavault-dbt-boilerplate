---
name: dv-docs
description: Pflegt die Projektdokumentation (Obsidian-Vault unter docs/) und den Changelog eines dbt/Data-Vault-Projekts nach der festen Vault-Struktur — richtige Ablage, Frontmatter, Tags, Callouts, Inhaltsverzeichnis und Navigation. Immer verwenden, wenn Doku geschrieben, ergänzt, verschoben oder geprüft wird, nach jeder Änderung an Modellen/Macros/Pipeline/Security (Changelog-Pflicht) sowie bei "Doku aktualisieren", "Kapitel anlegen", "Changelog", "Obsidian", "docs/".
---

# Projektdokumentation pflegen (Obsidian-Vault)

Die Doku liegt als Obsidian-Vault unter `docs/` (bzw. `docs/<vault>/`, erkennbar am Ordner
`.obsidian/`). Sie muss in Obsidian **und** in GitHub/GitLab lesbar sein. Maßstab: so viel
Text wie nötig, maximaler Informationsgehalt — Tabellen, konkrete Befehle, Vorlagen,
Prüfabfragen statt Prosa. Keine Dopplungen: auf das maßgebliche Kapitel verlinken.

## Struktur (verbindlich)

```
<vault>/
├── README.md                    Startseite (einzige README)
├── changelog.md                 Änderungsprotokoll — Pflicht bei jeder Änderung
├── 01-benutzer/                 Benutzerhandbuch: Konzepte, Spalten, Namenskonventionen, Installation,
│                                dbt-Befehle, neue Entity (Kurzablauf), Daten prüfen, Berechtigungen, FAQ, Glossar
├── 02-entwickler/               Entwicklerhandbuch: Leitfaden, Quick Reference, Projektstruktur, Tests,
│   └── 04-objekte-anlegen/      Deployment Workflow, Troubleshooting, Checklisten
│       ├── staging/             External Table, Staging View, PSA
│       ├── raw-vault/           Hub, Satellite, Link, Transaction Link, Eff/DC/MA-Satellite, Reference, Attribut hinzufügen
│       ├── business-vault/      Current View, PIT (Bridges, Soft Rules)
│       └── mart/                Dimensionale Modellierung (SCD1/2), persistierte Marts, Security
├── 03-system/                   allgemein/ (Übersicht … CI/CD, Macros), security/
├── 04-<mandant>-architektur/    PROJEKTSPEZIFISCH: projektdokumentation/, quellsysteme/,
│                                raw-vault/, business-vault/, information-mart/, meetings/, assets/
├── lessons-learned/             Entscheidungen, Fallstricke mit Messwerten
├── schulung/                    Handouts, Praxis-Durchstich, Use Cases
├── uebersichten/                Bases über den ganzen Vault
└── vorlagen/                    Vorlagen "Kapitel" und "Inhaltsverzeichnis"
```

**Handbücher 01–03 sind mandantenneutral** (Platzhalter `<mandant>`, `<concept>`, `<entity>`,
`<quelle>`, `<domain>`). Server, Datenbanken, Quellsysteme, Gruppen, Projektstand und das
konkrete Datenmodell gehören nach `04-<mandant>-architektur/`.

## Wohin gehört was?

| Inhalt | Ablage |
|--------|--------|
| Neue Quelle angebunden | `04-…/quellsysteme/<quelle>.md` (Herkunft, Tabellen, Business Keys, Besonderheiten) + Diagramm in `design/` → Sync nach `04-…/raw-vault/` |
| Neues Vault-/Mart-Objekt | Diagramm in `design/` (Skill `dv-design-sync`); nur bei neuem **Muster** ein Kapitel in `02-entwickler/04-objekte-anlegen/` |
| Business-Vault-Regel | `04-…/business-vault/00-business-vault.md` (Tabelle ergänzen) |
| Erkenntnis mit Messwert / Fehlschlag | `lessons-learned/NN-<thema>.md` |
| Meeting, Abstimmung, Analyse | `04-…/meetings/JJJJ-MM-TT-<thema>.md` bzw. `04-…/projektdokumentation/` |
| Neues Macro | Tabelle in `03-system/allgemein/*-wiederverwendbare-macros.md` |
| Pipeline-Änderung | `03-system/allgemein/*-ci-cd-pipeline.md`, ggf. `02-entwickler/*-deployment-workflow.md` |
| Neue Namensregel | `01-benutzer/*-namenskonventionen.md` |
| Jede Änderung an models/, macros/, seeds/, security/, Pipeline, Doku-Struktur | **Zeile in `changelog.md`** |

## Changelog (Pflicht)

Neue Zeile **direkt unter dem Tabellenkopf** von `<vault>/changelog.md`, im selben Commit
wie die Änderung:

```
| JJJJ-MM-TT | | <bereich> | <was + Wirkung, Objekte in `code`> | <Ticket/Commit> |
```

- Bereich: `staging` | `raw-vault` | `business-vault` | `mart` | `security` | `macros` | `pipeline` | `doku` | `betrieb`
- Version leer lassen; wird beim Release (`vX.Y.Z`) nachgetragen.
- Breaking Changes beginnen mit `BREAKING:` (Full Refresh nötig, Objekt/Spalte entfällt,
  Hash-Input geändert) und nennen die nötige Maßnahme.
- Eine Zeile je fachlicher Änderung, nicht je Datei. Kein Eintrag für reine Tippfehler.

## Notiz-Format

```markdown
---
title: "Anzeigename"                 # Pflicht (Plugin Front Matter Title zeigt ihn an)
aliases: ["Kurzname"]                # nur Inhaltsverzeichnisse
tags:
  - <bereich>                        # benutzer | entwickler[/staging|raw-vault|business-vault|mart] |
                                     # system[/security] | architektur[/raw-vault|business-vault|
                                     # information-mart|projektdokumentation|quellsysteme] |
                                     # lessons-learned | schulung[/…]
  - typ/<typ>                        # optional: inhaltsverzeichnis, nachschlagen, glossar, faq,
                                     # troubleshooting, checkliste, changelog, er-diagramm
---
[Dokumentation](<rel>/README.md) › [Index Ebene 1](…) › [Index Ebene 2](…)

# Titel

Inhalt …

---

◀ [Vorheriges](…) · [Übersicht](00-<ordner>.md) · [Nächstes](…) ▶
```

Regeln:
- **Dateinamen:** `NN-kebab-case.md`, keine Umlaute/Leerzeichen/Unterstriche; Inhaltsverzeichnis
  `00-<ordnername>.md` (steht in Obsidian oben), Base `00-<ordnername>.base`; datierte Dokumente
  `JJJJ-MM-TT-<thema>.md`; keine Suffixe wie `_v2`/`_final`.
- **Links:** nur relative Markdown-Links `[Text](../pfad/datei.md)`, **keine** `[[Wikilinks]]`.
  Links auf Repo-Dateien relativ zum Vault-Ort (`../../models/…`).
- **Hinweise als Callouts:** `> [!NOTE]`, `> [!TIP]`, `> [!WARNING]`, `> [!IMPORTANT]`.
- **Kein H1-Präfix** mit Nummern oder Emojis (`# Hub erstellen`, nicht `# 5.1 🔨 Hub erstellen`).
- **Neues Kapitel:** im Inhaltsverzeichnis des Ordners an der richtigen Stelle verlinken;
  Breadcrumb und Vor/Zurück-Navigation der Nachbarn anpassen (die Reihenfolge im
  Inhaltsverzeichnis ist maßgeblich).
- **Neuer Ordner:** `00-<ordner>.md` (Vorlage `vorlagen/inhaltsverzeichnis.md`) +
  `00-<ordner>.base`; in der Startseite und im übergeordneten Inhaltsverzeichnis verlinken.
- **Generierte Notizen** (Kommentar `<!-- generiert von scripts/sync_design_to_vault.py`) nie
  von Hand ändern — Quelle in `design/` ändern und Sync ausführen.
- **Diagramme:** Mermaid-Block in der `.md` (Obsidian rendert keine `.mmd`); Präsentationsfassung
  als Canvas über Skill `dv-er-diagram`.

## Prüfen vor dem Abschluss

1. Alle relativen Links der geänderten Notizen zeigen auf existierende Dateien
   (z. B. `grep -o '](\([^)]*\))'` + Existenzprüfung).
2. Frontmatter vorhanden (`title`, `tags`), Tag passt zum Ordner.
3. Kapitel im Inhaltsverzeichnis verlinkt, Navigation stimmt.
4. Keine Mandantendaten in 01–03 (Servernamen, Personen, Gruppen-Präfixe).
5. Changelog-Zeile vorhanden.

## CLAUDE.md des Projekts

Die Projekt-`CLAUDE.md` verweist auf diesen Skill und nennt den Vault-Pfad. Fehlt der
Abschnitt „Dokumentation“, ihn ergänzen:

```markdown
## Dokumentation
- Obsidian-Vault: `docs/` (Start `docs/README.md`), Struktur und Regeln: Skill `dv-docs`
- Bei jeder Änderung an models/, macros/, seeds/, security/ oder der Pipeline: Zeile in `docs/changelog.md`
- Projektspezifisches nur in `docs/04-<mandant>-architektur/`, Handbücher 01–03 bleiben neutral
```
