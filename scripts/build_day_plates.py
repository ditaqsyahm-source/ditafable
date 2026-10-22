#!/usr/bin/env python3
"""
Bespoke 3D Pixar Storybook Plates & Manifest Generator for DITA-04 (@ditafable)
Reads curriculum content packet and generates 3D Pixar scene plates via FLUX.1-schnell,
writing public/images/day_XXX/ and public/broll_manifest_day_XXX.json.
"""

import os
import sys
import json
import subprocess
import argparse

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HERMES_PYTHON = r"C:\Users\K4G3\AppData\Local\hermes\tools\python-3.14.7+20260901-win32-x64\python.exe"
FLUX_SCRIPT = r"C:\Users\K4G3\AppData\Local\hermes\scripts\flux_generate.py"

def parse_timecode(tc):
    parts = tc.split("-")
    def to_sec(s):
        s = s.strip()
        m, sec = map(float, s.split(":"))
        return m * 60.0 + sec
    return to_sec(parts[0]), to_sec(parts[1])

def generate_fallback_storybook_plate(out_path, prompt, idx, day_str):
    """Algorithmic fallback plate if cloud FLUX hits quota or network error."""
    try:
        from PIL import Image, ImageDraw
        import random

        w, h = 720, 1280
        themes = [
            ((24, 45, 32), (8, 16, 12)),   # Emerald forest dusk
            ((48, 32, 20), (14, 10, 6)),   # Warm golden oak
            ((36, 24, 48), (12, 8, 18)),   # Twilight purple
            ((60, 40, 18), (18, 12, 6)),   # Sunset amber
            ((12, 18, 42), (4, 6, 16)),    # Starlight midnight
        ]
        top_rgb, bot_rgb = themes[(idx - 1) % len(themes)]

        im = Image.new("RGB", (w, h), bot_rgb)
        draw = ImageDraw.Draw(im)
        for y in range(h):
            ratio = y / h
            r = int(top_rgb[0] * (1 - ratio) + bot_rgb[0] * ratio)
            g = int(top_rgb[1] * (1 - ratio) + bot_rgb[1] * ratio)
            b = int(top_rgb[2] * (1 - ratio) + bot_rgb[2] * ratio)
            draw.line([(0, y), (w, y)], fill=(r, g, b))

        glow_im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        glow_draw = ImageDraw.Draw(glow_im)

        # Ambient central warmth orb
        cx, cy = w // 2, int(h * 0.42)
        radius = 260
        for r in range(radius, 0, -8):
            alpha = int(45 * (1 - r / radius))
            glow_draw.ellipse([(cx - r, cy - r), (cx + r, cy + r)], fill=(245, 158, 11, alpha))

        # Floating fairy dust specks
        random.seed(hash(prompt) + idx)
        for _ in range(50):
            sx = random.randint(40, w - 40)
            sy = random.randint(100, h - 200)
            srad = random.randint(3, 8)
            salpha = random.randint(90, 220)
            glow_draw.ellipse([(sx - srad, sy - srad), (sx + srad, sy + srad)], fill=(254, 240, 138, salpha))

        im.paste(glow_im, (0, 0), glow_im)
        im.save(out_path, "JPEG", quality=92)
        print(f"  ✓ Fallback Storybook Plate generated: {os.path.basename(out_path)}")
        return True
    except Exception as e:
        print(f"  ✗ Fallback generator error: {e}")
        return False

