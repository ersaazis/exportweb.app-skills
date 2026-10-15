---
name: exportweb-cms
description: >-
  Equips AI agents to operate, query, and update the ExportWeb B2B Exporter CMS platform via the Model Context Protocol (MCP).
  Includes 25 production tools for Assets/Media Upload, Products, Galleries, Articles, Buyer Inquiries/RFQs, Site Settings, Multilingual Locales, and Executive Dashboard.
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
| **Publish B2B Article** | `articles_create` | `{"title": "Global Trade Guide", "content": "# Overview...", "cover_image": "https://..."}` |
| **Add Photo to Facility Gallery** | `galleries_create` | `{"title": "Factory Kiln Line", "image_url": "https://..."}` *(or `"image_base64"`)* |
| **Update Site Logo / Favicon** | `settings_update` | `{"logo_base64": "...", "favicon_base64": "..."}` *(old files auto-pruned)* |
| **Update Social Media & Contact** | `settings_update` | `{"whatsapp_number": "+628112345678", "linkedin": "https://linkedin.com/..."}` |
| **Update Localized SEO** | `settings_update` | `{"lang_code": "de", "seo_title": "ExportWeb Deutschland", "seo_description": "..."}` |
| **List Incoming Buyer RFQs** | `inquiries_list` | `{"status": "new", "limit": 10}` |
| **Update Buyer RFQ Status** | `inquiries_update_status` | `{"id": "inq_123", "status": "replied"}` |
| **Check Dashboard Volume** | `dashboard_stats` | `{}` |

---

## 🔑 The 4 Golden Rules for AI Models

1. **How to Handle Images (Two Easy Options)**:
   - **Option A (Recommended - 2 Steps)**: Call `assets_upload` first with `file_base64` or `source_url`. It returns a permanent public URL (e.g. `https://assets.exportweb.app/...`). Then use that URL in `images`, `cover_image`, `image_url`, etc.
   - **Option B (One-Shot)**: Directly provide inline Base64 data inside `image_base64`, `images_base64`, `cover_image_base64`, `logo_base64`, or `favicon_base64`. The server uploads and links it in one request.
2. **Never Write Raw JSON Strings for Social Links (Rule 3)**:
   - **Do NOT** format social links as `{\"linkedin\":\"...\"}`.
   - **DO** pass individual keys directly: `"linkedin": "https://..."`, `"whatsapp": "+62..."`, `"instagram": "https://..."`, `"youtube": "https://..."`.
3. **Slugs are Automatic**:
   - You **do not** need to specify `slug` in `products_create` or `articles_create`. If omitted, the server automatically generates a clean, URL-safe slug from `name` or `title`.
4. **Automatic Storage Cleanup (Rule 5)**:
   - When you delete a product, gallery photo, or article, or replace a logo/favicon, the server **automatically deletes the discarded image files from Cloudflare R2 / MinIO storage** and clears the website cache.

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

## 📋 5 Ready-to-Use Operator Workflows

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
*Returns:*
```json
{
  "status": "uploaded",
  "url": "https://assets.exportweb.app/clients/exportweb/products/charcoal-briquette.png",
  "key": "clients/exportweb/products/charcoal-briquette.png"
}
```

### Workflow 2: Creating a Product with Specifications & Image
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
    "description": "100% natural coconut shell briquettes with 2.2% max ash, 80% fixed carbon, and 2.5-hour burn time.",
    "images": [
      "https://assets.exportweb.app/clients/exportweb/products/charcoal-briquette.png"
    ],
    "is_featured": true,
    "is_active": true
  }
}
```

### Workflow 3: Publishing an SEO Market Intelligence Article
```json
{
  "name": "articles_create",
  "arguments": {
    "title": "How International Importers Authenticate Coconut Shell Briquette Quality",
    "category": "Market Intelligence",
    "excerpt": "A technical procurement guide on ash content, drop test durability, and DG 4.2 shipping compliance.",
    "content": "# Laboratory Quality Standards\n\nEnterprise buyers prioritize ASTM D3172 proximate testing...",
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

### Workflow 5: Updating Corporate Branding, Social Channels & Localized SEO
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
    "about_company": "PT ExportWeb Nusantara liefert zertifizierte Shisha-Briketts direkt ab Werk."
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
