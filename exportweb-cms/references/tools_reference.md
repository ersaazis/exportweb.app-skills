# ExportWeb MCP Tools Reference Guide

This document provides exhaustive technical specifications for all **25 tools** exposed by the ExportWeb Go Model Context Protocol (MCP) server.

All tool invocations follow the **JSON-RPC 2.0** format:
```json
{
  "jsonrpc": "2.0",
  "id": "msg_001",
  "method": "tools/call",
  "params": {
    "name": "<TOOL_NAME>",
    "arguments": { ... }
  }
}
```

---

## 🖼️ 1. Assets & Media Storage Tools

Tools to upload and store high-resolution B2B photography, plant walkthroughs, and branding assets to Cloudflare R2 / MinIO storage.

### `assets_upload`
Upload an image or asset file to storage via inline Base64 data or remote URL fetch.
- **Parameters**:
  - `file_base64` *(string, optional)*: Base64-encoded string of the file (supports raw base64 or `data:<mime>;base64,...` URI).
  - `source_url` *(string, optional)*: Remote HTTP/HTTPS URL to download, optimize, and ingest into storage.
  - `filename` *(string, optional)*: Desired filename (e.g. `"autoclave-01.webp"`, `"brand-logo.svg"`). Auto-derived if omitted.
  - `category` *(string, optional)*: Target category folder:
    - `"branding"`: Logos, browser favicons, OpenGraph social preview banners.
    - `"products"`: Export commodity photos, technical packaging diagrams.
    - `"gallery"`: Production facilities, kilns, autoclaves, quality control laboratories, container stuffing docks.
    - `"articles"`: Market intelligence covers, technical infographics, certification scans.
    - `"general"`: Miscellaneous client documents, technical spec PDFs (default: `"general"`).
  - `content_type` *(string, optional)*: Explicit MIME type. Auto-detected from bytes or extension if omitted.
- **Allowed File Extensions**:
  - Images: `.jpg`, `.jpeg`, `.png`, `.webp`, `.svg`, `.gif`, `.avif`.
  - Documents: `.pdf`.
- **Optimal Image Dimensions & Ratios**:
  - *OpenGraph Banner*: `1200 x 630 px` (1.91:1 ratio, max 1MB).
  - *Brand Logo*: Vector SVG or `512 x 512 px` transparent PNG (max 500KB).
  - *Browser Favicon*: `32x32`, `180x180 px` (`.ico`, `.png`, `.svg`, max 100KB).
  - *Product Catalog*: `1200 x 900 px` (4:3) or `1000 x 1000 px` (1:1) (max 2MB).
  - *Facility Gallery*: `1920 x 1080 px` (16:9) or `1200 x 900 px` (4:3) (max 3MB).
  - *Article Cover*: `1200 x 675 px` (16:9) (max 2MB).
- **Returns**: Object with:
  - `status`: `"uploaded"`
  - `url`: Permanent public asset HTTPS URL (`https://assets.exportweb.app/clients/{tenant}/...`).
  - `key`: S3/R2 object storage key (`clients/{tenant}/{category}/{filename}`).
  - `filename`: Clean sanitized filename.
  - `category`: Storage category.

---

## 📦 2. Products & Commodities Tools

Manage product offerings, technical specifications, and international export trade parameters.

### `products_search`
Search products and export service packages by keyword, category, or status.
- **Parameters**:
  - `query` *(string, optional)*: Keyword to match against product name, category, or description.
  - `category` *(string, optional)*: Filter by category (e.g., `"Commodities"`, `"Services"`).
  - `is_active` *(boolean, optional)*: Filter by active status (`true` / `false`).
- **Returns**: Array of product summary objects.

