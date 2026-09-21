# Dokumentation

Einstiegspunkt für die Projektdokumentation. Fachsprache ist Deutsch.
Jedes Handbuch ist ein Ordner: `README.md` ist das Inhaltsverzeichnis, jedes Kapitel
eine eigene Datei mit Vor-/Zurück-Navigation am Fuss.

## Handbücher

Die Handbücher sind bewusst projektunabhängig formuliert (Platzhalter `<mandant>`,
`<concept>`, `<entity>`). Was nur für dieses Projekt gilt — Server, Datenbanken,
Quellsysteme, Projektstand —, gehört nach [`projekt/`](projekt/).

| Bereich | Zielgruppe | Inhalt |
|---------|-----------|--------|
| [`system/`](system/) | Architekten, Betrieb | Systemdokumentation: Komponenten, Datenmodell, Umgebungen, Security, CI/CD, Reproduzierbarkeit |
| [`benutzer/`](benutzer/) | Analysten, Endanwender | Benutzerhandbuch: Grundkonzepte, tägliche Operationen, Troubleshooting, Datenzugriff, FAQ, Glossar |
| [`entwickler/`](entwickler/) | Entwickler, Data Engineers | Entwicklerhandbuch: DV-Leitfaden, Staging, [Vault-Objekte](entwickler/objekte/), Marts, Tests, Deployment |
| [`security/`](security/) | Entwickler, Betrieb | Berechtigungen: sec-Schema, OLS/RLS/CLS, Berechtigung vergeben, Verifikation, Rollout |
| [`lessons-learned/`](lessons-learned/) | alle | Entscheidungen, Fallstricke, Probleme & Lösungen — mit Messwerten |
| [`projekt/`](projekt/) | alle | **Projektspezifisch:** Umgebungen, Quellsysteme, Projektstand |

Ältere Einzeldokumente: [MODEL_ARCHITECTURE.md](MODEL_ARCHITECTURE.md) (Architekturmodell),
[CLAUDE.md](CLAUDE.md) (Hinweise für KI-Assistenten).

## Einstieg

| Wenn du … | dann hier starten |
|-----------|-------------------|
| die Plattform verstehen willst | [system/01-uebersicht.md](system/01-uebersicht.md) |
| Daten abfragen oder auswerten willst | [benutzer/01-einfuehrung-was-ist-data-vault.md](benutzer/01-einfuehrung-was-ist-data-vault.md) |
| ein neues Vault-Objekt bauen willst | [entwickler/05-neue-entity-erstellen-komplett.md](entwickler/05-neue-entity-erstellen-komplett.md) |
| einen Hub, Satellite oder Link anlegen willst | [entwickler/objekte/](entwickler/objekte/) |
| wissen willst, was die `dss_*`-Spalten bedeuten | [system/03-datenmodell.md](system/03-datenmodell.md) |
| jemandem eine Berechtigung geben willst | [security/05-berechtigung-vergeben.md](security/05-berechtigung-vergeben.md) |
| ein Problem debuggst | [lessons-learned/](lessons-learned/) · [entwickler/13-troubleshooting.md](entwickler/13-troubleshooting.md) |

## Namenskonvention

- **Ordner und Dateien:** durchgehend Kleinschreibung, Wörter mit Bindestrich getrennt
  (`kebab-case`), keine Unterstriche, keine Leerzeichen, keine Umlaute im Dateinamen.
- **Kapiteldateien:** zweistelliges Präfix in Lesereihenfolge (`01-`, `02-`, …), der
  Ordner-`README.md` ist das Inhaltsverzeichnis.
- **Endung:** `.md` für Text, Assets im Unterordner `assets/` des jeweiligen Bereichs.
- **Datierte Dokumente** (z.B. Analysen, Klärungen): Präfix `JJJJ-MM-TT-` gefolgt vom
  Thema, z. B. `2026-07-06-anbindung-quellsystem-x.md`.
- **Sprache:** Dateinamen und Überschriften auf Deutsch, Fachbegriffe (Hub, Satellite,
  Link, Mart, Staging) bleiben unübersetzt.
- **Kein Versions- oder Statussuffix** im Dateinamen (`_v2`, `_final`, `_1`) — der Stand
  steht im Dokumentkopf, die Historie liegt in Git.
