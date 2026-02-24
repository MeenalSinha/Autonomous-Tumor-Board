#!/usr/bin/env python3
"""
Compatibility Verification Script
Checks that all files are compatible and properly structured.
Run this before packaging or committing.
"""

import os
import sys
import ast
import importlib.util
from pathlib import Path


def check_python_syntax(file_path):
    """Check if a Python file has valid syntax."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            ast.parse(f.read())
        return True, None
    except SyntaxError as e:
        return False, str(e)


def check_imports_structure(file_path):
    """Check if imports are properly structured."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            tree = ast.parse(f.read())
        
        # Check for imports
        imports = [node for node in ast.walk(tree) if isinstance(node, (ast.Import, ast.ImportFrom))]
        return True, len(imports)
    except Exception as e:
        return False, str(e)


def check_file_structure():
    """Verify project structure."""
    required_files = [
        'README.md',
        'LICENSE',
        'requirements.txt',
        'setup.py',
        '.gitignore',
        'app.py',
        'api.py',
        'test_system.py',
    ]
    
    required_dirs = [
        'agents',
        'models',
        'orchestrator',
        'utils',
        'data',
        '.github/workflows',
    ]
    
    missing_files = []
    missing_dirs = []
    
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    for dir in required_dirs:
        if not os.path.exists(dir):
            missing_dirs.append(dir)
    
    return missing_files, missing_dirs


def check_documentation():
    """Check documentation files exist."""
    doc_files = [
        'README.md',
        'SETUP_GUIDE.md',
        'FEATURES.md',
        'QUICKSTART.md',
        'LICENSE',
        'CHANGELOG.md',
        'CONTRIBUTING.md',
        'INSTALL.md',
    ]
    
    existing = []
    missing = []
    
    for doc in doc_files:
        if os.path.exists(doc):
            existing.append(doc)
        else:
            missing.append(doc)
    
    return existing, missing


def check_python_files():
    """Check all Python files for syntax errors."""
    python_files = []
    errors = []
    
    for root, dirs, files in os.walk('.'):
        # Skip virtual environments and cache
        if 'venv' in root or '__pycache__' in root or '.git' in root:
            continue
        
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                python_files.append(file_path)
                
                is_valid, error = check_python_syntax(file_path)
                if not is_valid:
                    errors.append((file_path, error))
    
    return python_files, errors


def main():
    """Run all compatibility checks."""
    print("="*60)
    print("COMPATIBILITY VERIFICATION")
    print("="*60)
    
    # Check 1: File Structure
    print("\n1️⃣  Checking project structure...")
    missing_files, missing_dirs = check_file_structure()
    
    if missing_files:
        print(f"   ⚠️  Missing files: {', '.join(missing_files)}")
    if missing_dirs:
        print(f"   ⚠️  Missing directories: {', '.join(missing_dirs)}")
    
    if not missing_files and not missing_dirs:
        print("   ✅ Project structure complete")
    
    # Check 2: Python Syntax
    print("\n2️⃣  Checking Python syntax...")
    python_files, syntax_errors = check_python_files()
    
    if syntax_errors:
        print(f"   ❌ Syntax errors found in {len(syntax_errors)} files:")
        for file, error in syntax_errors:
            print(f"      - {file}: {error}")
    else:
        print(f"   ✅ All {len(python_files)} Python files have valid syntax")
    
    # Check 3: Documentation
    print("\n3️⃣  Checking documentation...")
    existing_docs, missing_docs = check_documentation()
    
    print(f"   ✅ Found {len(existing_docs)} documentation files")
    if missing_docs:
        print(f"   ⚠️  Missing optional docs: {', '.join(missing_docs)}")
    
    # Check 4: Key Modules
    print("\n4️⃣  Checking key modules...")
    key_modules = [
        'agents/pathology_agent.py',
        'agents/imaging_agent.py',
        'agents/guideline_agent.py',
        'agents/mdt_synthesizer.py',
        'models/case_models.py',
        'orchestrator/controller.py',
        'utils/report_generator.py',
    ]
    
    all_exist = True
    for module in key_modules:
        if os.path.exists(module):
            print(f"   ✅ {module}")
        else:
            print(f"   ❌ {module} - MISSING")
            all_exist = False
    
    # Check 5: Configuration Files
    print("\n5️⃣  Checking configuration files...")
    config_files = [
        'requirements.txt',
        '.gitignore',
        '.env.example',
        'Dockerfile',
        'docker-compose.yml',
        '.github/workflows/ci.yml',
    ]
    
    for config in config_files:
        if os.path.exists(config):
            print(f"   ✅ {config}")
        else:
            print(f"   ⚠️  {config} - optional but recommended")
    
    # Summary
    print("\n" + "="*60)
    print("VERIFICATION SUMMARY")
    print("="*60)
    
    total_checks = 5
    passed_checks = 0
    
    if not missing_files and not missing_dirs:
        passed_checks += 1
    if not syntax_errors:
        passed_checks += 1
    if len(existing_docs) >= 5:
        passed_checks += 1
    if all_exist:
        passed_checks += 1
    if all(os.path.exists(f) for f in config_files[:3]):
        passed_checks += 1
    
    print(f"\n✅ Passed: {passed_checks}/{total_checks} checks")
    
    if passed_checks == total_checks:
        print("\n🎉 ALL CHECKS PASSED - Ready for packaging!")
        return 0
    elif passed_checks >= total_checks - 1:
        print("\n⚠️  Minor issues found - Review and fix before packaging")
        return 0
    else:
        print("\n❌ Critical issues found - Must fix before packaging")
        return 1


if __name__ == "__main__":
    sys.exit(main())