### `products_create`
Register a new product or export package in the catalog.
- **Parameters**:
  - `name` *(string, **required**)*: Product title (e.g. `"Premium Coconut Charcoal Briquettes"`).
  - `slug` *(string, optional)*: Unique URL slug. Automatically generated from `name` if omitted.
  - `category` *(string, optional)*: Category designation (defaults to `"General"`).
  - `hs_code` *(string, optional)*: Harmonized System tariff code (e.g. `"4402.90.10"`).
  - `origin` *(string, optional)*: Country of origin or load port (e.g. `"Semarang, Indonesia"`).
  - `moq` *(string, optional)*: Minimum Order Quantity (e.g. `"1x20ft FCL (18 MT)"`).
  - `packing_detail` *(string, optional)*: Packaging details (e.g. `"10kg master carton with inner plastic liner"`).
  - `supply_capacity` *(string, optional)*: Monthly production capacity (e.g. `"300 Metric Tons / Month"`).
  - `incoterms` *(string, optional)*: Supported trade terms (e.g. `"FOB, CIF, CFR, EXW"`).
  - `description` *(string, optional)*: Detailed product specifications and descriptions.
    - *HTML Formatting Standard*: Supports clean semantic HTML5 rendered inside Tailwind `.prose`. Wrap sections in `<h2>`, `<h3>`, `<p>`, `<ul>`, and specification tables (`<table>`, `<thead>`, `<tbody>`).
    - *Anti-XSS Sanitization*: Automatically cleaned via `SanitizeArticleHTML`. Scripts, styles, and unsafe event handlers are stripped.
  - `images` *(array of string, optional)*: Array of HTTPS URLs for product photographs.
  - `images_base64` *(array of string/objects, optional)*: Inline Base64 image data to auto-upload to storage.
  - `image_base64` *(string, optional)*: Single inline Base64 image to auto-upload.
  - `source_url` *(string, optional)*: Remote image URL to download and ingest into storage.
  - `is_featured` *(boolean, optional)*: Whether to feature the item on the storefront home.
  - `is_active` *(boolean, optional)*: Active status in catalog (default: `true`).
- **Returns**: Object with created product ID, slug, and status.

### `products_read`
Retrieve full product details, specifications, and images by ID or slug.
- **Parameters**:
  - `id` *(string, optional)*: Product ID (e.g. `"prod_abc123"`).
  - `slug` *(string, optional)*: Product URL slug (e.g. `"premium-coconut-charcoal-briquettes"`).
  *(At least one identifier must be provided)*
- **Returns**: Full product object with localized translations.

### `products_update`
Update specifications or status of an existing product.
- **Parameters**:
  - `id` *(string, **required**)*: Product ID to update.
  - `name` *(string, optional)*: Updated product name.
  - `slug` *(string, optional)*: Updated URL slug.
  - `category` *(string, optional)*: Updated category.
  - `hs_code` *(string, optional)*: Updated HS Code.
  - `origin` *(string, optional)*: Updated origin.
  - `moq` *(string, optional)*: Updated MOQ.
  - `packing_detail` *(string, optional)*: Updated packing details.
  - `supply_capacity` *(string, optional)*: Updated monthly supply volume.
  - `incoterms` *(string, optional)*: Updated Incoterms.
  - `description` *(string, optional)*: Updated description text (sanitized via `SanitizeArticleHTML`).
  - `images` *(array of string, optional)*: Updated list of image URLs.
  - `images_base64` *(array, optional)*: New Base64 images to upload and append.
  - `source_url` *(string, optional)*: Remote image URL to download and append.
  - `is_featured` *(boolean, optional)*: Updated featured flag.
  - `is_active` *(boolean, optional)*: Updated active status.
- **Returns**: Updated product status.

### `products_delete`
Permanently remove a product from the catalog. Automatically prunes all associated image assets from Cloudflare R2 / MinIO storage and invalidates storefront cache.
- **Parameters**:
  - `id` *(string, **required**)*: Product ID to remove.
- **Returns**: Success confirmation.

---

## 🖼️ 3. Facility & Media Galleries Tools

Curate visual proof of factory facilities, machinery, laboratory tests, and container stuffing.

### `galleries_search`
Search photo documentation by title, category, or description.
- **Parameters**:
  - `query` *(string, optional)*: Keyword query.
  - `category` *(string, optional)*: Category filter (e.g. `"Facility"`, `"Loading"`, `"Testing"`).
- **Returns**: Array of gallery items.

### `galleries_create`
Add a verified photo or facility asset to the gallery.
- **Parameters**:
  - `title` *(string, **required**)*: Asset title (e.g. `"Automated Kiln Battery #3"`).
  - `image_url` *(string, optional)*: Public HTTPS asset URL (or provide `image_base64` / `source_url`).
  - `image_base64` *(string, optional)*: Inline Base64 image data to auto-upload to storage.
  - `source_url` *(string, optional)*: Remote image URL to download and ingest into storage.
  - `filename` *(string, optional)*: Custom filename for uploaded asset.
  - `category` *(string, optional)*: Categorization (e.g. `"Facility"`, `"Loading"`, `"Lab"`).
  - `description` *(string, optional)*: Technical caption or description.
  - `sort_order` *(integer, optional)*: Numeric display order (default `0`).
