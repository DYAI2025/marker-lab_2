#!/usr/bin/env python3
"""
Marker Repair Engine - Lean-Deep 3.2 Standard
==============================================

Comprehensive three-phase marker processing system that validates, repairs,
and qualifies markers according to Lean-Deep 3.2 standards.

Phase 1: Extraction of repairable markers
Phase 2: Iterative repair and normalization  
Phase 3: Final qualification and organization

Usage:
    python tools/marker_repair_engine.py

Features:
- Continuous processing with resumability
- Progress tracking and detailed reporting
- Quarantine system for problematic markers
- LD32_ prefix normalization
- Complete frame validation and repair
- Example count enforcement (minimum 5)
"""

import os
import json
import yaml
import shutil
import logging
import traceback
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
import re

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('marker_repair.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class MarkerRepairEngine:
    """
    Comprehensive marker repair and validation engine for Lean-Deep 3.2
    """
    
    def __init__(self, 
                 marker_dir: str = "marker",
                 final_dir: str = "final_marker_set", 
                 quarantine_dir: str = "quarantine"):
        """Initialize the repair engine with directory paths"""
        self.marker_dir = Path(marker_dir)
        self.final_dir = Path(final_dir)
        self.quarantine_dir = Path(quarantine_dir)
        self.progress_file = Path("marker_repair_progress.json")
        
        # Required frame fields for Lean-Deep 3.2
        self.required_frame_fields = ['signal', 'concept', 'pragmatics', 'narrative']
        self.min_examples = 5
        
        # Statistics tracking
        self.stats = {
            'phase1_processed': 0,
            'phase1_extracted': 0,
            'phase1_quarantined': 0,
            'phase2_processed': 0,
            'phase2_repaired': 0,
            'phase2_failed': 0,
            'phase3_processed': 0,
            'phase3_qualified': 0,
            'phase3_quarantined': 0,
            'total_start_time': None,
            'last_processed_file': None
        }
        
        # Ensure directories exist
        self._setup_directories()
        
        # Load existing progress
        self._load_progress()
    
    def _setup_directories(self):
        """Create necessary directories"""
        for directory in [self.marker_dir, self.final_dir, self.quarantine_dir]:
            directory.mkdir(exist_ok=True)
        
        # Create quarantine subdirectories
        (self.quarantine_dir / "yaml_errors").mkdir(exist_ok=True)
        (self.quarantine_dir / "repair_failed").mkdir(exist_ok=True)
        (self.quarantine_dir / "validation_failed").mkdir(exist_ok=True)
    
    def _load_progress(self):
        """Load previous progress if exists"""
        if self.progress_file.exists():
            try:
                with open(self.progress_file, 'r') as f:
                    saved_stats = json.load(f)
                    self.stats.update(saved_stats)
                logger.info(f"Loaded previous progress: {self.stats['last_processed_file']}")
            except Exception as e:
                logger.warning(f"Could not load progress file: {e}")
    
    def _save_progress(self):
        """Save current progress"""
        try:
            with open(self.progress_file, 'w') as f:
                json.dump(self.stats, f, indent=2, default=str)
        except Exception as e:
            logger.error(f"Failed to save progress: {e}")
    
    def _log_quarantine_reason(self, file_path: Path, reason: str, error_details: str = ""):
        """Log detailed reason for quarantine"""
        log_file = self.quarantine_dir / f"{file_path.stem}.log"
        
        log_entry = {
            'original_file': str(file_path),
            'quarantine_reason': reason,
            'timestamp': datetime.now().isoformat(),
            'error_details': error_details,
            'phase': self._get_current_phase()
        }
        
        try:
            with open(log_file, 'w', encoding='utf-8') as f:
                json.dump(log_entry, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Failed to write quarantine log: {e}")
    
    def _get_current_phase(self) -> str:
        """Determine current processing phase"""
        if hasattr(self, '_current_phase'):
            return self._current_phase
        return "unknown"
    
    def _normalize_id(self, marker_id: str, filename: str) -> str:
        """Normalize marker ID to Lean-Deep 3.2 standard with LD32_ prefix"""
        if not marker_id:
            marker_id = filename
        
        # Remove old prefixes and file extensions
        marker_id = re.sub(r'^(S_|A_|C_|M_|MM_)', '', marker_id)
        marker_id = re.sub(r'\.(yaml|yml)$', '', marker_id, flags=re.IGNORECASE)
        
        # Add LD32_ prefix if not present
        if not marker_id.startswith('LD32_'):
            marker_id = f'LD32_{marker_id}'
        
        return marker_id
    
    def _ensure_complete_frame(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Ensure marker has complete frame object with all required fields"""
        if 'frame' not in data or not isinstance(data['frame'], dict):
            data['frame'] = {}
        
        frame = data['frame']
        for field in self.required_frame_fields:
            if field not in frame or not frame[field]:
                frame[field] = ""  # Empty string placeholder as specified
        
        return data
    
    def _ensure_minimum_examples(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Ensure marker has at least 5 examples"""
        examples = []
        
        # Collect examples from various possible fields
        for field in ['examples', 'beispiele', 'example']:
            if field in data and isinstance(data[field], list):
                # Filter out empty strings and None values, and skip auto-generated ones
                for ex in data[field]:
                    if ex and str(ex).strip() and not str(ex).startswith('AUTO_GENERATED_EXAMPLE'):
                        examples.append(str(ex))
                if field != 'examples':
                    del data[field]  # Remove alternative field names
        
        # Remove duplicates while preserving order
        seen = set()
        unique_examples = []
        for ex in examples:
            if ex not in seen:
                seen.add(ex)
                unique_examples.append(ex)
        
        # Only pad with generic examples if we don't have enough real examples
        marker_id = data.get('id', 'MARKER')
        while len(unique_examples) < self.min_examples:
            unique_examples.append(f"TODO: Relevantes Beispiel für {marker_id} hinzufügen")
        
        data['examples'] = unique_examples
        return data
    
    def _clean_legacy_fields(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Remove legacy and redundant fields"""
        legacy_fields = {
            'marker_name', 'marker', 'level', 'version', 'status', 'lang',
            'name', 'beschreibung', 'atomic_pattern', 'pattern', 'regex_flags',
            'created_at', 'kategorie', 'category', 'metadata'
        }
        
        for field in legacy_fields:
            if field in data:
                del data[field]
        
        return data
    
    # PHASE 1: Extract repairable markers
    def phase1_extract_markers(self) -> List[Path]:
        """
        Phase 1: Identify and extract all parseable YAML markers
        Move unparseable files to quarantine
        """
        self._current_phase = "phase1"
        logger.info("=== PHASE 1: Extracting repairable markers ===")
        
        extractable_markers = []
        yaml_files = list(self.marker_dir.glob("*.yaml")) + list(self.marker_dir.glob("*.yml"))
        
        logger.info(f"Found {len(yaml_files)} YAML files to process")
        
        for file_path in yaml_files:
            self.stats['phase1_processed'] += 1
            self.stats['last_processed_file'] = str(file_path)
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    yaml.safe_load(f)  # Test if parseable
                
                extractable_markers.append(file_path)
                self.stats['phase1_extracted'] += 1
                logger.debug(f"✓ Extracted: {file_path.name}")
                
            except yaml.YAMLError as e:
                # Move to quarantine with detailed error log
                quarantine_path = self.quarantine_dir / "yaml_errors" / file_path.name
                shutil.move(file_path, quarantine_path)
                self._log_quarantine_reason(
                    file_path,
                    "YAML parsing error",
                    f"YAMLError: {str(e)}"
                )
                self.stats['phase1_quarantined'] += 1
                logger.warning(f"✗ Quarantined (YAML error): {file_path.name}")
                
            except Exception as e:
                # Move to quarantine with error details
                quarantine_path = self.quarantine_dir / "yaml_errors" / file_path.name
                shutil.move(file_path, quarantine_path)
                self._log_quarantine_reason(
                    file_path,
                    "File processing error",
                    f"Error: {str(e)}\nTraceback: {traceback.format_exc()}"
                )
                self.stats['phase1_quarantined'] += 1
                logger.error(f"✗ Quarantined (processing error): {file_path.name}")
            
            # Save progress periodically
            if self.stats['phase1_processed'] % 50 == 0:
                self._save_progress()
                logger.info(f"Phase 1 progress: {self.stats['phase1_processed']}/{len(yaml_files)}")
        
        logger.info(f"Phase 1 complete: {len(extractable_markers)} markers extracted, "
                   f"{self.stats['phase1_quarantined']} quarantined")
        
        return extractable_markers
    
    # PHASE 2: Repair and normalize markers
    def phase2_repair_markers(self, marker_files: List[Path]) -> List[Path]:
        """
        Phase 2: Repair and normalize markers to Lean-Deep 3.2 standard
        """
        self._current_phase = "phase2"
        logger.info("=== PHASE 2: Repairing and normalizing markers ===")
        
        repaired_markers = []
        
        for file_path in marker_files:
            self.stats['phase2_processed'] += 1
            self.stats['last_processed_file'] = str(file_path)
            
            try:
                # Load marker data
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = yaml.safe_load(f) or {}
                
                if not isinstance(data, dict):
                    raise ValueError("Marker data is not a dictionary")
                
                # Apply Lean-Deep 3.2 normalization
                original_id = data.get('id', file_path.stem)
                data['id'] = self._normalize_id(original_id, file_path.stem)
                data = self._ensure_complete_frame(data)
                data = self._ensure_minimum_examples(data)
                data = self._clean_legacy_fields(data)
                
                # Add metadata
                data['author'] = data.get('author', 'MarkerRepairEngine')
                data['created'] = data.get('created', datetime.now().date().isoformat())
                data['lean_deep_version'] = '3.2'
                data['last_repaired'] = datetime.now().isoformat()
                
                # Write repaired marker back
                with open(file_path, 'w', encoding='utf-8') as f:
                    yaml.safe_dump(data, f, allow_unicode=True, sort_keys=False, default_flow_style=False)
                
                repaired_markers.append(file_path)
                self.stats['phase2_repaired'] += 1
                logger.debug(f"✓ Repaired: {file_path.name} -> ID: {data['id']}")
                
            except Exception as e:
                # Move to repair failed quarantine
                quarantine_path = self.quarantine_dir / "repair_failed" / file_path.name
                shutil.move(file_path, quarantine_path)
                self._log_quarantine_reason(
                    file_path,
                    "Repair failed",
                    f"Error: {str(e)}\nTraceback: {traceback.format_exc()}"
                )
                self.stats['phase2_failed'] += 1
                logger.error(f"✗ Repair failed: {file_path.name}")
            
            # Save progress periodically
            if self.stats['phase2_processed'] % 25 == 0:
                self._save_progress()
                logger.info(f"Phase 2 progress: {self.stats['phase2_processed']}/{len(marker_files)}")
        
        logger.info(f"Phase 2 complete: {len(repaired_markers)} markers repaired, "
                   f"{self.stats['phase2_failed']} failed")
        
        return repaired_markers
    
    # PHASE 3: Final qualification
    def phase3_qualify_markers(self, marker_files: List[Path]) -> None:
        """
        Phase 3: Final validation and organization of markers
        """
        self._current_phase = "phase3"
        logger.info("=== PHASE 3: Final qualification and organization ===")
        
        for file_path in marker_files:
            self.stats['phase3_processed'] += 1
            self.stats['last_processed_file'] = str(file_path)
            
            try:
                # Load and validate repaired marker
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = yaml.safe_load(f)
                
                validation_result = self._validate_ld32_marker(data)
                
                if validation_result['valid']:
                    # Move to final_marker_set
                    final_path = self.final_dir / file_path.name
                    shutil.move(file_path, final_path)
                    self.stats['phase3_qualified'] += 1
                    logger.info(f"✓ Qualified: {file_path.name}")
                else:
                    # Move to validation failed quarantine
                    quarantine_path = self.quarantine_dir / "validation_failed" / file_path.name
                    shutil.move(file_path, quarantine_path)
                    self._log_quarantine_reason(
                        file_path,
                        "Validation failed",
                        f"Validation errors: {validation_result['errors']}"
                    )
                    self.stats['phase3_quarantined'] += 1
                    logger.warning(f"✗ Validation failed: {file_path.name}")
                
            except Exception as e:
                # Move to quarantine with error details
                quarantine_path = self.quarantine_dir / "validation_failed" / file_path.name
                try:
                    shutil.move(file_path, quarantine_path)
                except:
                    pass  # File might already be moved
                self._log_quarantine_reason(
                    file_path,
                    "Phase 3 processing error",
                    f"Error: {str(e)}\nTraceback: {traceback.format_exc()}"
                )
                self.stats['phase3_quarantined'] += 1
                logger.error(f"✗ Phase 3 error: {file_path.name}")
            
            # Save progress periodically
            if self.stats['phase3_processed'] % 25 == 0:
                self._save_progress()
                logger.info(f"Phase 3 progress: {self.stats['phase3_processed']}/{len(marker_files)}")
        
        logger.info(f"Phase 3 complete: {self.stats['phase3_qualified']} markers qualified, "
                   f"{self.stats['phase3_quarantined']} quarantined")
    
    def _validate_ld32_marker(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate marker against Lean-Deep 3.2 criteria"""
        errors = []
        
        # Check required top-level fields
        if 'id' not in data or not data['id']:
            errors.append("Missing or empty 'id' field")
        elif not data['id'].startswith('LD32_'):
            errors.append(f"ID must start with 'LD32_' prefix, found: {data['id']}")
        
        # Validate frame object
        if 'frame' not in data:
            errors.append("Missing 'frame' object")
        elif not isinstance(data['frame'], dict):
            errors.append("Frame must be a dictionary")
        else:
            frame = data['frame']
            for field in self.required_frame_fields:
                if field not in frame:
                    errors.append(f"Missing frame field: {field}")
                elif not isinstance(frame[field], str):
                    errors.append(f"Frame field '{field}' must be a string")
        
        # Validate examples
        if 'examples' not in data:
            errors.append("Missing 'examples' field")
        elif not isinstance(data['examples'], list):
            errors.append("Examples must be a list")
        elif len(data['examples']) < self.min_examples:
            errors.append(f"Must have at least {self.min_examples} examples, found {len(data['examples'])}")
        
        # Check lean_deep_version
        if data.get('lean_deep_version') != '3.2':
            errors.append("Must specify lean_deep_version: '3.2'")
        
        return {
            'valid': len(errors) == 0,
            'errors': errors
        }
    
    def run_complete_process(self) -> Dict[str, Any]:
        """Run the complete three-phase marker repair process"""
        logger.info("🚀 Starting Marker Repair Engine - Lean-Deep 3.2")
        logger.info("=" * 60)
        
        self.stats['total_start_time'] = datetime.now().isoformat()
        
        try:
            # Phase 1: Extract repairable markers
            extractable_markers = self.phase1_extract_markers()
            self._save_progress()
            
            if not extractable_markers:
                logger.warning("No extractable markers found. Process complete.")
                return self.stats
            
            # Phase 2: Repair and normalize
            repaired_markers = self.phase2_repair_markers(extractable_markers)
            self._save_progress()
            
            if not repaired_markers:
                logger.warning("No markers successfully repaired. Process complete.")
                return self.stats
            
            # Phase 3: Final qualification
            self.phase3_qualify_markers(repaired_markers)
            self._save_progress()
            
            # Generate final report
            self._generate_final_report()
            
        except KeyboardInterrupt:
            logger.info("Process interrupted by user. Progress saved.")
            self._save_progress()
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            logger.error(traceback.format_exc())
            self._save_progress()
        
        return self.stats
    
    def _generate_final_report(self):
        """Generate comprehensive final report"""
        logger.info("\n" + "=" * 60)
        logger.info("MARKER REPAIR ENGINE - FINAL REPORT")
        logger.info("=" * 60)
        logger.info(f"Processing started: {self.stats['total_start_time']}")
        logger.info(f"Processing completed: {datetime.now().isoformat()}")
        logger.info("")
        logger.info("PHASE 1 - EXTRACTION:")
        logger.info(f"  Files processed: {self.stats['phase1_processed']}")
        logger.info(f"  Markers extracted: {self.stats['phase1_extracted']}")
        logger.info(f"  Files quarantined: {self.stats['phase1_quarantined']}")
        logger.info("")
        logger.info("PHASE 2 - REPAIR:")
        logger.info(f"  Markers processed: {self.stats['phase2_processed']}")
        logger.info(f"  Successfully repaired: {self.stats['phase2_repaired']}")
        logger.info(f"  Repair failed: {self.stats['phase2_failed']}")
        logger.info("")
        logger.info("PHASE 3 - QUALIFICATION:")
        logger.info(f"  Markers processed: {self.stats['phase3_processed']}")
        logger.info(f"  Successfully qualified: {self.stats['phase3_qualified']}")
        logger.info(f"  Validation failed: {self.stats['phase3_quarantined']}")
        logger.info("")
        logger.info("FINAL RESULTS:")
        logger.info(f"  ✅ Qualified markers in final_marker_set/: {self.stats['phase3_qualified']}")
        total_quarantined = (self.stats['phase1_quarantined'] + 
                           self.stats['phase2_failed'] + 
                           self.stats['phase3_quarantined'])
        logger.info(f"  ⚠️  Total quarantined markers: {total_quarantined}")
        logger.info(f"  📊 Success rate: {(self.stats['phase3_qualified'] / max(self.stats['phase1_processed'], 1)) * 100:.1f}%")
        logger.info("")
        logger.info("Check quarantine/ directory for detailed error logs.")
        logger.info("=" * 60)


def main():
    """Main entry point"""
    # Change to repository root directory
    script_dir = Path(__file__).parent
    repo_root = script_dir.parent
    os.chdir(repo_root)
    
    logger.info(f"Working directory: {os.getcwd()}")
    
    # Initialize and run the repair engine
    engine = MarkerRepairEngine()
    final_stats = engine.run_complete_process()
    
    # Clean up progress file on successful completion
    if engine.progress_file.exists():
        engine.progress_file.unlink()
    
    return final_stats


if __name__ == "__main__":
    main()