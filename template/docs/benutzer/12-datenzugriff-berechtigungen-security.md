[Dokumentation](../README.md) › [Data Vault 2.1 - Benutzer-Dokumentation](README.md)

# 9. Datenzugriff & Berechtigungen (Security)

Der Zugriff auf die Daten ist auf drei Ebenen abgesichert. Das merkst du im Alltag so:

### Was du sehen kannst — und warum

| Ebene | Wirkung für dich |
|---|---|
| **Objektzugriff (OLS)** | Du siehst nur die Mart-Views deines Bereichs (z.B. `mart_finance`) — Rohdaten (`stg`, `vault`) sind grundsätzlich nicht zugänglich |
| **Zeilenfilter (RLS)** | Innerhalb einer Tabelle siehst du nur die Zeilen, für die du berechtigt bist (z.B. bestimmte Kostenstellen). Andere Zeilen fehlen **kommentarlos** — es gibt keine Fehlermeldung |
| **Spalten-Maskierung (CLS)** | Sensible Spalten (z.B. `person_name`) zeigen `***`, wenn dir die Freigabe fehlt — der Rest der Tabelle funktioniert normal |

### Zugriff beantragen

Der Zugriff besteht aus **zwei** Teilen — beide sind nötig:

1. **Objektzugriff**: Aufnahme in die Entra-ID-Gruppe deines Bereichs bei der IT beantragen,
   z.B. `<gruppen-prefix>-finance-employees-ro`. Damit darfst du die Views deines Bereichs *öffnen*.
2. **Zeilenberechtigung**: Legt fest, *welche* Zeilen du darin siehst.
   - Du darfst alles sehen → Aufnahme in `<gruppen-prefix>-finance-full-ro`
   - Du bist eingeschränkt (bestimmte Kostenstellen, Konten) → **Jira-Ticket**, der fachliche
     Data Owner gibt frei, danach wird dein Einzelrecht eingetragen

Fehlt Teil 2, kannst du die Views zwar öffnen, siehst aber **null Zeilen** — ohne
Fehlermeldung. Das ist der häufigste Fall bei neuen Nutzern.

3. **PII-Spalten** (z.B. Personennamen): eigenes Jira-Ticket, Freigabe durch den Data Owner.

### Häufige Fragen

**Ich sehe 0 Zeilen / weniger als erwartet.**
Deine Zeilen-Berechtigung fehlt oder ist zu eng. Prüfe zuerst die Entra-Gruppenmitgliedschaft (IT), dann per Ticket melden. Nach Gruppenänderungen einmal ab- und wieder anmelden.

**Eine Spalte zeigt nur `***`.**
Das ist die CLS-Maskierung — kein Fehler. Freigabe per Jira-Ticket beim Data Owner beantragen (Kontext `person_pii`).

**In Power BI sehen alle dasselbe / niemand etwas.**
Das SSO-Passthrough der Datenquelle ist nicht aktiv — bitte beim BI-Admin melden.

---

◀ [Best Practices](11-best-practices.md) · [Übersicht](README.md) · [Kontakt & Support](13-kontakt-support.md) ▶
