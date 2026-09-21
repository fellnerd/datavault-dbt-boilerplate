[Dokumentation](../README.md)

# Projektspezifische Dokumentation

Die Handbücher in `benutzer/`, `entwickler/`, `system/` und `security/` sind bewusst
projektunabhängig formuliert (Platzhalter wie `<mandant>`, `<concept>`, `<entity>`).

**Hierher gehört, was nur für dieses Projekt gilt:**

- Server, Datenbanken, Umgebungen und ihre Namen
- Angebundene Quellsysteme und ihre Besonderheiten
- Projektstand, Phasen, offene Punkte, Entscheidungslogbuch
- Konkrete Security-Kontexte, AD-Gruppen und Berechtigungsmatrix
- Architekturdiagramm und Business Case

Empfohlene Gliederung:

```
projekt/
├── README.md                 Überblick, Ansprechpartner
├── umgebungen.md             Server, Datenbanken, Targets
├── quellsysteme.md           Angebundene Systeme
├── security.md               Kontexte, Gruppen, Matrix
└── projektdokumentation/     Phasen, Stand, Entscheidungen
```
