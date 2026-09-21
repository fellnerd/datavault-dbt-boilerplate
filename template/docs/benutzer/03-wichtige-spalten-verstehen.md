[Dokumentation](../README.md) › [Data Vault 2.1 - Benutzer-Dokumentation](README.md)

# Wichtige Spalten verstehen

### Metadata-Spalten (dss_...)

Jede Tabelle hat spezielle Spalten, die mit `dss_` beginnen:

| Spalte | Bedeutung | Beispiel |
|--------|-----------|----------|
| `dss_load_date` | Wann wurde dieser Eintrag geladen? | `2024-12-27 14:30:00` |
| `dss_record_source` | Woher stammt die Information? | `<quellsystem>.<tabelle>` |
| `dss_is_current` | Ist das der aktuelle Stand? | `Y` = Ja, `N` = Historisch |
| `dss_end_date` | Bis wann war dieser Stand gültig? | `2024-06-15` oder `NULL` (=noch gültig) |

### Hash-Spalten (hk_..., hd_...)

| Spalte | Bedeutung | Wozu? |
|--------|-----------|-------|
| `hk_company` | Eindeutige ID für Firma | Verknüpfung zwischen Tabellen |
| `hd_company` | "Fingerabdruck" aller Attribute | Erkennt Änderungen automatisch |

---

◀ [Grundkonzepte (einfach erklärt)](02-grundkonzepte-einfach-erklaert.md) · [Übersicht](README.md) · [Erste Schritte](04-erste-schritte.md) ▶
