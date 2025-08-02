# Marker Tools - Lean-Deep 3.2

## Übersicht

Dieses Verzeichnis enthält Werkzeuge zur Verarbeitung und Qualifizierung von semantischen Markern nach dem Lean-Deep 3.2 Standard.

## Verfügbare Tools

### 1. Marker Repair Engine (`marker_repair_engine.py`)

**Hauptwerkzeug für die vollständige Marker-Reparatur und -Qualifizierung**

Dreiphasiger Automatisierungsprozess:
- **Phase 1**: Extraktion reparaturfähiger Marker
- **Phase 2**: Reparatur und Normalisierung zu LD3.2
- **Phase 3**: Finale Qualifizierung und Organisation

```bash
# Vollständige Verarbeitung des Marker-Bestands
python3 tools/marker_repair_engine.py
```

**Funktionen:**
- ✅ LD32_ Präfix-Normalisierung
- ✅ Vollständige Frame-Validierung (signal/concept/pragmatics/narrative)
- ✅ Mindestens 5 Beispiele pro Marker
- ✅ Quarantäne-System mit detaillierter Fehlerprotokollierung
- ✅ Kontinuierliche Verarbeitung mit Fortschrittsspeicherung
- ✅ 68.8% Erfolgsrate auf aktuellem Marker-Bestand

### 2. Legacy Marker Qualifier (`qualify_marker_set.py`)

**Einfacher Validator für Lean-Deep 3.1**

```bash
python3 tools/qualify_marker_set.py
```

Prüft Marker gegen LD3.1-Kriterien und kopiert qualifizierte Marker nach `final_marker_set/`.

### 3. Marker Completer (`complete_markers.py`)

**Normalisierungs-Tool für LD3.11-Struktur**

```bash
python3 tools/complete_markers.py
```

Grundlegende Normalisierung ohne vollständige LD3.2-Compliance.

### 4. Test Suite (`test_repair_engine.py`)

**Test-Framework für Marker Repair Engine**

```bash
python3 tools/test_repair_engine.py
```

Testet die Engine auf einem kleinen Marker-Satz vor der vollständigen Verarbeitung.

## Empfohlener Workflow

### Für vollständige Marker-Qualifizierung (LD3.2):

```bash
# 1. Vollständige Reparatur und Qualifizierung
python3 tools/marker_repair_engine.py

# 2. Überprüfung der Ergebnisse
ls -la final_marker_set/     # Qualifizierte Marker
ls -la quarantine/           # Problematische Marker mit Logs

# 3. Review der quarantinierten Marker
find quarantine/ -name "*.log" -exec cat {} \;
```

### Für schnelle Tests:

```bash
# Test auf kleinem Marker-Satz
python3 tools/test_repair_engine.py
```

## Verzeichnisstruktur nach Verarbeitung

```
├── marker/                    # Sollte nur noch .zip und .md Dateien enthalten
├── final_marker_set/         # 240+ qualifizierte LD3.2-Marker
├── quarantine/               # 109 problematische Marker
│   ├── yaml_errors/         # YAML-Parsing-Fehler
│   ├── repair_failed/       # Reparatur-Fehler  
│   └── validation_failed/   # Validierungs-Fehler
└── tools/
    ├── marker_repair_engine.py  # Haupt-Engine
    ├── test_repair_engine.py    # Test-Tool
    ├── qualify_marker_set.py    # Legacy LD3.1-Validator
    └── complete_markers.py      # Legacy Normalizer
```

## Qualitätskriterien (Lean-Deep 3.2)

Alle Tools arbeiten nach folgenden Standards:

### Pflichtfelder
- **ID**: Eindeutig mit `LD32_` Präfix
- **Frame**: Vollständiges Objekt mit signal/concept/pragmatics/narrative
- **Examples**: Mindestens 5 relevante Beispiele
- **Metadaten**: lean_deep_version: '3.2', author, created, last_repaired

### Strukturelle Anforderungen
- Gültige YAML-Syntax
- Konsistente Feld-Benennung
- Keine Legacy-Felder (marker_name, level, version, etc.)

## Erfolgsmetriken (aktueller Bestand)

Nach der vollständigen Verarbeitung mit der Repair Engine:

- **📊 Erfolgsrate**: 68.8% (240 von 349 Dateien)
- **✅ Qualifizierte Marker**: 240 in final_marker_set/
- **⚠️ Quarantinierte Marker**: 109 (hauptsächlich YAML-Fehler)
- **🔄 Verarbeitungszeit**: ~1.3 Sekunden für kompletten Bestand
- **💾 Verbleibende Dateien**: 2 Non-YAML-Dateien in marker/

## Troubleshooting

### Häufige Probleme

**YAML-Parsing-Fehler**: 
- Konsultiere Logs in `quarantine/yaml_errors/`
- Häufig durch fehlende Anführungszeichen oder falsche Einrückung

**Berechtigungsfehler**:
- Stelle sicher, dass alle Verzeichnisse beschreibbar sind
- Engine benötigt Berechtigung zum Verschieben von Dateien

**Speicherplatz**:
- Benötigt temporären Speicher für Quarantäne-Operationen
- Mindestens 2x Größe des marker/ Verzeichnisses

### Support

Für erweiterte Konfiguration oder Anpassungen siehe:
- Source Code der jeweiligen Tools
- Detaillierte Logs in `marker_repair.log`
- Quarantäne-Logs für spezifische Fehleranalyse