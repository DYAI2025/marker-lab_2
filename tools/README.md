# Tools Directory

This directory contains automation tools for the Marker Lab.

## qualify_marker_set.py

The main qualification tool that implements continuous processing of semantic markers according to the Lean Deep 3.1 model.

### Usage

```bash
# Run marker qualification process
python3 tools/qualify_marker_set.py

# Or make it executable and run directly
chmod +x tools/qualify_marker_set.py
./tools/qualify_marker_set.py
```

### What it does

1. **Scans** all YAML files in the `marker/` directory
2. **Validates** each marker against Lean Deep 3.1 criteria:
   - Complete `frame` object with: `signal`, `concept`, `pragmatics`, `narrative`
   - At least 5 `examples`
   - Valid YAML structure
   - Non-empty required fields
3. **Copies** qualified markers to `final_marker_set/` directory
4. **Reports** detailed validation results

### Output

- Qualified markers are automatically copied to `final_marker_set/`
- Detailed logging shows which markers passed/failed and why
- Summary statistics at the end

This tool enables **continuous processing** - run it whenever new markers are added to automatically qualify and promote them to the final set.