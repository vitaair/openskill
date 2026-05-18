#!/usr/bin/env node
import fs from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const DEFAULT_MARKDOWN_IT = path.resolve(__dirname, '../../vendor/markdown-it/index.mjs');

function parseArgs(argv) {
  const args = {};
  for (let i = 2; i < argv.length; i += 1) {
    const key = argv[i];
    if (!key.startsWith('--')) continue;
    const name = key.slice(2);
    const next = argv[i + 1];
    if (!next || next.startsWith('--')) {
      args[name] = true;
    } else {
      args[name] = next;
      i += 1;
    }
  }
  return args;
}

function escapeHtml(value) {
  return String(value ?? '')
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;')
    .replaceAll("'", '&#39;');
}

function slugify(text, seen) {
  const base = text
    .trim()
    .toLowerCase()
    .replace(/[^\p{L}\p{N}\s_-]/gu, '')
    .replace(/\s+/g, '-')
    .replace(/-+/g, '-')
    .replace(/^-|-$/g, '') || 'section';
  const count = seen.get(base) || 0;
  seen.set(base, count + 1);
  return count ? `${base}-${count + 1}` : base;
}

function isExternalUrl(url) {
  return /^(?:[a-z][a-z0-9+.-]*:|#|\/)/i.test(url);
}

function toPosixRelative(fromDir, targetPath) {
  let rel = path.relative(fromDir, targetPath).split(path.sep).join('/');
  if (!rel.startsWith('.') && !rel.startsWith('/')) rel = `./${rel}`;
  return rel;
}

function rewriteRelativeUrl(rawUrl, sourceDir, outputDir) {
  if (!rawUrl || isExternalUrl(rawUrl)) return rawUrl;
  const [withoutHash, hash = ''] = rawUrl.split('#');
  const [pathname, query = ''] = withoutHash.split('?');
  if (!pathname) return rawUrl;
  const absolute = path.resolve(sourceDir, pathname);
  const rel = toPosixRelative(outputDir, absolute);
  return `${rel}${query ? `?${query}` : ''}${hash ? `#${hash}` : ''}`;
}

function renderToc(items) {
  if (!items.length) return '';
  const links = items
    .filter((item) => item.level <= 3)
    .map((item) => `<li class="md-toc-l${item.level}"><a href="#${escapeHtml(item.id)}">${escapeHtml(item.text)}</a></li>`)
    .join('');
  return `<nav class="md-toc"><strong>目录</strong><ul>${links}</ul></nav>`;
}

function splitFrontmatter(markdown) {
  const normalized = markdown.replace(/^\uFEFF/, '');
  if (!normalized.startsWith('---\n') && !normalized.startsWith('---\r\n')) {
    return { metadata: [], body: markdown };
  }
  const lines = normalized.split(/\r?\n/);
  const end = lines.findIndex((line, index) => index > 0 && line.trim() === '---');
  if (end < 0) return { metadata: [], body: markdown };
  return {
    metadata: parseFrontmatter(lines.slice(1, end)),
    body: lines.slice(end + 1).join('\n').replace(/^\s+/, '')
  };
}

function parseFrontmatter(lines) {
  const items = [];
  let current = null;
  for (const line of lines) {
    if (!line.trim() || line.trim().startsWith('#')) continue;
    const listMatch = line.match(/^\s*-\s+(.+)$/);
    if (listMatch && current) {
      current.values.push(cleanYamlScalar(listMatch[1]));
      continue;
    }
    const pairMatch = line.match(/^([A-Za-z0-9_.-]+):\s*(.*)$/);
    if (!pairMatch) continue;
    current = { key: pairMatch[1], values: [] };
    const rawValue = pairMatch[2].trim();
    if (rawValue) current.values.push(cleanYamlScalar(rawValue));
    items.push(current);
  }
  return items;
}

function cleanYamlScalar(value) {
  return value
    .replace(/^['"]|['"]$/g, '')
    .replace(/,$/, '')
    .trim();
}

function renderMetadata(items) {
  if (!items.length) return '';
  const rows = items
    .map((item) => {
      const values = item.values.length ? item.values : [''];
      const renderedValues = values
        .map((value) => `<span class="md-meta-value">${escapeHtml(value)}</span>`)
        .join('');
      return `<div class="md-meta-row"><strong>${escapeHtml(item.key)}</strong><div>${renderedValues}</div></div>`;
    })
    .join('');
  return `<details class="md-meta" open><summary>元数据</summary>${rows}</details>`;
}

async function main() {
  const args = parseArgs(process.argv);
  if (!args.input) {
    throw new Error('Missing --input');
  }

  const inputPath = path.resolve(args.input);
  const sourceDir = path.dirname(inputPath);
  const outputDir = path.resolve(args['output-dir'] || args.output && path.dirname(args.output) || process.cwd());
  const markdownItPath = path.resolve(args['markdown-it'] || DEFAULT_MARKDOWN_IT);
  const { default: MarkdownIt } = await import(pathToFileURL(markdownItPath).href);

  const headings = [];
  const seenSlugs = new Map();
  const md = new MarkdownIt({
    html: false,
    linkify: true,
    typographer: false,
    breaks: false
  });

  const defaultHeadingOpen = md.renderer.rules.heading_open || ((tokens, idx, options, env, self) => self.renderToken(tokens, idx, options));
  md.renderer.rules.heading_open = (tokens, idx, options, env, self) => {
    const next = tokens[idx + 1];
    const text = next && next.type === 'inline' ? next.content : '';
    const id = slugify(text, seenSlugs);
    const level = Number(tokens[idx].tag.replace('h', '')) || 2;
    tokens[idx].attrSet('id', id);
    headings.push({ id, text, level });
    return defaultHeadingOpen(tokens, idx, options, env, self);
  };

  for (const ruleName of ['link_open', 'image']) {
    const defaultRule = md.renderer.rules[ruleName] || ((tokens, idx, options, env, self) => self.renderToken(tokens, idx, options));
    md.renderer.rules[ruleName] = (tokens, idx, options, env, self) => {
      const attrName = ruleName === 'image' ? 'src' : 'href';
      const current = tokens[idx].attrGet(attrName);
      if (current) {
        tokens[idx].attrSet(attrName, rewriteRelativeUrl(current, sourceDir, outputDir));
      }
      if (ruleName === 'link_open') {
        const href = tokens[idx].attrGet('href') || '';
        if (/^https?:\/\//i.test(href)) {
          tokens[idx].attrSet('target', '_blank');
          tokens[idx].attrSet('rel', 'noopener noreferrer');
        }
      }
      return defaultRule(tokens, idx, options, env, self);
    };
  }

  const markdown = await fs.readFile(inputPath, 'utf8');
  const { metadata, body: markdownBody } = splitFrontmatter(markdown);
  const body = md.render(markdownBody);
  const title = args.title || path.basename(inputPath);
  const sourceRel = toPosixRelative(outputDir, inputPath);
  const toc = args.toc === 'false' ? '' : renderToc(headings);
  const metadataHtml = args.frontmatter === 'hide' ? '' : renderMetadata(metadata);
  const html = [
    `<article class="md-embed" data-source="${escapeHtml(sourceRel)}">`,
    `<header class="md-embed-head"><h3>${escapeHtml(title)}</h3><a href="${escapeHtml(sourceRel)}">打开 Markdown</a></header>`,
    metadataHtml,
    toc,
    `<div class="md-body">${body}</div>`,
    '</article>'
  ].join('\n');

  if (args.output) {
    await fs.mkdir(path.dirname(path.resolve(args.output)), { recursive: true });
    await fs.writeFile(path.resolve(args.output), html, 'utf8');
    console.log(path.resolve(args.output));
  } else {
    process.stdout.write(html);
  }
}

main().catch((error) => {
  console.error(error.message || error);
  process.exit(1);
});
