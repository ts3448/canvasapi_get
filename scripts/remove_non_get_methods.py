#!/usr/bin/env python3
"""
Script to automatically remove methods identified by find_non_get_methods.py.
Processes the automated removal report and safely deletes methods from source files.
"""

import re
import shutil
from pathlib import Path
from collections.abc import Sequence


class MethodRemovalData:
    """Data class to hold method removal information."""
    
    def __init__(
        self, 
        file_path: str, 
        class_name: str, 
        method_name: str, 
        start_line: int, 
        end_line: int, 
        http_method: str,
        request_line: int
    ) -> None:
        """Initialize method removal data.
        
        Args:
            file_path: Path to the file containing the method.
            class_name: Name of the class containing the method.
            method_name: Name of the method to remove.
            start_line: Starting line number of the method.
            end_line: Ending line number of the method.
            http_method: HTTP method used in the request call.
            request_line: Line number of the actual request call.
        """
        self.file_path = file_path
        self.class_name = class_name
        self.method_name = method_name
        self.start_line = start_line
        self.end_line = end_line
        self.http_method = http_method
        self.request_line = request_line


def parse_removal_report(report_content: str) -> list[MethodRemovalData]:
    """Parse the automated removal report into structured data.
    
    Args:
        report_content: Content of the removal report.
        
    Returns:
        List of MethodRemovalData objects.
    """
    methods = []
    current_file = None
    
    lines = report_content.strip().split('\n')
    
    for i, line in enumerate(lines):
        line = line.strip()
        
        if line.startswith('FILE: '):
            current_file = line[6:]  # Remove 'FILE: ' prefix
            
        elif line.startswith('REMOVE_METHOD: '):
            if not current_file:
                continue
                
            method_info = line[15:]  # Remove 'REMOVE_METHOD: ' prefix
            class_name, method_name = method_info.split('.', 1)
            
            # Parse the next few lines for additional info
            lines_info = None
            http_method = None
            request_line = None
            
            for j in range(i + 1, min(i + 5, len(lines))):
                next_line = lines[j].strip()
                if next_line.startswith('LINES: '):
                    lines_info = next_line[7:]
                elif next_line.startswith('HTTP_METHOD: '):
                    http_method = next_line[13:]
                elif next_line.startswith('REQUEST_LINE: '):
                    request_line = int(next_line[14:])
                elif next_line == '---':
                    break
            
            if lines_info and http_method and request_line:
                start_line, end_line = map(int, lines_info.split('-'))
                
                methods.append(MethodRemovalData(
                    file_path=current_file,
                    class_name=class_name,
                    method_name=method_name,
                    start_line=start_line,
                    end_line=end_line,
                    http_method=http_method,
                    request_line=request_line
                ))
    
    return methods


def create_backup(file_path: str) -> str:
    """Create a backup of the file before modification.
    
    Args:
        file_path: Path to the file to backup.
        
    Returns:
        Path to the backup file.
        
    Raises:
        FileNotFoundError: If the source file doesn't exist.
        PermissionError: If unable to create backup.
    """
    backup_path = f"{file_path}.backup"
    shutil.copy2(file_path, backup_path)
    return backup_path


def validate_method_signature(lines: list[str], method_data: MethodRemovalData) -> bool:
    """Validate that the method at the specified lines matches expectations.
    
    Args:
        lines: All lines from the file.
        method_data: Method removal data to validate.
        
    Returns:
        True if method signature matches expectations.
    """
    if method_data.start_line <= 0 or method_data.start_line > len(lines):
        return False
        
    method_line = lines[method_data.start_line - 1].strip()
    
    # Check if line contains a method definition
    if not method_line.startswith('def '):
        return False
        
    # Extract method name from definition
    match = re.match(r'def\s+(\w+)\s*\(', method_line)
    if not match:
        return False
        
    actual_method_name = match.group(1)
    return actual_method_name == method_data.method_name


