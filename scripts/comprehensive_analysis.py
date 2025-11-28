#!/usr/bin/env python3
"""
Comprehensive Implementation Status Analysis for CareerCoach.ai
Uses multiple methods to assess true implementation completeness
"""

import os
import re
import ast
import json
from pathlib import Path
from typing import Dict, List, Set, Tuple
from dataclasses import dataclass, asdict
import subprocess

@dataclass
class ComponentAnalysis:
    name: str
    files: List[str]
    total_lines: int = 0
    code_lines: int = 0
    functions: int = 0
    classes: int = 0
    api_endpoints: int = 0
    test_coverage: float = 0.0
    completeness_score: float = 0.0

class ImplementationAnalyzer:
    def __init__(self, repo_path: str):
        self.repo_path = Path(repo_path)
        self.analysis = {}

    def count_lines_in_file(self, file_path: Path) -> Tuple[int, int]:
        """Count total lines and code lines (excluding comments/blank lines)"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()

            total_lines = len(lines)
            code_lines = 0

            for line in lines:
                stripped = line.strip()
                if stripped and not stripped.startswith('#'):
                    code_lines += 1

            return total_lines, code_lines
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            return 0, 0

    def analyze_python_file(self, file_path: Path) -> Dict:
        """Analyze Python file structure"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

            # Parse AST
            tree = ast.parse(content, filename=str(file_path))

            functions = []
            classes = []

            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    functions.append(node.name)
                elif isinstance(node, ast.ClassDef):
                    classes.append(node.name)

            # Count API endpoints (FastAPI route decorators)
            api_endpoints = len(re.findall(r'@(?:router|app)\.(?:get|post|put|delete|patch)', content))

            return {
                'functions': len(functions),
                'classes': len(classes),
                'api_endpoints': api_endpoints,
                'function_names': functions[:5],  # First 5 for reference
                'class_names': classes[:3]  # First 3 for reference
            }
        except Exception as e:
            print(f"Error analyzing {file_path}: {e}")
            return {'functions': 0, 'classes': 0, 'api_endpoints': 0, 'function_names': [], 'class_names': []}

    def find_component_files(self, component_name: str) -> List[Path]:
        """Find files related to a component"""
        component_files = {
            'auth': ['**/auth*.py', '**/authentication*.py', '**/oauth*.py', '**/login*.py'],
            'job_matching': ['**/job*.py', '**/matching*.py', '**/recommendation*.py', '**/ai_job*.py'],
            'resume_parsing': ['**/resume*.py', '**/parsing*.py', '**/parser*.py'],
            'payment': ['**/payment*.py', '**/stripe*.py', '**/subscription*.py', '**/billing*.py'],
            'analytics': ['**/analytics*.py', '**/dashboard*.py', '**/metrics*.py'],
            'cache': ['**/cache*.py', '**/redis*.py'],
            'rate_limiting': ['**/rate*.py', '**/limit*.py'],
            'error_handling': ['**/error*.py', '**/exception*.py'],
            'logging': ['**/log*.py', '**/logging*.py'],
            'monitoring': ['**/monitor*.py', '**/metrics*.py', '**/prometheus*.py'],
            'admin': ['**/admin*.py', '**/management*.py'],
            'reporting': ['**/report*.py', '**/export*.py']
        }

        files = []
        patterns = component_files.get(component_name.lower().replace(' ', '_'), [])

        for pattern in patterns:
            files.extend(list(self.repo_path.glob(pattern)))

        # Remove duplicates
        return list(set(files))

    def calculate_completeness_score(self, component: str, analysis: Dict) -> float:
        """Calculate completeness score based on multiple factors"""
        score = 0.0
        max_score = 100.0

        # File existence (20 points)
        if analysis['total_lines'] > 0:
            score += 20

        # Code volume (20 points)
        if analysis['code_lines'] > 100:
            score += 20
        elif analysis['code_lines'] > 50:
            score += 10

        # Structure complexity (20 points)
        functions_score = min(analysis['functions'] * 2, 10)
        classes_score = min(analysis['classes'] * 5, 10)
        score += functions_score + classes_score

        # API endpoints (20 points)
        if analysis['api_endpoints'] > 0:
            score += min(analysis['api_endpoints'] * 5, 20)

        # Test coverage estimation (20 points) - rough heuristic
        test_files = len([f for f in analysis.get('files', []) if 'test' in str(f).lower()])
        if test_files > 0:
            score += min(test_files * 10, 20)

        return min(score, max_score)

    def analyze_component(self, component_name: str) -> ComponentAnalysis:
        """Analyze a specific component"""
        files = self.find_component_files(component_name)

        analysis = ComponentAnalysis(
            name=component_name,
            files=[str(f.relative_to(self.repo_path)) for f in files]
        )

        # Analyze each file
        for file_path in files:
            if file_path.suffix == '.py':
                total_lines, code_lines = self.count_lines_in_file(file_path)
                analysis.total_lines += total_lines
                analysis.code_lines += code_lines

                file_analysis = self.analyze_python_file(file_path)
                analysis.functions += file_analysis['functions']
                analysis.classes += file_analysis['classes']
                analysis.api_endpoints += file_analysis['api_endpoints']

        # Calculate completeness score
        analysis.completeness_score = self.calculate_completeness_score(component_name, {
            'total_lines': analysis.total_lines,
            'code_lines': analysis.code_lines,
            'functions': analysis.functions,
            'classes': analysis.classes,
            'api_endpoints': analysis.api_endpoints,
            'files': files
        })

        return analysis

    def run_full_analysis(self) -> Dict:
        """Run analysis on all components"""
        components = [
            'auth', 'job_matching', 'resume_parsing', 'payment',
            'analytics', 'cache', 'rate_limiting', 'error_handling',
            'logging', 'monitoring', 'admin', 'reporting'
        ]

        results = {}
        for component in components:
            print(f"Analyzing {component}...")
            results[component] = self.analyze_component(component)

        return results

    def generate_report(self, results: Dict) -> str:
        """Generate a comprehensive report"""
        report = "# CareerCoach.ai Implementation Status Analysis\n\n"
        report += f"Generated on: {os.popen('date').read().strip()}\n\n"
        report += "## Methodology\n\n"
        report += "This analysis uses multiple metrics:\n"
        report += "- **Lines of Code**: Total and code-only lines\n"
        report += "- **Structure**: Functions, classes, API endpoints\n"
        report += "- **Completeness Score**: 0-100 based on multiple factors\n"
        report += "- **File Coverage**: Number of relevant files found\n\n"

        # Group by categories
        categories = {
            "Critical Path": ['auth', 'job_matching', 'resume_parsing', 'payment'],
            "Important Features": ['analytics', 'cache', 'rate_limiting', 'error_handling'],
            "Supporting Code": ['admin', 'reporting'],
            "Infrastructure": ['logging', 'monitoring']
        }

        for category_name, components in categories.items():
            report += f"## {category_name}\n\n"
            report += "| Component | Files | Lines | Functions | Classes | API Endpoints | Completeness |\n"
            report += "|-----------|-------|-------|-----------|---------|---------------|--------------|\n"

            category_total_lines = 0
            category_completeness = 0

            for comp_name in components:
                if comp_name in results:
                    comp = results[comp_name]
                    report += f"| {comp.name.replace('_', ' ').title()} | {len(comp.files)} | {comp.code_lines:,} | {comp.functions} | {comp.classes} | {comp.api_endpoints} | {comp.completeness_score:.1f}% |\n"
                    category_total_lines += comp.code_lines
                    category_completeness += comp.completeness_score

            avg_completeness = category_completeness / len(components) if components else 0
            report += f"\n**Category Summary**: {category_total_lines:,} lines, {avg_completeness:.1f}% average completeness\n\n"

        # Detailed breakdown
        report += "## Detailed Component Analysis\n\n"
        for comp_name, comp in results.items():
            report += f"### {comp.name.replace('_', ' ').title()}\n\n"
            report += f"- **Files Found**: {len(comp.files)}\n"
            report += f"- **Total Lines**: {comp.total_lines:,}\n"
            report += f"- **Code Lines**: {comp.code_lines:,}\n"
            report += f"- **Functions**: {comp.functions}\n"
            report += f"- **Classes**: {comp.classes}\n"
            report += f"- **API Endpoints**: {comp.api_endpoints}\n"
            report += f"- **Completeness Score**: {comp.completeness_score:.1f}%\n\n"

            if comp.files:
                report += "**Files**:\n"
                for file in comp.files[:10]:  # Show first 10
                    report += f"- `{file}`\n"
                if len(comp.files) > 10:
                    report += f"- ... and {len(comp.files) - 10} more\n"
            report += "\n"

        return report

