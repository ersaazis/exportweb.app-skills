---
name: exportweb-cms
description: >-
  Equips AI agents to operate, query, and update the ExportWeb B2B Exporter CMS platform via the Model Context Protocol (MCP).
  Includes 25 production tools for Assets/Media Upload, Products, Galleries, Articles, Buyer Inquiries/RFQs, Site Settings,
  11 Multilingual Locales, TinyMCE-Compatible Clean HTML, and Executive Dashboard.
---

# ExportWeb CMS Operator Skill

The `exportweb-cms` skill equips AI agents (including small-context models like Flash-Lite, Haiku, GPT-4o-mini, 8k-16k LLMs) to operate the **ExportWeb B2B Exporter Platform** via its embedded **Model Context Protocol (MCP)** JSON-RPC 2.0 server.

---

## ⚡ Quick-Card for Small-Context Models (Copy & Paste)

If you have a small context window, use this fast lookup table to know exactly what tool to call:

| Task / Goal | Tool to Call | Minimal Required Arguments |
| :--- | :--- | :--- |
| **Upload any Image/Asset** | `assets_upload` | `{"file_base64": "...", "filename": "sample.jpg", "category": "products"}` *(or `"source_url"`)* |
| **Create Export Product** | `products_create` | `{"name": "Grade A Coffee", "images": ["https://..."]}` *(slug is auto-generated)* |
| **Create Product (Inline Image)** | `products_create` | `{"name": "Grade A Coffee", "image_base64": "..."}` |
| **Publish B2B Article (Clean HTML)** | `articles_create` | `{"title": "Global Trade Guide", "content": "<h2>Standards</h2><p>...</p>", "cover_image": "https://..."}` |
| **Add Photo to Facility Gallery** | `galleries_create` | `{"title": "Factory Kiln Line", "image_url": "https://..."}` *(or `"image_base64"`)* |
| **Update Site Logo / Favicon** | `settings_update` | `{"logo_base64": "...", "favicon_base64": "..."}` *(old files auto-pruned)* |
| **Update Social Media & Contact** | `settings_update` | `{"whatsapp_number": "+628112345678", "linkedin": "https://linkedin.com/..."}` |
| **Update Localized SEO** | `settings_update` | `{"lang_code": "de", "seo_title": "ExportWeb Deutschland", "seo_description": "..."}` |
| **List Configured Languages** | `languages_list` | `{"enabled_only": false}` |
| **Toggle Export Language** | `languages_toggle` | `{"code": "ar", "is_enabled": true}` |
| **List Incoming Buyer RFQs** | `inquiries_list` | `{"status": "new", "limit": 10}` |
| **Update Buyer RFQ Status** | `inquiries_update_status` | `{"id": "inq_123", "status": "replied"}` |
| **Check Dashboard Volume** | `dashboard_stats` | `{}` |

---

## 🔑 The 5 Golden Rules for AI Models

1. **How to Handle Images (Two Easy Options)**:
   - **Option A (Recommended - 2 Steps)**: Call `assets_upload` first with `file_base64` or `source_url`. It returns a permanent public URL (e.g. `https://assets.exportweb.app/clients/{tenant}/...`). Then use that URL in `images`, `cover_image`, `image_url`, etc.
   - **Option B (One-Shot)**: Directly provide inline Base64 data inside `image_base64`, `images_base64`, `cover_image_base64`, `logo_base64`, or `favicon_base64`. The server uploads, optimizes, and links it in one request.
2. **Never Write Raw JSON Strings for Social Links (Rule 3)**:
   - **Do NOT** format social links as `{\"linkedin\":\"...\"}`.
   - **DO** pass individual keys directly: `"linkedin": "https://..."`, `"whatsapp": "+62..."`, `"instagram": "https://..."`, `"youtube": "https://..."`.
3. **Slugs are Automatic**:
   - You **do not** need to specify `slug` in `products_create` or `articles_create`. If omitted, the server automatically generates a clean, URL-safe slug from `name` or `title`.
4. **Automatic Storage Cleanup & Anti-Spam Lifecycle (Rule 5)**:
   - When you delete a product, gallery photo, or article, or replace a logo/favicon/cover, the server **automatically deletes the discarded image files from Cloudflare R2 / MinIO storage** and clears the website cache.
