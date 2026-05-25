import sys
from pathlib import Path

DOCS_DIR = Path("docs")
OUT_DIR = Path("_doctor_md")

def convert_file(filepath):
    lines = filepath.read_text(encoding="utf-8").splitlines()
    out = []
    i = 0
    title = "Documentation"
    sidebar = []

    while i < len(lines):
        line = lines[i].strip()
        if not line or line.startswith("//"):
            i += 1
            continue

        if line.startswith("title#"):
            title = line[6:].strip()
            i += 1
            continue

        if line.startswith("sidebar#"):
            parts = line[8:].split("|")
            if len(parts) == 2:
                sidebar.append((parts[0].strip(), parts[1].strip()))
            i += 1
            continue

        if line.startswith("hero#"):
            out.append("# " + line[5:].strip())
            if i + 1 < len(lines) and lines[i+1].strip().startswith("desc#"):
                out.append("> " + lines[i+1].strip()[5:].strip())
                i += 1
            i += 1
            continue

        if line.startswith("h1#"):
            out.append("# " + line[3:].strip())
            i += 1
            continue
        if line.startswith("h2#"):
            out.append("## " + line[3:].strip())
            i += 1
            continue
        if line.startswith("h3#"):
            out.append("### " + line[3:].strip())
            i += 1
            continue

        if line.startswith("p#"):
            out.append(line[2:].strip())
            i += 1
            continue

        if line.startswith("code#"):
            lang = line[5:].strip() or "text"
            out.append("")
            out.append("```" + lang)
            i += 1
            while i < len(lines) and not lines[i].strip().startswith("end#"):
                out.append(lines[i])
                i += 1
            out.append("```")
            out.append("")
            i += 1
            continue

        if line.startswith("table#"):
            headers = [h.strip() for h in line[6:].split("|")]
            out.append("| " + " | ".join(headers) + " |")
            out.append("|" + "|".join(["---" for _ in headers]) + "|")
            i += 1
            while i < len(lines) and not lines[i].strip().startswith("end#"):
                row = lines[i].strip()
                if row:
                    cells = [c.strip() for c in row.split("|")]
                    out.append("| " + " | ".join(cells) + " |")
                i += 1
            out.append("")
            i += 1
            continue

        if line.startswith("alert#"):
            typ = line[6:].strip()
            emojis = {"info":"ℹ️","warning":"⚠️","success":"✅","error":"❌","tip":"💡"}
            emoji = emojis.get(typ, "ℹ️")
            text = ""
            if i + 1 < len(lines):
                nxt = lines[i+1].strip()
                if nxt.startswith("p#"):
                    text = nxt[2:].strip()
                    i += 1
            out.append("> **" + emoji + " " + typ.upper() + "**: " + text)
            out.append("")
            i += 1
            continue

        if line.startswith("list#"):
            i += 1
            while i < len(lines) and not lines[i].strip().startswith("end#"):
                item = lines[i].strip()
                if item.startswith("-"):
                    out.append(item)
                i += 1
            out.append("")
            i += 1
            continue

        if line.startswith("card#"):
            title = line[5:].strip()
            desc = ""
            if i + 1 < len(lines) and lines[i+1].strip().startswith("desc#"):
                desc = lines[i+1].strip()[5:].strip()
                i += 1
            out.append("**" + title + "**")
            out.append("")
            out.append(desc)
            out.append("")
            i += 1
            continue

        if line.startswith("grid#"):
            i += 1
            while i < len(lines) and not lines[i].strip().startswith("end#"):
                inner = lines[i].strip()
                if inner.startswith("card#"):
                    t = inner[5:].strip()
                    d = ""
                    if i + 1 < len(lines) and lines[i+1].strip().startswith("desc#"):
                        d = lines[i+1].strip()[5:].strip()
                        i += 1
                    out.append("**" + t + "**")
                    out.append("")
                    out.append(d)
                    out.append("")
                i += 1
            i += 1
            continue

        if line.startswith("divider#"):
            out.append("---")
            out.append("")
            i += 1
            continue

        if line.startswith("img#"):
            parts = line[4:].split("|")
            src = parts[0].strip()
            alt = parts[1].strip() if len(parts) > 1 else ""
            out.append("![" + alt + "](" + src + ")")
            out.append("")
            i += 1
            continue

        i += 1

    # Frontmatter
    fm = ["---", 'title: "' + title + '"', "layout: doctor"]
    if sidebar:
        fm.append("sidebar:")
        for name, href in sidebar:
            fm.append('  - name: "' + name + '"')
            fm.append('    href: "' + href + '"')
    fm.append("---")
    fm.append("")

    return "\n".join(fm + out)


def main():
    DOCS_DIR.mkdir(exist_ok=True)
    OUT_DIR.mkdir(exist_ok=True)

    files = list(DOCS_DIR.glob("*.doctor"))
    if not files:
        default = DOCS_DIR / "index.doctor"
        default.write_text('title# Welcome\n\nhero# Doctor\n desc# Your site is live.\n\nh2# Start Here\n\np# Edit docs/index.doctor to customize.\n', encoding="utf-8")
        files = [default]

    for f in sorted(files):
        print("Converting: " + f.name)
        md = convert_file(f)
        out = OUT_DIR / f.with_suffix(".md").name
        out.write_text(md, encoding="utf-8")
        print("  -> " + str(out))

    # Copy ALL converted .md files to docs/ folder so they don't overwrite root index.html
    docs_output = Path("docs")
    docs_output.mkdir(exist_ok=True)
    for md_file in OUT_DIR.glob("*.md"):
        dest = docs_output / md_file.name
        dest.write_text(md_file.read_text(encoding="utf-8"), encoding="utf-8")
        print("  -> copied to " + str(dest))

    print("Done.")


if __name__ == "__main__":
    main()
