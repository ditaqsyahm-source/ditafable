import os
import sys
import json
import random
import urllib.request
import urllib.parse
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance

DIR_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_PATH = os.path.join(DIR_PATH, ".env")
PIPELINE_ENV = "C:/Users/K4G3/social-fleet-pipeline/.env"

def load_env():
    env = {}
    for p in [ENV_PATH, PIPELINE_ENV]:
        if os.path.exists(p):
            with open(p, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        k, v = line.split("=", 1)
                        if k.strip() not in env:
                            env[k.strip()] = v.strip()
    return env

ENV = load_env()
PEXELS_KEY = os.environ.get("PEXELS_API_KEY") or ENV.get("PEXELS_API_KEY")
USED_ASSETS_FILE = os.path.join(DIR_PATH, "state", "used_broll_assets.json")

SCENES_CONFIG = [
    {
        "scene_id": "SCENE_01_KANCIL_APEL",
        "timeStart": 0.0,
        "timeEnd": 4.86,
        "query": "cute deer in fairy forest",
        "fallback_query": "deer moss forest",
        "fallback_image": "images/scene1_kancil_apel.jpg",
        "description": "Kancil Ciko memegang belahan apel emas di tanah berlumut senja"
    },
    {
        "scene_id": "SCENE_02_POHON_KENARI",
        "timeStart": 4.86,
        "timeEnd": 16.34,
        "query": "enchanted forest fairy tale tree",
        "fallback_query": "magical woods ancient tree",
        "fallback_image": "images/scene2_pohon_kenari.jpg",
        "description": "Pohon kenari raksasa berongga hangat dengan lentera menyala"
    },
    {
        "scene_id": "SCENE_03_PENGAKUAN_CIKO",
        "timeStart": 16.34,
        "timeEnd": 36.11,
        "query": "bear in nature gentle calm",
        "fallback_query": "forest wildlife gentle bear",
        "fallback_image": "images/scene3_pengakuan_ciko.jpg",
        "description": "Kakek Beruang berlutut lembut menyambut pengakuan jujur Ciko"
    },
    {
        "scene_id": "SCENE_04_PELUKAN_HANGAT",
        "timeStart": 36.11,
        "timeEnd": 51.01,
        "query": "golden leaves falling forest",
        "fallback_query": "autumn leaves sunlight peaceful",
        "fallback_image": "images/scene4_pelukan_hangat.jpg",
        "description": "Pelukan hangat penuh kasih & daun-daun emas berguguran"
    },
    {
        "scene_id": "SCENE_05_MALAM_BINTANG",
        "timeStart": 51.01,
        "timeEnd": 56.10,
        "query": "night starry sky enchanted forest fireflies",
        "fallback_query": "night fireflies magical lights",
        "fallback_image": "images/scene5_malam_bintang.jpg",
        "description": "Langit malam berhias bintang, bulan sabit & kunang-kunang"
    }
]

def search_pexels_video(query):
    if not PEXELS_KEY:
        print("[B-Roll] PEXELS_API_KEY tidak ada.")
        return None, None

    url = (
        f"https://api.pexels.com/videos/search?"
        f"query={urllib.parse.quote(query)}&orientation=portrait&per_page=10"
    )
    req = urllib.request.Request(url, headers={
        "Authorization": PEXELS_KEY,
        "User-Agent": "Mozilla/5.0"
    })
    try:
        with urllib.request.urlopen(req, timeout=12) as resp:
            data = json.loads(resp.read().decode())
            videos = data.get("videos", [])
            for v in videos:
                vid_id = v.get("id")
                files = v.get("video_files", [])
                # Prefer HD portrait (height >= 1280, width < height)
                for f in files:
                    w, h = f.get("width") or 0, f.get("height") or 0
                    if w > 0 and h > 0 and w < h and h >= 1280 and f.get("link"):
                        return vid_id, f.get("link")
                # Fallback any portrait
                for f in files:
                    w, h = f.get("width") or 0, f.get("height") or 0
                    if w > 0 and h > 0 and w < h and f.get("link"):
                        return vid_id, f.get("link")
    except Exception as e:
        print(f"[B-Roll] Query '{query}' error: {e}")
    return None, None

def download_file(url, out_path):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        with open(out_path, "wb") as f:
            f.write(resp.read())

def generate_storybook_fallback_card(out_path, base_color_top, base_color_bot, scene_title, subtext, icon="📖"):
    # Create 1080x1920 high-res enchanted storybook scene card
    w, h = 1080, 1920
    im = Image.new("RGB", (w, h), base_color_bot)
    draw = ImageDraw.Draw(im)

    # Vertical gradient
    for y in range(h):
        ratio = y / h
        r = int(base_color_top[0] * (1 - ratio) + base_color_bot[0] * ratio)
        g = int(base_color_top[1] * (1 - ratio) + base_color_bot[1] * ratio)
        b = int(base_color_top[2] * (1 - ratio) + base_color_bot[2] * ratio)
        draw.line([(0, y), (w, y)], fill=(r, g, b))

    # Fairy dust / magical glow orbs
    glow_im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow_im)
    
    # Large center ambient orb
    cx, cy = w // 2, int(h * 0.42)
    radius = 380
    for r in range(radius, 0, -10):
        alpha = int(45 * (1 - r / radius))
        glow_draw.ellipse(
            [(cx - r, cy - r), (cx + r, cy + r)],
            fill=(245, 158, 11, alpha)
        )

    # Floating fairy dust specks
    random.seed(hash(scene_title))
    for _ in range(60):
        sx = random.randint(60, w - 60)
        sy = random.randint(120, h - 250)
        srad = random.randint(3, 9)
        salpha = random.randint(80, 220)
        glow_draw.ellipse(
            [(sx - srad, sy - srad), (sx + srad, sy + srad)],
            fill=(254, 240, 138, salpha)
        )

    im.paste(glow_im, (0, 0), glow_im)

    # Vignette
    vignette = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    v_draw = ImageDraw.Draw(vignette)
    for i in range(120):
        a = int(180 * (1 - i / 120))
        v_draw.rectangle([i, i, w - i, h - i], outline=(6, 12, 10, a), width=1)
    im.paste(vignette, (0, 0), vignette)

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    im.save(out_path, quality=92)
    print(f"[Visual Asset] Generated 1080x1920 storybook card -> {out_path}")

