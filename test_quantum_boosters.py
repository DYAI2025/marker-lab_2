#!/usr/bin/env python3
"""
Simple test script to validate the quantum booster modules
"""

import sys
from pathlib import Path

# Add the current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

from quantum_boosters import QuantumBoosterPipeline

def test_quantum_boosters():
    """Test the quantum booster pipeline with sample data"""
    
    # Sample marker data for testing
    test_markers = [
        ("LD32_TEST_MARKER_1", {
            "id": "LD32_TEST_MARKER_1",
            "frame": {
                "signal": "Testing signal pattern",
                "concept": "Core concept for testing",
                "pragmatics": "Practical application context",
                "narrative": "Story about the marker usage"
            },
            "examples": [
                "Example 1: First test case",
                "Example 2: Second test case", 
                "Example 3: Third test case",
                "Example 4: Fourth test case",
                "Example 5: Fifth test case"
            ],
            "lean_deep_version": "3.2"
        }),
        ("LD32_TEST_MARKER_2", {
            "id": "LD32_TEST_MARKER_2", 
            "frame": {
                "signal": "Different signal pattern",
                "concept": "Alternative concept for testing",
                "pragmatics": "Different practical application",
                "narrative": "Alternative story about usage"
            },
            "examples": [
                "Example A: First alternative case",
                "Example B: Second alternative case",
                "Example C: Third alternative case", 
                "Example D: Fourth alternative case",
                "Example E: Fifth alternative case"
            ],
            "lean_deep_version": "3.2"
        }),
        ("LD32_SIMILAR_MARKER", {
            "id": "LD32_SIMILAR_MARKER",
            "frame": {
                "signal": "Testing signal pattern",  # Similar to marker 1
                "concept": "Core concept for testing", # Similar to marker 1
                "pragmatics": "Slightly different context",
                "narrative": "Different story"
            },
            "examples": [
                "Similar example 1",
                "Similar example 2", 
                "Similar example 3",
                "Similar example 4",
                "Similar example 5"
            ],
            "lean_deep_version": "3.2"
        })
    ]
    
    print("🧪 Testing Quantum Booster Pipeline")
    print("=" * 50)
    
    # Initialize the quantum booster pipeline
    pipeline = QuantumBoosterPipeline()
    
    # Run comprehensive analysis
    results = pipeline.analyze_marker_quality(test_markers)
    
    # Display results
    print("\n📊 Analysis Results:")
    print("-" * 30)
    
    print(f"\n🔍 Duplicate Detection:")
    if results['duplicates']:
        for marker1, marker2, similarity in results['duplicates']:
            print(f"  - {marker1} ↔ {marker2}: {similarity:.3f} similarity")
    else:
        print("  - No duplicates found")
    
    print(f"\n🌊 Entropy Analysis:")
    for marker_id, analysis in results['entropy_analyses'].items():
        meets_budget = "✅" if analysis['meets_budget'] else "❌"
        total_complexity = analysis['total_complexity']
        print(f"  - {marker_id}: {meets_budget} {total_complexity:.1f} bits")
        
        if analysis['recommendations']:
            for rec in analysis['recommendations'][:2]:  # Show first 2 recommendations
                print(f"    💡 {rec}")
    
    print(f"\n⚡ Energy Efficiency:")
    efficiency = results['efficiency_metrics']
    print(f"  - Information per Joule: {efficiency['information_per_joule']:.2e} bits/J")
    print(f"  - Landauer Ratio: {efficiency['landauer_ratio']:.6f}%")
    
    print(f"\n🎯 Optimization Suggestions:")
    suggestions = pipeline.suggest_optimizations(results)
    for i, suggestion in enumerate(suggestions, 1):
        print(f"  {i}. {suggestion}")
    
    print(f"\n✅ Quantum Booster Pipeline test completed successfully!")
    return True

if __name__ == "__main__":
    try:
        test_quantum_boosters()
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)