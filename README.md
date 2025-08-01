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
Copilot/Codex kann die Aufgaben automatisch übernehmen, wenn die Struktur klar ist.

## Kriterien für "finale" Marker

- Enthält ein vollständiges `frame`-Objekt mit den Feldern: `signal`, `concept`, `pragmatics`, `narrative`
- Hat mindestens fünf `examples`
# marker-lab_2
