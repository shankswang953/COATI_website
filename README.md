# COATI website

[Website](https://shankswang953.github.io/COATI_website/) · [Tutorials](https://shankswang953.github.io/COATI_website/tutorials.html) · [COATI package](https://github.com/shankswang953/COATI)

This repository owns the COATI documentation website, its static assets,
animation source and GitHub Pages deployment. The installable Python package,
experiments and executable tutorial notebooks are maintained in the separate
[COATI](https://github.com/shankswang953/COATI) repository.

## Structure

```text
docs/                 Website pages and saved tutorial outputs
assets/               Logo, overview figures and videos
animations/           Reusable animation source
scripts/              Website build and notebook-copy helpers
requirements.txt      Website-only build dependencies
package-ref.txt       COATI commit used for the API and notebook content
.github/workflows/    Public GitHub Pages deployment
```

## Local preview

Keep the two checkouts next to each other:

```bash
git clone https://github.com/shankswang953/COATI.git
git clone https://github.com/shankswang953/COATI_website.git
cd COATI_website
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ../COATI
python -m pip install -r requirements.txt
python scripts/build_website.py --serve
```

Open <http://127.0.0.1:8000/>. HTML is generated under `docs/_build/html/`.
Use `--package-root /path/to/COATI` when the checkouts are not siblings.
The build copies saved notebook outputs and renders the API documentation;
it does not execute notebook cells or run any training.

## Publication

Push changes to this repository's `main` branch to publish the website.
The **Publish documentation** workflow installs the COATI revision recorded in
`package-ref.txt`, then builds and deploys the public site. No OpenAI account is
required to view it. Changes in the package repository do not publish a website.

To refresh package documentation, update `package-ref.txt` to the desired COATI
commit and rebuild with the matching package checkout. Commit the refreshed
`docs/tutorials/` copies here alongside any prose changes.
