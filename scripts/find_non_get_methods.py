#!/usr/bin/env python3
"""
Script to find all methods that use Requester.request() with non-GET HTTP methods.
This will help identify methods that need to be removed from the codebase.
"""

import ast
from pathlib import Path


class RequestCallVisitor(ast.NodeVisitor):
    """AST visitor to find _requester.request() calls with non-GET methods."""

    def __init__(self) -> None:
        """Initialize the visitor."""
        self.current_method: str | None = None
        self.current_class: str | None = None
        self.results: list[dict[str, str | int]] = []
        self.method_starts: dict[str, int] = {}

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        """Visit class definition and track current class.

        Args:
            node: The AST class definition node.
        """
        old_class = self.current_class
        self.current_class = node.name
        self.generic_visit(node)
        self.current_class = old_class

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        """Visit function definition and track current method.

        Args:
            node: The AST function definition node.
        """
        old_method = self.current_method
        self.current_method = node.name

        # Store method start line for boundary detection
        method_key = (
            f"{self.current_class}.{node.name}" if self.current_class else node.name
        )
        self.method_starts[method_key] = node.lineno

        self.generic_visit(node)
        self.current_method = old_method

    def visit_Call(self, node: ast.Call) -> None:
        """Visit function calls and identify _requester.request() with non-GET methods.

        Args:
            node: The AST call node.
        """
        if self._is_requester_request_call(node):
            http_method = self._extract_http_method(node)
            if http_method and http_method != "GET":
                self.results.append(
                    {
                        "class": self.current_class or "module_level",
                        "method": self.current_method or "unknown",
                        "http_method": http_method,
                        "line": node.lineno,
                    }
                )

        self.generic_visit(node)

    @staticmethod
    def _is_requester_request_call(node: ast.Call) -> bool:
        """Check if node is a _requester.request() call.

        Args:
            node: The AST call node to check.

        Returns:
            True if this is a _requester.request() call.
        """
        return (
            isinstance(node.func, ast.Attribute)
            and node.func.attr == "request"
            and isinstance(node.func.value, ast.Attribute)
            and node.func.value.attr == "_requester"
        )

    @staticmethod
    def _extract_http_method(node: ast.Call) -> str | None:
        """Extract HTTP method from request call arguments.

        Args:
            node: The AST call node.

        Returns:
            The HTTP method string or None if not found.
        """
        if node.args and isinstance(node.args[0], ast.Constant):
            first_arg = node.args[0]
            if isinstance(first_arg.value, str):  # type: ignore
                return first_arg.value  # type: ignore
        return None


def find_python_files(project_root: str) -> list[Path]:
    """Find all Python files in the canvasapi_get directory.

    Args:
        project_root: Path to the project root directory.

    Returns:
        List of Python file paths.
    """
    root_path = Path(project_root)
    canvasapi_dir = root_path / "canvasapi_get"

    if not canvasapi_dir.exists():
        return []

    return list(canvasapi_dir.glob("*.py"))


def parse_file_for_non_get_methods(file_path: Path) -> list[dict[str, str | int]]:
    """Parse a single file for non-GET _requester.request() calls.

    Args:
        file_path: Path to the Python file to analyze.

    Returns:
        List of dictionaries containing method information.

    Raises:
        Exception: If file cannot be read or parsed.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        tree = ast.parse(content)
        visitor = RequestCallVisitor()
        visitor.visit(tree)

        # Add file path to each result
        for result in visitor.results:
            result["file"] = str(file_path)

        return visitor.results

    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return []


def detect_method_boundaries(
    file_path: Path, method_name: str, class_name: str | None = None
) -> tuple[int, int]:
    """Detect the start and end lines of a method for complete removal.

    Args:
        file_path: Path to the Python file.
        method_name: Name of the method to find boundaries for.
        class_name: Name of the class containing the method, if any.

    Returns:
        Tuple of (start_line, end_line) for the method.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        tree = ast.parse("".join(lines))

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name == method_name:
                # Check if we're in the right class context
                if class_name:
                    # Find parent class
                    for parent in ast.walk(tree):
                        if (
                            isinstance(parent, ast.ClassDef)
                            and parent.name == class_name
                            and any(child == node for child in ast.walk(parent))
                        ):
                            break
                    else:
                        continue  # Method not in expected class

                start_line = node.lineno

                # Find end line by looking at the last statement in the method
                if node.body:
                    last_stmt = node.body[-1]
                    end_line = getattr(last_stmt, "end_lineno", last_stmt.lineno)
                else:
                    end_line = start_line

                return start_line, end_line or start_line

        return 0, 0  # Method not found

    except Exception:
        return 0, 0


