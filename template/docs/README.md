---
title: "Start"
aliases:
  - "Start"
  - "Dokumentation"
tags:
  - typ/inhaltsverzeichnis
---
# Dokumentation

Einstiegspunkt für die Projektdokumentation. Fachsprache ist Deutsch.
Jedes Handbuch ist ein Ordner: `README.md` ist das Inhaltsverzeichnis, jedes Kapitel
eine eigene Datei mit Vor-/Zurück-Navigation am Fuss.

## Handbücher

Die Handbücher `01-benutzer/`, `02-entwickler/`, `03-system/`, `lessons-learned/` und `schulung/`
sind bewusst projektunabhängig formuliert (Platzhalter `<mandant>`, `<concept>`, `<entity>`).
Was nur für dieses Projekt gilt — Server, Datenbanken, Quellsysteme, Projektstand —, gehört nach
[`projekt/`](projekt/README.md).

| Bereich | Zielgruppe | Inhalt |
|---------|-----------|--------|
| [`01-benutzer/`](01-benutzer/README.md) | Analysten, Endanwender | Benutzerhandbuch: Grundkonzepte, tägliche Operationen, Troubleshooting, Datenzugriff, FAQ, Glossar |
| [`02-entwickler/`](02-entwickler/README.md) | Entwickler, Data Engineers | Entwicklerhandbuch: DV-Leitfaden, Staging, [Vault-Objekte](02-entwickler/objekte/README.md), Marts, Tests, Deployment |
| [`03-system/`](03-system/README.md) | Architekten, Betrieb | Systemdokumentation: Komponenten, Datenmodell, Umgebungen, Security, CI/CD, Reproduzierbarkeit |
| [`lessons-learned/`](lessons-learned/README.md) | alle | Entscheidungen, Fallstricke, Probleme & Lösungen — mit Messwerten |
| [`schulung/`](schulung/README.md) | Schulungsteilnehmende | Schulungsplan, Handouts, Praxis-Durchstich, Use Cases |

## Weitere Bereiche

| Ordner | Inhalt |
|--------|--------|
| [`projekt/`](projekt/README.md) | **Projektspezifisch:** Umgebungen, Quellsysteme, Projektstand, Entscheidungen, Architekturdiagramm |
| [`03-system/security/`](03-system/security/README.md) | Datenzugriffs-Security in der Praxis: sec-Schema, OLS/RLS/CLS, Berechtigungen, Rollout |
| [`MODEL_ARCHITECTURE.md`](MODEL_ARCHITECTURE.md) | Architekturmodell (Schemas, Layer, Hash-Berechnung) als Einzeldokument |

## Einstieg

| Wenn du … | dann hier starten |
|-----------|-------------------|
| die Plattform verstehen willst | [03-system/allgemein/01-uebersicht.md](03-system/allgemein/01-uebersicht.md) |
| Daten abfragen oder auswerten willst | [01-benutzer/01-einfuehrung-was-ist-data-vault.md](01-benutzer/01-einfuehrung-was-ist-data-vault.md) |
| ein neues Vault-Objekt bauen willst | [02-entwickler/05-neue-entity-erstellen-komplett.md](02-entwickler/05-neue-entity-erstellen-komplett.md) |
| einen Hub, Satellite oder Link anlegen willst | [02-entwickler/objekte/](02-entwickler/objekte/README.md) |
| wissen willst, was die `dss_*`-Spalten bedeuten | [03-system/allgemein/03-datenmodell.md](03-system/allgemein/03-datenmodell.md) |
| jemandem eine Berechtigung geben willst | [03-system/security/05-berechtigung-vergeben.md](03-system/security/05-berechtigung-vergeben.md) |
| den Projektstand suchst | [projekt/](projekt/README.md) |
| ein Problem debuggst | [lessons-learned/](lessons-learned/README.md) · [02-entwickler/13-troubleshooting.md](02-entwickler/13-troubleshooting.md) |

## Namenskonvention