- **Returns**: Created gallery item ID and status.

### `galleries_read`
Retrieve gallery item details.
- **Parameters**:
  - `id` *(string, **required**)*: Gallery item ID.
- **Returns**: Gallery item record.

### `galleries_update`
Update title, caption, sort order, or image URL of an existing photo. Automatically prunes previous image from storage if replaced with a new one.
- **Parameters**:
  - `id` *(string, **required**)*: Gallery ID to update.
  - `title` *(string, optional)*: New title.
  - `image_url` *(string, optional)*: New image URL.
  - `image_base64` *(string, optional)*: New Base64 image to upload.
  - `source_url` *(string, optional)*: Remote image URL to download and replace existing.
  - `category` *(string, optional)*: New category.
  - `description` *(string, optional)*: New description.
  - `sort_order` *(integer, optional)*: New sort sequence.
- **Returns**: Updated record status.

### `galleries_delete`
Delete a gallery photo record. Automatically prunes the photo asset from Cloudflare R2 / MinIO storage and clears storefront cache.
- **Parameters**:
  - `id` *(string, **required**)*: Gallery ID to delete.
- **Returns**: Confirmation.

---

## 📰 4. Articles & Market Intelligence Tools

Publish international B2B educational articles and maintain multi-language SEO rankings.

### `articles_search`
Search market intelligence articles by keyword or category.
- **Parameters**:
  - `query` *(string, optional)*: Search keyword.
  - `category` *(string, optional)*: Category filter (e.g. `"Export Guide"`, `"Industry Trends"`).
  - `is_published` *(boolean, optional)*: Publication status (`true` / `false`).
  - `lang_code` *(string, optional)*: Language code (default: `"en"`).
- **Returns**: List of article summaries matching query.

### `articles_create`
Publish a new export intelligence article with complete metadata.
- **Parameters**:
  - `title` *(string, **required**)*: Article headline.
  - `slug` *(string, optional)*: URL slug. Auto-generated from `title` if omitted.
  - `content` *(string, **required**)*: Clean semantic HTML or Markdown body:
    - *TinyMCE Compatibility*: Styled automatically via Tailwind `.prose`. Use `<h2>`, `<h3>`, `<p>`, `<ul>`, `<ol>`, `<blockquote>`, `<table>`, `<figure>`, `<figcaption>`.
    - *Whitelisted Tags*: `p, br, h1-h6, strong, b, em, i, u, s, blockquote, ul, ol, li, a, img, pre, code, span, hr, table, thead, tbody, tr, th, td, figure, figcaption, div, caption, col, colgroup, iframe`.
    - *Whitelisted Attributes*: `href, src, alt, title, class, id, style, target, rel, width, height, frameborder, allow, allowfullscreen, loading, scope`.
    - *Iframe Whitelist*: YouTube (`youtube.com/embed/`, `youtube-nocookie.com/embed/`) and Vimeo (`player.vimeo.com/video/`). Untrusted iframes are stripped.
    - *Automatic Anti-XSS*: Strips `<script>`, `<style>`, `<object>`, `<embed>`, `<svg>`, `<math>`, comments, `on*` events, and `javascript:` URLs. Forces `rel="noopener noreferrer"` on `target="_blank"`.
  - `excerpt` *(string, optional)*: Executive summary / lead paragraph.
  - `category` *(string, optional)*: Article category (e.g. `"Market Intelligence"`, `"Export Compliance"`).
  - `cover_image` *(string, optional)*: Feature image HTTPS URL.
  - `cover_image_base64` *(string, optional)*: Inline Base64 image data to auto-upload as cover.
  - `source_url` *(string, optional)*: Remote image URL to download and set as cover.
  - `author` *(string, optional)*: Author byline.
  - `is_published` *(boolean, optional)*: Published flag (default: `true`).
  - `meta_title` *(string, optional)*: SEO title tag (under 60 characters).
  - `meta_description` *(string, optional)*: SEO meta description (under 160 characters).
  - `meta_keywords` *(string, optional)*: Comma-separated keyword string.
  - `lang_code` *(string, optional)*: Target language locale from the 11 supported languages (`"en"`, `"id"`, `"es"`, `"zh"`, `"ar"`, `"fr"`, `"de"`, `"ja"`, `"pt"`, `"ru"`, `"vi"`, default: `"en"`).
- **Returns**: Created article record.

### `articles_read`
Retrieve article content and SEO metadata by ID or slug.
- **Parameters**:
  - `id` *(string, optional)*: Article ID.
  - `slug` *(string, optional)*: Article slug.
  - `lang_code` *(string, optional)*: Desired language locale (default: `"en"`).