def scan_all_files(project_root: str) -> list[dict[str, str | int]]:
    """Scan all Python files for non-GET request methods.

    Args:
        project_root: Path to the project root directory.

    Returns:
        List of all non-GET method information found.
    """
    py_files = find_python_files(project_root)
    all_results: list[dict[str, str | int]] = []

    print(f"Found {len(py_files)} Python files to scan...")

    for py_file in py_files:
        print(f"Scanning {py_file.name}...")
        results = parse_file_for_non_get_methods(py_file)

        # Add method boundary information for each result
        for result in results:
            file_path = Path(result["file"])
            method_name = str(result["method"])
            class_name = (
                str(result["class"]) if result["class"] != "module_level" else None
            )

            start_line, end_line = detect_method_boundaries(
                file_path, method_name, class_name
            )
            result["method_start_line"] = start_line
            result["method_end_line"] = end_line

        all_results.extend(results)

    return all_results


def generate_removal_report(results: list[dict[str, str | int]]) -> str:
    """Generate a structured report suitable for automated method removal.

    Args:
        results: List of method information dictionaries.

    Returns:
        Formatted report string for automated processing.
    """
    if not results:
        return "No non-GET request methods found."

    report = f"# AUTOMATED REMOVAL REPORT\n"
    report += f"# Found {len(results)} methods using non-GET requests\n\n"

    # Group by file for organized removal
    by_file: dict[str, list[dict[str, str | int]]] = {}
    for method_info in results:
        file_path = str(method_info["file"])
        if file_path not in by_file:
            by_file[file_path] = []
        by_file[file_path].append(method_info)

    for file_path in sorted(by_file.keys()):
        report += f"FILE: {file_path}\n"

        # Sort by line number (descending) for safe removal from bottom up
        methods = sorted(
            by_file[file_path], key=lambda x: int(x["method_start_line"]), reverse=True
        )

        for method_info in methods:
            report += f"REMOVE_METHOD: {method_info['class']}.{method_info['method']}\n"
            report += f"LINES: {method_info['method_start_line']}-{method_info['method_end_line']}\n"
            report += f"HTTP_METHOD: {method_info['http_method']}\n"
            report += f"REQUEST_LINE: {method_info['line']}\n"
            report += "---\n"

        report += "\n"

    return report


def generate_summary_stats(results: list[dict[str, str | int]]) -> str:
    """Generate summary statistics of findings.

    Args:
        results: List of method information dictionaries.

    Returns:
        Summary statistics string.
    """
    if not results:
        return "No non-GET request methods found."

    # Count by HTTP method
    by_method: dict[str, int] = {}
    for method_info in results:
        http_method = str(method_info["http_method"])
        by_method[http_method] = by_method.get(http_method, 0) + 1

    # Count by file
    by_file: dict[str, int] = {}
    for method_info in results:
        file_path = str(method_info["file"])
        by_file[file_path] = by_file.get(file_path, 0) + 1

    summary = f"SUMMARY: {len(results)} non-GET methods found\n\n"
    summary += "By HTTP Method:\n"
    for method, count in sorted(by_method.items()):
        summary += f"  {method}: {count} methods\n"

    summary += f"\nAffected Files: {len(by_file)} files\n"
    for file_path, count in sorted(by_file.items(), key=lambda x: x[1], reverse=True):
        file_name = Path(file_path).name
        summary += f"  {file_name}: {count} methods\n"

    return summary


def main() -> None:
    """Main function to execute the method finder and generate removal report."""
    project_root = "."

    print("Scanning for non-GET _requester.request() method calls...")
    results = scan_all_files(project_root)

    print(f"\nScan complete! Found {len(results)} non-GET methods.")

    print("\n" + "=" * 50)
    print("SUMMARY STATISTICS")
    print("=" * 50)
    print(generate_summary_stats(results))

    print("\n" + "=" * 50)
    print("AUTOMATED REMOVAL REPORT")
    print("=" * 50)
    print(generate_removal_report(results))

    print("\n" + "=" * 50)
    print("USAGE INSTRUCTIONS")
    print("=" * 50)
    print("1. Review the methods listed above")
    print("2. Use the LINES information to remove methods from files")
    print("3. Process files from bottom to top (lines in descending order)")
    print("4. Remove entire method definitions using the line ranges")
    print("5. Test application after each file modification")


if __name__ == "__main__":
    main()
