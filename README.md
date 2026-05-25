# Doctor

> A single-file documentation language that compiles to GitHub Pages HTML.

Doctor lets you write documentation in a clean, minimal syntax and publish it as a beautiful site — all from one file.

---

## Table of Contents

- [Quick Start](#quick-start)
- [Installation](#installation)
- [Your First Doctor File](#your-first-doctor-file)
- [Syntax Reference](#syntax-reference)
  - [Title](#title)
  - [Hero](#hero)
  - [Headings](#headings)
  - [Paragraphs](#paragraphs)
  - [Sidebar](#sidebar)
  - [Tables](#tables)
  - [Lists](#lists)
  - [Code Blocks](#code-blocks)
  - [Alerts](#alerts)
  - [Cards](#cards)
  - [Dividers](#dividers)
  - [Images](#images)
  - [Grids](#grids)
- [Advanced Usage](#advanced-usage)
  - [Custom Landing Pages](#custom-landing-pages)
  - [The Showcase](#the-showcase)
  - [The Playground](#the-playground)
- [GitHub Pages Setup](#github-pages-setup)
- [File Structure](#file-structure)
- [Troubleshooting](#troubleshooting)
- [Examples](#examples)

---

## Quick Start

1. Create `docs/index.doctor`
2. Write your content
3. Push to GitHub
4. Your site is live

```
docs/index.doctor
```

```doctor
title# My Documentation

hero# Welcome
desc# Everything you need to know.

h2# Getting Started

p# Doctor compiles this file into a beautiful HTML site.

h2# Features

list#
- Simple syntax
- Auto-deploy to GitHub Pages
- Dark mode support
end#
```

---

## Installation

Doctor requires no installation. It runs entirely through GitHub Actions.

### What You Need

- A GitHub account
- A repository
- One `.doctor` file in a `docs/` folder

### Repository Setup

Create these files in your repo:

```
your-repo/
├── .github/
│   └── workflows/
│       └── build.yml          # GitHub Actions workflow
├── docs/
│   └── index.doctor           # Your documentation
├── doctor.py                  # The compiler
├── _config.yml                # Jekyll config
└── index.html                 # Optional landing page
```

---

## Your First Doctor File

Create `docs/index.doctor`:

```doctor
title# Prism Docs

hero# Prism
desc# A documentation site built with Doctor.

h2# What is Doctor?

p# Doctor is a single-file markup language that compiles to GitHub Pages HTML. No complex setup. No local build tools. Just write and push.

h2# Quick Example

code# doctor
title# My Page

hero# Hello World
desc# This is my first Doctor site.

h2# Features

list#
- Fast compilation
- Clean syntax
- Beautiful output
end#
end#

h2# Learn More

p# Check out the full syntax reference below.
```

Commit and push. GitHub Actions will compile this to HTML and deploy it.

---

## Syntax Reference

### Title

Sets the page title and appears in browser tabs.

```doctor
title# My Documentation Site
```

**Result:** Browser tab shows "My Documentation Site".

---

### Hero

A large heading with an optional description. Perfect for page headers.

```doctor
hero# Prism
desc# We build things that work.
```

**Result:**

# Prism
> We build things that work.

The `desc#` line is optional but recommended.

---

### Headings

Three levels of headings.

```doctor
h1# Main Heading
h2# Section Heading
h3# Subsection Heading
```

**Result:**

# Main Heading
## Section Heading
### Subsection Heading

Use `h1#` sparingly — the hero usually serves as your main title.

---

### Paragraphs

Simple text blocks.

```doctor
p# This is a paragraph of text. It can be as long as you need and will wrap naturally in the output.
```

**Result:**

This is a paragraph of text. It can be as long as you need and will wrap naturally in the output.

---

### Sidebar

Navigation links that appear in the left sidebar.

```doctor
sidebar# Getting Started | #start
sidebar# Components | #components
sidebar# API Reference | #api
sidebar# Examples | #examples
```

**Result:** A sidebar with clickable navigation links.

Each sidebar item has two parts separated by `|`:
- **Name** — the text shown
- **Href** — the link destination

---

### Tables

Structured data with headers and rows.

```doctor
table# Project | Year | Status
Meridian | 2025 | Active
Solstice | 2024 | Archived
Aperture | 2023 | Completed
end#
```

**Result:**

| Project | Year | Status |
|---------|------|--------|
| Meridian | 2025 | Active |
| Solstice | 2024 | Archived |
| Aperture | 2023 | Completed |

**Rules:**
- First line after `table#` defines headers
- Separate columns with `|`
- End with `end#`

---

### Lists

Bullet lists for features, steps, or any grouped items.

```doctor
list#
- Product design
- Frontend engineering
- Design systems
- Deployment pipelines
end#
```

**Result:**

- Product design
- Frontend engineering
- Design systems
- Deployment pipelines

---

### Code Blocks

Syntax-highlighted code snippets.

```doctor
code# python
def hello():
    print("Hello Doctor")

hello()
end#
```

**Result:**

```python
def hello():
    print("Hello Doctor")

hello()
```

The language after `code#` determines syntax highlighting. Use any common language: `python`, `javascript`, `css`, `html`, `bash`, `ruby`, `go`, etc.

---

### Alerts

Contextual messages with emoji indicators.

```doctor
alert# info
p# This feature requires v2.0+

alert# warning
p# Breaking change in next release

alert# success
p# Deployment completed

alert# error
p# Build failed

alert# tip
p# Use Ctrl+Enter to run code
```

**Result:**

> **ℹ️ INFO**: This feature requires v2.0+

> **⚠️ WARNING**: Breaking change in next release

> **✅ SUCCESS**: Deployment completed

> **❌ ERROR**: Build failed

> **💡 TIP**: Use Ctrl+Enter to run code

**Available types:** `info`, `warning`, `success`, `error`, `tip`

---

### Cards

Title and description blocks for features or highlights.

```doctor
card# The Classic
desc# Acetate frames, timeless design

card# The Minimal
desc# Titanium, featherlight build

card# The Bold
desc# Statement pieces for standouts
```

**Result:** Three feature cards with titles and descriptions.

---

### Dividers

Horizontal rules for separating sections.

```doctor
h2# Section One
p# Content here

divider#

h2# Section Two
p# More content
```

**Result:** A horizontal line between Section One and Section Two.

---

### Images

Embed images with source and alt text.

```doctor
img# ./assets/hero.jpg|Hero banner of our studio
```

**Format:** `img# path|alt text`

**Image sources:**
- **Relative:** `./assets/photo.jpg` (file in repo)
- **External:** `https://cdn.example.com/image.png`
- **GitHub raw:** `https://raw.githubusercontent.com/...`

---

### Grids

Group multiple cards in a grid layout.

```doctor
grid#
card# Fast
desc# Compiles in seconds

card# Simple
desc# One file, one syntax

card# Beautiful
desc# Clean, modern output
end#
```

**Result:** A 2-column grid of feature cards.

---

## Advanced Usage

### Custom Landing Pages

Create an `index.html` in your repo root for a custom landing page that redirects to your docs.

```html
<!DOCTYPE html>
<html>
<head>
  <title>My Project</title>
  <style>
    body { font-family: system-ui; max-width: 600px; margin: 80px auto; padding: 20px; }
    h1 { font-size: 3em; }
    p { color: #666; }
    a { display: inline-block; margin-top: 20px; padding: 12px 24px; background: #000; color: #fff; text-decoration: none; border-radius: 6px; }
  </style>
</head>
<body>
  <h1>My Project</h1>
  <p>A short description of what this does.</p>
  <a href="./docs/">Read Docs</a>
</body>
</html>
```

Your workflow must preserve this file:

```yaml
- name: Ensure root index.html exists
  run: |
    if [ -f index.html ]; then
      cp index.html _site/index.html
    fi
```

---

### The Showcase

The showcase is a separate page that demonstrates all Doctor syntax with side-by-side code and output.

Create `showcase.html` in your repo root. It features:
- Rotating carousel of all Doctor features
- Split view: code on left, result on right
- Auto-advancing slides (8 seconds)
- Manual navigation with Previous/Next buttons
- Dot indicators for quick jumping
- Keyboard navigation (arrow keys)

Link to it from your landing page:

```html
<a href="./showcase.html">See Showcase</a>
```

---

### The Playground

The playground is embedded in every docs page. It lets visitors:
- Type Doctor code in a live editor
- Click "Run" or press **Ctrl+Enter** to compile
- See instant preview of the rendered output
- Experiment with all Doctor syntax

The playground auto-runs on page load with a pre-loaded example.

---

## GitHub Pages Setup

### Enable Pages

1. Go to **Settings → Pages** in your repo
2. Under **Build and deployment**, select **GitHub Actions**
3. Save

### Workflow File

Your `.github/workflows/build.yml` should:

1. Checkout code
2. Setup Python
3. Run `python doctor.py` to convert `.doctor` files
4. Build with Jekyll
5. Deploy to Pages

```yaml
name: Build Doctor Docs
on:
  push:
    branches: [main, master]
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Convert Doctor to Markdown
        run: python doctor.py

      - name: Build with Jekyll
        uses: actions/jekyll-build-pages@v1
        with:
          source: .
          destination: ./_site

      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: ./_site

  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    needs: build
    steps:
      - name: Deploy to GitHub Pages
        uses: actions/deploy-pages@v4
```

---

## File Structure

### Minimal Setup

```
your-repo/
├── .github/workflows/build.yml
├── docs/
│   └── index.doctor
├── doctor.py
└── _config.yml
```

### Full Setup with Landing Page

```
your-repo/
├── .github/workflows/build.yml
├── docs/
│   └── index.doctor          # Documentation content
├── index.html                # Landing page
├── showcase.html             # Feature showcase
├── doctor.py                 # Compiler
├── _config.yml               # Jekyll config
└── assets/
    └── images/               # Static images
```

---

## Troubleshooting

### 404 Error

**Cause:** Missing `index.html` or `index.md` at site root.

**Fix:** Ensure `doctor.py` outputs `docs/index.md` and Jekyll builds it, or provide a custom `index.html`.

### Build Fails

**Cause:** Workflow step exits with error.

**Fix:** Add `|| echo` fallbacks to all run steps so failures don't block deployment.

### Images Don't Show

**Cause:** Wrong path or missing file.

**Fix:**
- Use relative paths: `./assets/image.png`
- Upload images to repo
- Use external URLs for images hosted elsewhere

### Styles Look Wrong

**Cause:** `doctor.html` layout not found.

**Fix:** Ensure `doctor.html` is in your repo root and referenced in `_config.yml`.

---

## Examples

### Documentation Site

```doctor
title# API Documentation

hero# REST API
desc# Complete reference for developers.

sidebar# Authentication | #auth
sidebar# Endpoints | #endpoints
sidebar# Errors | #errors

h2# Authentication

p# All requests require a Bearer token in the Authorization header.

code# bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  https://api.example.com/v1/users
end#

alert# warning
p# Tokens expire after 24 hours. Refresh before expiry.

h2# Endpoints

table# Method | Endpoint | Description
GET | /users | List all users
POST | /users | Create user
GET | /users/:id | Get user by ID
DELETE | /users/:id | Delete user
end#

h2# Error Codes

list#
- 400 — Bad Request
- 401 — Unauthorized
- 404 — Not Found
- 500 — Server Error
end#
```

### Product Page

```doctor
title# Optician — Precision Eyewear

hero# Optician
desc# See the world with clarity.

h2# Services

table# Service | Price | Time
Eye Exam | $89 | 30 min
Fitting | Free | 20 min
Adjustments | Free | 10 min
end#

h2# Featured Frames

card# The Classic
desc# Acetate, timeless design

card# The Minimal
desc# Titanium, featherlight

card# The Bold
desc# Statement pieces

h2# Visit Us

p# 42 Lens Street, Downtown
p# Open Tue–Sat, 10am–6pm

divider#

alert# tip
p# Book online for 10% off your first exam.
```

---

## License

Doctor is open source. Use it for personal projects, documentation, or anything you build.

---

## Credits

Built with Doctor. Published on GitHub Pages.

*Built with Optician* 👓