- **Returns**: Article full content and metadata.

### `articles_update`
Update body content, SEO metadata, or publish status of an article. Automatically prunes old cover image from storage if replaced.
- **Parameters**:
  - `id` *(string, **required**)*: Article ID.
  - `title` *(string, optional)*: Updated headline.
  - `slug` *(string, optional)*: Updated slug.
  - `cover_image` *(string, optional)*: New cover image URL.
  - `cover_image_base64` *(string, optional)*: New Base64 image to upload as cover.
  - `source_url` *(string, optional)*: Remote image URL to download as cover.
  - `content` *(string, optional)*: Updated clean HTML content (sanitized via `SanitizeArticleHTML`).
  - `excerpt` *(string, optional)*: Updated excerpt.
  - `category` *(string, optional)*: Updated category.
  - `author` *(string, optional)*: Updated author name.
  - `is_published` *(boolean, optional)*: Updated publish status.
  - `meta_title` *(string, optional)*: Updated SEO title.
  - `meta_description` *(string, optional)*: Updated SEO meta description.
  - `meta_keywords` *(string, optional)*: Updated SEO keywords.
  - `lang_code` *(string, optional)*: Target language locale.
- **Returns**: Updated article record.

### `articles_delete`
Delete an article and all its localized versions. Automatically prunes cover images from storage.
- **Parameters**:
  - `id` *(string, **required**)*: Article ID to delete.
- **Returns**: Confirmation.

---

## 📬 5. Buyer Inquiries & Leads Tools

Monitor international buyer RFQs, triage inquiries, and direct notification routing.

### `inquiries_list`
Fetch buyer inquiries with optional status filtering.
- **Parameters**:
  - `query` *(string, optional)*: Search buyer name, email, or company.
  - `status` *(string, optional)*: Filter by status: `"new"`, `"replied"`, `"closed"`.
  - `page` *(integer, optional)*: Pagination page (default: `1`).
  - `limit` *(integer, optional)*: Page limit (default: `50`).
- **Returns**: List of inquiry records with metadata and pagination counters.

### `inquiries_read`
Inspect full details of a specific buyer inquiry.
- **Parameters**:
  - `id` *(string, **required**)*: Inquiry ID (e.g. `"inq_123"`).
- **Returns**: Full inquiry details including contact info, message, target commodity, quantity, and timestamp.

### `inquiries_update_status`
Transition the workflow status of an inquiry.
- **Parameters**:
  - `id` *(string, **required**)*: Inquiry ID.
  - `status` *(string, **required**)*: Allowed values: `"new"`, `"replied"`, `"closed"`.
- **Returns**: Confirmation with new status.

### `inquiries_set_forwarding_email`
Configure the corporate sales inbox that receives real-time lead alerts.
- **Parameters**:
  - `email` *(string, **required**)*: Valid corporate email address (e.g. `"sales@exportweb.app"`).
- **Returns**: Updated recipient email confirmation.

---

## ⚙️ 6. Site Settings, Corporate Identity & SEO Tools

Manage tenant corporate identity, contact coordinates, discrete social media profiles, branding assets, and multilingual SEO tags.

### `settings_get`
Retrieve current tenant configuration, branding URLs, and contact parameters.
- **Parameters**:
  - `lang_code` *(string, optional)*: Optional locale for localized settings (e.g. `"en"`, `"id"`, `"es"`, `"zh"`, `"ar"`, `"fr"`, `"de"`, `"ja"`, `"pt"`, `"ru"`, `"vi"`).
- **Returns**: Complete settings dictionary with branding URLs and localized SEO tags.

