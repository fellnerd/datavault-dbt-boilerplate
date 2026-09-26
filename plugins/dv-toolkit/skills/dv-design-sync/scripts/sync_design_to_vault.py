#!/usr/bin/env python3
"""Spiegelt Mermaid-Diagramme aus design/ als Markdown-Notizen in einen Obsidian-Vault.

design/ bleibt die Model-First-Quelle (gepflegt über dv-design-sync). Obsidian rendert keine
.mmd-Dateien, nur ```mermaid-Blöcke in .md — dieses Skript erzeugt je Diagramm eine .md mit
Frontmatter, Breadcrumb, Quellverweis und dem Mermaid-Block.

Konfiguration: design/vault-sync.json im Repo-Root, z. B.
{
  "vault": "docs/datavault-ewb",
  "breadcrumb": [["Dokumentation", "README.md"], ["EWB — Architektur & Projekt", "ewb-architektur/README.md"]],
  "tags": ["typ/er-diagramm"],
  "groups": {
    "ewb-architektur/datavault-design": {"title": "Data-Vault-Design", "tag": "ewb-architektur/datavault-design"}
  },
  "diagrams": [
    {"source": "design/raw-vault/_common/er-finance.mmd",
     "target": "ewb-architektur/datavault-design/mart_finance/er-finance.md",
     "title": "Raw Vault — Finance",
     "extra": "Präsentationsfassung: [er-finance.canvas](er-finance.canvas)"}
  ]
}

Aufruf (aus dem Repo-Root):
  python3 scripts/sync_design_to_vault.py          # schreibt geänderte Dateien
  python3 scripts/sync_design_to_vault.py --check  # nur prüfen, Exit 1 wenn veraltet (CI)
"""
import json, os, posixpath, sys

MARK = "<!-- generiert von scripts/sync_design_to_vault.py aus {src} — nicht von Hand bearbeiten, Änderungen in design/ vornehmen -->"


def rel(target_dir, path):
    return posixpath.relpath(path, target_dir or ".").replace(" ", "%20")


def render(cfg, d):
    vault = cfg["vault"]
    tdir = posixpath.dirname(d["target"])
    group = next((g for g in sorted(cfg.get("groups", {}), key=len, reverse=True) if d["target"].startswith(g + "/")), None)
    ginfo = cfg.get("groups", {}).get(group, {})
    crumbs = [f"[{t}]({rel(tdir, p)})" for t, p in cfg.get("breadcrumb", [])]
    if group:
        crumbs.append(f"[{ginfo.get('title', group)}]({rel(tdir, group + '/README.md')})")
    tags = ([ginfo["tag"]] if ginfo.get("tag") else []) + cfg.get("tags", [])
    src_rel = posixpath.relpath(d["source"], posixpath.join(vault, tdir)).replace(" ", "%20")
    body = open(d["source"], encoding="utf-8").read().rstrip("\n")
    out = ["---", "title: " + json.dumps(d["title"], ensure_ascii=False), "tags:"] + [f"  - {t}" for t in tags] + ["---", MARK.format(src=d["source"]), " › ".join(crumbs), "",
           f"# {d['title']}", "",
           f"> **Kopie** von [`{d['source']}`]({src_rel}) — Model-First-Quelle ist `design/` (gepflegt über dv-design-sync).",
           "> Änderungen dort vornehmen und `scripts/sync_design_to_vault.py` ausführen.", ""]
    if d.get("extra"):
        out += [d["extra"], ""]
    out += ["```mermaid", body, "```", ""]
    return "\n".join(out)


def main():
    check = "--check" in sys.argv
    cfg = json.load(open("design/vault-sync.json", encoding="utf-8"))
    stale = []
    for d in cfg["diagrams"]:
        path = os.path.join(cfg["vault"], d["target"])
        new = render(cfg, d)
        old = open(path, encoding="utf-8").read() if os.path.exists(path) else None
        if old == new:
            continue
        stale.append(path)
        if not check:
            os.makedirs(os.path.dirname(path), exist_ok=True)
            open(path, "w", encoding="utf-8").write(new)
    verb = "veraltet" if check else "aktualisiert"
    print(f"{len(cfg['diagrams'])} Diagramme, {len(stale)} {verb}" + "".join(f"\n  {p}" for p in stale))
    sys.exit(1 if check and stale else 0)


if __name__ == "__main__":
    main()
