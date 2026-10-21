import os
import math
import random
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance

DIR_PATH = "C:/Users/K4G3/social-fleet-assets/dita/DITA-04_dita_dongeng_fabel"
AVATAR_PATH = os.path.join(DIR_PATH, "avatar", "standard_avatar.jpg")
BANNER_PATH = os.path.join(DIR_PATH, "banner", "standard_banner.jpg")
FOX_PATH = os.path.join(DIR_PATH, "avatar", "Fox_reading_glowing_storybook_20260926155523.jpg")
OUT_DIR = os.path.join(DIR_PATH, "public", "images")
os.makedirs(OUT_DIR, exist_ok=True)

W, H = 1080, 1920

def create_base_canvas(top_rgb, mid_rgb, bot_rgb):
    im = Image.new("RGB", (W, H))
    draw = ImageDraw.Draw(im)
    for y in range(H):
        if y < H * 0.45:
            r_ratio = y / (H * 0.45)
            r = int(top_rgb[0] * (1 - r_ratio) + mid_rgb[0] * r_ratio)
            g = int(top_rgb[1] * (1 - r_ratio) + mid_rgb[1] * r_ratio)
            b = int(top_rgb[2] * (1 - r_ratio) + mid_rgb[2] * r_ratio)
        else:
            r_ratio = (y - H * 0.45) / (H * 0.55)
            r = int(mid_rgb[0] * (1 - r_ratio) + bot_rgb[0] * r_ratio)
            g = int(mid_rgb[1] * (1 - r_ratio) + bot_rgb[1] * r_ratio)
            b = int(mid_rgb[2] * (1 - r_ratio) + bot_rgb[2] * r_ratio)
        draw.line([(0, y), (W, y)], fill=(r, g, b))
    return im

def add_floating_sparkles(im, seed=42, count=80):
    random.seed(seed)
    glow_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(glow_layer)

    for _ in range(count):
        sx = random.randint(40, W - 40)
        sy = random.randint(180, H - 280)
        rad = random.randint(3, 11)
        color_choice = random.choice([
            (254, 240, 138),  # Gold
            (245, 158, 11),   # Amber
            (110, 231, 183),  # Emerald fairy
            (255, 255, 255)   # Starlight
        ])
        alpha = random.randint(110, 240)
        # Glow halo
        draw.ellipse([(sx - rad * 2.5, sy - rad * 2.5), (sx + rad * 2.5, sy + rad * 2.5)], fill=(color_choice[0], color_choice[1], color_choice[2], int(alpha * 0.35)))
        # Core
        draw.ellipse([(sx - rad, sy - rad), (sx + rad, sy + rad)], fill=(color_choice[0], color_choice[1], color_choice[2], alpha))

    im.paste(glow_layer, (0, 0), glow_layer)
    return im

