[Dokumentation](../README.md) › [Data Vault 2.1 - Benutzer-Dokumentation](README.md)

# 12. Häufige Fragen (FAQ)

### Für Analysten & Endanwender

**F: Wie finde ich den aktuellen Stand eines Unternehmens?**
```sql
SELECT * FROM vault.sat_company 
WHERE dss_is_current = 'Y'
  AND hk_company = '<hash>';
```

**F: Wie sehe ich alle historischen Änderungen?**
```sql
SELECT * FROM vault.sat_company 
WHERE hk_company = '<hash>'
ORDER BY dss_load_date DESC;
```

**F: Wie war der Stand am 01.06.2024?**
```sql
-- Option 1: Mit PIT-Tabelle (schnell)
SELECT * FROM vault.pit_company p
JOIN vault.sat_company s ON p.hk_company = s.hk_company 
WHERE p.snapshot_date = '2024-06-01';

-- Option 2: Direkt (für einzelne Abfragen)
SELECT * FROM vault.sat_company 
WHERE dss_load_date <= '2024-06-01'
  AND (dss_end_date > '2024-06-01' OR dss_end_date IS NULL);
```

**F: Wie viele Kunden haben wir?**
```sql
SELECT COUNT(*) 
FROM vault.link_company_role 
WHERE role_code = 'CLIENT';
```

**F: Welche Unternehmen sind in Deutschland?**
```sql
SELECT c.name, co.name AS country
FROM vault.sat_company c
JOIN vault.link_company_country lcc ON c.hk_company = lcc.hk_company
JOIN vault.sat_country co ON lcc.hk_country = co.hk_country
WHERE c.dss_is_current = 'Y' 
  AND co.name = 'Deutschland';
```

### Für Entwickler

**F: Warum werden meine Änderungen nicht übernommen?**
- Prüfen Sie mit `dbt run --select <model>` ob das Model läuft
- Bei inkrementellen Models: `dbt run --full-refresh --select <model>`
- Logfiles prüfen: `logs/dbt.log`

**F: Wie füge ich ein neues Feld hinzu?**
1. In `sources.yml` die Spalte zur External Table hinzufügen
2. In `stg_*.sql` die Spalte übernehmen
3. In `sat_*.sql` die Spalte zum Payload hinzufügen
4. `dbt run --full-refresh --select sat_*`

**F: Was bedeutet "Hash Diff has changed"?**
Das bedeutet, dass sich mindestens ein Attribut geändert hat. Der Hash Diff ist ein "Fingerabdruck" aller Attribute - ändert sich einer, ändert sich der Fingerabdruck.

---

◀ [Changelog](14-changelog.md) · [Übersicht](README.md) · [Glossar](16-glossar.md) ▶
