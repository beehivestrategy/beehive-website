# WeChat Official Account Article Publishing Guide

## Overview

This guide ensures every WeChat article follows the same format, style, and publishing workflow. It prevents common issues like blank images, formatting loss, and publishing errors.

## Article Structure (Mandatory)

Every WeChat article MUST follow this structure in order:

1. **Top Icon** — Centered Beehive icon (48x48px)
2. **Intro Paragraph** — Bold lead-in with justified text
3. **Section Headings** — Amber underline (border-bottom: 2px solid #f59e0b)
4. **Body Paragraphs** — 15px font, line-height 2, justified
5. **Numbered Lists** — Amber circle badges (if applicable)
6. **Highlight Boxes** — Amber left border, gray background (if applicable)
7. **Use Case Items** — Emoji label + description (if applicable)
8. **FAQ Section** — Q&A format
9. **CTA Section** — Company info, centered, with CTA icon
10. **Footer** — End marker + copyright

## Formatting Standards

### Typography
| Element | Font Size | Line Height | Color | Weight |
|---------|-----------|-------------|-------|--------|
| Section heading (h2) | 18px | 1.3 | #0a0e0d | bold |
| Body paragraph | 15px | 2.0 | #333 | normal |
| List item title | 15px | 1.8 | #0a0e0d | bold |
| List item description | 14px | 1.8 | #666 | normal |
| Highlight box | 14px | 1.8 | #666 | normal |
| FAQ question | 15px | 1.5 | #0a0e0d | bold |
| FAQ answer | 14px | 1.8 | #666 | normal |
| CTA title | 16px | 1.5 | #0a0e0d | bold |
| CTA body | 14px | 1.8 | #666 | normal |
| Footer | 12px | 1.5 | #999/#ccc | normal |

### Colors
- **Primary text**: #0a0e0d (near-black)
- **Body text**: #333 (dark gray)
- **Secondary text**: #666 (medium gray)
- **Muted text**: #999 (light gray)
- **Accent color**: #f59e0b (amber)
- **Highlight bg**: #f8f9fa (light gray)

### CSS Rules
- **Inline CSS only** — no classes or stylesheets
- **No flexbox** — use `display: inline-block` and `vertical-align: middle`
- **No opacity** — use rgba colors instead
- **No position** — avoid absolute/relative positioning
- **No box-shadow** — not supported by WeChat
- **No external images** — all images must be on mmbiz.qpic.cn CDN

## Content Injection — Blank Image Prevention

### Root Cause of Blank Images

When content is injected into the WeChat ProseMirror editor using the ClipboardEvent paste API in **multiple chunks**, the editor creates `nodeleaf` elements with `ProseMirror-separator` class as placeholder nodes between chunks. These render as **blank image placeholders** in the published article.

### Prevention Rules

1. **Use a SINGLE paste operation** — inject all content at once
2. **If chunking is necessary** (editor freezes), run the cleanup script after injection
3. **Always verify image count** before publishing

### Content Injection Method (Recommended)

```javascript
// Step 1: Prepare the full HTML content as a single string
var htmlContent = '<section style="text-align:center;...">' + 
  '<img src="https://mmbiz.qpic.cn/..." style="width:48px;height:48px;" />' +
  '</section>' +
  '<p style="font-size:15px;...">Intro text</p>' +
  // ... all content in one string ...
  '<p style="text-align:center;...">蜂启咨询 © 2026 | beehivestrategy.com</p>';

// Step 2: Create a single ClipboardEvent paste
var editor = document.querySelector('[contenteditable="true"]');
editor.focus();

var clipboardData = new DataTransfer();
clipboardData.setData('text/html', htmlContent);

var pasteEvent = new ClipboardEvent('paste', {
  bubbles: true,
  cancelable: true,
  clipboardData: clipboardData
});

editor.dispatchEvent(pasteEvent);

// Step 3: Wait for editor to process
setTimeout(function() {
  // Run cleanup (see below)
  cleanupSeparatorNodes();
}, 2000);
```

### Cleanup Script (Run After Every Injection)

```javascript
function cleanupSeparatorNodes() {
  var view = window.__mpBodyChecktextView;
  if (!view) {
    var editor = document.querySelector('[contenteditable="true"]');
    if (editor && editor.pmViewDesc) view = editor.pmViewDesc.view;
  }
  if (!view) {
    console.log('No ProseMirror view found');
    return;
  }

  var state = view.state;
  var doc = state.doc;
  var nodesToDelete = [];

  // Find all nodeleaf/image nodes that are separators
  doc.forEach(function(child, offset, index) {
    if (child.type.name === 'nodeleaf') {
      // Check if it contains an image with empty src or separator class
      var hasRealImage = false;
      if (child.content) {
        child.content.forEach(function(grandchild) {
          if (grandchild.type.name === 'image') {
            var src = grandchild.attrs.src || '';
            var fileId = grandchild.attrs['data-fileid'] || '';
            if (src && fileId && fileId !== 'none') {
              hasRealImage = true;
            }
          }
        });
      }
      if (!hasRealImage) {
        nodesToDelete.push({ offset: offset, size: child.nodeSize });
      }
    }
  });

  // Delete from end to beginning (to preserve positions)
  var tr = state.tr;
  for (var i = nodesToDelete.length - 1; i >= 0; i--) {
    var node = nodesToDelete[i];
    tr = tr.delete(node.offset, node.offset + node.size);
  }

  if (nodesToDelete.length > 0) {
    view.dispatch(tr);
    console.log('Removed ' + nodesToDelete.length + ' separator nodes');
  } else {
    console.log('No separator nodes found');
  }
}
```

### Image Verification (Run Before Publishing)

```javascript
function verifyImages() {
  var view = window.__mpBodyChecktextView;
  if (!view) {
    var editor = document.querySelector('[contenteditable="true"]');
    if (editor && editor.pmViewDesc) view = editor.pmViewDesc.view;
  }
  if (!view) return 'No ProseMirror view found';

  var doc = view.state.doc;
  var imageCount = 0;
  var images = [];

  doc.forEach(function(child, offset, index) {
    if (child.type.name === 'nodeleaf' && child.content) {
      child.content.forEach(function(grandchild) {
        if (grandchild.type.name === 'image') {
          var src = grandchild.attrs.src || '';
          var fileId = grandchild.attrs['data-fileid'] || '';
          if (src && fileId && fileId !== 'none') {
            imageCount++;
            images.push({
              index: index,
              fileId: fileId,
              src: src.substring(0, 80)
            });
          }
        }
      });
    }
  });

  return JSON.stringify({
    totalImages: imageCount,
    images: images,
    status: imageCount > 0 ? 'OK' : 'WARNING: No images found'
  }, null, 2);
}
```

## Publishing Workflow

### Step 1: Prepare Content
1. Start from `templates/wechat-template.html`
2. Replace placeholder text with article content
3. Ensure all images use mmbiz.qpic.cn URLs
4. Verify inline CSS only (no classes)

### Step 2: Inject Content into WeChat Editor
1. Navigate to WeChat article editor (mp.weixin.qq.com)
2. Set article title in the title field
3.5. Set author to "蜂启咨询" (Chinese company name)
4. Focus on the content editor
5. Inject content using **single paste operation** (see above)
6. Wait 2 seconds for editor to process
7. Run cleanup script to remove any separator nodes
8. Run image verification

### Step 3: Set Cover Image
1. Scroll to cover image section
2. Upload or select from image library
3. Verify cover image is set (not empty)

### Step 4: Set Summary
1. Fill in the summary field (120 chars max)
2. Use first paragraph or custom summary

### Step 5: Configure Article Settings
- Original declaration: As needed
- Comments: Enabled (auto-featured)
- Platform recommendation: Enabled

### Step 6: Save and Review
1. Click "Save as Draft"
2. Preview the article
3. Check for blank images or formatting issues
4. Verify all sections are present

### Step 7: Publish
1. Click "Publish" button
2. Confirm in the dialog
3. Scan QR code with WeChat app (admin/operator account)
4. Article will be published after verification

## Checklist (Run Before Every Publish)

- [ ] Content follows template structure (10 sections)
- [ ] All CSS is inline (no classes)
- [ ] All images on mmbiz.qpic.cn CDN
- [ ] No separator/blank image nodes
- [ ] Cover image is set
- [ ] Summary is filled (≤120 chars)
- [ ] Author is "蜂启咨询" (Chinese company name)
- [ ] Title is set correctly
- [ ] FAQ section included
- [ ] CTA section with company info
- [ ] Footer with copyright

## Common Issues and Fixes

### Blank Images in Article
**Cause**: Content injected in multiple chunks creates ProseMirror separator nodes
**Fix**: Run cleanup script after injection, or use single paste operation

### "图片不能为空" (Image Cannot Be Empty) Error
**Cause**: Cover image not properly set
**Fix**: Upload/select cover image in the cover section before publishing

### Editor Freezes During Injection
**Cause**: Content too large for single paste
**Fix**: Chunk content into 2-3 max (not 4+), run cleanup script after each chunk

### CSS Properties Stripped
**Cause**: WeChat strips unsupported CSS during publishing
**Fix**: Only use properties listed in the template header comments

### External Images Removed
**Cause**: WeChat removes non-CDN image URLs
**Fix**: Upload all images to WeChat CDN first, use mmbiz.qpic.cn URLs
