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
    │   └── sample_payloads.json   # Working example request & response payloads
    └── scripts/
        └── test_connection.py     # Standalone Python CLI to verify connection & token
```

---

## 🚀 Available Skills

### 1. `exportweb-cms`
A comprehensive operator skill that equips AI agents (including small-context models) to:
- **Authenticate**: Use dynamic 256-bit Bearer secret tokens (`ew_sec_...`) obtained from the ExportWeb Admin Panel (`/admin/account-settings`).
- **Upload Assets & Media**: Upload brand logos, favicons, OG banners, product photos, facility galleries, and article covers to Cloudflare R2 / MinIO via Base64 or remote URL fetch (`assets_upload`).
- **Manage Products & Services**: Perform full CRUD operations on export commodities with inline image uploads, auto-slug generation, and automated asset pruning on delete.
- **Manage Galleries**: Upload and curate high-resolution facility, container stuffing, kiln, and testing photo documentation.
- **Publish Market Intelligence**: Draft, translate, and publish SEO-optimized AIDA export intelligence articles with inline cover images.
- **Handle Inquiries & Leads**: List incoming international buyer RFQs, inspect buyer requirements, update status, and configure notification forwarding emails.
- **Configure Site Settings**: Manage corporate identity, contact coordinates, discrete social media profiles (Zero Raw JSON), WhatsApp trade desks, and multi-language SEO tags.
- **Manage Multilingual Locales**: Inspect and toggle 11 localized trade languages (`en`, `id`, `es`, `zh`, `ar`, `fr`, `de`, `ja`, `pt`, `ru`, `vi`).
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

Repository ini berisi kumpulan *skills* untuk AI Agent (Antigravity CLI, Claude, Cursor, dll.) agar dapat berinteraksi langsung dengan sistem CMS ExportWeb menggunakan **Model Context Protocol (MCP)**.

### Fitur Utama Skill `exportweb-cms`
1. **Otentikasi Aman**: Menggunakan Bearer token kriptografis 256-bit (`ew_sec_...`) yang dapat di-generate dan di-reset kapan saja dari menu `/admin/account-settings`.
2. **25 Tools Produksi Lengkap**:
   - **Upload Media & Aset** (1 tool): Unggah gambar logo, favicon, OG banner, foto produk, dan artikel via Base64 atau URL remote ke Cloudflare R2 / MinIO (`assets_upload`).
   - **Katalog Produk** (5 tools): Cari, tambah, baca detail, update spesifikasi (mendukung upload gambar inline & auto-slug), dan hapus produk ekspor (otomatis menghapus gambar terkait dari storage).
   - **Galeri Fasilitas** (5 tools): Kelola foto pabrik, proses produksi, pengujian lab, dan stuffing kontainer dengan pembersihan storage otomatis saat dihapus/diganti.
   - **Artikel & Wawasan Pasar** (5 tools): Kelola artikel riset pasar global lengkap dengan metadata SEO dan upload cover inline.
   - **Inquiry & Lead Buyer** (4 tools): Pantau RFQ dari buyer internasional, ubah status, dan atur email penerima notifikasi.
   - **Profil & Pengaturan Web** (2 tools): Update profil perusahaan, logo, favicon, OG image, nomor WhatsApp, media sosial diskret (Zero Raw JSON), dan SEO multibahasa.
   - **Bahasa & Lokalisasi** (2 tools): Daftar dan aktif/nonaktifkan 11 bahasa ekspor (`id`, `en`, `es`, `zh`, `ar`, dll.).
   - **Dashboard Eksekutif** (1 tool): Pantau statistik ringkas platform secara realtime.

### Cara Push ke GitHub
Repository ini dipersiapkan untuk remote:
```bash
git remote -v
# origin  https://github.com/ersaazis/exportweb.app-skills.git (fetch/push)

git push -u origin main
```

---

## 📄 License
MIT License. Created for the ExportWeb ecosystem.
