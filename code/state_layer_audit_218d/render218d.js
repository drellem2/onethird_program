// mg-218d — the renderer bridge.  Reads a markdown file, prints HTML on stdout.
//
// COVERAGE.md says of presentation.py: "the way to test it is to install a GFM renderer
// and compare."  This is that renderer.  Two are used, because agreeing with one renderer
// is agreeing with one renderer:
//
//     marked        — GFM-flavoured, the closest widely-available model of what GitHub shows
//     markdown-it   — CommonMark + the GFM table extension, a separate implementation
//
// Install (they are NOT vendored into this repo, on purpose — see README.md):
//     npm install --prefix <dir> marked markdown-it
//     NODE_PATH=<dir>/node_modules node render218d.js <engine> <file>
'use strict';
const fs = require('fs');

const engine = process.argv[2];
const file = process.argv[3];
const src = fs.readFileSync(file, 'utf8');

if (engine === 'marked') {
  const { marked } = require('marked');
  process.stdout.write(marked.parse(src, { gfm: true, breaks: false }));
} else if (engine === 'markdown-it') {
  const MarkdownIt = require('markdown-it');
  const md = new MarkdownIt('commonmark', { html: true });
  md.enable(['table', 'strikethrough']);
  process.stdout.write(md.render(src));
} else {
  console.error('unknown engine: ' + engine);
  process.exit(2);
}
