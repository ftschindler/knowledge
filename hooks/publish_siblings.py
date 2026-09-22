"""Publish the sibling directories of the bundle, and give the site a landing page.

`docs/` is the OKF bundle root: every non-reserved markdown file in it is a
concept, so a page that describes the site, or one addressed to a reader rather
than carrying knowledge, cannot live there. Those live in sibling directories
outside the bundle, and this hook adds them to the build:

* `about/` describes the site itself.
* `blog/` is the human-facing surface: dated posts saying what changed, linking
  into the concepts that carry the reasoning. Material's blog plugin discovers
  posts by path, and runs its own `on_files` at priority -50 precisely so that
  files injected here are already in the list when it looks. Its entrypoint is
  a stub this hook writes, for the reason given at `_ensure_blog_entrypoint`.

Three consequences follow, all handled here:

* MkDocs serves whichever page lands at the site root, which would be the
  bundle's own `index.md`. That index moves to `/index/` so `about/welcome.md`
  can take the root. Links to it are rewritten automatically, because MkDocs
  resolves relative markdown links through the same file list this edits.
* Edit links are `repo_url + edit_uri + file.edit_uri`, and `edit_uri` points
  into `docs/`. Injected files step back out of it.
* A link from a sibling into the bundle is written as it is true on disk, and
  corrected for the build; see `on_page_markdown`.
"""

from __future__ import annotations

import re
from pathlib import Path

from mkdocs.structure.files import File

SIBLING_DIRS = ("about", "blog")
BUNDLE_DIR = "docs"
BLOG_DIR = "blog"
BLOG_ENTRYPOINT = "# Blog\n\n"
LANDING_PAGE = "welcome.md"
BUNDLE_INDEX_URL = "index/"

# `](../docs/x.md` or `](../../docs/x.md`: any number of steps up, then the
# bundle directory. The capture keeps the steps and the substitution drops the
# directory, which is the whole correction.
INTO_BUNDLE = re.compile(rf"\]\(((?:\.\./)+){BUNDLE_DIR}/")


def on_page_markdown(markdown, page, config, files):
    """Rewrite links from a sibling directory into the bundle.

    On disk a sibling is next to the bundle, so a link into it reads
    `../docs/x.md` from `about/`, or `../../docs/x.md` from `blog/posts/`. That
    is what an editor, Obsidian and GitHub all follow. To MkDocs the sibling
    sits inside the bundle root, where the same targets are `../x.md` and
    `../../x.md`. Authors write the form that is true on disk and this corrects
    it for the build, so one spelling works everywhere.
    """
    if not page.file.src_uri.startswith(tuple(f"{d}/" for d in SIBLING_DIRS)):
        return markdown
    return INTO_BUNDLE.sub(r"](\1", markdown)


def _ensure_blog_entrypoint(files, config):
    """Write the page the blog plugin hangs its post list on.

    The plugin wants `<docs_dir>/<blog_dir>/index.md` and bootstraps a `# Blog`
    stub when it is missing, but that bootstrap does not survive this layout:
    the file it appends is not found by the lookup on the next line, and the
    build dies on a `None`. Writing the stub before the plugin looks, and putting
    it in the file list, avoids that path. A stub written during `on_files` is
    not in the list already, because the source directory was scanned before
    this ran.

    The stub is a build artefact and is gitignored, so the OKF hooks, which read
    what is staged, never see a non-concept inside the bundle directory. It has
    no body on purpose: a blog needs no introduction, and anything written here
    would sit above the post list.
    """
    src_uri = f"{BLOG_DIR}/index.md"
    entrypoint = Path(config.docs_dir) / src_uri
    if not entrypoint.is_file():
        entrypoint.parent.mkdir(parents=True, exist_ok=True)
        entrypoint.write_text(BLOG_ENTRYPOINT, encoding="utf-8")
    if files.get_file_from_path(src_uri) is None:
        files.append(
            File(
                src_uri,
                src_dir=config.docs_dir,
                dest_dir=config.site_dir,
                use_directory_urls=config.use_directory_urls,
            )
        )


def on_files(files, config):
    repo = Path(config.config_file_path).parent

    _ensure_blog_entrypoint(files, config)

    index = files.get_file_from_path("index.md")
    if index is not None:
        index.dest_uri = BUNDLE_INDEX_URL + "index.html"
        index.abs_dest_path = str(Path(config.site_dir) / index.dest_uri)
        index.url = BUNDLE_INDEX_URL

    for directory in SIBLING_DIRS:
        for path in sorted((repo / directory).rglob("*.md")):
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