- **Ordner und Dateien:** durchgehend Kleinschreibung, Wörter mit Bindestrich getrennt
  (`kebab-case`), keine Unterstriche, keine Leerzeichen, keine Umlaute im Dateinamen.
- **Kapiteldateien:** zweistelliges Präfix in Lesereihenfolge (`01-`, `02-`, …), der
  Ordner-`README.md` ist das Inhaltsverzeichnis.
- **Endung:** `.md` für Text, Assets im Unterordner `assets/` des jeweiligen Bereichs.
- **Datierte Dokumente** (z. B. Analysen, Klärungen, Use Cases): Präfix `JJJJ-MM-TT-` gefolgt vom
  Thema, z. B. `2026-07-06-anbindung-quellsystem-x.md`.
- **Sprache:** Dateinamen und Überschriften auf Deutsch, Fachbegriffe (Hub, Satellite,
  Link, Mart, Staging) bleiben unübersetzt.
- **Kein Versions- oder Statussuffix** im Dateinamen (`_v2`, `_final`, `_1`) — der Stand
  steht im Dokumentkopf, die Historie liegt in Git.

## Arbeiten mit Obsidian

Dieser Ordner (`docs/`) ist zugleich ein Obsidian-Vault (*Ordner als Vault öffnen*).
Damit die Doku in Obsidian **und** in GitHub/GitLab funktioniert, gilt zusätzlich:

- **Links:** nur relative Markdown-Links (`[Text](../ordner/datei.md)`), keine `[[Wikilinks]]`.
  Obsidian ist so eingestellt und zieht Links beim Umbenennen oder Verschieben automatisch nach.
- **Properties:** jede Notiz trägt `title` (Anzeigename in Explorer, Graph und Tabs über das Plugin
  „Front Matter Title“) und `tags` für ihren Bereich (z. B. `benutzer`, `system/security`) und bei
  Bedarf einen Typ (`typ/inhaltsverzeichnis`, `typ/glossar`, `typ/faq`, `typ/troubleshooting`,
  `typ/checkliste`, `typ/changelog`, `typ/er-diagramm`). Inhaltsverzeichnisse haben zusätzlich
  `aliases` mit dem Handbuchnamen, damit sie im Schnellwechsler nicht nur als „README" erscheinen.
- **Hinweise:** als Callouts (`> [!TIP]`, `> [!WARNING]`, `> [!IMPORTANT]`, `> [!NOTE]`) — werden in
  Obsidian, GitHub und GitLab als Hinweisboxen dargestellt.
- **Design-Diagramme:** Model-First-Quelle bleibt `design/`. Sollen ER-Diagramme im Vault erscheinen,
  spiegelt sie der Skill `dv-design-sync` (Skript `sync_design_to_vault.py`, Konfiguration
  `design/vault-sync.json`) nach `projekt/…-design/` — die Kopien nicht von Hand ändern.
- **Neue Kapitel:** über *Vorlage einfügen* mit den Vorlagen aus `vorlagen/` anlegen.
- **Übersichten (Bases):** [`dokumentation.base`](uebersichten/dokumentation.base) — alle Dokumente
  nach Bereich, zuletzt geändert, Nachschlagen, Handbücher, wenig verlinkte Seiten.
- **Graph-Ansicht:** Farbe je Bereich — Benutzer blau, Entwickler grün, System ocker,
  Projekt rot, Schulung türkis, Lessons Learned violett (gleiche Farbpunkte im Datei-Explorer).
  Diese Startseite ist im Graph ausgeblendet, weil sie mit jeder Notiz verbunden ist.
- **Gemeinsame Einstellungen:** Darstellung (CSS-Snippet `datavault`), Graph, Lesezeichen,
  Vorlagen und die Plugins „Front Matter Title“ und „Advanced Canvas“ liegen versioniert in
  `.obsidian/`; persönliche Arbeitsbereich-Dateien (`workspace*.json`) sind von Git ausgenommen.
