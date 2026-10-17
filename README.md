# ExportWeb Skills Repository

Welcome to **ExportWeb Skills** (`exportweb.app-skills`), the official skills repository for integrating AI Agents (Antigravity, Claude, Cursor, OpenCode, ChatGPT, etc.) with the [ExportWeb](https://exportweb.app) B2B Exporter Platform.

This repository provides standardized, production-tested agent skills and reference specifications for interacting with ExportWeb's native Go Model Context Protocol (MCP) server.

---

## 📁 Repository Structure

```text
exportweb.app-skills/
├── README.md                      # Overview & Quickstart (Bilingual EN/ID)
├── .gitignore                     # Repository git ignore rules
└── exportweb-cms/                 # Primary Skill: ExportWeb CMS & Operator Skill
    ├── SKILL.md                   # Agent Skill Manifest & Fast Small-Model Cheat Sheet
    ├── references/
    │   └── tools_reference.md     # Complete specification for all 25 MCP tools
    ├── examples/
    │   ├── mcp_config_http.json   # Remote HTTP JSON-RPC MCP configuration
    │   ├── mcp_config_sse.json    # SSE Streaming MCP configuration
    │   └── sample_payloads.json   # Working example request & response payloads (11 Locales, Clean HTML, R2 Uploads)
    └── scripts/
        └── test_connection.py     # Standalone Python CLI to verify connection & token
```

---

## 🚀 Available Skills

### 1. `exportweb-cms`
A comprehensive operator skill that equips AI agents (including small-context models) to:
- **Authenticate**: Use dynamic 256-bit Bearer secret tokens (`ew_sec_...`) obtained from the ExportWeb Admin Panel (`/admin/account-settings`).
- **Upload Assets & Media**: Upload brand logos, browser favicons, OG preview banners (1200x630), product photos (4:3/1:1), facility galleries (16:9), and article covers to Cloudflare R2 / MinIO via Base64 or remote URL fetch (`assets_upload`).
- **Manage Products & Commodities**: Perform full CRUD operations on export commodities with clean semantic HTML specification tables, inline image uploads, auto-slug generation, and automated asset pruning on delete.
- **Manage Facility Galleries**: Upload and curate high-resolution facility, container stuffing, kiln, and testing photo documentation with automated storage cleanup.
- **Publish Market Intelligence with Clean HTML**: Draft, translate, and publish SEO-optimized B2B export intelligence articles using clean HTML (`<h2>`, `<h3>`, `<p>`, `<ul>`, `<blockquote>`, `<table>`, and whitelisted YouTube/Vimeo embeds) rendered safely inside Tailwind `.prose`.
- **Anti-XSS Security**: Benefit from Go server-side HTML sanitization (`SanitizeArticleHTML`) that strips dangerous scripts, unapproved iframes, inline event handlers, and malicious styles while automatically securing external links (`rel="noopener noreferrer"`).
- **Manage 11 Standardized Multilingual Locales**: Inspect, translate, and toggle 11 international trade languages with dedicated subfolder routing (`/{lang}/...`):
  - English (`en` - Universal Default)
  - Indonesian (`id`)
  - Spanish (`es`)
  - Chinese Simplified (`zh`)
  - Arabic (`ar` - Full RTL Support)
  - French (`fr`)
  - German (`de`)
  - Japanese (`ja`)
  - Portuguese (`pt`)
  - Russian (`ru`)
  - Vietnamese (`vi`)
- **Handle Inquiries & Leads**: List incoming international buyer RFQs, inspect buyer requirements, update status, and configure notification forwarding emails.
- **Configure Site Settings**: Manage corporate identity, contact coordinates, discrete social media profiles (Zero Raw JSON), WhatsApp trade desks, and multi-language SEO tags.
- **Executive Dashboard**: Read live business metrics, inquiry volumes, and catalog statistics.

👉 **View full instructions in [`exportweb-cms/SKILL.md`](exportweb-cms/SKILL.md)**.

---

## ⚡ Quickstart

### 1. Retrieve your MCP Secret Token
1. Log in to your ExportWeb Admin Panel: `https://your-domain.com/admin/login`
2. Navigate to **Account Setting** (`/admin/account-settings`)
3. Under the **Model Context Protocol (MCP) Secret Token** card, copy your secret token (format: `ew_sec_<64_hex_chars>`).

### 2. Configure Your AI Agent Client

#### Option A: Remote HTTP JSON-RPC (Recommended)
Add to your client configuration file (`mcp_config.json` or `claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "exportweb-cms": {
      "serverUrl": "https://exportweb.app/mcp",
      "headers": {
        "Authorization": "Bearer ew_sec_YOUR_SECRET_TOKEN_HERE"
      }
    }
  }
}
```

#### Option B: SSE Streaming
```json
{
  "mcpServers": {
    "exportweb-cms": {
      "serverUrl": "https://exportweb.app/mcp/sse",
      "headers": {
        "Authorization": "Bearer ew_sec_YOUR_SECRET_TOKEN_HERE"
      }
    }
  }
}
```

### 3. Verify Connection
Use the included standalone verification script:

```bash
python3 exportweb-cms/scripts/test_connection.py \
  --url https://exportweb.app \
  --token ew_sec_YOUR_SECRET_TOKEN_HERE
```

---

## 🇮🇩 Ringkasan Bahasa Indonesia

Repository ini berisi kumpulan *skills* untuk AI Agent (Antigravity CLI, Claude, Cursor, ChatGPT, dll.) agar dapat berinteraksi langsung dengan sistem CMS ExportWeb menggunakan **Model Context Protocol (MCP)**.

### 4 Pilar Utama Pembaruan Skill `exportweb-cms`
1. **11 Bahasa Ekspor Standar Konsisten**:
   Mendukung penuh 11 bahasa perdagangan internasional dengan routing subfolder alami (`/{lang}/...`) dan isolasi SEO tabbed:
   - Inggris (`en` - Default Universal)
   - Indonesia (`id`)
   - Spanyol (`es`)
   - Mandarin Sederhana (`zh`)
   - Arab (`ar` - Mendukung penuh arah teks kanan-ke-kiri / RTL)
   - Prancis (`fr`)
   - Jerman (`de`)
   - Jepang (`ja`)
   - Portugis (`pt`)
   - Rusia (`ru`)
   - Vietnam (`vi`)
2. **Kerapihan HTML & Tipografi Tailwind (`.prose`)**:
   Konten artikel dan deskripsi produk dirender secara elegan menggunakan `@tailwindcss/typography`. Panduan mewajibkan struktur HTML semantik (`<h2>`, `<h3>`, `<p>`, `<ul>`, `<blockquote>`, `<figure>`, `<figcaption>`) dan tabel spesifikasi teknis (`<table>`, `<thead>`, `<tbody>`), bebas dari tag kosong atau gaya inline sembarangan.
3. **Arsitektur Upload File & Siklus Pembersihan Aset Anti-Spam**:
   Mendukung upload gambar dan dokumen langsung ke Cloudflare R2 / MinIO melalui Base64 maupun URL remote. Penggantian logo/cover dan penghapusan produk/galeri akan secara otomatis menghapus file lama dari penyimpanan cloud (mencegah bloat/spam).
4. **Dukungan Rich Text TinyMCE & Sanitasi Anti-XSS**:
   Didukung oleh TinyMCE 7 di Admin dan sanitasi Go server-side (`SanitizeArticleHTML`) yang mengizinkan pemformatan kaya dan embed video YouTube/Vimeo tepercaya, sembari membersihkan skrip berbahaya, event handler inline (`onclick`, `onerror`), serta otomatis menambahkan `rel="noopener noreferrer"` pada tautan eksternal.

### Cara Push ke GitHub
Repository ini dipersiapkan untuk remote:
```bash
git remote -v
# origin  git@github.com:ersaazis/exportweb.app-skills.git (fetch/push)

git push -u origin main
```

---

## 📄 License
MIT License. Created for the ExportWeb ecosystem.
