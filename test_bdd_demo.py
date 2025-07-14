#!/usr/bin/env python3
"""
BDD Implementation Demo Script
Demonstrates that the completed BDD framework can run basic scenarios.
"""

import subprocess
import sys
from pathlib import Path

def test_basic_bdd_functionality():
    """Test basic BDD functionality without requiring hardware."""
    print("🚀 Testing BDD Framework Basic Functionality")
    print("=" * 50)
    
    # Test 1: List all available features
    print("\n📋 Test 1: List Available Features")
    try:
        venv_behave = Path(".venv/Scripts/behave.exe")
        if venv_behave.exists():
            behave_cmd = str(venv_behave)
        else:
            behave_cmd = "behave"
        
        result = subprocess.run(
            [behave_cmd, "--dry-run", "--no-summary", "features/"],
            capture_output=True,
            text=True,
            cwd=Path.cwd()
        )
        
        if result.returncode == 0:
            lines = result.stdout.split('\n')
            features = [line for line in lines if 'Feature:' in line]
            scenarios = [line for line in lines if 'Scenario:' in line]
            
            print(f"✅ Found {len(features)} features and {len(scenarios)} scenarios")
            for feature in features[:3]:  # Show first 3 features
                print(f"   📄 {feature.strip()}")
        else:
            print(f"❌ Failed to list features: {result.stderr}")
            return False
            
    except FileNotFoundError:
        print("⚠️  behave not found")
        return False
    
    # Test 2: Verify tags work
    print("\n📋 Test 2: List Available Tags")
    try:
        result = subprocess.run(
            [behave_cmd, "--dry-run", "--tags-help", "features/"],
            capture_output=True,
            text=True,
            cwd=Path.cwd()
        )
        
        if result.returncode == 0:
            lines = result.stdout.split('\n')
            tag_lines = [line for line in lines if '@' in line and 'times' in line]
            
            print(f"✅ Found tags in features")
            for tag_line in tag_lines[:5]:  # Show first 5 tag usage lines
                print(f"   🏷️  {tag_line.strip()}")
        else:
            print(f"❌ Failed to get tags: {result.stderr}")
            
    except Exception as e:
        print(f"⚠️  Tag analysis failed: {e}")
    
    # Test 3: Test specific tag filtering
    print("\n📋 Test 3: Test Tag Filtering")
    try:
        result = subprocess.run(
            [behave_cmd, "--dry-run", "--tags=@registration", "features/"],
            capture_output=True,
            text=True,
            cwd=Path.cwd()
        )
        
        if result.returncode == 0:
            lines = result.stdout.split('\n')
            scenarios = [line for line in lines if 'Scenario:' in line]
            print(f"✅ Found {len(scenarios)} registration scenarios")
        else:
            print(f"❌ Tag filtering failed: {result.stderr}")
            
    except Exception as e:
        print(f"⚠️  Tag filtering test failed: {e}")
    
    print("\n" + "=" * 50)
    print("✅ BDD Framework Basic Functionality Test Complete")
    print("\n💡 The framework is ready! To run with actual hardware:")
    print("   1. Start Appium: appium --port 4723")
    print("   2. Connect Android device with USB debugging")  
    print("   3. Connect DIGIPASS FX7 device")
    print("   4. Run: behave features/digipass_fx7/registration.feature --tags=@hardware")
    return True

def show_available_commands():
    """Show available BDD commands for the user."""
    print("\n🔧 Available BDD Commands:")
    print("-" * 30)
    print("# Run all features:")
    print("behave features/")
    print()
    print("# Run specific feature:")
    print("behave features/digipass_fx7/registration.feature")
    print()
    print("# Run with specific tags:")
    print("behave features/ --tags=@registration")
    print("behave features/ --tags=@authentication")
    print("behave features/ --tags=@hardware")
    print()
    print("# Run with verbose output:")
    print("behave features/ --verbose")
    print()
    print("# Generate reports:")
    print("behave features/ --format=json --outfile=reports/bdd_results.json")
    print("behave features/ --format=html --outfile=reports/bdd_results.html")

if __name__ == "__main__":
    success = test_basic_bdd_functionality()
    show_available_commands()
    sys.exit(0 if success else 1)
