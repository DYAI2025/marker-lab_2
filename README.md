# 🧠 Marker Lab

Dieses Repository enthält, kuratiert und evaluiert semantische Marker für GPT-Systeme.  
Ziel ist es, Marker nach dem Lean Deep 3.2-Modell zu entwickeln, mit vollständigen Bedeutungsrahmen und mindestens fünf Beispielen.

## 🚀 Self-Healing Merkle Pipeline

Das Repository implementiert eine hochentwickelte **Self-Healing Merkle Pipeline** für die automatisierte Marker-Verarbeitung mit Quantencomputer-inspirierten Algorithmen und formaler Verifikation.

### Architektur-Komponenten

1. **Scanner** - Rekursive Datei-Erkennung mit SHA-256 content-addressable Caching
2. **Multi-Parser** - Quorum-basierte YAML-Validierung mit mehreren Parser-Implementierungen
3. **Validation Gates** - TLA+ inspirierte Template-Systeme für Invarianten-Prüfung
4. **Repair Engine** - Regelbasierte Marker-Reparatur mit GPT-Unterstützung
5. **Verifier Ring** - Doppel-Roundtrip-Verifikation mit atomaren Operationen

### Sicherheits- und Zuverlässigkeitsgarantien

- **Determinismus**: Jeder Verarbeitungsschritt basiert auf Datei-Hash und expliziten Parametern
- **Fortsetzungsfähigkeit**: Crash-resistente SQLite-Datenbank mit WAL-Modus
- **Manipulationserkennung**: SHA-256 Validierung vor und nach Reparatur
- **Rollback-Fähigkeit**: Reversible Transformationen mit Delta-Patches
- **Qualitätsversprechen**: Shannon-Redundanz für Fehlerkorrektur

## 🎯 Verwendung

### Haupt-Pipeline ausführen

```bash
# Vollständige Pipeline ausführen
python integrity_pipeline.py run

# Aktuelle Statistiken anzeigen
python integrity_pipeline.py stats

# Heutigen Bericht anzeigen
python integrity_pipeline.py --report today
```

### Legacy-Tools

```bash
# Marker-Qualifizierung (Lean Deep 3.1)
python tools/qualify_marker_set.py

# Erweiterte Reparatur-Engine (Lean Deep 3.2)  
python tools/marker_repair_engine.py

# Marker-Normalisierung (Lean Deep 3.11)
python tools/complete_markers.py
```

## 📁 Ordnerstruktur

- `marker/` → Rohdaten, unfertige oder unvollständige Marker
- `final_marker_set/` → Qualifizierte Marker (LD3.2-konform + ≥5 Beispiele)
- `marker_templates/` → Leere Schemata für neue Marker
- `quarantine/` → Isolierte Problemfälle mit detaillierten Fehlerlogs
- `tools/` → Automatisierte Prüfung und Legacy-Systeme
- `logs/` → Pipeline-Berichte und Laufzeit-Logs
- `templates/` → TLA+ Schemas und formale Spezifikationen

## 🧪 Quantum-Inspired Booster-Module

Die Pipeline enthält erweiterte Algorithmen für maximale Qualität:

### Grover-Duplicate-Pruner
Semantische Duplikat-Erkennung mit MinHash und Locality-Sensitive Hashing

### Entropy-Budget-Guard  
Misst Kolmogorov-Komplexität und stellt sicher, dass Marker ausreichend Informationsdichte haben

### Schrödingers Preview
Git-Branch-basiertes Preview-System für gestaffelte Marker-Verifikation

### Landauer-Limiter
Energie-Effizienz-Feedback-Loop basierend auf Landauers Prinzip

## 🔬 Kriterien für "finale" Marker (Lean-Deep 3.2)

- **ID**: Beginnt mit `LD32_` Präfix (oder Legacy-Präfixe S_, A_, C_, M_, MM_)
- **Frame**: Vollständiges Objekt mit den Feldern: `signal`, `concept`, `pragmatics`, `narrative`
- **Examples**: Mindestens 5 qualitativ hochwertige Beispiele
- **Version**: `lean_deep_version: "3.2"`
- **Metadaten**: `author`, `created`, `last_repaired`

## 🏗️ Technische Details

### Abhängigkeiten

```bash
pip install -r requirements.txt
```

**Kernmodule:**
- PyYAML ≥6.0.1 (YAML-Parsing)
- ruamel.yaml ≥0.18.5 (Alternative YAML-Engine)
- hypothesis ≥6.82.0 (Property-based Testing)
- rich ≥13.5.2 (Terminal-UI)
- tqdm ≥4.66.1 (Fortschrittsanzeige)
- sqlite-utils ≥3.34 (Datenbank-Utilities)

### Progress-Tracking

Die Pipeline verwendet eine SQLite-Datenbank mit WAL-Modus für crash-resistente Fortschrittsverfolgung:

```sql
-- Progress-Tabelle
CREATE TABLE progress (
    file_hash TEXT PRIMARY KEY,
    file_path TEXT NOT NULL,
    state TEXT NOT NULL,  -- FOUND, SCANNED, PARSED, VALIDATED, REPAIRED, VERIFIED, QUARANTINED
    timestamp REAL NOT NULL,
    error_log TEXT,
    size INTEGER,
    last_modified REAL
);
```

### Content-Addressable Caching

Alle Dateien werden über SHA-256-Hashes identifiziert und in einer Merkle-Tree-Topologie organisiert:

```
.cache/
├── ab/
│   └── 34ef56...  # Cached content
├── cd/
│   └── 78901a...
└── ...
```

## 📊 Monitoring und Berichterstattung

### Automatische Berichte

- **Tägliche Berichte**: `logs/YYYY-MM-DD_report.md`
- **Quarantine-Logs**: `quarantine/*/filename.log` (JSON-Format)
- **Pipeline-Statistiken**: Über `python integrity_pipeline.py stats`

### Qualitäts-Metriken

- **Success Rate**: Anteil erfolgreich verarbeiteter Marker
- **Entropy Budget**: Informationsdichte-Messungen
- **Processing Efficiency**: Landauer-Limiter Energie-Analyse
- **Duplicate Detection**: Semantische Ähnlichkeits-Scores

## 🤝 Mitarbeit

1. **Neue Marker hinzufügen**: Erstelle YAML-Dateien im `marker/` Verzeichnis
2. **Pipeline ausführen**: `python integrity_pipeline.py run`
3. **Qualität prüfen**: Überprüfe `final_marker_set/` für qualifizierte Marker
4. **Probleme beheben**: Analysiere `quarantine/` für fehlgeschlagene Marker

Die Pipeline ist selbstheilend und idempotent - mehrfache Ausführung ist sicher und empfohlen.

## 🔬 Formale Verifikation

Das System nutzt TLA+ für formale Spezifikationen:

- **Invarianten**: Lean-Deep 3.2 Struktur-Garantien
- **Liveness**: Fortschritts-Eigenschaften  
- **Safety**: Daten-Integritäts-Checks
- **Idempotenz**: Wiederholbare Verarbeitungs-Garantien

Siehe `templates/LD32_schema.tla` für die vollständige Spezifikation.

---

*Das Self-Healing Merkle Pipeline System transformiert Ihren Marker-Zoo in ein konsistentes, informationstheoretisch sauberes Repository mit maximaler Zuverlässigkeit bei minimalem manuellen Aufwand.*