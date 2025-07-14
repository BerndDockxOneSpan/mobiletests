#!/usr/bin/env python3
"""
BDD Test Runner for DIGIPASS FX7 Tests

This script provides utilities to run Gherkin/BDD tests for the DIGIPASS FX7 project.
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path

def run_behave_tests(
    feature_path: str = "features/",
    tags: str = None,
    format_type: str = "pretty",
    output_dir: str = "reports/",
    dry_run: bool = False
):
    """
    Run Behave tests with specified parameters.
    
    Args:
        feature_path: Path to feature files
        tags: Tag filter (e.g., "@hardware", "@registration")
        format_type: Output format (pretty, json, junit)
        output_dir: Directory for test reports
        dry_run: Whether to perform a dry run
    """
    
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Build behave command
    cmd = ["behave"]
    
    # Add feature path
    cmd.append(feature_path)
    
    # Add tags if specified
    if tags:
        cmd.extend(["--tags", tags])
    
    # Add format
    cmd.extend(["--format", format_type])
    
    # Add JUnit output for CI/CD
    if format_type == "junit" or not dry_run:
        cmd.extend(["--junit", "--junit-directory", output_dir])
    
    # Add dry run flag
    if dry_run:
        cmd.append("--dry-run")
    
    # Add verbose output
    cmd.append("--verbose")
    
    print(f"Running command: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        print("STDOUT:")
        print(result.stdout)
        
        if result.stderr:
            print("STDERR:")
            print(result.stderr)
        
        return result.returncode == 0
        
    except FileNotFoundError:
        print("Error: 'behave' command not found. Make sure it's installed:")
        print("pip install behave")
        return False
    except Exception as e:
        print(f"Error running tests: {e}")
        return False

def list_available_features():
    """List all available feature files."""
    features_dir = Path("features")
    if not features_dir.exists():
        print("No features directory found")
        return
    
    print("Available feature files:")
    for feature_file in features_dir.rglob("*.feature"):
        print(f"  - {feature_file}")

def list_available_tags():
    """List all available tags from feature files."""
    features_dir = Path("features")
    tags = set()
    
    for feature_file in features_dir.rglob("*.feature"):
        try:
            with open(feature_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line.startswith('@'):
                        # Extract tags from the line
                        line_tags = [tag.strip() for tag in line.split() if tag.startswith('@')]
                        tags.update(line_tags)
        except Exception as e:
            print(f"Error reading {feature_file}: {e}")
    
    if tags:
        print("Available tags:")
        for tag in sorted(tags):
            print(f"  - {tag}")
    else:
        print("No tags found in feature files")

def main():
    """Main entry point for the BDD test runner."""
    parser = argparse.ArgumentParser(description="Run DIGIPASS FX7 BDD Tests")
    
    # Add command line arguments
    parser.add_argument(
        "--features", "-f",
        default="features/",
        help="Path to feature files (default: features/)"
    )
    
    parser.add_argument(
        "--tags", "-t",
        help="Run scenarios with specific tags (e.g., '@hardware', '@registration')"
    )
    
    parser.add_argument(
        "--format",
        choices=["pretty", "json", "junit", "html"],
        default="pretty",
        help="Output format (default: pretty)"
    )
    
    parser.add_argument(
        "--output", "-o",
        default="reports/",
        help="Output directory for reports (default: reports/)"
    )
    
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Perform a dry run without executing steps"
    )
    
    parser.add_argument(
        "--list-features",
        action="store_true",
        help="List all available feature files"
    )
    
    parser.add_argument(
        "--list-tags",
        action="store_true",
        help="List all available tags"
    )
    
    args = parser.parse_args()
    
    # Handle list commands
    if args.list_features:
        list_available_features()
        return
    
    if args.list_tags:
        list_available_tags()
        return
    
    # Run tests
    success = run_behave_tests(
        feature_path=args.features,
        tags=args.tags,
        format_type=args.format,
        output_dir=args.output,
        dry_run=args.dry_run
    )
    
    if success:
        print("\n✅ Tests completed successfully!")
        sys.exit(0)
    else:
        print("\n❌ Tests failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()