def remove_method_from_file(file_path: str, methods: list[MethodRemovalData], dry_run: bool = False) -> dict[str, str | int]:
    """Remove methods from a single file.
    
    Args:
        file_path: Path to the file to modify.
        methods: List of methods to remove from this file.
        dry_run: If True, only simulate removal without actual changes.
        
    Returns:
        Dictionary with removal results and statistics.
        
    Raises:
        FileNotFoundError: If the file doesn't exist.
        PermissionError: If unable to read/write the file.
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Sort methods by start_line in descending order for safe removal
    sorted_methods = sorted(methods, key=lambda x: x.start_line, reverse=True)
    
    removed_count = 0
    skipped_count = 0
    backup_created = False
    
    for method_data in sorted_methods:
        # Validate method signature before removal
        if not validate_method_signature(lines, method_data):
            print(f"  WARNING: Method signature validation failed for {method_data.method_name}")
            skipped_count += 1
            continue
        
        # Create backup on first successful validation
        if not dry_run and not backup_created:
            backup_path = create_backup(file_path)
            backup_created = True
            print(f"  Created backup: {backup_path}")
        
        # Remove lines (convert to 0-based indexing)
        start_idx = method_data.start_line - 1
        end_idx = method_data.end_line
        
        if not dry_run:
            del lines[start_idx:end_idx]
        
        removed_count += 1
        
        if dry_run:
            print(f"  [DRY RUN] Would remove {method_data.class_name}.{method_data.method_name} (lines {method_data.start_line}-{method_data.end_line})")
        else:
            print(f"  Removed {method_data.class_name}.{method_data.method_name} (lines {method_data.start_line}-{method_data.end_line})")
    
    # Write modified content back to file
    if not dry_run and removed_count > 0:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.writelines(lines)
    
    return {
        'file_path': file_path,
        'removed_count': removed_count,
        'skipped_count': skipped_count,
        'backup_created': backup_created
    }


def group_methods_by_file(methods: list[MethodRemovalData]) -> dict[str, list[MethodRemovalData]]:
    """Group methods by their file path.
    
    Args:
        methods: List of method removal data.
        
    Returns:
        Dictionary mapping file paths to lists of methods.
    """
    grouped = {}
    for method in methods:
        if method.file_path not in grouped:
            grouped[method.file_path] = []
        grouped[method.file_path].append(method)
    
    return grouped


def process_removal_report(report_file: str, dry_run: bool = False) -> dict[str, str | int]:
    """Process the entire removal report and remove identified methods.
    
    Args:
        report_file: Path to the removal report file.
        dry_run: If True, only simulate removal without actual changes.
        
    Returns:
        Dictionary with overall processing results.
        
    Raises:
        FileNotFoundError: If the report file doesn't exist.
    """
    print(f"Processing removal report: {report_file}")
    print(f"Mode: {'DRY RUN' if dry_run else 'ACTUAL REMOVAL'}")
    print("=" * 50)
    
    with open(report_file, 'r', encoding='utf-8') as f:
        report_content = f.read()
    
    methods = parse_removal_report(report_content)
    print(f"Parsed {len(methods)} methods for removal")
    
    grouped_methods = group_methods_by_file(methods)
    print(f"Affecting {len(grouped_methods)} files")
    print()
    
    total_removed = 0
    total_skipped = 0
    files_processed = 0
    
    for file_path, file_methods in grouped_methods.items():
        print(f"Processing {file_path} ({len(file_methods)} methods)")
        
        if not Path(file_path).exists():
            print(f"  ERROR: File not found - {file_path}")
            total_skipped += len(file_methods)
            continue
        
        try:
            result = remove_method_from_file(file_path, file_methods, dry_run)
            total_removed += result['removed_count']
            total_skipped += result['skipped_count']
            files_processed += 1
            
        except Exception as e:
            print(f"  ERROR: Failed to process {file_path}: {e}")
            total_skipped += len(file_methods)
        
        print()
    
    return {
        'total_methods': len(methods),
        'total_removed': total_removed,
        'total_skipped': total_skipped,
        'files_processed': files_processed,
        'files_total': len(grouped_methods)
    }


def generate_summary_report(results: dict[str, str | int]) -> str:
    """Generate a summary report of the removal operation.
    
    Args:
        results: Results dictionary from process_removal_report.
        
    Returns:
        Formatted summary report string.
    """
    summary = "REMOVAL OPERATION SUMMARY\n"
    summary += "=" * 50 + "\n"
    summary += f"Total methods identified: {results['total_methods']}\n"
    summary += f"Methods successfully removed: {results['total_removed']}\n"
    summary += f"Methods skipped (validation failed): {results['total_skipped']}\n"
    summary += f"Files processed successfully: {results['files_processed']}\n"
    summary += f"Total files affected: {results['files_total']}\n"
    summary += "\n"
    
    if results['total_removed'] > 0:
        summary += "SUCCESS: Methods have been removed from the codebase.\n"
        summary += "Backup files (.backup) have been created for modified files.\n"
        summary += "Please test your application to ensure functionality.\n"
    else:
        summary += "No methods were removed. Check for validation errors above.\n"
    
    return summary


def main() -> None:
    """Main function to execute method removal."""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python remove_non_get_methods.py <report_file> [--dry-run]")
        print("  report_file: Path to the removal report generated by find_non_get_methods.py")
        print("  --dry-run: Preview changes without actually removing methods")
        sys.exit(1)
    
    report_file = sys.argv[1]
    dry_run = '--dry-run' in sys.argv
    
    if not Path(report_file).exists():
        print(f"ERROR: Report file not found: {report_file}")
        sys.exit(1)
    
    try:
        results = process_removal_report(report_file, dry_run)
        print(generate_summary_report(results))
        
    except Exception as e:
        print(f"ERROR: Failed to process removal report: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
