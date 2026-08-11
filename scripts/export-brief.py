#!/usr/bin/env python3
"""
Export a policy brief to PDF.

Usage:
    python3 scripts/export-brief.py path/to/brief.md
    python3 scripts/export-brief.py path/to/brief.md -o output.pdf
    python3 scripts/export-brief.py path/to/brief.md --open

Handles:
  - Docusaurus YAML → pandoc YAML mapping
  - SVG figures → PNG via Chrome headless
  - HTML figures → PNG companion lookup (brief.html → brief.png)
"""

import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

CHROME = (
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
)
TEMPLATE = Path(__file__).parent / "templates" / "policy-brief.tex"
REPO_ROOT = Path(__file__).parent.parent

# Docusaurus YAML fields that pandoc should ignore (strip from temp file)
STRIP_FIELDS = {
    "id", "sidebar_label", "sidebar_position", "slug",
    "tags", "dependencies", "related_initiatives", "linked_policies",
    "policy_type", "subdomain",
}

# Fields to rename so pandoc/template can use them
REMAP_FIELDS = {
    "last_updated": "date",
    "description": "description",  # keep as-is; template uses $description$
}


def chrome_render(src: Path, out_png: Path, width=1400, height=900):
    """Render an HTML or SVG file to PNG using Chrome headless."""
    url = src.as_uri() if src.suffix == ".svg" else src.as_uri()
    subprocess.run([
        CHROME,
        "--headless=new",
        "--disable-gpu",
        "--hide-scrollbars",
        f"--screenshot={out_png}",
        f"--window-size={width},{height}",
        "--default-background-color=ffffff",
        url,
    ], check=True, capture_output=True)


def preprocess_markdown(src: Path, tmp_dir: Path) -> Path:
    """
    Return path to a preprocessed .md in tmp_dir, ready for pandoc:
    - Strip Docusaurus-only YAML fields
    - Map last_updated → date
    - Convert SVG img refs → PNG (rendering via Chrome if needed)
    - Swap HTML iframe/src refs → PNG companion
    """
    content = src.read_text(encoding="utf-8")
    src_dir = src.parent

    # ── YAML frontmatter processing ───────────────────────────────────────────
    yaml_match = re.match(r"^---\n(.*?)\n---\n", content, re.DOTALL)
    if yaml_match:
        yaml_block = yaml_match.group(1)
        body = content[yaml_match.end():]

        lines = yaml_block.split("\n")
        filtered = []
        skip_next = False
        for line in lines:
            if skip_next:
                if line.startswith("  ") or line.startswith("- "):
                    continue
                skip_next = False

            field_match = re.match(r"^(\w+):", line)
            if field_match:
                field = field_match.group(1)
                if field in STRIP_FIELDS:
                    skip_next = True
                    continue
                if field == "last_updated":
                    line = re.sub(r"^last_updated:", "date:", line)
            filtered.append(line)

        content = "---\n" + "\n".join(filtered) + "\n---\n" + body

    # ── Figure processing ─────────────────────────────────────────────────────
    figures_dir = tmp_dir / "figures"
    figures_dir.mkdir(exist_ok=True)

    def handle_svg(match):
        alt = match.group(1)
        rel_path = match.group(2)
        svg_path = (src_dir / rel_path).resolve()

        if not svg_path.exists():
            return match.group(0)  # leave as-is if file not found

        png_path = figures_dir / (svg_path.stem + ".png")
        if not png_path.exists():
            try:
                chrome_render(svg_path, png_path)
            except Exception as e:
                print(f"  Warning: could not render {svg_path.name}: {e}",
                      file=sys.stderr)
                return match.group(0)

        return f"![{alt}]({png_path})"

    # Replace SVG image references
    content = re.sub(
        r"!\[([^\]]*)\]\(([^)]+\.svg)\)",
        handle_svg,
        content,
    )

    # Replace HTML iframe src → PNG companion
    def handle_html_iframe(match):
        html_ref = match.group(1)
        html_path = (src_dir / html_ref).resolve()
        png_candidate = html_path.with_suffix(".png")

        if png_candidate.exists():
            rel = png_candidate.relative_to(src_dir)
            # Replace the entire iframe block with a markdown image
            return f"![Figure]({png_candidate})"
        else:
            print(f"  Warning: no PNG companion for {html_path.name} — "
                  f"figure omitted in PDF. Generate {png_candidate.name} "
                  f"to include it.", file=sys.stderr)
            return f"*[Interactive figure: {html_path.name} — view in browser]*"

    # Match both <iframe src="..."> and src="*.html" patterns
    content = re.sub(
        r'<iframe[^>]+src=["\']([^"\']+\.html)["\'][^>]*>.*?</iframe>',
        handle_html_iframe,
        content,
        flags=re.DOTALL | re.IGNORECASE,
    )

    # Also handle plain markdown image refs pointing to .html
    def handle_html_img(match):
        alt = match.group(1)
        html_ref = match.group(2)
        html_path = (src_dir / html_ref).resolve()
        png_candidate = html_path.with_suffix(".png")
        if png_candidate.exists():
            return f"![{alt}]({png_candidate})"
        return f"*[Interactive figure: {html_path.name} — view in browser]*"

    content = re.sub(
        r"!\[([^\]]*)\]\(([^)]+\.html)\)",
        handle_html_img,
        content,
    )

    # Copy any local PNG/JPG assets so relative paths resolve from tmp_dir
    def copy_local_asset(match):
        alt = match.group(1)
        rel = match.group(2)
        if rel.startswith("http"):
            return match.group(0)
        asset_path = (src_dir / rel).resolve()
        if asset_path.exists():
            dest = figures_dir / asset_path.name
            shutil.copy2(asset_path, dest)
            return f"![{alt}]({dest})"
        return match.group(0)

    content = re.sub(
        r"!\[([^\]]*)\]\(([^)]+\.(?:png|jpg|jpeg|gif|pdf))\)",
        copy_local_asset,
        content,
    )

    out_md = tmp_dir / src.name
    out_md.write_text(content, encoding="utf-8")
    return out_md


def export(src: Path, output: Path, open_after: bool = False):
    print(f"Exporting: {src.name}")

    with tempfile.TemporaryDirectory() as tmp:
        tmp_dir = Path(tmp)
        processed = preprocess_markdown(src, tmp_dir)

        cmd = [
            "pandoc",
            str(processed),
            "--pdf-engine=xelatex",
            f"--template={TEMPLATE}",
            "--resource-path=" + str(tmp_dir / "figures") + ":" + str(src.parent),
            "-V", "graphics=true",
            "-o", str(output),
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode != 0:
            print(f"  Error:\n{result.stderr}", file=sys.stderr)
            sys.exit(1)

    print(f"  → {output}")

    if open_after:
        subprocess.run(["open", str(output)])


def main():
    parser = argparse.ArgumentParser(
        description="Export a policy brief to PDF"
    )
    parser.add_argument("input", help="Path to .md brief")
    parser.add_argument("-o", "--output", help="Output PDF path")
    parser.add_argument("--open", action="store_true",
                        help="Open PDF after export")
    args = parser.parse_args()

    src = Path(args.input).resolve()
    if not src.exists():
        print(f"File not found: {src}", file=sys.stderr)
        sys.exit(1)

    if args.output:
        output = Path(args.output).resolve()
    else:
        output = src.with_suffix(".pdf")

    export(src, output, open_after=args.open)


if __name__ == "__main__":
    main()