def build_plates_for_day(day_num, force=False):
    day_str = f"{day_num:03d}"
    packet_path = os.path.join(ROOT_DIR, "curriculum", f"content_packet_day_{day_str}.json")
    if not os.path.exists(packet_path):
        print(f"[Plates Builder] Error: packet not found {packet_path}")
        return False

    with open(packet_path, "r", encoding="utf-8") as f:
        packet = json.load(f)

    cues = packet.get("production_prompts_for_fullmontage", {}).get("midjourney_flux_visual_cues", [])
    if not cues:
        print(f"[Plates Builder] Warning: no visual cues in Day {day_num}")
        return False

    # Get actual audio duration if available
    audio_meta_path = os.path.join(ROOT_DIR, "public", f"audio_meta_day_{day_str}.json")
    total_audio_sec = None
    if os.path.exists(audio_meta_path):
        try:
            with open(audio_meta_path, "r", encoding="utf-8") as mf:
                mdata = json.load(mf)
                if mdata.get("duration_frames"):
                    total_audio_sec = mdata["duration_frames"] / 24.0
        except Exception:
            pass

    out_dir = os.path.join(ROOT_DIR, "public", "images", f"day_{day_str}")
    os.makedirs(out_dir, exist_ok=True)

    manifest = []
    py_exec = HERMES_PYTHON if os.path.exists(HERMES_PYTHON) else sys.executable

    print(f"============================================================")
    print(f"  BUILDING 3D PIXAR PLATES FOR DITA-04 DAY {day_str}")
    print(f"  Target Dir: {out_dir}")
    print(f"============================================================")

    for idx, sc in enumerate(cues, 1):
        sid = sc.get("scene_id") or f"SCENE_{idx:02d}"
        t_start, t_end = parse_timecode(sc["timecode"])
        prompt = sc["prompt"].replace("--ar 9:16", "").strip()
        img_name = f"scene_{idx:02d}.jpg"
        img_path = os.path.join(out_dir, img_name)
        web_path = f"images/day_{day_str}/{img_name}"

        if not os.path.exists(img_path) or force or os.path.getsize(img_path) < 1000:
            print(f"[{idx}/{len(cues)}] Generating: {prompt[:65]}...")
            cmd = [
                py_exec, FLUX_SCRIPT, prompt,
                "-o", img_path,
                "-w", "720", "-H", "1280",
                "--steps", "4", "--json"
            ]
            res = subprocess.run(cmd, capture_output=True, text=True)
            if res.returncode != 0 or not os.path.exists(img_path) or os.path.getsize(img_path) < 1000:
                print(f"  ✗ FLUX unavailable, generating artistic storybook plate...")
                generate_fallback_storybook_plate(img_path, prompt, idx, day_str)
            else:
                print(f"  ✓ Generated: {img_name} ({os.path.getsize(img_path) / 1024:.1f} KB)")
        else:
            print(f"[{idx}/{len(cues)}] Cache hit: {img_name} ({os.path.getsize(img_path) / 1024:.1f} KB)")

        manifest.append({
            "scene_id": sid,
            "timeStart": t_start,
            "timeEnd": t_end,
            "videoSrc": None,
            "imageSrc": web_path,
            "description": prompt[:100]
        })

    # Adjust last scene to reach total audio duration if defined
    if total_audio_sec and manifest:
        if manifest[-1]["timeEnd"] < total_audio_sec:
            manifest[-1]["timeEnd"] = round(total_audio_sec + 0.5, 2)

    manifest_file = os.path.join(ROOT_DIR, "public", f"broll_manifest_day_{day_str}.json")
    with open(manifest_file, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    print(f"[Plates Builder] Day {day_str} Manifest saved: {manifest_file}")
    return True

def main():
    parser = argparse.ArgumentParser(description="Build 3D Pixar plates for ditafable")
    parser.add_argument("--day", type=int, default=None, help="Day index")
    parser.add_argument("--all", action="store_true", help="Build for all available content packets")
    parser.add_argument("--force", action="store_true", help="Force regenerate plates")
    args = parser.parse_args()

    if args.all:
        import glob
        packets = sorted(glob.glob(os.path.join(ROOT_DIR, "curriculum", "content_packet_day_*.json")))
        for p in packets:
            with open(p, "r", encoding="utf-8") as pf:
                d = json.load(pf)
                day = d.get("metadata", {}).get("day_number")
                if day and day > 1: # Day 1 already has custom plates
                    build_plates_for_day(day, force=args.force)
    elif args.day:
        build_plates_for_day(args.day, force=args.force)
    else:
        print("Specify --day <N> or --all")

if __name__ == "__main__":
    main()
