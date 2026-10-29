# Universal Tab Download (UTDL) v002

A plain JavaScript bookmarklet that captures the current page as two separate
downloads: Markdown text and a self-contained HTML page archive.

## Navigation map

- What it does
- Files
- Install
- Limitations
- Public-safety boundary

## What it does

When run on the current browser tab, UTDL v002:

1. Downloads a Markdown extraction of visible page content.
2. Downloads an HTML copy of the page after removing scripts, attempting to
   inline images and linked stylesheets, and making links and iframe URLs
   absolute.

Filenames use a local timestamp and a lowercase, ASCII, hyphen-separated page
title. This version deliberately creates two normal downloads; it does not
create a ZIP or other package.

## Files

- `utdl.js` — readable source of the reviewed v002 behavior.
- `utdl.bookmarklet.txt` — one-line `javascript:` URL for a browser
  bookmark.

## Install

**In a text editor:** open `utdl.bookmarklet.txt` and copy its complete,
single line.

**In Chrome or another compatible browser:** create a bookmark, paste the line
into the bookmark's URL field, save it, then invoke that bookmark while viewing
a page.

The browser may require approval for two automatic downloads from a site.

## Limitations

- Cross-origin images or stylesheets without permissive CORS headers cannot be
  embedded and remain external URLs.
- CSS background images and web fonts are not embedded.
- Tables approximate `colspan` and do not support `rowspan`.
- Strict content-security policies can block bookmarklet-initiated downloads.
- The HTML capture is a self-contained HTML document when embedding succeeds;
  it is not an MHTML capture.

## Public-safety boundary

Review the content of pages before sharing the resulting files. The browser
downloads may contain page text, URLs, images, and metadata that are not safe
to publish. This repository contains only the generic bookmarklet source and
installation text; it contains no captured pages or browser data.