5. **Clean Semantic HTML & Anti-XSS Compliance**:
   - Always output clean, semantic HTML5 for rich text (`articles_create`, `articles_update`, and product descriptions). The backend sanitizes all markup via `SanitizeArticleHTML` before rendering in Tailwind `.prose`. Never send `<script>`, raw inline event handlers (`onclick`, `onerror`), or unapproved iframe embeds.

---

## 🌐 The 11 Standard Export Languages Matrix

ExportWeb features native subfolder routing (`/{lang}/...`) supporting **11 standardized international trade languages**. When calling `articles_create`, `articles_read`, `articles_update`, `settings_update`, or `languages_toggle`, use these official 2-letter ISO codes:

| Code | Language | Native Name | Script Direction | Default Status |
| :---: | :--- | :--- | :---: | :---: |
| **`en`** | English | English | LTR | **Primary Default** |
| **`id`** | Indonesian | Bahasa Indonesia | LTR | Enabled |
| **`es`** | Spanish | Español | LTR | Enabled |
| **`zh`** | Chinese Simplified | 简体中文 | LTR | Enabled |
| **`ar`** | Arabic | العربية | **RTL** | Enabled |
| **`fr`** | French | Français | LTR | Enabled |
| **`de`** | German | Deutsch | LTR | Enabled |
| **`ja`** | Japanese | 日本語 | LTR | Enabled |
| **`pt`** | Portuguese | Português | LTR | Enabled |
| **`ru`** | Russian | Русский | LTR | Enabled |
| **`vi`** | Vietnamese | Tiếng Việt | LTR | Enabled |

### Key Multilingual Rules:
1. **Universal Default (`en`)**: English is the universal master locale. When creating an article or product for the first time, provide high-quality English first (`lang_code: "en"`).
2. **Dedicated Subfolder Routing**: The platform serves localized versions at `/{lang}/blog/{slug}`, `/{lang}/products/{slug}`, etc.
3. **Arabic (`ar`) RTL Governance**: For Arabic content, output natural B2B terminology used in Middle Eastern trade (GCC/UAE/Saudi Arabia). The storefront layout automatically applies `<html dir="rtl">` and RTL flex/grid alignment for `/ar` routes.
4. **Localized SEO Isolation**: In `settings_update`, supply `lang_code` alongside `seo_title`, `seo_description`, `seo_keywords`, and `about_company` to store separate metadata for that specific market.

---

## 🖋️ Kerapihan HTML & Tailwind Typography (`.prose`) Standards

ExportWeb renders article bodies and product descriptions inside `<div class="prose prose-slate prose-lg max-w-none article-content">`. The platform utilizes `@tailwindcss/typography` to style clean semantic markup automatically.

### Clean HTML Structure Rules:
1. **Never use `<h1>` in Content**: The page title is already rendered as the unique `<h1>`. In `content`, always start main sections with `<h2>` and subsections with `<h3>` or `<h4>`.
2. **B2B Technical Specifications Table**: Always format technical parameters (proximate analysis, moisture, ash content, dimensions, packing) in clean semantic tables:
   ```html
   <table class="w-full text-left border-collapse">
     <thead>
       <tr>
         <th>Specification Parameter</th>
         <th>Testing Standard</th>
         <th>Guaranteed Range</th>
       </tr>
     </thead>
     <tbody>
       <tr>
         <td>Fixed Carbon</td>
         <td>ASTM D3172</td>
         <td>&gt;= 75.0% - 82.0%</td>
       </tr>
       <tr>
         <td>Total Moisture</td>
         <td>ISO 589</td>
         <td>&lt;= 5.0% Max</td>
       </tr>
     </tbody>
   </table>
   ```
3. **Paragraphs & Headings**: Wrap body paragraphs in `<p>...</p>`. Do NOT insert empty spacer tags like `<p>&nbsp;</p>` or `<br><br><br>`.
4. **Lists for Key Deliverables**: Use `<ul>` and `<ol>` with clean `<li>` items.
5. **Executive Callouts & Buyer Guarantees**: Use `<blockquote>` for plant director pledges, anti-fraud guarantees, or trade desk commitments:
   ```html
   <blockquote>
     <p>All export consignments undergo third-party laboratory verification (SGS/Sucofindo) prior to container seal surrender.</p>
   </blockquote>
   ```
