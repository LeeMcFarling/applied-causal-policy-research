# Assets — GovOps brief

Expected figure files for `../govops-rmc-tech-layer.md`, per the figure convention in
`AI_Integrations/YAML_FRONTMATTER_GUIDE.md` (`./assets/<name>.svg|png`, referenced as
`![Figure N: caption](./assets/<name>.png)`). Drop files in here using these exact names
and the markdown file will pick them up with no further edits.

| Filename | Figure | Content |
|---|---|---|
| `figure-1-repository-organization.png` | 1 | Repository organization — jurisdiction/policy-domain directories resolving to regulatory objects |
| `figure-3-clause-to-step-resolution.png` | 3 | Clause-to-step resolution diagram (California Density Bonus Law example) |
| `figure-4-cross-jurisdictional-workflows.png` | 4 | Four-jurisdiction workflow comparison (CA/CO/CT/TX) |
| `figure-5-efficient-frontier.png` | 5 | Permitting timeline vs. Protective Outcomes Index, efficient frontier |
| `figure-6-workflow-observability.png` | 6 | Workflow object connected to operational systems via API |
| `figure-7-amendment-diff.png` | 7 | Legal amendment + resulting workflow diff |
| `figure-8b-jurisdiction-pca-projection.png` | 8b | 2D PCA projection of jurisdiction feature space |
| `figure-9-treatment-control-map.png` | 9 | Geographic treatment/control assignment map (Colorado) |
| `figure-10-difference-in-differences.png` | 10 | DiD design, Longmont vs. Loveland |
| `figure-11-regression-discontinuity.png` | 11 | RD design at a jurisdictional boundary |

Not included: Figure 2 (YAML schema) and Figure 8a (feature matrix) — both are already
rendered directly as a code block and a markdown table in the brief, so no image is needed
for either.

SVG works too if that's the source format — `export-brief.py` converts SVG to PNG via
Chrome headless at export time, same as the rest of the repo's figures.