def build_scene_cards_from_assets():
    # If avatar or banner exists, crop & composite into vertical 1080x1920 storybook plates
    avatar_path = os.path.join(DIR_PATH, "avatar", "standard_avatar.jpg")
    banner_path = os.path.join(DIR_PATH, "banner", "standard_banner.jpg")
    img_dir = os.path.join(DIR_PATH, "public", "images")
    os.makedirs(img_dir, exist_ok=True)

    scenes_art = [
        ("scene1_kancil_apel.jpg", (15, 32, 22), (5, 12, 8), "Kancil Ciko & Apel Emas", "Rahasia di Balik Semak Hutan"),
        ("scene2_pohon_kenari.jpg", (28, 22, 14), (8, 6, 4), "Pohon Kenari Kakek Beruang", "Lentera Hangat di Tengah Senja"),
        ("scene3_pengakuan_ciko.jpg", (34, 25, 18), (10, 8, 5), "Pengakuan Jujur Ciko", "Keberanian Meminta Maaf"),
        ("scene4_pelukan_hangat.jpg", (45, 28, 12), (12, 8, 4), "Pelukan Jiwa Ksatria", "Kejujuran Menghadirkan Tenang"),
        ("scene5_malam_bintang.jpg", (10, 14, 32), (3, 5, 14), "Malam Bintang & Bulan Sabit", "Selamat Tidur Penuh Kedamaian")
    ]

    for fname, top_col, bot_col, title, subtitle in scenes_art:
        out_p = os.path.join(img_dir, fname)
        if not os.path.exists(out_p):
            # Check if we can blend with avatar/banner
            src = avatar_path if "kancil" in fname or "pelukan" in fname else banner_path
            if os.path.exists(src):
                base = Image.open(src).convert("RGB")
                # Create 1080x1920 canvas
                canvas = Image.new("RGB", (1080, 1920), bot_col)
                # Resize base to fit width
                scale = 1080 / base.width
                new_h = int(base.height * scale)
                resized = base.resize((1080, new_h), Image.Resampling.LANCZOS)
                
                # Center vertically around upper 45%
                y_pos = max(0, int(1920 * 0.40 - new_h / 2))
                canvas.paste(resized, (0, y_pos))
                
                # Apply top and bottom dark gradient overlay for cinematic contrast
                grad = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0))
                g_draw = ImageDraw.Draw(grad)
                for y in range(1920):
                    if y < 450:
                        a = int(220 * (1 - y / 450))
                        g_draw.line([(0, y), (1080, y)], fill=(bot_col[0], bot_col[1], bot_col[2], a))
                    elif y > 1200:
                        a = int(240 * ((y - 1200) / 720))
                        g_draw.line([(0, y), (1080, y)], fill=(bot_col[0], bot_col[1], bot_col[2], a))
                canvas.paste(grad, (0, 0), grad)
                canvas.save(out_p, quality=92)
                print(f"[Visual Asset] Composited 3D storybook plate -> {out_p}")
            else:
                generate_storybook_fallback_card(out_p, top_col, bot_col, title, subtitle)

