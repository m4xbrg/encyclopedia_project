import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def run_step(script: str) -> int:
    """Run a script using the current Python executable."""
    result = subprocess.run([sys.executable, str(ROOT / script)])
    return result.returncode


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run generation then compilation"
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "--generate-only",
        action="store_true",
        help="Run only the generation step",
    )
    group.add_argument(
        "--compile-only",
        action="store_true",
        help="Run only the compilation step",
    )
    args = parser.parse_args()

    if args.generate_only:
        return run_step("generate.py")
    if args.compile_only:
        return run_step("compile_pdf.py")

    gen_rc = run_step("generate.py")
    comp_rc = run_step("compile_pdf.py")
    return gen_rc or comp_rc


if __name__ == "__main__":
    sys.exit(main())

