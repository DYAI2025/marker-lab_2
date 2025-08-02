#!/usr/bin/env python3
"""
Test script for marker repair engine functionality
"""

import sys
import os
from pathlib import Path

# Add the tools directory to path so we can import the repair engine
sys.path.insert(0, str(Path(__file__).parent))

from marker_repair_engine import MarkerRepairEngine

def test_small_batch():
    """Test the repair engine on a small batch of markers"""
    print("Testing Marker Repair Engine on small batch...")
    
    # Use test directories
    engine = MarkerRepairEngine(
        marker_dir="test_marker",
        final_dir="test_final", 
        quarantine_dir="test_quarantine"
    )
    
    # Run the complete process
    stats = engine.run_complete_process()
    
    print("\nTest completed!")
    return stats

if __name__ == "__main__":
    # Change to repo root
    os.chdir(Path(__file__).parent.parent)
    test_small_batch()