import re
from pathlib import Path

class Doctor:
    def __init__(self):
        self.components = []
        self.title = "Documentation"
        self.nav_items = []
        self.sidebar_items = []

    def parse(self, source):
        lines = source.split('\n')
        i = 0
        while i < len(lines):
            line = lines[i].strip()

            if not line or line.startswith('//'):
                i += 1
                continue

            if line.startswith('title#'):
                self.title = line[6:].strip()
                i += 1
                continue

            if line.startswith('nav#'):
                parts = line[4:].strip().split('|')
                if len(parts) == 2:
                    self.nav_items.append({'text': parts[0].strip(), 'href': parts[1].strip()})
                i += 1
                continue

            if line.startswith('sidebar#'):
                parts = line[8:].strip().split('|')
                if len(parts) == 2:
                    self.sidebar_items.append({'text': parts[0].strip(), 'href': parts[1].strip()})
                i += 1
                continue

            if line.startswith('hero#'):
                title = line[5:].strip()
                desc = ""
                if i + 1 < len(lines) and lines[i + 1].strip().startswith('desc#'):
                    desc = lines[i + 1].strip()[5:].strip()
                    i += 1
                self.components.append(self._hero(title, desc))
                i += 1
                continue

            if line.startswith('h1#'):
                self.components.append(self._heading(line[3:].strip(), 1))
                i += 1
                continue
            if line.startswith('h2#'):
                self.components.append(self._heading(line[3:].strip(), 2))
                i += 1
                continue
            if line.startswith('h3#'):
                self.components.append(self._heading(line[3:].strip(), 3))
                i += 1
                continue

            if line.startswith('p#'):
                text = line[2:].strip()
                text = re.sub(r'`([^`]+)`', r'<code>\1</code>', text)
                text = re.sub(r'\*\*([^\*]+)\*\*', r'<strong>\1</strong>', text)
                text = re.sub(r'\*([^*]+)\*', r'<em>\1</em>', text)
                text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', text)
                self.components.append(f'<p>{text}</p>')
                i += 1
                continue

            if line.startswith('code#'):
                lang = line[5:].strip() or 'text'
                code_lines = []
                i += 1
                while i < len(lines) and not lines[i].strip().startswith('end#'):
                    code_lines.append(lines[i])
                    i += 1
                code_content = '\n'.join(code_lines)
                code_content = code_content.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
                self.components.append(f'<pre><code class="language-{lang}">{code_content}</code></pre>')
                i += 1
                continue

            if line.startswith('table#'):
                headers = [h.strip() for h in line[6:].strip().split('|')]
                rows = []
                i += 1
                while i < len(lines) and not lines[i].strip().startswith('end#'):
                    row = lines[i].strip()
                    if row:
                        rows.append([c.strip() for c in row.split('|')])
                    i += 1
                self.components.append(self._table(headers, rows))
                i += 1
                continue

            if line.startswith('alert#'):
                type_ = line[6:].strip()
                text = ""
                if i + 1 < len(lines):
                    text = lines[i + 1].strip()
                    if text.startswith('p#'):
                        text = text[2:].strip()
                        i += 1
                self.components.append(self._alert(type_, text))
                i += 1
                continue

            if line.startswith('list#'):
                items = []
                i += 1
                while i < len(lines) and not lines[i].strip().startswith('end#'):
                    item = lines[i].strip()
                    if item.startswith('-'):
                        items.append(item[1:].strip())
                    i += 1
                self.components.append(self._list(items))
                i += 1
                continue

            if line.startswith('card#'):
                title = line[5:].strip()
                desc = ""
                if i + 1 < len(lines) and lines[i + 1].strip().startswith('desc#'):
                    desc = lines[i + 1].strip()[5:].strip()
                    i += 1
                self.components.append(self._card(title, desc))
                i += 1
                continue

            if line.startswith('grid#'):
                cols = int(line[5:].strip() or 2)
                cards = []
                i += 1
                while i < len(lines) and not lines[i].strip().startswith('end#'):
                    line_inner = lines[i].strip()
                    if line_inner.startswith('card#'):
                        card_title = line_inner[5:].strip()
                        card_desc = ""
                        if i + 1 < len(lines) and lines[i + 1].strip().startswith('desc#'):
                            card_desc = lines[i + 1].strip()[5:].strip()
                            i += 1
                        cards.append({'title': card_title, 'desc': card_desc})
                    i += 1
                self.components.append(self._grid(cards, cols))
                i += 1
                continue

            if line.startswith('divider#'):
                self.components.append('<hr>')
                i += 1
                continue

            if line.startswith('img#'):
                parts = line[4:].strip().split('|')
                src = parts[0].strip()
                alt = parts[1].strip() if len(parts) > 1 else ""
                self.components.append(f'<img src="{src}" alt="{alt}" style="max-width:100%;border-radius:8px;">')
                i += 1
                continue

            i += 1

        return self._build_html()

    def _hero(self, title, desc):
        return f'<div class="hero"><h1>{title}</h1><p>{desc}</p></div>'

    def _heading(self, text, level):
        anchor = re.sub(r'[^\w\s-]', '', text).strip().replace(' ', '-').lower()
        return f'<h{level} id="{anchor}">{text}</h{level}>'

    def _table(self, headers, rows):
        ths = ''.join([f'<th>{h}</th>' for h in headers])
        trs = ''
        for row in rows:
            tds = ''.join([f'<td>{c}</td>' for c in row])
            trs += f'<tr>{tds}</tr>'
        return f'<table><thead><tr>{ths}</tr></thead><tbody>{trs}</tbody></table>'

    def _alert(self, type_, text):
        icons = {'info': '&#8505;', 'warning': '&#9888;', 'success': '&#9989;', 'error': '&#10060;', 'tip': '&#128161;'}
        icon = icons.get(type_, '&#8505;')
        return f'<div class="alert alert-{type_}"><span class="alert-icon">{icon}</span><span>{text}</span></div>'

    def _list(self, items):
        lis = ''.join([f'<li>{item}</li>' for item in items])
        return f'<ul>{lis}</ul>'

    def _card(self, title, desc):
        return f'<div class="card"><h3>{title}</h3><p>{desc}</p></div>'

    def _grid(self, cards, cols):
        cards_html = ''.join([self._card(c['title'], c['desc']) for c in cards])
        return f'<div class="grid grid-cols-{cols}">{cards_html}</div>'

    def _build_html(self):
        nav_html = ''
        if self.nav_items:
            links = ''.join([f'<a href="{n["href"]}">{n["text"]}</a>' for n in self.nav_items])
            nav_html = f'<nav class="top-nav"><div class="nav-brand">{self.title}</div><div class="nav-links">{links}</div></nav>'

        sidebar_html = ''
        if self.sidebar_items:
            links = ''.join([f'<a href="{s["href"]}">{s["text"]}</a>' for s in self.sidebar_items])
            sidebar_html = f'<aside class="sidebar"><div class="sidebar-content">{links}</div></aside>'

        content = '\n'.join(self.components)

        theme_css = """
        :root { --bg: #ffffff; --text: #1a1a2e; --muted: #6b7280; --border: #e5e7eb; --primary: #3b82f6; --primary-light: #eff6ff; --code-bg: #f3f4f6; --sidebar-bg: #f9fafb; --card-bg: #ffffff; --shadow: 0 1px 3px rgba(0,0,0,0.1); }
        @media (prefers-color-scheme: dark) { :root { --bg: #0f172a; --text: #e2e8f0; --muted: #94a3b8; --border: #1e293b; --primary: #60a5fa; --primary-light: #1e293b; --code-bg: #1e293b; --sidebar-bg: #1e293b; --card-bg: #1e293b; --shadow: 0 1px 3px rgba(0,0,0,0.3); } }
        """

        css = f"""
        <style>
        {theme_css}
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: var(--bg); color: var(--text); line-height: 1.6; }}
        .top-nav {{ position: fixed; top: 0; left: 0; right: 0; height: 60px; background: var(--bg); border-bottom: 1px solid var(--border); display: flex; align-items: center; justify-content: space-between; padding: 0 2rem; z-index: 100; }}
        .nav-brand {{ font-weight: 700; font-size: 1.25rem; color: var(--primary); }}
        .nav-links {{ display: flex; gap: 1.5rem; }}
        .nav-links a {{ color: var(--text); text-decoration: none; font-size: 0.9rem; }}
        .nav-links a:hover {{ color: var(--primary); }}
        .layout {{ display: flex; min-height: 100vh; padding-top: 60px; }}
        .sidebar {{ width: 260px; background: var(--sidebar-bg); border-right: 1px solid var(--border); position: fixed; top: 60px; bottom: 0; left: 0; overflow-y: auto; }}
        .sidebar-content {{ padding: 1.5rem; display: flex; flex-direction: column; gap: 0.5rem; }}
        .sidebar-content a {{ color: var(--muted); text-decoration: none; padding: 0.5rem 0.75rem; border-radius: 6px; font-size: 0.9rem; transition: all 0.2s; }}
        .sidebar-content a:hover {{ background: var(--primary-light); color: var(--primary); }}
        .main {{ flex: 1; margin-left: 260px; padding: 2rem 3rem; max-width: 900px; width: 100%; }}
        .hero {{ padding: 3rem 0; margin-bottom: 2rem; border-bottom: 1px solid var(--border); }}
        .hero h1 {{ font-size: 2.5rem; margin-bottom: 1rem; }}
        .hero p {{ font-size: 1.25rem; color: var(--muted); max-width: 600px; }}
        h1, h2, h3 {{ margin: 2rem 0 1rem; font-weight: 600; }}
        h1 {{ font-size: 2rem; }} h2 {{ font-size: 1.5rem; }} h3 {{ font-size: 1.25rem; }}
        p {{ margin-bottom: 1rem; color: var(--text); }}
        a {{ color: var(--primary); }}
        code {{ background: var(--code-bg); padding: 0.2rem 0.4rem; border-radius: 4px; font-family: 'Monaco', 'Consolas', monospace; font-size: 0.9em; }}
        pre {{ background: var(--code-bg); padding: 1rem; border-radius: 8px; overflow-x: auto; margin: 1rem 0; border: 1px solid var(--border); }}
        pre code {{ background: none; padding: 0; }}
        table {{ width: 100%; border-collapse: collapse; margin: 1.5rem 0; background: var(--card-bg); border-radius: 8px; overflow: hidden; box-shadow: var(--shadow); }}
        th, td {{ padding: 0.75rem 1rem; text-align: left; border-bottom: 1px solid var(--border); }}
        th {{ background: var(--sidebar-bg); font-weight: 600; font-size: 0.9rem; }}
        tr:hover {{ background: var(--primary-light); }}
        .alert {{ padding: 1rem 1.25rem; border-radius: 8px; margin: 1rem 0; display: flex; align-items: center; gap: 0.75rem; border: 1px solid var(--border); }}
        .alert-info {{ background: #eff6ff; border-color: #bfdbfe; color: #1e40af; }}
        .alert-warning {{ background: #fffbeb; border-color: #fde68a; color: #92400e; }}
        .alert-success {{ background: #ecfdf5; border-color: #a7f3d0; color: #065f46; }}
        .alert-error {{ background: #fef2f2; border-color: #fecaca; color: #991b1b; }}
        .alert-tip {{ background: #faf5ff; border-color: #e9d5ff; color: #6b21a8; }}
        ul {{ margin: 1rem 0; padding-left: 1.5rem; }}
        li {{ margin: 0.5rem 0; }}
        .grid {{ display: grid; gap: 1rem; margin: 1.5rem 0; }}
        .grid-cols-2 {{ grid-template-columns: repeat(2, 1fr); }}
        .grid-cols-3 {{ grid-template-columns: repeat(3, 1fr); }}
        .grid-cols-4 {{ grid-template-columns: repeat(4, 1fr); }}
        .card {{ background: var(--card-bg); border: 1px solid var(--border); border-radius: 8px; padding: 1.5rem; box-shadow: var(--shadow); }}
        .card h3 {{ margin: 0 0 0.5rem; font-size: 1.1rem; }}
        .card p {{ margin: 0; color: var(--muted); font-size: 0.9rem; }}
        hr {{ border: none; border-top: 1px solid var(--border); margin: 2rem 0; }}
        img {{ max-width: 100%; height: auto; }}
        @media (max-width: 768px) {{ .sidebar {{ display: none; }} .main {{ margin-left: 0; padding: 1rem; }} .grid-cols-2, .grid-cols-3, .grid-cols-4 {{ grid-template-columns: 1fr; }} }}
        </style>
        """

        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{self.title}</title>
    {css}
</head>
<body>
    {nav_html}
    <div class="layout">
        {sidebar_html}
        <main class="main">
            {content}
        </main>
    </div>
</body>
</html>"""


def compile_all():
    docs_dir = Path('docs')
    out_dir = Path('_site')
    out_dir.mkdir(exist_ok=True)

    for doctor_file in docs_dir.glob('*.doctor'):
        with open(doctor_file, 'r', encoding='utf-8') as f:
            source = f.read()

        compiler = Doctor()
        html = compiler.parse(source)

        output_file = out_dir / doctor_file.with_suffix('.html').name
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html)

        print(f"Compiled: {doctor_file} -> {output_file}")

    index_doctor = docs_dir / 'index.doctor'
    if index_doctor.exists():
        index_html = out_dir / 'index.html'
        if not index_html.exists():
            with open(index_doctor, 'r', encoding='utf-8') as f:
                source = f.read()
            compiler = Doctor()
            html = compiler.parse(source)
            with open(index_html, 'w', encoding='utf-8') as f:
                f.write(html)
            print(f"Copied index: {index_doctor} -> {index_html}")


if __name__ == '__main__':
    compile_all()
