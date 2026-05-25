#!/usr/bin/env python3
"""
Doctor → Markdown converter
Transforms .doctor files to .md for Jekyll/GitHub Pages
"""
import re
import sys
from pathlib import Path

DOCS_DIR = Path("docs")
OUT_DIR = Path("_doctor_md")

def convert_doctor_to_markdown(source):
    """Convert Doctor syntax to Markdown + Jekyll frontmatter."""
    lines = source.split('\n')
    result = []
    i = 0
    
    title = "Documentation"
    nav_items = []
    sidebar_items = []
    
    while i < len(lines):
        line = lines[i].rstrip()
        
        if not line.strip() or line.strip().startswith('//'):
            i += 1
            continue
        
        if line.startswith('title#'):
            title = line[6:].strip()
            i += 1
            continue
        
        if line.startswith('nav#'):
            parts = line[4:].strip().split('|')
            if len(parts) == 2:
                nav_items.append(f"- name: {parts[0].strip()}\n  href: {parts[1].strip()}")
            i += 1
            continue
        
        if line.startswith('sidebar#'):
            parts = line[8:].strip().split('|')
            if len(parts) == 2:
                sidebar_items.append(f"- name: {parts[0].strip()}\n  href: {parts[1].strip()}")
            i += 1
            continue
        
        if line.startswith('hero#'):
            hero_title = line[5:].strip()
            desc = ""
            if i + 1 < len(lines) and lines[i + 1].strip().startswith('desc#'):
                desc = lines[i + 1].strip()[5:].strip()
                i += 1
            result.append(f"# {hero_title}")
            if desc:
                result.append(f"\n> {desc}\n")
            i += 1
            continue
        
        if line.startswith('h1#'):
            result.append(f"# {line[3:].strip()}")
            i += 1
            continue
        if line.startswith('h2#'):
            result.append(f"## {line[3:].strip()}")
            i += 1
            continue
        if line.startswith('h3#'):
            result.append(f"### {line[3:].strip()}")
            i += 1
            continue
        
        if line.startswith('p#'):
            text = line[2:].strip()
            result.append(text)
            i += 1
            continue
        
        if line.startswith('code#'):
            lang = line[5:].strip() or 'text'
            result.append(f"\n```{lang}")
            i += 1
            while i < len(lines) and not lines[i].strip().startswith('end#'):
                result.append(lines[i])
                i += 1
            result.append("```\n")
            i += 1
            continue
        
        if line.startswith('table#'):
            headers = [h.strip() for h in line[6:].strip().split('|')]
            result.append('| ' + ' | '.join(headers) + ' |')
            result.append('|' + '|'.join(['---' for _ in headers]) + '|')
            i += 1
            while i < len(lines) and not lines[i].strip().startswith('end#'):
                row = lines[i].strip()
                if row:
                    cells = [c.strip() for c in row.split('|')]
                    result.append('| ' + ' | '.join(cells) + ' |')
                i += 1
            result.append("")
            i += 1
            continue
        
        if line.startswith('alert#'):
            type_ = line[6:].strip()
            emojis = {'info': 'ℹ️', 'warning': '⚠️', 'success': '✅', 'error': '❌', 'tip': '💡'}
            emoji = emojis.get(type_, 'ℹ️')
            text = ""
            if i + 1 < len(lines):
                text = lines[i + 1].strip()
                if text.startswith('p#'):
                    text = text[2:].strip()
                    i += 1
            result.append(f"> **{emoji} {type_.upper()}**: {text}")
            result.append("")
            i += 1
            continue
        
        if line.startswith('list#'):
            i += 1
            while i < len(lines) and not lines[i].strip().startswith('end#'):
                item = lines[i].rstrip()
                if item.strip().startswith('-'):
                    result.append(item)
                i += 1
            result.append("")
            i += 1
            continue
        
        if line.startswith('card#'):
            title = line[5:].strip()
            desc = ""
            if i + 1 < len(lines) and lines[i + 1].strip().startswith('desc#'):
                desc = lines[i + 1].strip()[5:].strip()
                i += 1
            result.append(f"**{title}**\n\n{desc}")
            result.append("")
            i += 1
            continue
        
        if line.startswith('grid#'):
            i += 1
            while i < len(lines) and not lines[i].strip().startswith('end#'):
                line_inner = lines[i].strip()
                if line_inner.startswith('card#'):
                    title = line_inner[5:].strip()
                    desc = ""
                    if i + 1 < len(lines) and lines[i + 1].strip().startswith('desc#'):
                        desc = lines[i + 1].strip()[5:].strip()
                        i += 1
                    result.append(f"**{title}**\n\n{desc}")
                    result.append("")
                i += 1
            i += 1
            continue
        
        if line.startswith('divider#'):
            result.append("---")
            result.append("")
            i += 1
            continue
        
        if line.startswith('img#'):
            parts = line[4:].strip().split('|')
            src = parts[0].strip()
            alt = parts[1].strip() if len(parts) > 1 else ""
            result.append(f"![{alt}]({src})")
            result.append("")
            i += 1
            continue
        
        i += 1
    
    frontmatter = ["---", f'title: "{title}"', "layout: doctor"]
    if nav_items:
        frontmatter.append("nav:")
        frontmatter.extend(["  " + n for n in nav_items])
    if sidebar_items:
        frontmatter.append("sidebar:")
        frontmatter.extend(["  " + s for s in sidebar_items])
    frontmatter.append("---\n")
    
    return "\n".join(frontmatter + result)


def convert_all():
    DOCS_DIR.mkdir(exist_ok=True)
    OUT_DIR.mkdir(exist_ok=True)
    
    doctor_files = list(DOCS_DIR.glob('*.doctor'))
    if not doctor_files:
        default = DOCS_DIR / 'index.doctor'
        default.write_text("""title# Welcome to Doctor

hero# Doctor
 desc# Your documentation site is live.

h2# Getting Started

p# Edit `docs/index.doctor` to customize this page.

alert#info
 p# This is a default page generated because no content was found.
""")
        doctor_files = [default]
    
    for doctor_file in sorted(doctor_files):
        print(f"Converting: {doctor_file.name}")
        source = doctor_file.read_text(encoding='utf-8')
        markdown = convert_doctor_to_markdown(source)
        
        output_file = OUT_DIR / doctor_file.with_suffix('.md').name
        output_file.write_text(markdown, encoding='utf-8')
        print(f"  -> {output_file}")
    
    # Copy index.md to root for Jekyll
    index_md = OUT_DIR / 'index.md'
    if index_md.exists():
        root_index = Path('index.md')
        root_index.write_text(index_md.read_text(encoding='utf-8'), encoding='utf-8')
        print(f"  -> Copied to {root_index}")


if __name__ == '__main__':
    convert_all()
    print("\nDone. Markdown files ready for Jekyll.")