def main():
    repo_path = "/workspaces/CareerCoach.ai"  # Adjust if needed

    # Try to detect the actual repo path
    current_dir = Path.cwd()
    if (current_dir / "main.py").exists():
        repo_path = str(current_dir)
    elif (current_dir.parent / "main.py").exists():
        repo_path = str(current_dir.parent)

    print(f"Analyzing repository at: {repo_path}")

    analyzer = ImplementationAnalyzer(repo_path)
    results = analyzer.run_full_analysis()

    report = analyzer.generate_report(results)

    # Save report
    with open("implementation_analysis_report.md", "w") as f:
        f.write(report)

    print("Analysis complete! Report saved to: implementation_analysis_report.md")

    # Print summary to console
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)

    categories = {
        "Critical Path": ['auth', 'job_matching', 'resume_parsing', 'payment'],
        "Important Features": ['analytics', 'cache', 'rate_limiting', 'error_handling'],
        "Supporting Code": ['admin', 'reporting'],
        "Infrastructure": ['logging', 'monitoring']
    }

    for category_name, components in categories.items():
        print(f"\n{category_name}:")
        total_lines = 0
        total_score = 0

        for comp_name in components:
            if comp_name in results:
                comp = results[comp_name]
                print(f"  - {comp.name.replace('_', ' ').title()}: {comp.code_lines:,} lines, {comp.completeness_score:.1f}% completeness")
                total_lines += comp.code_lines
                total_score += comp.completeness_score

        avg_score = total_score / len(components) if components else 0
        print(f"  → {total_lines:,} lines, {avg_score:.1f}% average completeness")

if __name__ == "__main__":
    main()