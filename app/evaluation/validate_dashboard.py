import ast
import sys
from pathlib import Path


DASHBOARD_FILE = Path(
    "app/evaluation/evaluation_dashboard.py"
)


def validate_file_exists():
    """Check that the dashboard file exists."""

    if not DASHBOARD_FILE.exists():

        print(
            f"❌ Dashboard file not found: "
            f"{DASHBOARD_FILE}"
        )

        return False

    print(
        f"✅ Dashboard file found: "
        f"{DASHBOARD_FILE}"
    )

    return True


def validate_syntax():
    """Check Python syntax."""

    try:

        source = DASHBOARD_FILE.read_text(
            encoding="utf-8"
        )

        ast.parse(
            source,
            filename=str(DASHBOARD_FILE),
        )

        print(
            "✅ Python syntax is valid"
        )

        return True

    except SyntaxError as error:

        print(
            "❌ Python syntax error"
        )

        print(
            f"Line: {error.lineno}"
        )

        print(
            f"Column: {error.offset}"
        )

        print(
            f"Message: {error.msg}"
        )

        return False


def validate_download_keys():
    """
    Check that Streamlit download buttons
    don't reuse the same key.
    """

    source = DASHBOARD_FILE.read_text(
        encoding="utf-8"
    )

    tree = ast.parse(
        source,
        filename=str(DASHBOARD_FILE),
    )

    download_keys = []

    for node in ast.walk(tree):

        if not isinstance(
            node,
            ast.Call,
        ):

            continue

        if not isinstance(
            node.func,
            ast.Attribute,
        ):

            continue

        if node.func.attr != "download_button":

            continue

        for keyword in node.keywords:

            if keyword.arg != "key":

                continue

            if isinstance(
                keyword.value,
                ast.Constant,
            ):

                key = keyword.value.value

                download_keys.append(
                    key
                )


    duplicates = {
        key
        for key in download_keys
        if download_keys.count(key) > 1
    }


    if duplicates:

        print(
            "❌ Duplicate download button keys found:"
        )

        for key in sorted(duplicates):

            print(
                f"   - {key}"
            )

        return False


    print(
        f"✅ Download button keys are unique "
        f"({len(download_keys)} found)"
    )

    return True


def validate_required_sections():
    """
    Check that all major dashboard sections
    are present.
    """

    source = DASHBOARD_FILE.read_text(
        encoding="utf-8"
    )


    required_sections = [
        "Evaluation History",
        "Run Comparison",
        "Evaluation Trend Analysis",
        "Evaluation Failure Analysis",
        "Evaluation Recommendations",
        "Final Evaluation Summary",
    ]


    missing_sections = []


    for section in required_sections:

        if section not in source:

            missing_sections.append(
                section
            )


    if missing_sections:

        print(
            "❌ Missing dashboard sections:"
        )

        for section in missing_sections:

            print(
                f"   - {section}"
            )

        return False


    print(
        "✅ All required dashboard sections "
        "are present"
    )

    return True


def main():

    print()
    print("=" * 70)
    print("Evaluation Dashboard Validation")
    print("=" * 70)
    print()


    checks = []


    # --------------------------------------------------------
    # File check
    # --------------------------------------------------------

    checks.append(
        validate_file_exists()
    )


    if not checks[-1]:

        sys.exit(1)


    # --------------------------------------------------------
    # Syntax check
    # --------------------------------------------------------

    checks.append(
        validate_syntax()
    )


    if not checks[-1]:

        sys.exit(1)


    # --------------------------------------------------------
    # Download key check
    # --------------------------------------------------------

    checks.append(
        validate_download_keys()
    )


    # --------------------------------------------------------
    # Section check
    # --------------------------------------------------------

    checks.append(
        validate_required_sections()
    )


    # --------------------------------------------------------
    # Final result
    # --------------------------------------------------------

    print()
    print("=" * 70)


    if all(checks):

        print(
            "✅ ALL DASHBOARD VALIDATION CHECKS PASSED"
        )

        print("=" * 70)

        sys.exit(0)


    print(
        "❌ DASHBOARD VALIDATION FAILED"
    )

    print("=" * 70)

    sys.exit(1)


if __name__ == "__main__":

    main()