"""Publish the sibling directories of the bundle, and give the site a landing page.

`docs/` is the OKF bundle root: every non-reserved markdown file in it is a
concept, so a page that describes the site, or one addressed to a reader rather
than carrying knowledge, cannot live there. Those live in sibling directories
outside the bundle, and this hook adds them to the build:

* `about/` describes the site itself.
* `blog/` is the human-facing surface: dated posts saying what changed, linking
  into the concepts that carry the reasoning. Material's blog plugin discovers
  posts by path, and runs its own `on_files` at priority -50 precisely so that
  files injected here are already in the list when it looks.

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


def _mirror_blog_entrypoint(repo, config):
    """Put the blog's entrypoint where the blog plugin insists on looking.

    The plugin resolves `<docs_dir>/<blog_dir>/index.md` against the filesystem
    rather than against the file list, and writes a `# Blog` stub when it finds
    nothing. That stub would then replace the injected entrypoint, so the blog
    would lose its own landing text. Mirroring the sibling's copy there first
    makes the check pass and leaves the source of truth in `blog/index.md`.

    The mirror is a build artefact and is gitignored. It is the one file this
    layout has to put inside the bundle directory, and it is never committed,
    so the OKF hooks, which read what is staged, never see it.
    """
    source = repo / BLOG_DIR / "index.md"
    if not source.is_file():
        return
    mirror = Path(config.docs_dir) / BLOG_DIR / "index.md"
    mirror.parent.mkdir(parents=True, exist_ok=True)
    content = source.read_text(encoding="utf-8")
    if not mirror.is_file() or mirror.read_text(encoding="utf-8") != content:
        mirror.write_text(content, encoding="utf-8")


def on_files(files, config):
    repo = Path(config.config_file_path).parent

    index = files.get_file_from_path("index.md")
    if index is not None:
        index.dest_uri = BUNDLE_INDEX_URL + "index.html"
        index.abs_dest_path = str(Path(config.site_dir) / index.dest_uri)
        index.url = BUNDLE_INDEX_URL

    _mirror_blog_entrypoint(repo, config)

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
            # The mirrored entrypoint is scanned in from the bundle directory,
            # so the injected copy would be a second file at the same address.
            existing = files.get_file_from_path(page.src_uri)
            if existing is not None:
                files.remove(existing)
            files.append(page)

    return files