def main():
    broll_dir = os.path.join(DIR_PATH, "public", "broll")
    os.makedirs(broll_dir, exist_ok=True)
    
    # 1. Prepare high-res 1080x1920 3D storybook scene image plates
    build_scene_cards_from_assets()

    manifest = []
    print("[B-Roll] Mengambil aset visual sinematik untuk Day 001...")

    for i, sc in enumerate(SCENES_CONFIG, 1):
        filename = f"broll_{i}.mp4"
        file_path = os.path.join(broll_dir, filename)
        web_path = f"broll/{filename}"
        img_web_path = sc["fallback_image"]

        scene_entry = {
            "scene_id": sc["scene_id"],
            "timeStart": sc["timeStart"],
            "timeEnd": sc["timeEnd"],
            "videoSrc": None,
            "imageSrc": img_web_path,
            "description": sc["description"]
        }

        # Check if video already exists
        if os.path.exists(file_path) and os.path.getsize(file_path) > 100000:
            print(f"  ✓ Scene {i}: {filename} sudah ada ({os.path.getsize(file_path)/(1024*1024):.2f} MB)")
            scene_entry["videoSrc"] = web_path
        else:
            # Attempt Pexels video fetch
            vid_id, dl_url = search_pexels_video(sc["query"])
            if not dl_url:
                vid_id, dl_url = search_pexels_video(sc["fallback_query"])
            
            if dl_url:
                try:
                    print(f"  -> Mengunduh klip Pexels {vid_id} untuk '{sc['query']}'...")
                    download_file(dl_url, file_path)
                    print(f"  ✓ Sukses mengunduh {filename} ({os.path.getsize(file_path)/(1024*1024):.2f} MB)")
                    scene_entry["videoSrc"] = web_path
                except Exception as e:
                    print(f"  ✗ Gagal mengunduh: {e}")
            else:
                print(f"  - Menggunakan high-res 3D storybook image plate: {img_web_path}")

        manifest.append(scene_entry)

    manifest_path = os.path.join(DIR_PATH, "public", "broll_manifest.json")
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    print(f"[B-Roll] Manifest {len(manifest)} scene tersimpan di {manifest_path}")

if __name__ == "__main__":
    main()
