# Universal Tab Download (UTDL) v003

A plain JavaScript bookmarklet that captures the current page as Markdown and a
self-contained HTML page archive, then delivers those two files in one ZIP
download.

## Navigation map

- What it does
- Files
- Install
- Limitations
- Public-safety boundary

## What it does

When run on the current browser tab, UTDL v003:

1. Builds a Markdown extraction of visible page content.
2. Builds an HTML copy after removing scripts, attempting to inline images and
   linked stylesheets, and making links and iframe URLs absolute.
3. Creates one ZIP download containing the Markdown and HTML files.

The ZIP is generated in the browser for the downloaded capture. It is not a
repository distribution package. Its purpose is to avoid the browser's
multiple-automatic-download permission prompt.

## Files

- `utdl.js` — readable source of the reviewed v003 behavior.
- `utdl.bookmarklet.txt` — one-line `javascript:` URL for a browser
  bookmark.

## Install

**In a text editor:** open `utdl.bookmarklet.txt` and copy its complete,
single line.

**In Chrome or another compatible browser:** create a bookmark, paste the line
into the bookmark's URL field, save it, then invoke that bookmark while viewing
a page.

## Limitations

- Cross-origin images or stylesheets without permissive CORS headers cannot be
  embedded and remain external URLs.
- CSS background images and web fonts are not embedded.
- Tables approximate `colspan` and do not support `rowspan`.
- Strict content-security policies can block bookmarklet-initiated downloads.
- The HTML capture is a self-contained HTML document when embedding succeeds;
  it is not an MHTML capture.
- The ZIP writer stores files without compression.

## Public-safety boundary

Review the content of pages before sharing the resulting ZIP or its contents.
The browser download may contain page text, URLs, images, and metadata that are
not safe to publish. This repository contains only generic bookmarklet source
and installation text; it contains no captured pages or browser data.

