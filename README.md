# jackblumenau.com

Personal academic website, built with [Jekyll](https://jekyllrb.com/) and served via GitHub Pages at <https://jackblumenau.com>.

## How the site is deployed

- Hosted on **GitHub Pages** from the `main` branch of `jblumenau/jblumenau.github.io`.
- GitHub builds the Jekyll site on push — you do not need to build it yourself to update the live site. Just commit and push.
- The custom domain is `jackblumenau.com`, configured via a `CNAME` file at the repo root. **Do not delete the `CNAME` file** — if it goes missing, GitHub unlinks the custom domain and the site disappears.
- The domain is verified to the GitHub account via a TXT record at Namecheap (`_github-pages-challenge-jblumenau`). **Do not remove that TXT record** — it prevents anyone else from hijacking the domain.

## Making a change

The standard workflow for any edit:

```bash
# Edit the relevant file(s) (see "Where things live" below)
git add -A
git commit -m "Describe what you changed"
git push
```

Within a minute or two, GitHub will rebuild and redeploy. Check <https://jackblumenau.com> in an incognito window to bypass caching.

## Where things live

| What you want to change | File to edit |
|---|---|
| Homepage text, role, bio | `index.md` |
| Research page intro / section headings | `research.md` |
| Add/edit/remove a publication | `_data/publications.yml` |
| Current projects page | `projects.md` |
| Teaching page | `teaching.md` |
| Speaking & consultancy page | `speaking.md` |
| Site-wide header / nav links | `_includes/nav.html` |
| Site-wide footer | `_includes/footer.html` |
| `<head>` tags, favicons, meta | `_includes/head.html` |
| Overall page template | `_layouts/default.html`, `page.html`, `research.html` |
| Colours, fonts, spacing, CSS | `assets/css/style.css` |
| Site title, author, social links | `_config.yml` |
| Custom domain | `CNAME` (contains `jackblumenau.com` — leave alone) |

## Adding a publication

Open `_data/publications.yml` and add a new entry at the top of the list, following the existing format. Each entry has fields like `title`, `authors`, `year`, `journal`, `doi`, `pdf`, and `status`. The research page reads from this file automatically — no need to edit any HTML.

## Adding a new page

1. Create a new Markdown file at the repo root, e.g. `newpage.md`.
2. Add Jekyll front matter at the top:
   ```yaml
   ---
   layout: page
   title: My New Page
   permalink: /newpage/
   ---
   ```
3. Write the page content in Markdown below the front matter.
4. Add a link to it in `_includes/nav.html` if you want it in the top navigation.

## Previewing changes locally (optional)

You don't need to do this — GitHub will build the site for you on push — but if you want to see changes before pushing, there are two options:

### Option A: Jekyll (proper way)

Requires Ruby 3+ (the system Ruby on older macOS is 2.6 and too old). Install with Homebrew:

```bash
brew install ruby
# Follow the instructions to put brew's ruby on your PATH
bundle install
bundle exec jekyll serve
```

Visit <http://localhost:4000>.

### Option B: Python preview script

A lightweight fallback that renders the site without Jekyll. From the repo folder:

```bash
python3 build_preview.py
```

It writes to `_site/` and starts a local server. Useful for quick visual checks but doesn't replicate every Jekyll feature — Option A is closer to the real thing.

## Safety notes

- **Never force-push `main`** unless you really know what you're doing. The branch is the live site.
- Keep an eye on Dependabot alerts on the repo — outdated gems mostly matter for local builds, not for the live site (GitHub builds with their own gems), but worth resolving periodically.
- If `jackblumenau.com` ever stops working, first check: (1) is `CNAME` still in the repo root? (2) is the TXT record still at Namecheap? (3) in repo Settings → Pages, is the source branch set to `main` and is the custom domain still listed?

## Repo layout

```
personal_site_v2_jekyll/
├── CNAME                   # Custom domain — do not delete
├── Gemfile                 # Ruby dependencies (for local previews)
├── _config.yml             # Site-wide config
├── _data/
│   └── publications.yml    # Publication list
├── _includes/              # Reusable HTML snippets (nav, footer, head)
├── _layouts/               # Page templates
├── assets/                 # CSS, images, fonts
├── papers/                 # PDF copies of papers
├── CV/                     # CV PDF
├── index.md                # Homepage
├── research.md             # Research page
├── projects.md             # Current projects
├── teaching.md             # Teaching page
├── speaking.md             # Speaking & consultancy page
├── build_preview.py        # Python fallback preview script
└── _site/                  # Build output — auto-generated, ignore
```
