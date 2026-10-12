# ExportWeb MCP Tools Reference Guide

This document provides exhaustive technical specifications for all **24 tools** exposed by the ExportWeb Go Model Context Protocol (MCP) server.

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

## 📦 1. Products & Commodities Tools

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
  - `slug` *(string, **required**)*: Unique URL slug (e.g. `"premium-coconut-charcoal-briquettes"`).
  - `category` *(string, optional)*: Category designation (defaults to `"General"`).
  - `hs_code` *(string, optional)*: Harmonized System tariff code (e.g. `"4402.90.10"`).
  - `origin` *(string, optional)*: Country of origin or load port (e.g. `"Semarang, Indonesia"`).
  - `moq` *(string, optional)*: Minimum Order Quantity (e.g. `"1x20ft FCL (18 MT)"`).
  - `packing_detail` *(string, optional)*: Packaging details (e.g. `"10kg master carton with inner plastic liner"`).
  - `supply_capacity` *(string, optional)*: Monthly production capacity (e.g. `"300 Metric Tons / Month"`).
  - `incoterms` *(string, optional)*: Supported trade terms (e.g. `"FOB, CIF, CFR, EXW"`).
  - `description` *(string, optional)*: Detailed product specifications and descriptions.
  - `images` *(array of string, optional)*: Array of HTTPS URLs for product photographs.
  - `is_featured` *(boolean, optional)*: Whether to feature the item on the storefront home.
  - `is_active` *(boolean, optional)*: Active status in catalog (default: `true`).
- **Returns**: Object with created product ID and status.

### `products_read`
Retrieve full product details, specifications, and images by ID or slug.
- **Parameters**:
  - `id` *(string, optional)*: Product ID (e.g. `"prod_abc123"`).
  - `slug` *(string, optional)*: Product URL slug (e.g. `"premium-coconut-charcoal-briquettes"`).
  *(At least one identifier must be provided)*
- **Returns**: Full product object.

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
  - `description` *(string, optional)*: Updated description text.
  - `images` *(array of string, optional)*: Updated list of image URLs.
  - `is_featured` *(boolean, optional)*: Updated featured flag.
  - `is_active` *(boolean, optional)*: Updated active status.
- **Returns**: Updated product object.

### `products_delete`
Permanently remove a product from the database.
- **Parameters**:
  - `id` *(string, **required**)*: Product ID to remove.
- **Returns**: Success confirmation.

---

## 🖼️ 2. Facility & Media Galleries Tools

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
  - `image_url` *(string, **required**)*: Public HTTPS asset URL.
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
Update title, caption, sort order, or image URL of an existing photo.
- **Parameters**:
  - `id` *(string, **required**)*: Gallery ID to update.
  - `title` *(string, optional)*: New title.
  - `image_url` *(string, optional)*: New image URL.
  - `category` *(string, optional)*: New category.
  - `description` *(string, optional)*: New description.
  - `sort_order` *(integer, optional)*: New sort sequence.
- **Returns**: Updated record.

### `galleries_delete`
Delete a gallery photo record.
- **Parameters**:
  - `id` *(string, **required**)*: Gallery ID to delete.
- **Returns**: Confirmation.

---

## 📰 3. Articles & Market Intelligence Tools

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
  - `slug` *(string, **required**)*: URL slug.
  - `content` *(string, **required**)*: Markdown or HTML formatted article body.
  - `excerpt` *(string, optional)*: Executive summary / lead paragraph.
  - `category` *(string, optional)*: Article category.
  - `cover_image` *(string, optional)*: Feature image HTTPS URL.
  - `author` *(string, optional)*: Author byline.
  - `is_published` *(boolean, optional)*: Published flag (default: `true`).
  - `meta_title` *(string, optional)*: SEO title tag (under 60 characters).
  - `meta_description` *(string, optional)*: SEO meta description (under 160 characters).
  - `meta_keywords` *(string, optional)*: Comma-separated keyword string.
  - `lang_code` *(string, optional)*: Language code (default: `"en"`).
- **Returns**: Created article record.

### `articles_read`
Retrieve article content and SEO metadata by ID or slug.
- **Parameters**:
  - `id` *(string, optional)*: Article ID.
  - `slug` *(string, optional)*: Article slug.
  - `lang_code` *(string, optional)*: Desired language locale (default: `"en"`).
- **Returns**: Article full content and metadata.

### `articles_update`
Update body content, SEO metadata, or publish status of an article.
- **Parameters**:
  - `id` *(string, **required**)*: Article ID.
  - `title` *(string, optional)*: Updated headline.
  - `slug` *(string, optional)*: Updated slug.
  - `content` *(string, optional)*: Updated content body.
  - `excerpt` *(string, optional)*: Updated excerpt.
  - `category` *(string, optional)*: Updated category.
  - `cover_image` *(string, optional)*: Updated cover URL.
  - `author` *(string, optional)*: Updated author name.
  - `is_published` *(boolean, optional)*: Updated publish status.
  - `meta_title` *(string, optional)*: Updated SEO title.
  - `meta_description` *(string, optional)*: Updated SEO meta description.
  - `meta_keywords` *(string, optional)*: Updated SEO keywords.
  - `lang_code` *(string, optional)*: Target language locale.
- **Returns**: Updated article record.

### `articles_delete`
Delete an article and all its localized versions.
- **Parameters**:
  - `id` *(string, **required**)*: Article ID to delete.
- **Returns**: Confirmation.

---

## 📬 4. Buyer Inquiries & Leads Tools

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
- **Returns**: Full inquiry details including contact info, message, and timestamp.

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

## ⚙️ 5. Site Settings & SEO Tools

Manage tenant corporate identity, contact coordinates, social media profiles, and default SEO tags.

### `settings_get`
Retrieve current tenant configuration and contact parameters.
- **Parameters**:
  - `lang_code` *(string, optional)*: Optional locale for localized settings.
- **Returns**: Complete settings dictionary.

### `settings_update`
Update corporate profile, plant locations, social links, and metadata.
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
  - `logo_url` *(string, optional)*: Main logo HTTPS URL.
  - `favicon_url` *(string, optional)*: Favicon HTTPS URL.
  - `og_image_url` *(string, optional)*: OpenGraph preview banner HTTPS URL.
  - `social_links` *(string, optional)*: JSON encoded string of social profiles (e.g. `{"linkedin":"...","youtube":"..."}`).
  - `header_scripts` *(string, optional)*: Custom header scripts (analytics/tags).
  - `body_scripts` *(string, optional)*: Custom body tracking scripts.
- **Returns**: Confirmation and updated settings state.

---

## 🌐 6. Languages & Multilingual Routing Tools

Control active subfolder languages for the tenant storefront.

### `languages_list`
List all configured languages and their active status.
- **Parameters**:
  - `enabled_only` *(boolean, optional)*: If `true`, returns only active languages.
- **Returns**: Array of language objects containing `code`, `name`, `native_name`, and `is_enabled`.

### `languages_toggle`
Enable or disable a specific language locale.
- **Parameters**:
  - `code` *(string, **required**)*: 2-letter ISO language code (e.g. `"ar"`, `"de"`, `"zh"`, `"ja"`, `"es"`, `"fr"`, `"pt"`, `"ru"`, `"vi"`).
  - `is_enabled` *(boolean, **required**)*: Set `true` to activate or `false` to deactivate.
- **Returns**: Updated locale status.

---

## 📊 7. Executive Dashboard Tools

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
