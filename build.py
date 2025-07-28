#!/usr/bin/env python3
import json
import pathlib
import shutil
from jinja2 import Environment, FileSystemLoader, select_autoescape


ROOT = pathlib.Path(__file__).parent
TEMPLATES = ROOT / "templates"
DIST = ROOT / "dist"

def get_pages():
    pages = {}
    pages_dir = TEMPLATES / "pages"
    for file in pages_dir.glob("*.html"):
        template_path = f"pages/{file.name}"
        output_file = file.name
        pages[template_path] = output_file
    return pages

PAGES = get_pages()


def main() -> None:
    # set up Jinja environment
    env = Environment(
        loader=FileSystemLoader(TEMPLATES),
        autoescape=select_autoescape(["html"])
    )
    
    # start fresh each run
    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir()
    
    # copy static assets
    if (ROOT / "css").exists():
        shutil.copytree(ROOT / "css", DIST / "css")
    if (ROOT / "img").exists():
        shutil.copytree(ROOT / "img", DIST / "img")
    if (ROOT / "js").exists():
        shutil.copytree(ROOT / "js", DIST / "js")
    if (ROOT / "favicon.ico").exists():
        shutil.copy(ROOT / "favicon.ico", DIST / "favicon.ico")
    if (ROOT / "CNAME").exists():
        shutil.copy(ROOT / "CNAME", DIST / "CNAME")
    else:
        raise FileNotFoundError("CNAME file not found. Please create a CNAME file in the root directory.")
    
    # load data
    with open(ROOT / "data/leaderboards.json", "r") as f:
        leaderboards = json.load(f)
    with open(ROOT / "data/press.json", "r") as f:
        press = json.load(f)
        press = sorted(press, key=lambda x: x["date"], reverse=True)
    
    # Collect all unique tags
    all_tags = set()
    for leaderboard in leaderboards["leaderboards"] if isinstance(leaderboards, dict) else leaderboards:
        for entry in leaderboard["results"]:
            if "tags" in entry and entry["tags"]:
                all_tags.update(entry["tags"])
    all_tags = sorted(set(list(all_tags)))
    
    # render all pages
    for tpl_name, out_name in PAGES.items():
        tpl = env.get_template(tpl_name)
        html = tpl.render(
            title="Nocode-bench", 
            leaderboards=leaderboards["leaderboards"] if isinstance(leaderboards, dict) else leaderboards,
            press=press,
            all_tags=all_tags,
        )
        (DIST / out_name).write_text(html)
        print(f"built {out_name}")
    
    print("All pages generated successfully!")


if __name__ == "__main__":
    main()