### `settings_update`
Update corporate profile, plant locations, social links, branding assets, and SEO metadata.
- **Parameters**:
  - `company_name` *(string, optional)*: Legal enterprise name.
  - `company_profile` *(string, optional)*: Value proposition / corporate overview.
  - `whatsapp_number` *(string, optional)*: Direct WhatsApp trade desk number (international format e.g. `"+628112345678"`).
  - `phone_number` *(string, optional)*: Landline phone.
  - `office_address` *(string, optional)*: Registered headquarters address.
  - `factory_address` *(string, optional)*: Physical plant / warehouse address.
  - `country` *(string, optional)*: Country of domicile.
  - `maps_embed_url` *(string, optional)*: Google Maps embed URL.
  - `seo_title` *(string, optional)*: Default site `<title>`.
  - `seo_description` *(string, optional)*: Default site meta description.
  - `seo_keywords` *(string, optional)*: Default site meta keywords.
  - `about_company` *(string, optional)*: Localized about company text (used when `lang_code` is specified).
  - `lang_code` *(string, optional)*: Language locale for saving localized SEO tags (`"en"`, `"id"`, `"es"`, `"zh"`, `"ar"`, `"fr"`, `"de"`, `"ja"`, `"pt"`, `"ru"`, `"vi"`).
  - `logo_url` *(string, optional)*: Main logo HTTPS URL.
  - `logo_base64` *(string, optional)*: Inline Base64 image data to auto-upload as brand logo (prunes old logo).
  - `logo_source_url` *(string, optional)*: Remote image URL to download as logo.
  - `favicon_url` *(string, optional)*: Favicon HTTPS URL.
  - `favicon_base64` *(string, optional)*: Inline Base64 image data to auto-upload as browser favicon (prunes old favicon).
  - `favicon_source_url` *(string, optional)*: Remote image URL to download as favicon.
  - `og_image_url` *(string, optional)*: OpenGraph preview banner HTTPS URL.
  - `og_image_base64` *(string, optional)*: Inline Base64 image data to auto-upload as OG banner (prunes old banner).
  - `og_image_source_url` *(string, optional)*: Remote image URL to download as OG banner.
  - `social_links` *(string or object, optional)*: JSON encoded string or structured object of social profiles.
  - `linkedin` *(string, optional)*: Discrete LinkedIn corporate URL.
  - `instagram` *(string, optional)*: Discrete Instagram profile URL.
  - `facebook` *(string, optional)*: Discrete Facebook page URL.
  - `twitter` *(string, optional)*: Discrete Twitter/X profile URL.
  - `youtube` *(string, optional)*: Discrete YouTube channel URL.
  - `whatsapp` *(string, optional)*: Discrete WhatsApp channel URL.
  - `header_scripts` *(string, optional)*: Custom header scripts (analytics/tags).
  - `body_scripts` *(string, optional)*: Custom body tracking scripts.
- **Returns**: Confirmation and updated settings state.

---

## 🌐 7. Languages & Multilingual Routing Tools

Control active subfolder languages for the tenant storefront. ExportWeb supports **11 standardized international trade languages**:

| Code | Language | Native Name | Direction | Default |
| :---: | :--- | :--- | :---: | :---: |
| **`en`** | English | English | LTR | **Primary Default** |
| **`id`** | Indonesian | Bahasa Indonesia | LTR | Active |
| **`es`** | Spanish | Español | LTR | Active |
| **`zh`** | Chinese Simplified | 简体中文 | LTR | Active |
| **`ar`** | Arabic | العربية | **RTL** | Active |
| **`fr`** | French | Français | LTR | Active |
| **`de`** | German | Deutsch | LTR | Active |
| **`ja`** | Japanese | 日本語 | LTR | Active |
| **`pt`** | Portuguese | Português | LTR | Active |
| **`ru`** | Russian | Русский | LTR | Active |
| **`vi`** | Vietnamese | Tiếng Việt | LTR | Active |

### `languages_list`
List all configured languages and their active status.
- **Parameters**:
  - `enabled_only` *(boolean, optional)*: If `true`, returns only active languages.
- **Returns**: Array of language objects containing `code`, `name`, `native_name`, `is_default`, `is_enabled`, and `is_rtl`.

### `languages_toggle`
Enable or disable a specific language locale.
- **Parameters**:
  - `code` *(string, **required**)*: 2-letter ISO language code: `"en"`, `"id"`, `"es"`, `"zh"`, `"ar"`, `"fr"`, `"de"`, `"ja"`, `"pt"`, `"ru"`, `"vi"`.
  - `is_enabled` *(boolean, **required**)*: Set `true` to activate or `false` to deactivate.
- **Returns**: Updated locale status.

---

## 📊 8. Executive Dashboard Tools

### `dashboard_stats`
Retrieve an executive overview of platform activity and database volumes.
- **Parameters**: None.
- **Returns**: Object with:
  - `total_products`: Number of active commodities in catalog.
  - `total_galleries`: Number of uploaded facility photos.
  - `total_articles`: Published article count.
  - `total_inquiries`: Total buyer leads received.
  - `new_inquiries`: Unprocessed leads requiring attention.
  - `enabled_languages`: Count of active multilingual locales.
  - `engine_version`: Active platform backend version.
