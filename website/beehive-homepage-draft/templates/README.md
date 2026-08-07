# Blog Article Template System

This folder turns `pages/blog-article.html` into a reusable template. Every new article uses the same layout, styling, and interactions — you only supply the content in a JSON file.

## Files

| File | Purpose |
|------|---------|
| `blog-article-template.html` | The master HTML template with `{{PLACEHOLDER}}` markers. Do not edit article content here. |
| `example-article.json` | Example config showing every field the generator understands. Copy this to create a new article. |
| `generate-article.js` | Node.js script that reads a JSON config and writes a finished HTML page. |

## How to Create a New Article

### 1. Copy the Example Config

```bash
cd beehive-homepage-draft/templates
cp example-article.json my-new-article.json
```

### 2. Edit the JSON File

Open `my-new-article.json` and change the values. The most important fields are:

- `slug` — becomes the output filename (`slug.html`).
- `outputDir` — where the HTML file is written. Default is `../pages`.
- `title`, `h1`, `metaDescription`, `canonicalUrl`, `ogImage` — SEO and social metadata.
- `publishedDateIso`, `modifiedDateIso`, `publishedDateDisplay`, `readTime` — article metadata.
- `category`, `tags`, `keywords` — taxonomy.
- `authorName`, `authorInitials` — byline.
- `toc` — table of contents entries. Each entry needs a unique `id` and a `label`.
- `content` — the article body. See **Content Block Types** below.
- `faq` — optional accordion FAQ. Also generates FAQPage JSON-LD schema.
- `sidebarRelated` — 3 related article cards in the sidebar.
- `recommended` — 3 larger cards in the Recommended Articles section.
- `cta` — bottom call-to-action title, description, and 4 stats.

### 3. Run the Generator

```bash
node generate-article.js my-new-article.json
```

The script writes `../pages/{slug}.html`.

### 4. Preview the Result

Open the generated file in a browser, or serve the `beehive-homepage-draft` folder:

```bash
cd beehive-homepage-draft
npx serve .
```

## Content Block Types

The `content` array supports these block types:

### Heading

```json
{
  "type": "h2",
  "id": "unique-section-id",
  "text": "Section Title"
}
```

The `id` must match an entry in `toc` so the table of contents links correctly.

### Paragraph

```json
{
  "type": "p",
  "text": "Your paragraph text. <strong>You can use inline HTML</strong> for emphasis or links."
}
```

### Bullet List

```json
{
  "type": "ul",
  "items": [
    "<strong>Point one:</strong> description.",
    "<strong>Point two:</strong> description."
  ]
}
```

### Numbered List

```json
{
  "type": "ol",
  "items": [
    "<strong>Step 1:</strong> do this.",
    "<strong>Step 2:</strong> do that."
  ]
}
```

### Stat Row

```json
{
  "type": "stats",
  "items": [
    { "value": "3x", "label": "Typical first-year ROI" },
    { "value": "78%", "label": "Faster query resolution" },
    { "value": "92%", "label": "Adoption in 6 months" }
  ]
}
```

Renders a 3-column row of stat cards.

### Blockquote

```json
{
  "type": "quote",
  "text": "A memorable quote from the article.",
  "cite": "Source or author"
}
```

### Raw HTML

```json
{
  "type": "html",
  "html": "<div class='custom-component'>...</div>"
}
```

Use sparingly for tables, images, or other custom markup that the standard blocks cannot express.

## FAQ Format

Each FAQ item generates an accordion panel and contributes to the JSON-LD `FAQPage` schema:

```json
"faq": [
  {
    "question": "How long does implementation take?",
    "answer": "Initial deployment typically takes two to four weeks."
  }
]
```

Leave the array empty or omit it to remove the FAQ section entirely.

## Customising the Template

If you need to change the layout, navigation, footer, or styling for **all** articles, edit `blog-article-template.html`. The generator copies the template verbatim and only replaces the `{{PLACEHOLDER}}` markers.

Common template-level changes:

- Update header links or logo path.
- Change brand colours in the `:root` design tokens.
- Adjust responsive breakpoints.
- Add new social share buttons.

## Moving to the Production Site

This template system currently lives in `beehive-homepage-draft/templates`. To use it for the live site:

1. Copy the three files (`blog-article-template.html`, `generate-article.js`, and an example config) to the production project folder.
2. Update asset paths in the template (`../assets/...`) to match the production structure (`/assets/images/...`).
3. Update the canonical URL base and navigation links if they differ.
4. Run the generator against production configs and save outputs to `blog/articles/`.

## Troubleshooting

| Problem | Likely Cause | Fix |
|---------|--------------|-----|
| Generated file is missing content | Placeholder not replaced | Ensure the JSON key name matches the template placeholder. |
| TOC links do not scroll | `id` mismatch | Make every `toc` entry `id` match an `h2` block `id`. |
| FAQ accordion does not open | Missing `.faq-item` markup | Keep the `faq` array structure exactly as shown. |
| Output path is wrong | `outputDir` or `slug` typo | Use a relative path from the config file location for `outputDir`. |
