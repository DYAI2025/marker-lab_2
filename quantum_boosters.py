#!/usr/bin/env python3
"""
Quantum-Inspired Booster Modules for Marker Integrity Pipeline
==============================================================

Implements the advanced algorithms described in the problem statement:
1. Grover-Duplicate-Pruner - Semantic duplicate detection using MinHash
2. Entropy-Budget-Guard - Kolmogorov complexity measurement
3. Schrödingers-Preview - Git branch preview system
4. Landauer-Limiter - Energy efficiency feedback loop

These modules extend the base pipeline with sophisticated quality assurance.
"""

import re
import math
import hashlib
import logging
from typing import Dict, List, Any, Tuple, Set
from collections import defaultdict
from pathlib import Path

logger = logging.getLogger("quantum_boosters")


class GroverDuplicatePruner:
    """
    Quantum-inspired probabilistic algorithm for semantic duplicate detection
    using MinHash and Locality-Sensitive Hashing (LSH)
    """
    
    def __init__(self, num_hashes: int = 128, threshold: float = 0.7):
        self.num_hashes = num_hashes
        self.threshold = threshold
        
        # Generate random hash parameters
        self.hash_params = []
        for _ in range(num_hashes):
            a = hash(f"param_a_{_}") % (2**32 - 1) + 1
            b = hash(f"param_b_{_}") % (2**32 - 1)
            self.hash_params.append((a, b))
    
    def _tokenize_text(self, text: str) -> Set[str]:
        """Tokenize text into shingles for MinHash"""
        if not text:
            return set()
        
        # Convert to lowercase and extract words
        words = re.findall(r'\w+', text.lower())
        
        # Create 2-grams (shingles)
        shingles = set()
        for i in range(len(words) - 1):
            shingle = f"{words[i]}_{words[i+1]}"
            shingles.add(shingle)
        
        # Add individual words as well
        shingles.update(words)
        
        return shingles
    
    def _compute_minhash(self, shingles: Set[str]) -> List[int]:
        """Compute MinHash signature for a set of shingles"""
        if not shingles:
            return [0] * self.num_hashes
        
        signature = []
        
        for a, b in self.hash_params:
            min_hash = float('inf')
            for shingle in shingles:
                # Hash the shingle
                h = hash(shingle) % (2**32 - 1)
                # Apply universal hash function
                hash_val = (a * h + b) % (2**32 - 1)
                min_hash = min(min_hash, hash_val)
            
            signature.append(int(min_hash))
        
        return signature
    
    def _extract_semantic_content(self, marker_data: Dict[str, Any]) -> str:
        """Extract semantic content from marker for comparison"""
        content_parts = []
        
        # Extract from frame
        if 'frame' in marker_data and isinstance(marker_data['frame'], dict):
            for field in ['signal', 'concept', 'pragmatics', 'narrative']:
                if field in marker_data['frame']:
                    content_parts.append(str(marker_data['frame'][field]))
        
        # Extract from examples
        if 'examples' in marker_data and isinstance(marker_data['examples'], list):
            for example in marker_data['examples']:
                if example and not str(example).startswith(('TODO:', 'AUTO_GENERATED_EXAMPLE')):
                    content_parts.append(str(example))
        
        # Extract from ID (semantic meaning)
        if 'id' in marker_data:
            # Remove prefixes and extract semantic part
            id_semantic = re.sub(r'^(LD32_|S_|A_|C_|M_|MM_)', '', str(marker_data['id']))
            content_parts.append(id_semantic)
        
        return ' '.join(content_parts)
    
    def detect_duplicates(self, markers: List[Tuple[str, Dict[str, Any]]]) -> List[Tuple[str, str, float]]:
        """
        Detect semantic duplicates using MinHash LSH
        Returns list of (marker1_id, marker2_id, similarity_score)
        """
        logger.info(f"🔍 Grover Duplicate Pruner analyzing {len(markers)} markers")
        
        # Compute signatures for all markers
        signatures = {}
        for marker_id, marker_data in markers:
            semantic_content = self._extract_semantic_content(marker_data)
            shingles = self._tokenize_text(semantic_content)
            signature = self._compute_minhash(shingles)
            signatures[marker_id] = signature
        
        # Find duplicates using LSH
        duplicates = []
        marker_ids = list(signatures.keys())
        
        for i, id1 in enumerate(marker_ids):
            for j, id2 in enumerate(marker_ids[i+1:], i+1):
                # Compute Jaccard similarity estimate
                sig1 = signatures[id1]
                sig2 = signatures[id2]
                
                matches = sum(1 for a, b in zip(sig1, sig2) if a == b)
                similarity = matches / len(sig1)
                
                if similarity >= self.threshold:
                    duplicates.append((id1, id2, similarity))
        
        logger.info(f"📊 Found {len(duplicates)} potential duplicate pairs")
        return duplicates


