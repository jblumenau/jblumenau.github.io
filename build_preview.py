#!/usr/bin/env python3
"""
Quick local build script for previewing the Jekyll site without installing Ruby/Jekyll.
Renders templates, resolves includes, and outputs to _site/ with relative paths.

Usage:  python3 build_preview.py
"""

import yaml, os, re, shutil

base = os.path.dirname(os.path.abspath(__file__))
site_dir = os.path.join(base, "_site")
os.makedirs(site_dir, exist_ok=True)

# --- Load config, data, includes, layouts ---

with open(os.path.join(base, "_config.yml")) as f:
    config = yaml.safe_load(f)

with open(os.path.join(base, "_data/publications.yml")) as f:
    pubs = yaml.safe_load(f)

includes = {}
for inc in os.listdir(os.path.join(base, "_includes")):
    with open(os.path.join(base, "_includes", inc)) as f:
        includes[inc] = f.read()

layouts = {}
for lay in os.listdir(os.path.join(base, "_layouts")):
    with open(os.path.join(base, "_layouts", lay)) as f:
        content = f.read()
        if content.startswith("---"):
            parts = content.split("---", 2)
            content = parts[2]
        layouts[lay] = content

# --- Helpers ---

def resolve_includes(html):
    for name, content in includes.items():
        html = html.replace("{%% include %s %%}" % name, content)
        html = html.replace("{% include " + name + " %}", content)
    return html

def resolve_site_vars(html):
    html = html.replace("{{ site.title }}", config.get("title", ""))
    html = html.replace("{{ site.email }}", config.get("email", ""))
    html = html.replace("{{ site.address }}", config.get("address", ""))
    html = html.replace("{{ site.baseurl }}", "")
    html = html.replace("{{ 'now' | date: '%Y' }}", "2026")
    # relative_url filter: just strip it for local preview
    html = re.sub(r"\{\{\s*'([^']*)'\s*\|\s*relative_url\s*\}\}", r"\1", html)
    return html

def make_paths_relative(html):
    """Convert absolute /paths to relative for local file:// preview."""
    html = html.replace('href="/research"', 'href="research.html"')
    html = html.replace('href="/projects"', 'href="projects.html"')
    html = html.replace('href="/projects#', 'href="projects.html#')
    html = html.replace('href="/teaching"', 'href="teaching.html"')
    html = html.replace('href="/speaking"', 'href="speaking.html"')
    html = html.replace('href="/CV/', 'href="CV/')
    html = html.replace('href="/"', 'href="index.html"')
    html = html.replace('href="/assets/', 'href="assets/')
    html = html.replace('src="/assets/', 'src="assets/')
    return html

NAV_SECTIONS = ["research", "projects", "teaching", "speaking"]

def resolve_page_vars(html, page):
    html = html.replace("{{ page.title }}", page.get("title", ""))
    if page.get("standfirst"):
        html = re.sub(r"\{%\s*if page\.standfirst\s*%\}", "", html)
        html = html.replace("{{ page.standfirst }}", page["standfirst"])
    else:
        html = re.sub(r"\{%\s*if page\.standfirst\s*%\}.*?\{%\s*endif\s*%\}", "", html, flags=re.DOTALL)
    nav_val = page.get("nav", "")
    for section in NAV_SECTIONS:
        pat = r"""\{%\s*if page\.nav == '""" + section + r"""'\s*%\}class="active"\{%\s*endif\s*%\}"""
        html = re.sub(pat, 'class="active"' if section == nav_val else '', html)

    if page.get("title"):
        title_str = "%s &ndash; %s" % (page["title"], config["title"])
    else:
        title_str = config["title"]
    html = re.sub(r"\{%\s*if page\.title\s*%\}.*?\{%\s*else\s*%\}.*?\{%\s*endif\s*%\}",
                   title_str, html, flags=re.DOTALL)

    html = re.sub(r"\{%\s*endif\s*%\}", "", html)
    return html

def build_pubs_html():
    html = ""
    for pub in pubs:
        html += '<div class="pub">\n'
        html += '  <div class="pub-title">%s</div>\n' % pub["title"]
        meta_parts = []
        if pub.get("authors"):
            meta_parts.append("with %s" % pub["authors"])
        journal_str = ""
        if pub.get("status") == "forthcoming":
            journal_str = "Forthcoming, <em>%s</em>, %s" % (pub["journal"], pub["year"])
        else:
            journal_str = "<em>%s</em>, %s" % (pub["journal"], pub["year"])
        if pub.get("note"):
            journal_str += " (%s)" % pub["note"]
        meta_parts.append(journal_str)
        html += '  <div class="pub-meta">%s</div>\n' % " &middot; ".join(meta_parts)
        html += '  <div class="pub-links">\n'
        if pub.get("pdf"):
            html += '    <a href="%s">Paper</a>\n' % pub["pdf"]
        if pub.get("doi"):
            html += '    <a href="%s">Paper</a>\n' % pub["doi"]
        if pub.get("abstract"):
            html += '    <a href="#" class="toggle-abstract">Abstract</a>\n'
        html += '  </div>\n'
        if pub.get("abstract"):
            html += '  <div class="pub-abstract">%s</div>\n' % pub["abstract"].strip()
        html += '</div>\n\n'
    return html

# --- Discover pages (any .md file in root) ---

pages = []
for f in sorted(os.listdir(base)):
    if f.endswith(".md"):
        out = "index.html" if f == "index.md" else f.replace(".md", ".html")
        pages.append({"src": f, "out": out})

# --- Build ---

for page_info in pages:
    with open(os.path.join(base, page_info["src"])) as f:
        raw = f.read()

    parts = raw.split("---", 2)
    fm = yaml.safe_load(parts[1]) if len(parts) > 2 and parts[1].strip() else {}
    body = parts[2] if len(parts) > 2 else raw

    layout_name = fm.get("layout", "default") + ".html"

    if layout_name == "research.html":
        layout_html = layouts["research.html"]
        pubs_html = build_pubs_html()
        layout_html = re.sub(
            r"\{%\s*for pub in site\.data\.publications\s*%\}.*?\{%\s*endfor\s*%\}",
            pubs_html, layout_html, flags=re.DOTALL)
        layout_html = layout_html.replace("{{ content }}", body.strip())
        html = layouts["default.html"].replace("{{ content }}", layout_html)
    elif layout_name == "page.html":
        layout_html = layouts["page.html"]
        layout_html = layout_html.replace("{{ content }}", body.strip())
        html = layouts["default.html"].replace("{{ content }}", layout_html)
    else:
        html = layouts["default.html"].replace("{{ content }}", body.strip())

    html = resolve_includes(html)
    html = resolve_page_vars(html, fm)
    html = resolve_site_vars(html)
    html = make_paths_relative(html)

    with open(os.path.join(site_dir, page_info["out"]), "w") as f:
        f.write(html)
    print("  Built: %s" % page_info["out"])

# --- Copy assets (only if newer) ---

for d in ["assets", "papers", "CV"]:
    src = os.path.join(base, d)
    dst = os.path.join(site_dir, d)
    if not os.path.exists(src):
        continue
    os.makedirs(dst, exist_ok=True)
    for root, dirs, files in os.walk(src):
        rel = os.path.relpath(root, src)
        dst_root = os.path.join(dst, rel)
        os.makedirs(dst_root, exist_ok=True)
        for fname in files:
            sf = os.path.join(root, fname)
            df = os.path.join(dst_root, fname)
            if not os.path.exists(df) or os.path.getmtime(sf) > os.path.getmtime(df):
                shutil.copy2(sf, df)

print("  Done! Open _site/index.html to preview.")
