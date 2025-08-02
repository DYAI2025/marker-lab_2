#!/usr/bin/env python3
"""
Marker Qualification Tool - Lean Deep 3.1 Model

Scans markers in marker/ directory, validates them against Lean Deep 3.1 criteria,
and copies qualified markers to final_marker_set/ directory.

Qualification criteria:
- Complete frame object with: signal, concept, pragmatics, narrative
- At least 5 examples
- Valid YAML structure
"""

import os
import yaml
import shutil
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class MarkerQualifier:
    """Validates and qualifies markers according to Lean Deep 3.1 model"""
    
    def __init__(self, marker_dir: str = "marker", final_dir: str = "final_marker_set"):
        """Initialize the qualifier with source and destination directories"""
        self.marker_dir = Path(marker_dir)
        self.final_dir = Path(final_dir)
        
        # Ensure directories exist
        self.marker_dir.mkdir(exist_ok=True)
        self.final_dir.mkdir(exist_ok=True)
    
    def validate_marker(self, marker_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate a marker against Lean Deep 3.1 criteria
        
        Returns:
            Dict with 'valid' boolean and 'errors' list
        """
        errors = []
        
        # Check required top-level fields
        required_fields = ['id', 'frame', 'examples']
        for field in required_fields:
            if field not in marker_data:
                errors.append(f"Missing required field: {field}")
        
        # Validate frame object
        if 'frame' in marker_data:
            frame = marker_data['frame']
            if not isinstance(frame, dict):
                errors.append("Frame must be an object/dictionary")
            else:
                required_frame_fields = ['signal', 'concept', 'pragmatics', 'narrative']
                for field in required_frame_fields:
                    if field not in frame:
                        errors.append(f"Missing required frame field: {field}")
                    elif not frame[field] or not isinstance(frame[field], str):
                        errors.append(f"Frame field '{field}' must be a non-empty string")
        
        # Validate examples
        if 'examples' in marker_data:
            examples = marker_data['examples']
            if not isinstance(examples, list):
                errors.append("Examples must be a list")
            elif len(examples) < 5:
                errors.append(f"Marker must have at least 5 examples, found {len(examples)}")
        
        # Validate ID
        if 'id' in marker_data:
            if not marker_data['id'] or not isinstance(marker_data['id'], str):
                errors.append("ID must be a non-empty string")
        
        return {
            'valid': len(errors) == 0,
            'errors': errors
        }
    
    def load_marker_file(self, file_path: Path) -> Optional[Dict[str, Any]]:
        """Load and parse a YAML marker file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except yaml.YAMLError as e:
            logger.error(f"YAML parsing error in {file_path}: {e}")
            return None
        except Exception as e:
            logger.error(f"Error loading {file_path}: {e}")
            return None
    
    def process_marker_file(self, file_path: Path) -> bool:
        """Process a single marker file and qualify it if valid"""
        logger.info(f"Processing marker file: {file_path}")
        
        # Load marker data
        marker_data = self.load_marker_file(file_path)
        if marker_data is None:
            logger.error(f"Failed to load marker file: {file_path}")
            return False
        
        # Validate marker
        validation_result = self.validate_marker(marker_data)
        
        if validation_result['valid']:
            # Copy to final_marker_set
            dest_path = self.final_dir / file_path.name
            try:
                shutil.copy2(file_path, dest_path)
                logger.info(f"✓ Qualified marker copied to: {dest_path}")
                return True
            except Exception as e:
                logger.error(f"Failed to copy marker to final set: {e}")
                return False
        else:
            logger.warning(f"✗ Marker {file_path} failed qualification:")
            for error in validation_result['errors']:
                logger.warning(f"  - {error}")
            return False
    
    def qualify_all_markers(self) -> Dict[str, int]:
        """Process all marker files in the marker directory"""
        logger.info(f"Starting marker qualification process...")
        logger.info(f"Source directory: {self.marker_dir}")
        logger.info(f"Destination directory: {self.final_dir}")
        
        stats = {'processed': 0, 'qualified': 0, 'failed': 0}
        
        # Find all YAML files in marker directory
        yaml_files = list(self.marker_dir.glob("*.yaml")) + list(self.marker_dir.glob("*.yml"))
        
        if not yaml_files:
            logger.info("No YAML marker files found in marker directory")
            return stats
        
        logger.info(f"Found {len(yaml_files)} marker files to process")
        
        for file_path in yaml_files:
            stats['processed'] += 1
            if self.process_marker_file(file_path):
                stats['qualified'] += 1
            else:
                stats['failed'] += 1
        
        logger.info(f"Qualification complete. Stats: {stats}")
        return stats


def main():
    """Main function to run the marker qualification process"""
    # Change to repository root directory
    script_dir = Path(__file__).parent
    repo_root = script_dir.parent
    os.chdir(repo_root)
    
    logger.info("Starting Marker Qualification Tool - Lean Deep 3.1")
    
    qualifier = MarkerQualifier()
    stats = qualifier.qualify_all_markers()
    
    # Print summary
    print("\n" + "="*50)
    print("MARKER QUALIFICATION SUMMARY")
    print("="*50)
    print(f"Total processed: {stats['processed']}")
    print(f"Successfully qualified: {stats['qualified']}")
    print(f"Failed qualification: {stats['failed']}")
    
    if stats['qualified'] > 0:
        print(f"\n✓ {stats['qualified']} markers qualified and copied to final_marker_set/")
    
    if stats['failed'] > 0:
        print(f"\n✗ {stats['failed']} markers failed qualification (see logs above)")


if __name__ == "__main__":
    main()
