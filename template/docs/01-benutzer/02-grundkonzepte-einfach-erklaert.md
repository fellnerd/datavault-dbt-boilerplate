---
title: "Grundkonzepte (einfach erklärt)"
tags:
  - benutzer
---
[Dokumentation](../README.md) › [Data Vault 2.1 - Benutzer-Dokumentation](README.md)

# Grundkonzepte (einfach erklärt)

### Die Bausteine des Data Vault

Unser Data Warehouse besteht aus verschiedenen Bausteinen. Hier eine einfache Erklärung:

#### 🔑 **Hubs** - "Die Visitenkarten"

Ein Hub ist wie eine **Visitenkarte** für jedes wichtige Geschäftsobjekt.

```
┌─────────────────────────────────────┐
│           hub_company               │
├─────────────────────────────────────┤
│  ID: ABC123                         │  ← Eindeutige Kennung
│  Erfasst am: 15.03.2024            │  ← Wann zum ersten Mal gesehen
│  Quelle: <Quellsystem>       │  ← Woher die Info stammt
└─────────────────────────────────────┘
```

**Beispiele in unserem System:**
- `hub_company` - Alle Unternehmen (Kunden, Lieferanten, Auftragnehmer)
- `hub_country` - Alle Länder

#### 📊 **Satellites** - "Die Aktenordner"

Ein Satellite ist wie ein **Aktenordner**, der alle Details und deren Änderungshistorie enthält.

```
┌─────────────────────────────────────┐
│         sat_company                 │
├─────────────────────────────────────┤
│  Firma ABC:                         │
│  ├── Version 1 (01.01.2024)        │
│  │   Name: "ABC GmbH"              │
│  │   Adresse: "Musterstr. 1"       │
│  │   Status: Aktuell ✓             │
│  ├── Version 2 (15.06.2024)        │
│  │   Name: "ABC AG"        ← Umfirmierung!
│  │   Adresse: "Musterstr. 1"       │
│  │   Status: Aktuell ✓             │
└─────────────────────────────────────┘
```

**Wichtige Satellites:**
- `sat_company` - Alle Firmendetails (Name, Adresse, Kontakt, ...)
- `sat_country` - Länderdetails (Name)
- `sat_company_client_ext` - Spezielle Kundendaten (Freistellungsbescheinigung)

#### 🔗 **Links** - "Die Verbindungen"

Ein Link verbindet Hubs miteinander - wie ein **Organisationsdiagramm**.

```
        hub_company                    hub_country
             │                              │
             └──────── link_company_country ┘
                  "ABC GmbH sitzt in Deutschland"
```

**Wichtige Links:**
- `link_company_role` - Welche Rolle hat ein Unternehmen? (Kunde/Lieferant/Auftragnehmer)
- `link_company_country` - In welchem Land sitzt das Unternehmen?
- `link_contact_contractor` - Welche Ansprechpartner hat ein Auftragnehmer?

#### 👶 **Dependent Child Satellites** - "Die Abhängigen"

Manchmal existiert ein Objekt nur im Kontext eines anderen - wie ein **Ansprechpartner** der nur durch seine Firma identifiziert werden kann:

```
        hub_contractor                    
             │                             
             └───── link_contact_contractor 
                           │
                    sat_contact_contractor_dc
                    (Name, E-Mail, Telefon des Ansprechpartners)
```

**Wann wird das verwendet?**
- Der Ansprechpartner hat keine eigene ID im Quellsystem
- Er wird durch Name + E-Mail identifiziert (= Dependent Child Keys)
- Die Attribute hängen am Link, nicht an einem eigenen Hub

**Wichtige DC Satellites:**
- `sat_contact_contractor_dc` - Ansprechpartner-Details für Auftragnehmer

#### ⏱️ **PIT-Tabellen** - "Der Zeitnavigator"

PIT (Point-in-Time) Tabellen sind wie ein **Kalender mit Lesezeichen** - sie helfen, schnell den Stand zu einem beliebigen Datum zu finden.

```
"Zeige mir alle Firmendaten, wie sie am 01.06.2024 waren"
     ↓
PIT-Tabelle findet sofort die richtigen Versionen
```

#### 👻 **Ghost Records** - "Die Platzhalter"

Manchmal fehlen Daten (z.B. ein Unternehmen ohne bekanntes Land). Ghost Records sind **Platzhalter** dafür:

- **Zero-Key** (000...000): "Diese Information ist unbekannt"
- **Error-Key** (FFF...FFF): "Hier ist ein Fehler aufgetreten"

---

◀ [Einführung: Was ist Data Vault?](01-einfuehrung-was-ist-data-vault.md) · [Übersicht](README.md) · [Wichtige Spalten verstehen](03-wichtige-spalten-verstehen.md) ▶
