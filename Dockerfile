FROM nikolaik/python-nodejs:python3.14-nodejs26-slim

# System dependencies. The TeX packages are what `myst build --pdf` needs:
# latexmk drives xelatex, the texlive-* sets cover the packages used by the
# MyST plain_latex template (fontspec, hyperref, listings, ...). fonts-dejavu-core
# provides "DejaVu Sans Mono", which myst.yml sets as the monospace font.
RUN apt-get update && apt-get install -y --no-install-recommends \
    procps \
    latexmk \
    texlive-xetex \
    texlive-latex-recommended \
    texlive-latex-extra \
    texlive-fonts-recommended \
    texlive-lang-german \
    fonts-dejavu-core \
    && rm -rf /var/lib/apt/lists/*

# Install mystmd globally (version pinned to match pyproject.toml dev group)
RUN npm install -g mystmd@1.10.1

# The HTML build does not execute notebooks, so no Python packages are needed yet.
# If notebook execution is added (myst build --execute), install the project
# dependencies here, e.g. via `uv export` to a requirements.txt.
