# DITA-04: Video Engine & Pilot Template Storybook Animasi

**Channel:** Dita Dongeng & Fabel (`@ditafable` / `DITA-04`)  
**Resolution:** 1080x1920 (9:16 Vertical Video)  
**Frame Rate:** 24 fps  
**Target Duration:** 45 - 60 detik (Pilot Day 001: 56.33 detik / 1352 frames)  
**Visual Style:** 3D Enchanted Forest Storybook / Disney-Pixar Whimsical Aesthetic (Faceless Compliant)  
**Voiceover Persona:** Kak Dita (`id-ID-GadisNeural`, rate `-3%`, warm bedtime storytelling pacing ~115-120 WPM)  
**Audio Architecture:** Triple Audio Muxing (Spoken Voiceover + Soft Ambient Bedtime Lullaby + Magic Sparkle Chimes SFX)  

---

## 1. Arsitektur Komposisi Remotion (`remotion/`)

### A. Komposisi Terdaftar (`remotion/Root.tsx`)
1. **`FableStorybookShorts` (1080x1920 @ 24fps)**:
   - Production Master untuk TikTok, Instagram Reels, dan YouTube Shorts.
   - Menggunakan CRF 19-22 H.264 video encoding dengan AAC 48kHz audio.
2. **`FableStorybookShorts720p` (720x1280 @ 24fps)**:
   - Fast Render / Cloud CI/CD Edition untuk approval cepat di runner GitHub Actions & Telegram Bot preview.

### B. Modul Komponen (`remotion/components/`)
1. **`FableStorybookShorts.tsx`**:
   - Master composition coordinator yang mengelola audio tracks, visual track dengan Ken Burns pan/zoom, layer partikel fairy dust, vignette dongeng, header branding, hook card, moral plaque, kinetic subtitles, dan outro bedtime card.
2. **`FairyDustParticles.tsx`**:
   - Layer partikel cahaya melayang (*bokeh / magic sparkles*) berwarna emas, putih, dan hijau toska dengan animasi sinusoida dinamis dan CSS drop-shadow glow (`mixBlendMode: "screen"`).
3. **`StorybookVignette.tsx`**:
   - Bingkai ornamen sudut klasik emas (*vintage corner filigree*) dan gradien vignette temaram untuk memfokuskan pandangan ke pusat visual.
4. **`SafeZoneOverlay.tsx`**:
   - Komponen verifikasi zona aman untuk platform video pendek (menjamin tidak ada teks yang tertutup ikon Like/Share atau deskripsi bawah).

---

## 2. Standar Zona Aman (Safe Zone Standards 1080x1920)

| Elemen UI | Koordinat / Posisi | Alasan Teknis & Safe Zone |
| :--- | :--- | :--- |
| **Top Channel Badge** | Y: 155px (Top Center) | Terlindung dari status bar HP, search bar, dan tombol navigasi atas. |
| **Hook Headline Card** | Y: 215px (Top Center) | Tampil pada 0.0s - 4.0s dengan spring bounce; tidak menutupi wajah karakter. |
| **Pusat Karakter 3D** | Y: 380px - 1100px | Ruang lega untuk ekspresi karakter 3D Pixar dan buku dongeng berpendar. |
| **Moral Plaque Plaque** | Y: 360px - 580px (Tengah) | Pelat pesan bijak yang muncul pada detik 36s - 49s saat pesan moral disampaikan. |
| **Kinetic Subtitle Box** | Bottom: 250px (Y: 1380px - 1560px) | Aman dari caption/audio ticker bawah (1550px+) dan tombol interaksi kanan. |
| **Outro Bedtime Pill** | Bottom: 120px (Y: 1720px - 1780px) | Tampil di 5 detik terakhir sebagai pengantar tidur dan jembatan loop mulus. |

---

## 3. Komponen HyperFrames 3D Storybook (`hyperframes_scenes/`)

- File: `hyperframes_scenes/scenes/scene_fable_storybook_day001.html`
- Spesifikasi:
  - Kanvas 1080x1920 responsif standalone dengan animasi GSAP 3.14.2.
  - Simulasi partikel kunang-kunang di canvas 2D 60fps.
  - Buku dongeng 3D timbul (*leather & gold embossed*) dengan efek perspektif 3D CSS.
  - Apel emas bercahaya shader radial gradien dan animasi denyut aura (*pulse-glow*).
  - Teks dialog kinetik dan moral plaque terintegrasi.

---

## 4. Pipeline Operasional Mandiri (`scripts/`)

1. **`python scripts/generate-voiceover.py [packet] [out_audio] [out_meta]`**:
   - Menghasilkan voiceover pengantar tidur menggunakan `id-ID-GadisNeural` dengan rate `-3%`.
   - Mengambil event `SentenceBoundary` dari Edge TTS untuk menghasilkan array `timed_subtitles` dengan timestamp presisi milidetik.
2. **`python scripts/build_pixar_storybook_plates.py`**:
   - Menghasilkan 5 plat visual 3D Pixar beresolusi 1080x1920 untuk masing-masing adegan Day 001.
3. **`python scripts/fetch-broll.py`**:
   - Sinkronisasi manifes adegan (`public/broll_manifest.json`) dengan dukungan video B-roll Pexels dan plat 3D Pixar.
4. **`npx tsx scripts/render-video.ts [--comp] [--out] [--frames]`**:
   - Bundling dan rendering Remotion composition menggunakan Google Chrome headless runner.
   - Dilengkapi ekstraksi otomatis 5 preview frames di detik-detik penting.
5. **`npx tsx scripts/pipeline-daily.ts --day <N>`**:
   - Skrip satu-perintah untuk orkestrasi end-to-end (TTS $\rightarrow$ Visual Asset $\rightarrow$ Remotion Render $\rightarrow$ State Update).

---

## 5. Artefak Deliverable Pilot Day 001

1. **Master Video (1080x1920 @ 24fps):**
   `C:/Users/K4G3/social-fleet-assets/dita/DITA-04_dita_dongeng_fabel/output/dita_fable_day_001_master.mp4` (35.93 MB)
2. **Preview Video (720x1280 @ 24fps):**
   `C:/Users/K4G3/social-fleet-assets/dita/DITA-04_dita_dongeng_fabel/output/dita_fable_day_001_preview720p.mp4` (14.04 MB)
3. **Audio Master & Timed Metadata:**
   - Voiceover: `public/voiceover_day_001.mp3` (56.09s, 97 kata)
   - BGM: `public/bgm/bgm_bedtime_lullaby.mp3` (Lullaby pentatonik hangat)
   - SFX: `public/sfx/magic_sparkle.mp3` (Chimes lonceng peri)
   - Metadata Subtitle: `public/audio_meta.json` (29 kinetic subtitle chunks)
4. **Preview Thumbnail Frames:**
   - Detik 02s: `output/preview_frames/frame_02s_hook.jpg`
   - Detik 12s: `output/preview_frames/frame_12s_dilemma.jpg`
   - Detik 28s: `output/preview_frames/frame_28s_confession.jpg`
   - Detik 42s: `output/preview_frames/frame_42s_moral_hug.jpg`
   - Detik 53s: `output/preview_frames/frame_53s_bedtime_outro.jpg`