6. **Images in Content**: Always include descriptive `alt` text and wrap images in `<figure>` with an optional `<figcaption>`:
   ```html
   <figure>
     <img src="https://assets.exportweb.app/clients/exportweb/articles/lab-testing.jpg" alt="Spectrometry proximate testing laboratory" loading="lazy" />
     <figcaption>Spectrometry proximate test for ash content verification.</figcaption>
   </figure>
   ```
7. **Responsive Video Embeds**: YouTube and Vimeo embeds must be wrapped cleanly:
   ```html
   <div class="aspect-video my-6">
     <iframe src="https://www.youtube.com/embed/dQw4w9WgXcQ" title="Factory walkthrough" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
   </div>
   ```

---

## 📁 Master File Upload & Asset Lifecycle Architecture

ExportWeb uses high-speed cloud object storage (**Cloudflare R2** / **MinIO** / **AWS S3**) partitioned by tenant: `clients/{tenantID}/{category}/{filename}`.

### 1. Two Upload Methods
- **Method A (Two-Step - Recommended)**: Call `assets_upload` first.
  - Returns permanent public URL: `https://assets.exportweb.app/clients/{tenantID}/products/briquette-hero.webp`
  - Reusable across products, galleries, articles, and settings.
- **Method B (One-Shot Inline Base64)**:
  - Directly pass Base64 string in `image_base64`, `images_base64`, `cover_image_base64`, `logo_base64`, `favicon_base64`, or `og_image_base64`.
  - Supports standard Base64 or Data URI format: `data:image/png;base64,iVBORw0KGgo...`.

### 2. Supported Categories
- `"branding"`: Logos, favicons, open-graph banners.
- `"products"`: Commodity photos, packaging shots, specification diagrams.
- `"gallery"`: Plant walkthroughs, kilns, laboratories, container stuffing docks.
- `"articles"`: Market intelligence covers, infographic charts, certificates.
- `"general"`: Miscellaneous tenant documents and assets.

### 3. Allowed File Extensions
`.jpg`, `.jpeg`, `.png`, `.webp`, `.svg`, `.gif`, `.avif`, `.pdf`.

### 4. Optimal Dimensions & Aspect Ratios
| Asset Type | Recommended Ratio | Ideal Dimensions | File Format | Max Recommended Size |
| :--- | :---: | :---: | :---: | :---: |
| **OpenGraph Banner** | 1.91 : 1 | `1200 x 630 px` | WebP / PNG / JPG | 1 MB |
| **Brand Logo** | Flexible | Vector or `512 x 512 px` | SVG / PNG (Transparent) | 500 KB |
| **Favicon** | 1 : 1 | `32x32`, `180x180` | ICO / SVG / PNG | 100 KB |
| **Product Photos** | 4 : 3 or 1 : 1 | `1200 x 900 px` | WebP / JPG | 2 MB |
| **Facility Gallery** | 16 : 9 or 4 : 3 | `1920 x 1080 px` | WebP / JPG | 3 MB |
| **Article Cover** | 16 : 9 | `1200 x 675 px` | WebP / JPG | 2 MB |
| **Technical Specs / COA** | Document | Standard A4 | PDF | 10 MB |

### 5. Automatic Storage Pruning (Rule 5 & Rule 13)
- When a product or gallery photo is deleted, all associated image files are automatically purged from R2/MinIO storage.
- When a brand logo, favicon, OG banner, or article cover is replaced, the previously stored file is deleted automatically to prevent bucket bloat.

---

## 🛡️ TinyMCE Rich Text Support & Anti-XSS Sanitization

ExportWeb integrates **TinyMCE 7** in the Admin Portal and protects all rich text using Go server-side sanitization (`service.SanitizeArticleHTML`). This allows rich editorial formatting while guaranteeing 100% protection against Stored Cross-Site Scripting (XSS).

### 1. Whitelisted HTML Tags
`p`, `br`, `h1`, `h2`, `h3`, `h4`, `h5`, `h6`, `strong`, `b`, `em`, `i`, `u`, `s`, `blockquote`, `ul`, `ol`, `li`, `a`, `img`, `pre`, `code`, `span`, `hr`, `table`, `thead`, `tbody`, `tr`, `th`, `td`, `figure`, `figcaption`, `div`, `caption`, `col`, `colgroup`, `iframe`.

### 2. Whitelisted Attributes
`href`, `src`, `alt`, `title`, `class`, `id`, `style`, `target`, `rel`, `width`, `height`, `frameborder`, `allow`, `allowfullscreen`, `loading`, `scope`.

