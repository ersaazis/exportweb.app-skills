---
name: exportweb-cms
description: >-
  Equips AI agents to operate, query, and update the ExportWeb B2B Exporter CMS platform via the Model Context Protocol (MCP).
  Includes 24 production tools for Products, Galleries, Articles, Buyer Inquiries/RFQs, Site Settings, Multilingual Locales, and Executive Dashboard.
---

# ExportWeb CMS Operator Skill

The `exportweb-cms` skill enables AI coding agents and autonomous operators to seamlessly manage content, commodities, media galleries, buyer inquiries, multilingual localization, and corporate settings on the **ExportWeb B2B Exporter Platform** via the native Go **Model Context Protocol (MCP)** server.

---

## 🎯 Purpose & Scope

This skill is designed for **AI Agent Operators** who need to:
1. **Manage Export Catalog**: Search, create, update, and remove export commodities, technical specifications, HS codes, packaging data, and container stuffing capacities.
2. **Curate Visual Proof & Facility Galleries**: Add and organize high-resolution photography of kilns, autoclaves, processing plants, container loading bays, and laboratory certificates.
3. **Publish Market Intelligence**: Author, edit, and localize search-optimized export intelligence articles (AIDA framework) to attract international importers.
4. **Triage Buyer Inquiries & Leads**: Fetch international buyer RFQs, inspect inquiry details, update follow-up statuses, and configure lead notification forwarding emails.
5. **Govern Site Identity & SEO**: Update corporate descriptions, physical plant addresses, WhatsApp trade desks, Google Maps embeds, and localized SEO titles/descriptions.
6. **Control Multilingual Locales**: Inspect and toggle the 11 supported international languages (`en`, `id`, `es`, `zh`, `ar`, `fr`, `de`, `ja`, `pt`, `ru`, `vi`).
7. **Monitor Real-time Dashboard**: Retrieve live catalog counts, inquiry pipelines, and storage metrics.

---

## 🔌 Connection & Authentication

The ExportWeb MCP server is natively embedded in the platform backend and exposes standard JSON-RPC 2.0 and Server-Sent Events (SSE) endpoints.

### Endpoints
- **HTTP Remote (JSON-RPC 2.0)**: `POST https://exportweb.app/mcp` (or `http://localhost:8080/mcp` in local development)
- **SSE Streaming**: `GET` / `POST https://exportweb.app/mcp/sse`

### Authentication Token (`ew_sec_...`)
All MCP requests require a cryptographic Bearer token:
```http
Authorization: Bearer ew_sec_0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef
```

#### How to Obtain or Rotate Your Token:
1. Log in to the ExportWeb Admin Panel: `/admin/login`
2. Navigate to **Account Setting** (`/admin/account-settings`).
3. Locate the **Model Context Protocol (MCP) Secret Token** card.
4. Copy the active token, or click **Reset Secret Token** to rotate credentials if compromised.

> [!CAUTION]
> **Strict Security Barrier**: The MCP protocol strictly isolates access to the authenticated administrator's `tenant_id`. Calls to modify user passwords, reset tokens, or access credentials via MCP are intercepted and rejected with error code `-32601` (`Operation forbidden`). Password and token rotations MUST be performed by a human in `/admin/account-settings`.

---

## 🛠️ The 24 MCP Tools Overview

The ExportWeb MCP server provides **24 specialized tools** divided into 7 operational domains:

| Domain | Available Tools | Description |
| :--- | :--- | :--- |
| **1. Products** (5 tools) | `products_search`, `products_create`, `products_read`, `products_update`, `products_delete` | Complete CRUD for export products, HS codes, MOQ, packaging specs, and hero images. |
| **2. Galleries** (5 tools) | `galleries_search`, `galleries_create`, `galleries_read`, `galleries_update`, `galleries_delete` | Curate verified facility, processing kiln, loading bay, and laboratory testing photos. |
| **3. Articles** (5 tools) | `articles_search`, `articles_create`, `articles_read`, `articles_update`, `articles_delete` | High-converting export intelligence articles with multilingual SEO metadata tags. |
| **4. Inquiries** (4 tools) | `inquiries_list`, `inquiries_read`, `inquiries_update_status`, `inquiries_set_forwarding_email` | Buyer lead management, inquiry triage (`new`, `replied`, `closed`), and notification email routing. |
| **5. Settings** (2 tools) | `settings_get`, `settings_update` | Tenant profile, WhatsApp trade desk, physical coordinates, social links, and SEO tags. |
| **6. Languages** (2 tools) | `languages_list`, `languages_toggle` | Audit and activate/deactivate supported language subfolders (`/en`, `/id`, `/zh`, etc.). |
| **7. Dashboard** (1 tool) | `dashboard_stats` | Live system overview: product count, active articles, total leads, and server version. |

> 📖 **For exhaustive argument schemas and return types, see [`references/tools_reference.md`](references/tools_reference.md)**.

---

## 📋 Standard Operator Workflows

### Workflow 1: Inspecting & Updating a Product Specification
When asked to update pricing terms, HS code, or description for an export commodity:

1. **Search or Read Product**:
   ```json
   {
     "name": "products_search",
     "arguments": { "query": "charcoal briquette" }
   }
   ```
2. **Fetch Full Details**:
   ```json
   {
     "name": "products_read",
     "arguments": { "slug": "premium-shisha-charcoal-briquettes" }
   }
   ```
3. **Execute Update**:
   ```json
   {
     "name": "products_update",
     "arguments": {
       "id": "prod_abc123",
       "hs_code": "4402.90.10",
       "incoterms": "FOB, CIF, CFR",
       "supply_capacity": "300 Metric Tons / Month",
       "moq": "1x20ft FCL (18 MT)"
     }
   }
   ```