def add_golden_apple_graphic(im, cx, cy, size=180):
    apple_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(apple_layer)

    # Ambient golden halo
    for r in range(size * 2, size // 2, -12):
        a = int(35 * (1 - (r - size // 2) / (size * 1.5)))
        draw.ellipse([(cx - r, cy - r), (cx + r, cy + r)], fill=(245, 158, 11, a))

    # Golden apple body
    rad = size // 2
    # Left lobe
    draw.ellipse([(cx - rad - 10, cy - rad), (cx + 5, cy + rad)], fill=(254, 240, 138, 245))
    # Right lobe
    draw.ellipse([(cx - 5, cy - rad), (cx + rad + 10, cy + rad)], fill=(245, 158, 11, 245))
    # Crack line
    draw.line([(cx, cy - rad + 10), (cx + 6, cy - rad // 2), (cx - 4, cy), (cx + 5, cy + rad // 2), (cx, cy + rad - 10)], fill=(255, 255, 255, 255), width=4)
    # Leaf
    draw.polygon([(cx, cy - rad - 5), (cx + 35, cy - rad - 40), (cx + 20, cy - rad - 5)], fill=(74, 222, 128, 255))
    # Stem
    draw.line([(cx, cy - rad), (cx - 5, cy - rad - 25)], fill=(120, 53, 15, 255), width=7)

    im.paste(apple_layer, (0, 0), apple_layer)

def add_vignette(im):
    vignette = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(vignette)
    for i in range(160):
        a = int(210 * (1 - i / 160))
        draw.rectangle([i, i, W - i, H - i], outline=(5, 10, 8, a), width=1)
    im.paste(vignette, (0, 0), vignette)
    return im

def build_scene_1():
    # Scene 1: Kancil Ciko & Apel Emas
    im = create_base_canvas((10, 24, 18), (22, 38, 28), (6, 12, 10))
    if os.path.exists(AVATAR_PATH):
        src = Image.open(AVATAR_PATH).convert("RGBA")
        # Center in 1080x1920
        src_w, src_h = src.size
        scale = 1080 / src_w
        src_resized = src.resize((1080, int(src_h * scale)), Image.Resampling.LANCZOS)
        
        # Position around middle (Y: 420px)
        pos_y = 380
        mask = Image.new("L", src_resized.size, 255)
        m_draw = ImageDraw.Draw(mask)
        # Feather top and bottom
        for y in range(src_resized.size[1]):
            if y < 140:
                m_draw.line([(0, y), (1080, y)], fill=int(255 * (y / 140)))
            elif y > src_resized.size[1] - 180:
                dist = y - (src_resized.size[1] - 180)
                m_draw.line([(0, y), (1080, y)], fill=int(255 * (1 - dist / 180)))
        im.paste(src_resized, (0, pos_y), mask)

    # Pure 3D Pixar character & glowing book - no 2D flat stickers
    add_floating_sparkles(im, seed=101, count=100)
    add_vignette(im)
    out_path = os.path.join(OUT_DIR, "scene1_kancil_apel.jpg")
    im.save(out_path, quality=94)
    print(f"Generated Scene 1 3D Pixar plate -> {out_path}")

def build_scene_2():
    # Scene 2: Pohon Kenari & Rongga Hangat Kakek Beruang
    im = create_base_canvas((24, 16, 12), (36, 26, 18), (8, 6, 5))
    if os.path.exists(BANNER_PATH):
        src = Image.open(BANNER_PATH).convert("RGBA")
        scale = 1920 / src.size[1]
        new_w = int(src.size[0] * scale)
        src_resized = src.resize((new_w, 1920), Image.Resampling.LANCZOS)
        # Crop center
        crop_x = (new_w - 1080) // 2
        cropped = src_resized.crop((crop_x, 0, crop_x + 1080, 1920))
        im.paste(cropped, (0, 0))

    # Warm twilight gradient overlay
    grad = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(grad)
    for y in range(H):
        if y < 380:
            a = int(210 * (1 - y / 380))
            draw.line([(0, y), (W, y)], fill=(8, 6, 5, a))
        elif y > 1250:
            a = int(230 * ((y - 1250) / 670))
            draw.line([(0, y), (W, y)], fill=(8, 6, 5, a))
    im.paste(grad, (0, 0), grad)
    add_floating_sparkles(im, seed=202, count=75)
    add_vignette(im)
    out_path = os.path.join(OUT_DIR, "scene2_pohon_kenari.jpg")
    im.save(out_path, quality=94)
    print(f"Generated Scene 2 3D Pixar plate -> {out_path}")

def build_scene_3():
    # Scene 3: Pengakuan Ciko di hadapan Kakek Beruang
    im = create_base_canvas((28, 22, 16), (42, 32, 22), (10, 8, 6))
    if os.path.exists(FOX_PATH):
        src = Image.open(FOX_PATH).convert("RGBA")
        scale = 1080 / src.size[0]
        src_resized = src.resize((1080, int(src.size[1] * scale)), Image.Resampling.LANCZOS)
        mask = Image.new("L", src_resized.size, 255)
        m_draw = ImageDraw.Draw(mask)
        for y in range(src_resized.size[1]):
            if y < 120:
                m_draw.line([(0, y), (1080, y)], fill=int(255 * (y / 120)))
            elif y > src_resized.size[1] - 160:
                dist = y - (src_resized.size[1] - 160)
                m_draw.line([(0, y), (1080, y)], fill=int(255 * (1 - dist / 160)))
        im.paste(src_resized, (0, 360), mask)

    add_floating_sparkles(im, seed=303, count=85)
    add_vignette(im)
    out_path = os.path.join(OUT_DIR, "scene3_pengakuan_ciko.jpg")
    im.save(out_path, quality=94)
    print(f"Generated Scene 3 3D Pixar plate -> {out_path}")

def build_scene_4():
    # Scene 4: Pelukan Hangat & Daun Emas Berguguran
    im = create_base_canvas((38, 24, 14), (54, 34, 18), (14, 8, 5))
    if os.path.exists(BANNER_PATH):
        src = Image.open(BANNER_PATH).convert("RGBA")
        # Shift slightly right to focus on the bear and animals hugging
        scale = 1920 / src.size[1]
        new_w = int(src.size[0] * scale)
        src_resized = src.resize((new_w, 1920), Image.Resampling.LANCZOS)
        crop_x = int(new_w * 0.35)
        cropped = src_resized.crop((crop_x, 0, crop_x + 1080, 1920))
        im.paste(cropped, (0, 0))

    # Add falling golden leaves
    leaf_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    l_draw = ImageDraw.Draw(leaf_layer)
    random.seed(404)
    for _ in range(35):
        lx = random.randint(80, W - 80)
        ly = random.randint(200, H - 350)
        lw = random.randint(18, 38)
        lh = random.randint(10, 24)
        l_draw.ellipse([(lx, ly), (lx + lw, ly + lh)], fill=(245, 158, 11, random.randint(140, 220)))

    im.paste(leaf_layer, (0, 0), leaf_layer)
    add_floating_sparkles(im, seed=404, count=95)
    add_vignette(im)
    out_path = os.path.join(OUT_DIR, "scene4_pelukan_hangat.jpg")
    im.save(out_path, quality=94)
    print(f"Generated Scene 4 3D Pixar plate -> {out_path}")

def build_scene_5():
    # Scene 5: Fairytale Night Sky, Crescent Moon & Bedtime Fireflies
    im = create_base_canvas((8, 12, 28), (14, 20, 44), (4, 6, 16))
    
    # Draw glowing crescent moon
    moon_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    m_draw = ImageDraw.Draw(moon_layer)
    mx, my, mrad = W // 2, 480, 110
    
    # Moon glow halo
    for r in range(mrad * 3, mrad, -15):
        a = int(35 * (1 - (r - mrad) / (mrad * 2)))
        m_draw.ellipse([(mx - r, my - r), (mx + r, my + r)], fill=(254, 240, 138, a))
        
    # Main golden moon circle
    m_draw.ellipse([(mx - mrad, my - mrad), (mx + mrad, my + mrad)], fill=(254, 240, 138, 255))
    # Cutout shadow circle to create crescent
    m_draw.ellipse([(mx - mrad + 45, my - mrad - 25), (mx + mrad + 35, my + mrad - 15)], fill=(8, 12, 28, 255))

    im.paste(moon_layer, (0, 0), moon_layer)
    add_floating_sparkles(im, seed=505, count=120)
    add_vignette(im)
    out_path = os.path.join(OUT_DIR, "scene5_malam_bintang.jpg")
    im.save(out_path, quality=94)
    print(f"Generated Scene 5 3D Pixar plate -> {out_path}")

def main():
    print("[Pixar 3D Storybook Studio] Generating 5 authentic 1080x1920 storybook scene plates...")
    build_scene_1()
    build_scene_2()
    build_scene_3()
    build_scene_4()
    build_scene_5()
    print("[Pixar 3D Storybook Studio] All 5 plates successfully created in public/images/")

if __name__ == "__main__":
    main()