### 3. Strict Iframe Embed Whitelist
Only trusted enterprise video embeds are permitted:
- **YouTube**: `https://www.youtube.com/embed/...` and `https://www.youtube-nocookie.com/embed/...`
- **Vimeo**: `https://player.vimeo.com/video/...`
*Any iframe with another source domain (e.g. arbitrary external sites, trackers) is stripped completely.*

### 4. Prohibited & Stripped XSS Vectors
The backend sanitizer automatically strips:
- Executable tags: `<script>`, `<style>`, `<object>`, `<embed>`, `<svg>`, `<math>`, HTML comments `<!-- -->`.
- All inline JavaScript event handlers: `onclick`, `onerror`, `onload`, `onmouseover`, `onfocus`, etc.
- Dangerous URL schemes: `javascript:`, `vbscript:`, `data:text/html`.
- Dangerous inline style properties: `expression(...)`, `url(data:...)`, `behavior:`.

### 5. Automatic Link Hardening
Whenever an anchor tag has `target="_blank"`, the backend automatically appends `rel="noopener noreferrer"` to prevent reverse tabnabbing attacks.

---

## 🔌 Connection & Authentication

### Endpoints
- **HTTP Remote (JSON-RPC 2.0)**: `POST https://exportweb.app/mcp` (or `http://localhost:8080/mcp` locally)
- **SSE Streaming**: `GET` / `POST https://exportweb.app/mcp/sse`

### Authentication Token (`ew_sec_...`)
Send your Bearer token in the HTTP header:
```http
Authorization: Bearer ew_sec_0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef
```
*(Or pass as URL query: `?token=ew_sec_...`)*

> [!CAUTION]
> **Strict Security Barrier**: Changing passwords, superadmin emails, or regenerating secret tokens is strictly forbidden via MCP and returns error code `-32601`. Those operations must be done by human admins in `/admin/account-settings`.

---

## 🛠️ The 25 MCP Tools Catalog

The ExportWeb MCP server provides **25 specialized tools** across 8 operational domains:

```text
1. Assets (1 tool)      : assets_upload
2. Products (5 tools)    : products_search, products_create, products_read, products_update, products_delete
3. Galleries (5 tools)   : galleries_search, galleries_create, galleries_read, galleries_update, galleries_delete
4. Articles (5 tools)    : articles_search, articles_create, articles_read, articles_update, articles_delete
5. Inquiries (4 tools)   : inquiries_list, inquiries_read, inquiries_update_status, inquiries_set_forwarding_email
6. Settings (2 tools)    : settings_get, settings_update
7. Languages (2 tools)   : languages_list, languages_toggle
8. Dashboard (1 tool)    : dashboard_stats
```

---

## 📋 6 Ready-to-Use Operator Workflows

### Workflow 1: Uploading an Image via Base64 or Remote URL
```json
{
  "name": "assets_upload",
  "arguments": {
    "file_base64": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=",
    "filename": "charcoal-briquette.png",
    "category": "products"
  }
}
```

### Workflow 2: Creating a Product with Clean Specifications & Image
```json
{
  "name": "products_create",
  "arguments": {
    "name": "Premium Coconut Charcoal Briquettes for Shisha",
    "category": "Commodities",
    "hs_code": "4402.90.10",
    "origin": "Semarang Port, Indonesia",
    "moq": "1x20ft FCL (18 MT)",
    "packing_detail": "1kg inner box with plastic liner, 10kg master carton",
    "supply_capacity": "300 MT / Month",
    "incoterms": "CIF, CFR, FOB",
    "description": "<h2>Technical Specification</h2><p>100% natural coconut shell briquettes engineered for clean, odorless burning.</p><table class=\"w-full\"><thead><tr><th>Metric</th><th>Guaranteed Value</th></tr></thead><tbody><tr><td>Fixed Carbon</td><td>Min 80%</td></tr><tr><td>Ash Content</td><td>Max 2.2%</td></tr><tr><td>Burning Time</td><td>2.5 - 3 Hours</td></tr></tbody></table>",
    "images": [
      "https://assets.exportweb.app/clients/exportweb/products/charcoal-briquette.png"
    ],
    "is_featured": true,
    "is_active": true
  }
}
```

