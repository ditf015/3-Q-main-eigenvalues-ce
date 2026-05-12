#!/usr/bin/env python3
"""Run the SageMath verifier notebook for a chosen (r, k, h).

Usage:
    python3 scripts/run_parameters.py 2 1 1

The script creates a temporary copy of the notebook with the requested
parameters, executes it with the SageMath Jupyter kernel, and writes generated
artifacts under:

    figures/G_r{r}_k{k}_h{h}/
    matrices/G_r{r}_k{k}_h{h}/
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK = ROOT / "Q_main_G_r_k_h_verifier.ipynb"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Q-main G_{r,k,h} verifier notebook.")
    parser.add_argument("r", type=int, help="Parameter r, with r >= 2.")
    parser.add_argument("k", type=int, help="Parameter k, with k >= 0.")
    parser.add_argument("h", type=int, help="Parameter h, with h >= 0.")
    parser.add_argument(
        "--keep-executed",
        action="store_true",
        help="Keep the executed temporary notebook under executed_notebooks/.",
    )
    return parser.parse_args()


def replace_parameter(source: str, name: str, value: int) -> str:
    pattern = rf"^{name}\s*=\s*.*$"
    replacement = f"{name} = {value}"
    new_source, count = re.subn(pattern, replacement, source, flags=re.M)
    if count != 1:
        raise RuntimeError(f"Could not replace parameter {name!r} in the parameter cell.")
    return new_source


def main() -> int:
    args = parse_args()
    if args.r < 2:
        raise SystemExit("r must be >= 2")
    if args.k < 0 or args.h < 0:
        raise SystemExit("k and h must be >= 0")
    if not NOTEBOOK.exists():
        raise SystemExit(f"Notebook not found: {NOTEBOOK}")
    if shutil.which("sage") is None:
        raise SystemExit("The 'sage' command was not found. Install SageMath and ensure it is on PATH.")

    nb = json.loads(NOTEBOOK.read_text(encoding="utf-8"))
    parameter_cell = nb["cells"][2]
    source = "".join(parameter_cell.get("source", []))
    for name, value in [("r", args.r), ("k", args.k), ("h", args.h)]:
        source = replace_parameter(source, name, value)
    parameter_cell["source"] = source.splitlines(True)

    executed_dir = ROOT / "executed_notebooks"
    tmp = ROOT / f"tmp_run_r{args.r}_k{args.k}_h{args.h}.ipynb"
    out_name = f"Q_main_G_r{args.r}_k{args.k}_h{args.h}_executed.ipynb"
    out_path = executed_dir / out_name
    executed_dir.mkdir(exist_ok=True)
    tmp.write_text(json.dumps(nb, ensure_ascii=False, indent=1), encoding="utf-8")

    try:
        cmd = (
            "jupyter nbconvert --to notebook --execute "
            f"{tmp.name!r} --output {str(out_path)!r} "
            "--ExecutePreprocessor.kernel_name=sagemath "
            "--ExecutePreprocessor.timeout=300"
        )
        print(f"Running notebook for r={args.r}, k={args.k}, h={args.h}", flush=True)
        subprocess.run(["sage", "-sh", "-c", cmd], cwd=ROOT, check=True)
    finally:
        tmp.unlink(missing_ok=True)

    if not args.keep_executed:
        out_path.unlink(missing_ok=True)
        try:
            executed_dir.rmdir()
        except OSError:
            pass

    print(f"Figures:  {ROOT / 'figures' / f'G_r{args.r}_k{args.k}_h{args.h}'}")
    print(f"Matrices: {ROOT / 'matrices' / f'G_r{args.r}_k{args.k}_h{args.h}'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
