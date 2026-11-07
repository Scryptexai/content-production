"""
check_portal.py — verify the brand portal before it is shown to anyone.

Checks, in order:
  1. HTML parses and every element closes.
  2. Every src / href that points into the repository resolves to a real file.
  3. Every referenced raster has a sensible intrinsic size (catches a swapped asset).
  4. No http(s) asset is loaded except the Google Fonts stylesheet (the page must survive offline).

Exit code 1 if anything fails. Run: python3 tools/check_portal.py
"""
import re
import subprocess
import sys
from html.parser import HTMLParser
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PAGE = ROOT / "portal/index.html"

VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta",
        "param", "source", "track", "wbr"}
ALLOWED_REMOTE = ("fonts.googleapis.com", "fonts.gstatic.com")


class Checker(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []
        self.errors = []
        self.refs = []

    def handle_starttag(self, tag, attrs):
        if tag not in VOID:
            self.stack.append((tag, self.getpos()))
        for k, v in attrs:
            if k in ("src", "href") and v:
                self.refs.append((v, self.getpos()))

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        if not self.stack:
            self.errors.append(f"stray </{tag}> at {self.getpos()}")
            return
        open_tag, pos = self.stack.pop()
        if open_tag != tag:
            self.errors.append(f"</{tag}> closes <{open_tag}> opened at {pos}")


def main():
    html = PAGE.read_text()
    c = Checker()
    c.feed(html)
    c.close()

    problems = list(c.errors)
    if c.stack:
        for tag, pos in c.stack:
            problems.append(f"unclosed <{tag}> opened at {pos}")

    checked = remote = 0
    for ref, pos in c.refs:
        if ref.startswith("#"):
            continue
        if ref.startswith("http"):
            host = re.sub(r"^https?://", "", ref).split("/")[0]
            remote += 1
            if host not in ALLOWED_REMOTE:
                problems.append(f"unexpected remote asset {ref} at {pos}")
            continue
        target = (PAGE.parent / ref).resolve()
        checked += 1
        if not target.exists():
            problems.append(f"missing file: {ref} at {pos}")

    # every raster referenced must be a real image with a sane size
    sizes = 0
    for ref, _ in c.refs:
        if ref.startswith(("#", "http")):
            continue
        target = (PAGE.parent / ref).resolve()
        if target.suffix.lower() in (".png", ".jpg", ".gif", ".mp3") and target.exists():
            if target.suffix.lower() == ".mp3":
                out = subprocess.run(["python3", str(HERE / "audio_info.py"), str(target)],
                                     capture_output=True, text=True).stdout.strip()
                if " s " not in out:
                    problems.append(f"audio will not parse: {ref}")
                sizes += 1
                continue
            src = f"{target}[0]" if target.suffix.lower() == ".gif" else str(target)
            w_h = subprocess.run(["identify", "-format", "%w %h", src],
                                 capture_output=True, text=True).stdout.split()
            if len(w_h) != 2 or not all(v.isdigit() for v in w_h):
                problems.append(f"unreadable image: {ref}")
            elif int(w_h[0]) < 8 or int(w_h[1]) < 8:
                problems.append(f"suspicious image size {w_h} for {ref}")
            sizes += 1

    print(f"portal: {PAGE.relative_to(ROOT)}")
    print(f"  local references : {checked}")
    print(f"  remote references: {remote} (fonts only)")
    print(f"  images/audio read: {sizes}")
    if problems:
        print(f"\nFAIL — {len(problems)} problem(s):")
        for p in problems:
            print("  -", p)
        return 1
    print("\nOK — markup closes, every local asset resolves, every image decodes.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
