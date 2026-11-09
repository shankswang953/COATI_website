"""Render tutorial copies from a COATI checkout without executing its notebooks."""
import argparse
from pathlib import Path
import subprocess
import nbformat


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--package-root", type=Path, required=True,
                        help="Path to the separate COATI package checkout")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    package = args.package_root.resolve()
    if not (package / "notebooks").is_dir():
        parser.error(f"No notebooks directory in {package}")
    out = root / "docs/tutorials"
    out.mkdir(parents=True, exist_ok=True)
    if (package / ".git").exists():
        tracked = subprocess.run(
            ["git", "ls-files", "-z", "--", "notebooks/*.ipynb", "notebooks/**/*.ipynb"],
            cwd=package, check=True, capture_output=True,
        ).stdout.decode().split("\0")
        sources = [package / name for name in tracked if name]
    else:
        sources = list((package / "notebooks").rglob("*.ipynb"))
    for source in sorted(sources):
        relative = source.relative_to(package / "notebooks")
        if any(part.startswith(".") or part in {"outputs", "_build"} for part in relative.parts):
            continue
        if source.stem in {"02_paired", "05_velocity"}:
            continue  # Their stable web URLs point to the consolidated comparison.
        notebook = nbformat.read(source, as_version=4)
        # Keep web titles short and retain all code and scientific outputs.
        titles = {"00_introduction": "Introduction", "01_gaussian": "Gaussian toy: sync vs no sync", "02_paired": "Paired modalities",
                  "03_split": "Splitting and growth", "04_inputs": "Input adapters",
                  "05_velocity": "Vector fields and UMAP velocity",
                  "06_heldout_biological": "Held-out biological reconstruction",
                  "07_dynamics": "Gastrulation dynamics and mass",
                  "08_map_quality": "Train and inspect a cross-modal map",
                  "09_lineage_features": "Lineage gene and peak dynamics",
                  "mouseGastrulation": "Mouse gastrulation",
                  "pretrainedModels": "Pretrained full-data models",
                  "heldoutDistribution": "Held-out distribution reconstruction",
                  "11_gaussian_reference": "Original Gaussian experiment",
                  "balancedGaussianbump": "Balanced Gaussian bump",
                  "unbalancedGaussianbump": "Unbalanced Gaussian bump",
                  "cyComparison": "Cy comparison",
                  "BranchSync": "BranchSync"}
        if notebook.cells and notebook.cells[0].cell_type == "markdown":
            first = notebook.cells[0].source.splitlines()
            first[0] = "# " + titles.get(source.stem, first[0].lstrip("# "))
            notebook.cells[0].source = "\n".join(first)
        for cell in notebook.cells:
            if cell.cell_type == "code":
                # Optional widget availability does not affect tutorial results.
                cell.outputs = [output for output in cell.get("outputs", [])
                                if not (output.output_type == "stream"
                                        and output.get("name") == "stderr"
                                        and "IProgress not found" in output.get("text", ""))]
        # Keep canonical documentation links on the separately hosted website.
        for cell in notebook.cells:
            if cell.cell_type == "markdown":
                cell.source = cell.source.replace(
                    "https://shankswang953.github.io/COATI/",
                    "https://shankswang953.github.io/COATI_website/",
                )
        # MyST-NB renders each notebook within the documentation theme.
        destination = out / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        nbformat.write(notebook, destination)
        print(relative.as_posix())


if __name__ == "__main__":
    main()