class EntropyBudgetGuard:
    """
    Measures Kolmogorov complexity of frame texts and enforces information density
    """
    
    def __init__(self, min_entropy_bits: int = 32):
        self.min_entropy_bits = min_entropy_bits
    
    def _estimate_kolmogorov_complexity(self, text: str) -> float:
        """
        Estimate Kolmogorov complexity using compression ratio
        (Approximation since true Kolmogorov complexity is uncomputable)
        """
        if not text:
            return 0.0
        
        # Use simple compression estimation
        import zlib
        
        # Convert to bytes
        text_bytes = text.encode('utf-8')
        
        # Compress
        compressed = zlib.compress(text_bytes)
        
        # Complexity estimate: compressed size / original size
        # Higher ratio indicates more random/complex content
        complexity_ratio = len(compressed) / len(text_bytes)
        
        # Convert to approximate bits of information
        entropy_estimate = len(text_bytes) * complexity_ratio * 8
        
        return entropy_estimate
    
    def _calculate_shannon_entropy(self, text: str) -> float:
        """Calculate Shannon entropy of text"""
        if not text:
            return 0.0
        
        # Count character frequencies
        char_counts = defaultdict(int)
        for char in text:
            char_counts[char] += 1
        
        # Calculate entropy
        text_len = len(text)
        entropy = 0.0
        
        for count in char_counts.values():
            probability = count / text_len
            if probability > 0:
                entropy -= probability * math.log2(probability)
        
        return entropy
    
    def analyze_information_density(self, marker_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze information density of marker content"""
        analysis = {
            'frame_entropy': {},
            'examples_entropy': [],
            'total_complexity': 0.0,
            'meets_budget': False,
            'recommendations': []
        }
        
        total_bits = 0.0
        
        # Analyze frame fields
        if 'frame' in marker_data and isinstance(marker_data['frame'], dict):
            for field in ['signal', 'concept', 'pragmatics', 'narrative']:
                if field in marker_data['frame']:
                    text = str(marker_data['frame'][field])
                    
                    # Skip empty fields
                    if not text.strip():
                        analysis['frame_entropy'][field] = 0.0
                        continue
                    
                    # Calculate both entropies
                    kolmogorov_est = self._estimate_kolmogorov_complexity(text)
                    shannon_entropy = self._calculate_shannon_entropy(text)
                    
                    analysis['frame_entropy'][field] = {
                        'kolmogorov_estimate': kolmogorov_est,
                        'shannon_entropy': shannon_entropy,
                        'character_count': len(text),
                        'word_count': len(text.split())
                    }
                    
                    total_bits += kolmogorov_est
        
        # Analyze examples
        if 'examples' in marker_data and isinstance(marker_data['examples'], list):
            for i, example in enumerate(marker_data['examples']):
                if example and not str(example).startswith(('TODO:', 'AUTO_GENERATED_EXAMPLE')):
                    text = str(example)
                    kolmogorov_est = self._estimate_kolmogorov_complexity(text)
                    shannon_entropy = self._calculate_shannon_entropy(text)
                    
                    analysis['examples_entropy'].append({
                        'index': i,
                        'kolmogorov_estimate': kolmogorov_est,
                        'shannon_entropy': shannon_entropy,
                        'character_count': len(text),
                        'word_count': len(text.split())
                    })
                    
                    total_bits += kolmogorov_est
        
        analysis['total_complexity'] = total_bits
        analysis['meets_budget'] = total_bits >= self.min_entropy_bits
        
        # Generate recommendations
        if not analysis['meets_budget']:
            deficit = self.min_entropy_bits - total_bits
            analysis['recommendations'].append(
                f"Information density too low. Need {deficit:.1f} more bits of complexity."
            )
            
            # Check which fields need improvement
            for field, entropy_data in analysis['frame_entropy'].items():
                if isinstance(entropy_data, dict) and entropy_data['kolmogorov_estimate'] < 8:
                    analysis['recommendations'].append(
                        f"Frame field '{field}' needs more descriptive content"
                    )
            
            # Check examples
            valid_examples = [e for e in analysis['examples_entropy'] if e['kolmogorov_estimate'] > 16]
            if len(valid_examples) < 3:
                analysis['recommendations'].append(
                    "Need more detailed, informative examples"
                )
        
        return analysis


class SchrodingersPreview:
    """
    Git branch preview system for staged marker verification
    """
    
    def __init__(self, base_branch: str = "main"):
        self.base_branch = base_branch
    
    def create_preview_branch(self, marker_id: str, content_hash: str) -> str:
        """Create a preview branch for marker staging"""
        import subprocess
        import os
        
        branch_name = f"preview/{content_hash[:8]}"
        
        try:
            # Check if git is available and we're in a git repo
            result = subprocess.run(['git', 'status'], 
                                  capture_output=True, text=True, cwd=os.getcwd())
            
            if result.returncode != 0:
                logger.warning("Not in a git repository - preview branching disabled")
                return ""
            
            # Create and checkout preview branch
            subprocess.run(['git', 'checkout', '-b', branch_name], 
                          capture_output=True, text=True, cwd=os.getcwd())
            
            logger.info(f"🌿 Created preview branch: {branch_name}")
            return branch_name
            
        except Exception as e:
            logger.error(f"Failed to create preview branch: {e}")
            return ""
    
    def stage_marker_preview(self, marker_data: Dict[str, Any], preview_path: Path) -> bool:
        """Stage marker in preview for review"""
        try:
            import yaml
            
            # Add preview metadata
            preview_data = marker_data.copy()
            preview_data['_preview_status'] = 'staged'
            preview_data['_preview_timestamp'] = str(Path(__file__).stat().st_mtime)
            
            # Write to preview location
            with open(preview_path, 'w', encoding='utf-8') as f:
                yaml.dump(preview_data, f, allow_unicode=True, sort_keys=False)
            
            logger.info(f"📋 Staged marker preview: {preview_path}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to stage preview: {e}")
            return False


class LandauerLimiter:
    """
    Energy efficiency feedback loop based on Landauer's principle
    """
    
    def __init__(self, thermal_limit_joules: float = 1e-6):
        self.thermal_limit = thermal_limit_joules
        self.processing_history = []
        
    def measure_processing_efficiency(self, 
                                    markers_processed: int, 
                                    processing_time: float,
                                    cpu_usage: float = 0.5) -> Dict[str, float]:
        """
        Measure information processing efficiency
        Based on Landauer's principle: kT ln(2) per bit erased
        """
        
        # Constants
        k_boltzmann = 1.38e-23  # J/K
        room_temp = 298.15      # K (25°C)
        landauer_limit = k_boltzmann * room_temp * math.log(2)  # ~2.9e-21 J per bit
        
        # Estimate information processed (very rough approximation)
        # Assume each marker represents ~1KB of semantic information
        bits_processed = markers_processed * 8192  # 1KB per marker
        
        # Theoretical minimum energy (Landauer limit)
        theoretical_min_energy = bits_processed * landauer_limit
        
        # Estimated actual energy consumption
        # Very rough approximation based on CPU power consumption
        cpu_power_watts = 50 * cpu_usage  # Assume 50W CPU at given usage
        actual_energy = cpu_power_watts * processing_time
        
        # Calculate efficiency metrics
        efficiency_ratio = theoretical_min_energy / actual_energy if actual_energy > 0 else 0
        information_per_joule = bits_processed / actual_energy if actual_energy > 0 else 0
        
        metrics = {
            'markers_processed': markers_processed,
            'processing_time': processing_time,
            'bits_processed': bits_processed,
            'theoretical_min_energy': theoretical_min_energy,
            'estimated_actual_energy': actual_energy,
            'efficiency_ratio': efficiency_ratio,
            'information_per_joule': information_per_joule,
            'landauer_ratio': efficiency_ratio * 100
        }
        
        # Store in history
        self.processing_history.append(metrics)
        
        return metrics
    
    def adjust_batch_size(self, current_batch_size: int, efficiency_metrics: Dict[str, float]) -> int:
        """
        Dynamically adjust batch size based on energy efficiency
        """
        info_per_joule = efficiency_metrics.get('information_per_joule', 0)
        
        # If efficiency is below threshold, reduce batch size
        if len(self.processing_history) >= 2:
            previous_efficiency = self.processing_history[-2]['information_per_joule']
            current_efficiency = info_per_joule
            
            if current_efficiency < previous_efficiency * 0.8:  # 20% drop
                new_batch_size = max(1, int(current_batch_size * 0.7))
                logger.info(f"⚡ Reducing batch size for efficiency: {current_batch_size} → {new_batch_size}")
                return new_batch_size
            elif current_efficiency > previous_efficiency * 1.2:  # 20% improvement
                new_batch_size = min(100, int(current_batch_size * 1.3))
                logger.info(f"⚡ Increasing batch size for efficiency: {current_batch_size} → {new_batch_size}")
                return new_batch_size
        
        return current_batch_size
    
    def generate_efficiency_report(self) -> str:
        """Generate energy efficiency report"""
        if not self.processing_history:
            return "No processing history available"
        
        latest = self.processing_history[-1]
        
        report = f"""
Energy Efficiency Report (Landauer Analysis)
===========================================

Latest Processing Metrics:
- Markers Processed: {latest['markers_processed']}
- Processing Time: {latest['processing_time']:.3f}s
- Information Processed: {latest['bits_processed']} bits
- Theoretical Minimum Energy: {latest['theoretical_min_energy']:.2e} J
- Estimated Actual Energy: {latest['estimated_actual_energy']:.2e} J
- Efficiency Ratio: {latest['efficiency_ratio']:.2e}
- Information per Joule: {latest['information_per_joule']:.2e} bits/J
- Landauer Ratio: {latest['landauer_ratio']:.6f}%

The Landauer limit represents the theoretical minimum energy required
for irreversible computation. Our current efficiency is {latest['landauer_ratio']:.6f}%
of this theoretical limit.
"""
        
        if len(self.processing_history) > 1:
            trend = "improving" if latest['information_per_joule'] > self.processing_history[-2]['information_per_joule'] else "declining"
            report += f"\nEfficiency Trend: {trend}"
        
        return report


class QuantumBoosterPipeline:
    """
    Integration layer for quantum-inspired booster modules
    """
    
    def __init__(self):
        self.grover_pruner = GroverDuplicatePruner()
        self.entropy_guard = EntropyBudgetGuard()
        self.schrodingers_preview = SchrodingersPreview()
        self.landauer_limiter = LandauerLimiter()
        
        logger.info("🚀 Quantum Booster Pipeline initialized")
    
    def analyze_marker_quality(self, markers: List[Tuple[str, Dict[str, Any]]]) -> Dict[str, Any]:
        """
        Comprehensive marker quality analysis using all booster modules
        """
        analysis_results = {
            'duplicates': [],
            'entropy_analyses': {},
            'efficiency_metrics': {},
            'recommendations': []
        }
        
        # 1. Duplicate detection
        duplicates = self.grover_pruner.detect_duplicates(markers)
        analysis_results['duplicates'] = duplicates
        
        if duplicates:
            analysis_results['recommendations'].append(
                f"Found {len(duplicates)} potential duplicate pairs - consider merging"
            )
        
        # 2. Entropy analysis for each marker
        for marker_id, marker_data in markers:
            entropy_analysis = self.entropy_guard.analyze_information_density(marker_data)
            analysis_results['entropy_analyses'][marker_id] = entropy_analysis
            
            if not entropy_analysis['meets_budget']:
                analysis_results['recommendations'].extend([
                    f"Marker {marker_id}: {rec}" for rec in entropy_analysis['recommendations']
                ])
        
        # 3. Energy efficiency measurement
        import time
        start_time = time.time()
        
        # Simulate processing work
        processing_time = time.time() - start_time
        efficiency_metrics = self.landauer_limiter.measure_processing_efficiency(
            len(markers), processing_time
        )
        analysis_results['efficiency_metrics'] = efficiency_metrics
        
        logger.info("🧠 Quantum booster analysis complete")
        return analysis_results
    
    def suggest_optimizations(self, analysis_results: Dict[str, Any]) -> List[str]:
        """Generate optimization suggestions based on analysis"""
        suggestions = []
        
        # Duplicate optimization
        if analysis_results['duplicates']:
            suggestions.append(
                "Consider implementing semantic merge strategies for duplicate markers"
            )
        
        # Entropy optimization
        low_entropy_markers = [
            marker_id for marker_id, analysis in analysis_results['entropy_analyses'].items()
            if not analysis['meets_budget']
        ]
        
        if low_entropy_markers:
            suggestions.append(
                f"Enhance information density for markers: {', '.join(low_entropy_markers[:3])}"
            )
        
        # Efficiency optimization
        efficiency = analysis_results.get('efficiency_metrics', {})
        if efficiency.get('landauer_ratio', 0) < 0.001:  # Less than 0.001% of Landauer limit
            suggestions.append(
                "Consider optimizing processing algorithms for better energy efficiency"
            )
        
        return suggestions


# Export main classes
__all__ = [
    'GroverDuplicatePruner',
    'EntropyBudgetGuard', 
    'SchrodingersPreview',
    'LandauerLimiter',
    'QuantumBoosterPipeline'
]