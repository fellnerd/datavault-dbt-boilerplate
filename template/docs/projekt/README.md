---
title: "Projektspezifische Dokumentation"
aliases:
  - "Projekt"
  - "Projektspezifische Dokumentation"
tags:
  - projekt
  - typ/inhaltsverzeichnis
---
[Dokumentation](../README.md)

# Projektspezifische Dokumentation

Die Handbücher in `01-benutzer/`, `02-entwickler/`, `03-system/` und `lessons-learned/` sind bewusst
projektunabhängig formuliert (Platzhalter wie `<mandant>`, `<concept>`, `<entity>`).

**Hierher gehört, was nur für dieses Projekt gilt:**

- Server, Datenbanken, Umgebungen und ihre Namen
- Angebundene Quellsysteme und ihre Besonderheiten
- Projektstand, Phasen, offene Punkte, Entscheidungslogbuch
- Konkrete Security-Kontexte, AD-Gruppen und Berechtigungsmatrix
- Architekturdiagramm und Business Case
- Vault- und Mart-Design-Diagramme (Spiegel aus `design/`)

Empfohlene Gliederung:

```
projekt/
├── README.md                    Überblick, Ansprechpartner
├── business-case.md             Fachlicher Nutzen
├── umgebungen.md                Server, Datenbanken, Targets
├── quellsysteme/                Angebundene Systeme (je System eine Notiz)
├── security.md                  Kontexte, Gruppen, Matrix
├── projektdokumentation/        Phasen, Stand, offene Punkte, Entscheidungslogbuch, Glossar
├── datavault-design/            ER-Diagramme Raw Vault je Domäne (generiert aus design/)
├── information-mart-design/     ER-Diagramme Information Marts (generiert aus design/)
├── meetings/                    Protokolle, datiert: JJJJ-MM-TT-thema.md
└── assets/                      Bilder, PDFs (z. B. architektur.png)
```

> [!TIP]
> Notizen in diesem Ordner mit dem Tag `projekt` (bzw. `projekt/<unterordner>`) versehen —
> dann erscheinen sie in der Graph-Farbe des Bereichs und in der Base
> [Dokumentation](../uebersichten/dokumentation.base).
