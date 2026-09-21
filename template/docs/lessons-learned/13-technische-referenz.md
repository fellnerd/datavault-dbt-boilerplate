[Dokumentation](../README.md) › [Lessons Learned - Data Vault 2.1 mit dbt auf Azure](README.md)

# Technische Referenz

### Verbindungsdaten
- **Server:** sql-datavault-weu-001.database.windows.net
- **Database:** DataVault
- **Auth:** Azure CLI (az login)

### VM Zugang
```bash
ssh <projekt>-dev  # Alias in ~/.ssh/config
cd ~/projects/datavault-dbt
source .venv/bin/activate
```

### GitHub Actions Runner
```bash
# Runner Service Status prüfen
sudo systemctl status actions.runner.fellnerd-datavault-dbt.dbt-runner-vm

# Runner neu starten
sudo systemctl restart actions.runner.fellnerd-datavault-dbt.dbt-runner-vm

# Runner Logs
journalctl -u actions.runner.fellnerd-datavault-dbt.dbt-runner-vm -f
```

### Aktueller Stand (2026-01-11)

**MDS Deployment-Updates (2026-01-11):**
- ✅ Deploy-Dialog auf Commits-Seite mit Modus-Auswahl (Load + Master / Nur Load)
- ✅ SSE-Streaming für Live-Logs während Deploy
- ✅ Korrektur: mds_load Tabellen heißen `<entity>` (nicht `load_<entity>`)
- ✅ API-Route korrigiert für konsistente Tabellennamen

**Data Vault Objekte:**
| Objekt | Records | Status |
|--------|---------|--------|
| `hub_company` | 22.457 | ✅ |
| `hub_country` | 242 | ✅ |
| `sat_company` | 22.457 | ✅ |
| `sat_country` | 242 | ✅ |
| `sat_company_client_ext` | ~7.500 | ✅ |
| `link_company_role` | 22.457 | ✅ |
| `link_company_country` | 22.457 | ✅ |
| `eff_sat_company_country` | 22.457 | ✅ |
| `pit_company` | ~900k | ✅ |
| `ref_role` | 3 | ✅ |

**Tests:** 39/39 bestanden

**DV 2.1 Optimierungen (2025-12-27):**
- ✅ Ghost Records Macro erstellt
- ✅ dss_is_current + dss_end_date in allen Satellites
- ✅ PIT-Tabelle für sat_company
- ✅ Effectivity Satellite für link_company_country
- ✅ Hash-Separator auf '^^' standardisiert

---

◀ [CI/CD Pipeline (GitHub Actions)](12-ci-cd-pipeline-github-actions.md) · [Übersicht](README.md) · [Multi-Active Satellite: Load Date muss ein BATCH-Wert sein (2026-08-17)](14-multi-active-satellite-load-date.md) ▶