### Workflow 3: Publishing an SEO Market Intelligence Article with Clean HTML
```json
{
  "name": "articles_create",
  "arguments": {
    "title": "How International Importers Authenticate Coconut Shell Briquette Quality",
    "category": "Market Intelligence",
    "excerpt": "A technical procurement guide on ash content, drop test durability, and DG 4.2 shipping compliance.",
    "content": "<h2>Laboratory Quality Standards</h2><p>Enterprise buyers prioritize ASTM D3172 proximate testing before authorizing Irrevocable Letters of Credit.</p><blockquote><p>Never accept consignments without certified SHT (Self-Heating Test) and DG 4.2 classification reports.</p></blockquote><h2>Key Inspection Criteria</h2><ul><li><strong>Ash Color:</strong> Pure white to silver grey without chemical odor.</li><li><strong>Drop Test:</strong> Zero fracture when dropped 3 times from 1-meter height onto concrete.</li></ul><div class=\"aspect-video my-6\"><iframe src=\"https://www.youtube.com/embed/dQw4w9WgXcQ\" title=\"Lab Testing Protocol\" allowfullscreen></iframe></div>",
    "cover_image": "https://assets.exportweb.app/clients/exportweb/articles/lab-inspection.jpg",
    "author": "Chief Export Specialist",
    "meta_title": "How Importers Authenticate Briquette Quality | ExportWeb",
    "meta_description": "Technical guide on verifying ash content, volatile matter, and container stuffing certifications.",
    "meta_keywords": "charcoal briquettes, export quality, laboratory testing, ASTM D3172",
    "lang_code": "en"
  }
}
```

### Workflow 4: Adding a Factory Photo to the Gallery
```json
{
  "name": "galleries_create",
  "arguments": {
    "title": "Continuous Hydraulic Briquette Extrusion Line",
    "image_url": "https://assets.exportweb.app/clients/exportweb/gallery/hydraulic-press.jpg",
    "category": "Facility",
    "description": "High-density continuous press with automated temperature and moisture sensors.",
    "sort_order": 1
  }
}
```

### Workflow 5: Updating Discrete Socials, Contact & Localized SEO
```json
{
  "name": "settings_update",
  "arguments": {
    "company_name": "PT ExportWeb Nusantara",
    "company_profile": "Leading Indonesian manufacturer of certified coconut shell charcoal and biomass products.",
    "whatsapp_number": "+628112345678",
    "linkedin": "https://linkedin.com/company/exportweb",
    "youtube": "https://youtube.com/@exportweb",
    "office_address": "Export Tower Level 18, Jakarta, Indonesia",
    "factory_address": "Kendal Industrial Estate Block B2, Central Java, Indonesia",
    "lang_code": "de",
    "seo_title": "ExportWeb Deutschland - Hochwertige Kokosnuss-Briketts",
    "seo_description": "Führender indonesischer Exporteur für B2B Shisha- und Grill-Holzkohlebriketts.",
    "about_company": "PT ExportWeb Nusantara liefert zertifizierte Shisha-Briketts direkt ab Werk nach Europa."
  }
}
```

### Workflow 6: Managing 11 Languages (List & Toggle)
```json
// 1. List configured languages
{
  "name": "languages_list",
  "arguments": {
    "enabled_only": false
  }
}

// 2. Activate Arabic locale (RTL)
{
  "name": "languages_toggle",
  "arguments": {
    "code": "ar",
    "is_enabled": true
  }
}
```

---

## ⚠️ Common Error Codes & Self-Healing Guide

| Status Code | Message | How to Fix |
| :--- | :--- | :--- |
| **HTTP 401** | `Unauthorized: missing or invalid token` | Check `Authorization: Bearer ew_sec_...`. Copy the active token from `/admin/account-settings`. |
| **HTTP 405** | `Method Not Allowed: MCP JSON-RPC requires POST` | Always send HTTP `POST` requests, never `GET`. |
| **JSON-RPC `-32601`** | `Operation forbidden: Administrative security credentials...` | Do not call `change_password` or `reset_secret_token` via MCP. |
| **JSON-RPC `-32602`** | `Invalid params` | Check that required fields (e.g. `name` for products, `title` and `content` for articles) are provided. |
| **Tool Error** | `Dangerous or unsupported file extension` | Supported extensions: `.jpg`, `.jpeg`, `.png`, `.webp`, `.svg`, `.gif`, `.avif`, `.pdf`. |

---

## 📚 Complete Technical Documentation
For full parameter specifications and database schemas across all 25 tools, see [`references/tools_reference.md`](references/tools_reference.md).
