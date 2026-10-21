# DITA-04: Sovereign Video Engine & Autonomous Pipeline (@ditafable)

[![Daily Fable Shorts Pipeline](https://github.com/ditaqsyahm-source/ditafable/actions/workflows/daily-shorts.yml/badge.svg)](https://github.com/ditaqsyahm-source/ditafable/actions/workflows/daily-shorts.yml)

Sovereign automated content engine and multi-platform publishing studio for **DITA-04 (@ditafable)** — Dongeng Fabel & Nilai Moral Anak (Pengantar Tidur). Combining Remotion 1080x1920, HyperFrames 3D Pixar enchanted forest storybook aesthetic, Edge-TTS Bedtime Audio Muxing, and Zernio + YouTube Data API v3 multi-platform distribution.

---

## 🎯 Identitas Saluran & Otoritas Ceruk
- **Channel ID:** `DITA-04`
- **Handles:**
  - **YouTube:** [@ditafable](https://youtube.com/@ditafable) (Channel ID: `UCxEyHnK7ru1XM7Ri0EWywLw`)
  - **TikTok:** [@ditafable](https://tiktok.com/@ditafable) (Account ID: `6ad8acf3c24aa78753a651ef`)
  - **Instagram:** [@ditafable](https://instagram.com/ditafable) (Account ID: `6ad8acd9aad76462b1a71e23`)
- **Cluster Persona:** Dita (Otoritas Solutif, Empati, Tumbuh Kembang Keluarga & Edukasi Ramah Anak)
- **Niche Moat:** Cerita Fabel 3D Pixar, kinetic typography, safe zone compliant, zero copyright risk.

---

## 🏛️ Arsitektur Mesin Produksi

```
ditafable/
├── .github/workflows/
│   └── daily-shorts.yml              # GitHub Actions Cloud Runner (19:30 WIB cron)
├── curriculum/
│   ├── master_curriculum_180_days.json # 180-day master roadmap
│   ├── MASTER_CURRICULUM_MATRIX.md     # Curriculum spec & moral themes
│   └── content_packet_day_*.json       # Daily episode metadata & voiceover scripts
├── hyperframes_scenes/                 # Standalone GSAP & HTML5 3D scenes
├── public/
│   ├── audio/                          # Split audio tracks
│   ├── bgm/                            # Ambient pentatonic bedtime lullaby
│   ├── sfx/                            # Magic sparkle chimes
│   ├── images/                         # 3D Pixar storybook plates
│   └── voiceover_day_*.mp3             # Synthesized bedtime voiceover
├── remotion/
│   ├── Root.tsx                        # Remotion composition registry (1080p & 720p)
│   ├── components/                     # Storybook coordinator, fairy dust, safe zone
│   └── compositions/                   # FableStorybookShorts master
├── scripts/
│   ├── pipeline-daily.ts               # Autonomous end-to-end daily orchestrator
│   ├── render-video.ts                 # Remotion headless rendering engine
│   ├── generate-voiceover.py           # Edge-TTS voiceover synthesizer with sentence boundaries
│   ├── fetch-broll.py                  # 3D visual plates & B-roll collector
│   ├── publish_video.py                # Multi-platform publisher (YouTube Data API v3 & Zernio uploadMediaDirect)
│   └── monthly_fleet_evaluator.py      # Monthly performance metrics auditor & Telegram dispatcher
├── state/
│   ├── campaign_state.json             # Active day pointer & channel connection status
│   └── published.json                  # Immutable publishing receipts and video hashes
├── package.json
└── tsconfig.json
```

---

## 🚀 Perintah Operasional (CLI)

```bash
# 1. Jalankan pipeline harian otonom (TTS -> Render -> Encode -> Publish)
npm run pipeline

# 2. Jalankan hari spesifik (misal Day 1)
npm run pipeline -- --day 1

# 3. Render video master saja (1080x1920)
npm run render:1080p

# 4. Render video cepat untuk review (720x1280)
npm run render:720p

# 5. Cek kesehatan status koneksi multi-platform
python scripts/publish_video.py status

# 6. Jalankan audit evaluasi performa bulanan
python scripts/monthly_fleet_evaluator.py
```

---

## ☁️ GitHub Actions Cloud CI/CD

Pipeline berjalan otomatis di cloud GitHub Actions setiap hari pukul **19:30 WIB** (`12:30 UTC`), waktu primetime pengantar tidur anak di Indonesia.

### Secrets Terkonfigurasi:
1. `ZERNIO_API_KEY`: API Key Zernio untuk upload media langsung ke registry.
2. `TIKTOK_ACCOUNT_ID`: Account ID `@ditafable` di Zernio (`6ad8acf3c24aa78753a651ef`).
3. `TIKTOK_USERNAME`: `ditafable`.
4. `INSTAGRAM_ACCOUNT_ID`: Account ID `@ditafable` di Zernio (`6ad8acd9aad76462b1a71e23`).
5. `INSTAGRAM_USERNAME`: `ditafable`.
6. `GOOGLE_CLIENT_ID`: Google OAuth 2.0 Client ID untuk YouTube Data API v3.
7. `GOOGLE_CLIENT_SECRET`: Google OAuth 2.0 Client Secret.
8. `YT_REFRESH_TOKEN`: Long-lived OAuth refresh token untuk YouTube channel `@ditafable`.
9. `PEXELS_API_KEY`: Pexels API key untuk fallback footage alam/hutan.

---

## 📜 Lisensi & Kepatuhan
Sovereign content pipeline dikelola di bawah komando Herman (Chief AI Orchestrator) atas mandat Owner (Nasrul Jihadi). Seluruh aset visual dan audio tunduk pada standar ramah keluarga (*family-friendly* / *made-for-kids compliant*).
