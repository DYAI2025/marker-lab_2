# 🧠 Marker Lab

Dieses Repository enthält, kuratiert und evaluiert semantische Marker für GPT-Systeme.  
Ziel ist es, Marker nach dem Lean Deep 3.1-Modell zu entwickeln, mit vollständigen Bedeutungsrahmen und mindestens fünf Beispielen.

## Ordnerstruktur

- `marker/` → Rohdaten, unfertige oder unvollständige Marker
- `final_marker_set/` → Qualifizierte Marker (LD3.1-konform + ≥5 Beispiele)
- `marker_templates/` → Leere Schemata für neue Marker
- `tools/` → Automatisierte Prüfung (z. B. qualify_marker_set.py)

## Mitarbeit

Verwende die Issue-Templates, um neue Marker zu befüllen oder fertige Marker zu qualifizieren.  
Die automatisierte Qualifizierung übernimmt die kontinuierliche Verarbeitung.

## Automatisierte Arbeitsanweisung

Das Repository implementiert kontinuierliche Marker-Qualifizierung:

1. **Neue Marker hinzufügen**: Erstelle YAML-Dateien im `marker/` Verzeichnis
2. **Automatische Prüfung**: Führe `python3 tools/qualify_marker_set.py` aus
3. **Qualifizierte Marker**: Werden automatisch nach `final_marker_set/` kopiert

### Continuous Processing
```bash
# Marker-Qualifizierung durchführen
python3 tools/qualify_marker_set.py

# Oder als ausführbare Datei
./tools/qualify_marker_set.py
```

Das Tool prüft alle Marker automatisch und qualifiziert sie gemäß Lean Deep 3.1-Kriterien.

## Kriterien für "finale" Marker

- Enthält ein vollständiges `frame`-Objekt mit den Feldern: `signal`, `concept`, `pragmatics`, `narrative`
- Hat mindestens fünf `examples`
