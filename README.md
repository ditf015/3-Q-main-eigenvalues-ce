# Graphs With Exactly Three Q-main Eigenvalues

This repository contains a SageMath notebook for constructing, verifying, and
visualizing the graph family `G_{r,k,h}`.  The notebook checks the signless
Laplacian matrix `Q`, the first four Q-walk columns

```text
[1, Q1, Q^2 1, Q^3 1],
```

and the number of Q-main eigenvalues.  It also draws the exact graph, its
construction skeleton, and the infinite family schematic for fixed `r,k`.

## Repository Contents

- `Q_main_G_r_k_h_verifier.ipynb`: main SageMath notebook.
- `scripts/run_parameters.py`: command-line runner for a chosen `(r,k,h)`.
- `scripts/run_default.sh`: quick run for `(r,k,h) = (2,0,0)`.
- `figures/G_r*_k*_h*/`: generated graph figures and graph exchange files.
- `matrices/G_r*_k*_h*/`: generated matrix artifacts.

The committed output folders are sample runs produced by the current notebook:

```text
figures/G_r2_k0_h0
figures/G_r2_k0_h1
figures/G_r2_k1_h1
figures/G_r2_k2_h1

matrices/G_r2_k0_h0
matrices/G_r2_k0_h1
matrices/G_r2_k1_h1
matrices/G_r2_k2_h1
```

## Requirements

The notebook is meant to be run with SageMath.

- SageMath 10.x with the Sage Jupyter kernel
- Python 3
- Matplotlib
- NetworkX
- Graphviz, optional but recommended for DOT/SVG exports

On macOS with Homebrew, Graphviz can be installed with:

```bash
brew install graphviz
```

If you use conda/mamba, `environment.yml` records a SageMath-oriented
environment:

```bash
mamba env create -f environment.yml
mamba activate q-main-sage
```

## Run In VSCode

1. Open `Q_main_G_r_k_h_verifier.ipynb`.
2. Select the `SageMath` kernel.
3. Edit `r`, `k`, and `h` in the parameter cell.
4. Run all cells.

For each run, the notebook writes outputs relative to the repository root:

```text
figures/G_r{r}_k{k}_h{h}/
matrices/G_r{r}_k{k}_h{h}/
```

For example, `r=2, k=1, h=1` writes:

```text
figures/G_r2_k1_h1/
matrices/G_r2_k1_h1/
```

## Run From The Command Line

From the repository root:

```bash
python3 scripts/run_parameters.py 2 1 1
```

or run the default sample:

```bash
scripts/run_default.sh
```

The script creates a temporary notebook, executes it with SageMath, removes the
temporary executed notebook by default, and leaves the generated figures and
matrices in the same `figures/` and `matrices/` layout.

To keep the executed notebook for inspection:

```bash
python3 scripts/run_parameters.py 2 1 1 --keep-executed
```

## Matrix Artifacts

Each `matrices/G_r*_k*_h*/` folder contains:

- `Q_signless_laplacian.mtx`: Matrix Market sparse matrix for `Q`.
- `Q_sparse_entries.csv`: sparse coordinate list for `Q`.
- `Q_walk_first_four_columns.csv`: the first four Q-walk columns.
- `vertex_order.csv`: vertex order used by the matrices.
- `matrix_metadata.json`: parameters and verification metadata.
- `README_matrices.md`: short description of the matrix files.

These files are intended to be readable by mathematical software and by AI
tools that need an explicit file-backed representation of the matrix data.

## Figure Artifacts

Each `figures/G_r*_k*_h*/` folder contains:

- `*_compressed_schematic.png/pdf`: paper-style compressed drawing of the
  current graph. This is the default large-graph preview: repeated pendant
  stars and recursive copies are represented by one drawn module plus
  multiplicity labels.
- `*_full_structural.png/pdf`: exact full graph in the structure-aware layout.
  This is only generated when the graph is below the configured exact-layout
  threshold.
- `*_skeleton_structural.png/pdf`: construction skeleton.
- `*_family_h_variable.png/pdf`: schematic for the infinite family with fixed
  `r,k` and varying `h`.
- `*.dot`, `*.gexf`, and `*_sfdp.svg`: Graphviz and Gephi exchange files.

The default drawing for large graphs is the compressed schematic.  It uses the
same visual grammar as graph-theory papers: a visible core, representative
rooted branches, ellipses or boxed recursive copies, and explicit multiplicity
labels.  Exact full-graph DOT/GEXF files are still written for inspection in
Graphviz or Gephi, but Graphviz `sfdp` rendering is disabled by default because
it can run for a long time on graphs with thousands of vertices and does not
produce a paper-style figure.  The notebook prints a proper straight-edge
crossing count for the compressed schematic and for structural drawings that
are generated.

## Does This Run On GitHub?

GitHub will render the notebook and display committed files, but a normal
GitHub repository page does not execute SageMath notebooks automatically.  To
run the code, clone the repository on a machine with SageMath installed and run
the notebook or `scripts/run_parameters.py`.

The generated files always go under:

```text
figures/G_r{r}_k{k}_h{h}/
matrices/G_r{r}_k{k}_h{h}/
```

Those folders can then be committed if you want to publish the new outputs.
They are ignored by default to keep large exploratory runs out of git; use
`git add -f figures/G_r... matrices/G_r...` when you intentionally want to
publish a new parameter run.
