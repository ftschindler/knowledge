"""Publish `about/`, and give the site a landing page.

`docs/` is the OKF bundle root: every non-reserved markdown file in it is a
concept, so pages that describe the site rather than carry knowledge cannot
live there. They live in `about/` instead, outside the bundle, and this hook
adds them to the build.

Two consequences follow, both handled here:

* MkDocs serves whichever page lands at the site root, which would be the
  bundle's own `index.md`. That index moves to `/index/` so `about/welcome.md`
  can take the root. Links to it are rewritten automatically, because MkDocs
  resolves relative markdown links through the same file list this edits.
* Edit links are `repo_url + edit_uri + file.edit_uri`, and `edit_uri` points
  into `docs/`. Injected files step back out of it.
"""

from __future__ import annotations

from pathlib import Path

from mkdocs.structure.files import File

ABOUT_DIR = "about"
BUNDLE_DIR = "docs"
LANDING_PAGE = "welcome.md"
BUNDLE_INDEX_URL = "index/"


def on_page_markdown(markdown, page, config, files):
    """Rewrite links from `about/` into the bundle so they resolve on the site.

    On disk `about/` is a sibling of the bundle, so a link into it reads
    `../docs/x.md`, which is what an editor, Obsidian and GitHub all follow. To
    MkDocs, `about/` sits inside the bundle root, where the same target is
    `../x.md`. Authors write the form that is true on disk and this corrects it
    for the build, so one spelling works everywhere.
    """
    if not page.file.src_uri.startswith(f"{ABOUT_DIR}/"):
        return markdown
    return markdown.replace(f"](../{BUNDLE_DIR}/", "](../")


def on_files(files, config):
    repo = Path(config.config_file_path).parent

    index = files.get_file_from_path("index.md")
    if index is not None:
        index.dest_uri = BUNDLE_INDEX_URL + "index.html"
        index.abs_dest_path = str(Path(config.site_dir) / index.dest_uri)
        index.url = BUNDLE_INDEX_URL

    for path in sorted((repo / ABOUT_DIR).rglob("*.md")):
        relative = path.relative_to(repo)
        page = File(
            str(relative),
            src_dir=str(repo),
            dest_dir=config.site_dir,
            use_directory_urls=config.use_directory_urls,
        )
        page.edit_uri = f"../{relative}"
        if path.name == LANDING_PAGE:
            page.dest_uri = "index.html"
            page.url = "."
            page.abs_dest_path = str(Path(config.site_dir) / page.dest_uri)
        files.append(page)

    return files
