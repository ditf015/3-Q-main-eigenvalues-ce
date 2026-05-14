# Matrix artifacts for G_{r,k,h}

Parameters: `r=2`, `k=1`, `h=0`.

`Q` has shape `192 x 192` and `576` nonzero entries.
`W4=[1,Q1,Q^2 1,Q^3 1]` has shape `192 x 4`.

Files:
- `Q_signless_laplacian.mtx`: Matrix Market sparse coordinate representation of Q.
- `Q_sparse_entries.csv`: sparse coordinate table with row/column vertex labels.
- `Q_walk_first_four_columns.csv`: the four Q-walk columns, one vertex per row.
- `vertex_order.csv`: row/column order used by Q and W4.
- `matrix_metadata.json`: parameters, dimensions, recurrence, and Q-main eigenvalue summary.

A reader can reconstruct Q from either the Matrix Market file or the sparse CSV using `vertex_order.csv`.
