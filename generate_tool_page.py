# -*- coding: utf-8 -*-
"""Generate standalone English tool pages for tools-en site."""
import io, sys

BASE = "https://maniu2475-glitch.github.io/tools-en/"
TODAY = "2026-10-26"

FAVICON = ("data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAEAAAABACAYAAACqaXHeAAAAn0lEQVR4nO3asQ2AMBCF"
           "0S9SAdqAsxVwJGACZjAUIAd8a7S0L/1/1r/HPn1vAmAAGIAJRWYAfwFVAdAA0ADQANAA0ADQAKAH+pwAFcBDwADwAHgAPADegAY"
           "AvQAXgBHYA7gAroAPwFegCnAAGIAGIAMYAL4BF9oD3T941acAAAAASUVORK5CYII=")

RELATED = [("json-formatter.html", "JSON Formatter"), ("base64.html", "Base64 encode/decode"),
    ("url-encode-decode.html", "URL encode/decode"), ("qr-code-generator.html", "QR code generator"),
    ("password-generator.html", "Password generator"), ("timestamp-converter.html", "Timestamp converter"),
    ("color-converter.html", "Color converter"), ("word-counter.html", "Word counter"),
    ("md5-generator.html", "Hash generator"), ("case-converter.html", "Case converter"),
    ("uuid-generator.html", "UUID generator"), ("cron-parser.html", "Cron parser"),
    ("percentage-calculator.html", "Percentage calculator"), ("bmi-calculator.html", "BMI calculator"),
    ("age-calculator.html", "Age calculator"), ("random-string-generator.html", "Random string generator"),
    ("chmod-calculator.html", "Chmod calculator"), ("regex-tester.html", "Regex tester")]

NAV = """<header class="site-header">
  <div class="container header-inner">
    <button class="menu-toggle" id="menuToggle" aria-label="menu">☰</button>
    <a class="logo" href="index.html#home"><span class="logo-icon">🧰</span><span class="logo-text">Online Toolbox</span></a>
    <nav class="main-nav" id="mainNav">
      <a href="index.html#tool-json" data-tool="json">JSON</a>
      <a href="index.html#tool-base64" data-tool="base64">Base64</a>
      <a href="index.html#tool-url" data-tool="url">URL</a>
      <a href="index.html#tool-qrcode" data-tool="qrcode">QR Code</a>
      <a href="index.html#tool-password" data-tool="password">Password</a>
      <a href="index.html#tool-timestamp" data-tool="timestamp">Timestamp</a>
      <a href="index.html#tool-color" data-tool="color">Color</a>
      <a href="index.html#tool-counter" data-tool="counter">Counter</a>
      <a href="index.html#tool-hash" data-tool="hash">Hash</a>
      <a href="index.html#tool-ip" data-tool="ip">IP Lookup</a>
      <a href="index.html#tool-unit" data-tool="unit">Units</a>
      <a href="index.html#tool-case" data-tool="case">Case</a>
      <a href="all-tools.html">All Tools</a>
    </nav>
  </div>
</header>"""

FAQ = """<h3>Frequently asked questions</h3>
      <div style="line-height:1.9"><details><summary><strong>Is this tool really free?</strong></summary><p>Yes, completely free with no signup, no login and no usage limits. Just open the page and use it.</p></details>
<details><summary><strong>Is my data uploaded to a server?</strong></summary><p>No. All processing happens locally in your browser - your data never leaves your device, so even sensitive content stays private.</p></details>
<details><summary><strong>Which browsers are supported?</strong></summary><p>All modern browsers including Chrome, Edge, Firefox and Safari, on both desktop and mobile.</p></details></div>"""


def page(slug, title, og_title, desc, h1, body, about):
    canonical = BASE + slug
    rel = chr(10).join('<a class="btn btn-outline" href="%s">%s</a>' % r for r in RELATED)
    html = f"""<!DOCTYPE html>

<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="keywords" content="{desc}">
<meta name="author" content="ToolBox">
<meta name="robots" content="index,follow">
<meta name="theme-color" content="#4f6ef7">
<meta name="google-site-verification" content="online-toolbox">
<meta name="baidu-site-verification" content="online-toolbox">
<link rel="canonical" href="{canonical}">
<link rel="sitemap" type="application/xml" href="sitemap.xml">
<meta property="og:type" content="website">
<meta property="og:title" content="{og_title}">
<meta property="og:description" content="{desc}">
<meta property="og:locale" content="en_US">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<link rel="alternate icon" href="{FAVICON}">
<link rel="stylesheet" href="style.css">
<script type="application/ld+json">{{"@context": "https://schema.org", "@type": "WebApplication", "name": "{og_title}", "url": "{canonical}", "applicationCategory": "UtilityApplication", "operatingSystem": "Any", "description": "{desc}"}}</script>
</head>
<body>
{NAV}
<main class="content" id="content">
  <section class="tool-panel active" id="tool-{slug.replace('.html','').replace('-','')}">
      <h1>{h1}</h1>
{body}
      <hr>
      <h2>About this tool</h2>
      <p style="line-height:1.9">{about}</p>
      <h3>Related tools</h3>
      <div class="btn-group" style="flex-wrap:wrap">
{rel}
      </div>
      {FAQ}
  </section>
</main>
<footer class="site-footer"><div class="container"><p>© 2025 Online Toolbox</p><p class="footer-links"><a href="index.html#home">🧰 Online Toolbox</a></p></div></footer>
<script src="app.js"></script>
<script src="extra.js"></script>
</body>
</html>
"""
    io.open(sys.argv[1] if False else "tools-en-page.html", "w", encoding="utf-8") if False else None
    return html


if __name__ == "__main__":
    pass