### Workflow 2: Publishing an Export Intelligence Article
To publish a B2B educational article that boosts organic search traffic:

1. **Verify Existing Slugs**:
   ```json
   {
     "name": "articles_search",
     "arguments": { "query": "importer evaluation" }
   }
   ```
2. **Create Article with Complete SEO Metadata**:
   ```json
   {
     "name": "articles_create",
     "arguments": {
       "title": "How Global B2B Buyers Evaluate Overseas Suppliers in 2026",
       "slug": "how-global-b2b-buyers-evaluate-overseas-suppliers-in-2026",
       "category": "Market Intelligence",
       "excerpt": "Discover the 5 critical digital trust checkpoints international importers inspect before requesting samples.",
       "content": "# The Digital Procurement Shift\n\nInternational buyers prioritize verified laboratory tests...",
       "author": "Chief Export Specialist",
       "is_published": true,
       "meta_title": "How Global B2B Buyers Evaluate Overseas Suppliers in 2026 | ExportWeb",
       "meta_description": "Comprehensive guide on how global enterprise importers evaluate suppliers and authenticate certifications.",
       "meta_keywords": "B2B procurement, export intelligence, supplier evaluation, international trade",
       "lang_code": "en"
     }
   }
   ```

### Workflow 3: Adding Verified Facility Media to Gallery
To showcase trust and plant infrastructure to prospective buyers:

1. **Verify Asset URL**: Confirm the image is hosted on an accessible HTTPS endpoint (such as Cloudflare R2 or CDN).
2. **Create Gallery Item**:
   ```json
   {
     "name": "galleries_create",
     "arguments": {
       "title": "Automatic Hydraulic Briquetting Press Line",
       "image_url": "https://assets.exportweb.app/clients/exportweb/facility-press-01.webp",
       "category": "Facility",
       "description": "Continuous high-density extrusion line with automated moisture regulation.",
       "sort_order": 10
     }
   }
   ```

### Workflow 4: Triaging Buyer Leads & Configuring Notifications
1. **List Pending Inquiries**:
   ```json
   {
     "name": "inquiries_list",
     "arguments": { "status": "new", "limit": 10 }
   }
   ```
2. **Inspect Specific Buyer RFQ**:
   ```json
   {
     "name": "inquiries_read",
     "arguments": { "id": "inq_xyz789" }
   }
   ```
3. **Mark Inquiry as Replied**:
   ```json
   {
     "name": "inquiries_update_status",
     "arguments": { "id": "inq_xyz789", "status": "replied" }
   }
   ```
4. **Update Sales Inbox Forwarding Email**:
   ```json
   {
     "name": "inquiries_set_forwarding_email",
     "arguments": { "email": "trade-desk@exportweb.app" }
   }
   ```

### Workflow 5: Updating Site Branding, Coordinates & Social Links
1. **Fetch Current Settings**:
   ```json
   {
     "name": "settings_get",
     "arguments": { "lang_code": "en" }
   }
   ```
2. **Update Profile & Social Channels**:
   ```json
   {
     "name": "settings_update",
     "arguments": {
       "company_name": "ExportWeb International",
       "whatsapp_number": "+628112345678",
       "phone_number": "+62215550199",
       "office_address": "Export Tower Level 18, Jakarta, Indonesia",
       "factory_address": "Kawasan Industri Kendal, Central Java, Indonesia",
       "social_links": "{\"linkedin\":\"https://linkedin.com/company/exportweb\",\"youtube\":\"https://youtube.com/@exportweb\"}"
     }
   }
   ```

---

## 🌐 Asset & URL Policy

When submitting image URLs to `products_create`, `products_update`, `galleries_create`, or `settings_update`:
- **Use Fully Qualified HTTPS URLs**: All assets should be hosted on a fast CDN or Cloud Bucket (e.g. `https://assets.exportweb.app/...`).
- **Standard Image Formats**: Prefer WebP, AVIF, JPEG, or PNG.
- **Zero Local File Paths**: Never pass local paths (`/tmp/...`, `file://...`, `C:\...`) to MCP arguments.

---

## ⚠️ Error Handling & Troubleshooting

| Status Code / Error | Likely Cause | Resolution |
| :--- | :--- | :--- |
| **HTTP 401 Unauthorized** | Missing or invalid Bearer token. | Check `Authorization: Bearer ew_sec_...` header. Generate a fresh token in `/admin/account-settings`. |
| **HTTP 405 Method Not Allowed** | Request used `GET` on `/mcp`. | Send JSON-RPC requests via `POST` with `Content-Type: application/json`. |
| **JSON-RPC `-32601` Operation forbidden** | Attempted to modify credentials (`change_password`, `reset_secret_token`). | Credential operations are locked out of MCP by design. Perform them via the Web UI. |
| **JSON-RPC `-32602` Invalid params** | Required fields missing or wrong data types. | Consult [`references/tools_reference.md`](references/tools_reference.md) for required keys and formats. |
| **Record Not Found** | Target ID or slug does not exist for this tenant. | Run corresponding search tool (`products_search`, `articles_search`) to retrieve valid IDs. |

---

## 📚 References & Resources
- Complete Tool Schemas: [`references/tools_reference.md`](references/tools_reference.md)
- HTTP Configuration Preset: [`examples/mcp_config_http.json`](examples/mcp_config_http.json)
- SSE Configuration Preset: [`examples/mcp_config_sse.json`](examples/mcp_config_sse.json)
- Sample Payloads: [`examples/sample_payloads.json`](examples/sample_payloads.json)
- Verification CLI: [`scripts/test_connection.py`](scripts/test_connection.py)
