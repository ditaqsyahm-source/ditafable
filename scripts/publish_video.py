#!/usr/bin/env python3
"""
DITA-04 Sovereign Multi-Platform Publisher (@ditafable)
Unified publishing engine for:
- YouTube Shorts (Direct YouTube Data API v3 Resumable Upload)
- TikTok (Zernio uploadMediaDirect + createPost)
- Instagram Reels (Zernio uploadMediaDirect + createPost)
"""

import os
import sys
import json
import urllib.parse
import urllib.request
import urllib.error
import hashlib
from datetime import datetime

DIR_PATH = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(DIR_PATH)
STATE_DIR = os.path.join(ROOT_DIR, "state")
PUBLISHED_PATH = os.path.join(STATE_DIR, "published.json")
CAMPAIGN_STATE_PATH = os.path.join(STATE_DIR, "campaign_state.json")
os.makedirs(STATE_DIR, exist_ok=True)

def load_env():
    env = dict(os.environ)
    env_paths = [
        os.path.join(ROOT_DIR, ".env"),
        os.path.join(DIR_PATH, ".env"),
        r"C:\Users\K4G3\social-fleet-pipeline\.env"
    ]
    for candidate in env_paths:
        if os.path.exists(candidate):
            with open(candidate, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        k, v = line.split("=", 1)
                        if k.strip() not in env:
                            env[k.strip()] = v.strip()
    return env

ENV = load_env()

def compute_file_hash(filepath):
    if not os.path.exists(filepath):
        return ""
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()

# -------------------------------------------------------------
# 1. YOUTUBE PUBLISHING (Direct YouTube Data API v3)
# -------------------------------------------------------------
def get_yt_access_token():
    refresh_token = ENV.get("YT_REFRESH_TOKEN")
    client_id = ENV.get("GOOGLE_CLIENT_ID")
    client_secret = ENV.get("GOOGLE_CLIENT_SECRET")
    
    if not refresh_token or not client_id or not client_secret:
        raise ValueError("Google YouTube OAuth credentials belum lengkap di environment")
        
    data = urllib.parse.urlencode({
        "refresh_token": refresh_token,
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": "refresh_token"
    }).encode("utf-8")
    
    req = urllib.request.Request("https://oauth2.googleapis.com/token", data=data, headers={
        "Content-Type": "application/x-www-form-urlencoded"
    })
    with urllib.request.urlopen(req) as resp:
        res = json.loads(resp.read().decode())
        return res.get("access_token")

def upload_to_youtube(video_path, title, description, tags=None, privacy="public", thumbnail_path=None):
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"File video tidak ditemukan: {video_path}")
        
    token = get_yt_access_token()
    file_size = os.path.getsize(video_path)
    clean_title = title.replace("<", "").replace(">", "").strip()[:100]
    clean_desc = description.replace("<", "").replace(">", "").strip()[:5000]
    
    snippet = {
        "title": clean_title,
        "description": clean_desc,
        "categoryId": "27",  # Education / Kids Moral Stories
        "defaultLanguage": "id"
    }
    if tags:
        snippet["tags"] = tags
        
    meta = {
        "snippet": snippet,
        "status": {
            "privacyStatus": privacy,
            "selfDeclaredMadeForKids": True
        }
    }
    
    init_req = urllib.request.Request(
        "https://www.googleapis.com/upload/youtube/v3/videos?uploadType=resumable&part=snippet,status",
        data=json.dumps(meta).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json; charset=UTF-8",
            "X-Upload-Content-Type": "video/mp4",
            "X-Upload-Content-Length": str(file_size)
        },
        method="POST"
    )
    with urllib.request.urlopen(init_req) as init_resp:
        upload_url = init_resp.headers.get("Location")
        
    if not upload_url:
        raise ValueError("YouTube tidak mengembalikan upload URL resumable")
        
    print(f"[YouTube] Mengunggah Shorts ({file_size / (1024*1024):.2f} MB)...")
    chunk_size = 8 * 1024 * 1024
    with open(video_path, "rb") as vf:
        offset = 0
        video_id = None
        while offset < file_size:
            chunk = vf.read(min(chunk_size, file_size - offset))
            n = len(chunk)
            req = urllib.request.Request(
                upload_url,
                data=chunk,
                headers={
                    "Content-Type": "video/mp4",
                    "Content-Length": str(n),
                    "Content-Range": f"bytes {offset}-{offset + n - 1}/{file_size}"
                },
                method="PUT"
            )
            try:
                with urllib.request.urlopen(req) as resp:
                    if resp.status in [200, 201]:
                        res_json = json.loads(resp.read().decode())
                        video_id = res_json.get("id")
                        break
            except urllib.error.HTTPError as e:
                if e.code == 308:
                    pass
                else:
                    raise e
            offset += n
            
    if not video_id:
        raise RuntimeError("Video upload selesai tetapi video ID tidak ditemukan")
        
    yt_url = f"https://youtube.com/shorts/{video_id}"
    print(f"[YouTube] ✅ BERHASIL TAYANG -> {yt_url}")
    
    if thumbnail_path and os.path.exists(thumbnail_path):
        try:
            with open(thumbnail_path, "rb") as tf:
                thumb_bytes = tf.read()
            t_req = urllib.request.Request(
                f"https://www.googleapis.com/upload/youtube/v3/thumbnails/set?videoId={video_id}",
                data=thumb_bytes,
                headers={
                    "Authorization": f"Bearer {token}",
                    "Content-Type": "image/jpeg"
                },
                method="POST"
            )
            with urllib.request.urlopen(t_req) as t_resp:
                if t_resp.status in [200, 201]:
                    print("[YouTube] Custom thumbnail berhasil diset!")
        except Exception as e:
            print(f"[YouTube] Set thumbnail dilewati (non-fatal): {e}")
            
    return {"platform": "youtube", "ok": True, "videoId": video_id, "url": yt_url}

# -------------------------------------------------------------
# 2. ZERNIO UPLOAD (TikTok & Instagram Reels via Presigned R2)
# -------------------------------------------------------------
def upload_file_to_zernio(file_path, content_type="video/mp4"):
    z_key = ENV.get("ZERNIO_API_KEY")
    if not z_key:
        raise ValueError("ZERNIO_API_KEY belum diset di environment")
        
    file_size = os.path.getsize(file_path)
    file_name = os.path.basename(file_path)
    
    # 1. Presign R2 upload URL
    presign_req = urllib.request.Request(
        "https://api.zernio.com/v1/media/presign",
        data=json.dumps({
            "filename": file_name,
            "contentType": content_type,
            "size": file_size
        }).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {z_key}",
            "Content-Type": "application/json"
        },
        method="POST"
    )
    with urllib.request.urlopen(presign_req) as p_resp:
        presign_data = json.loads(p_resp.read().decode())
        upload_url = presign_data.get("uploadUrl")
        public_url = presign_data.get("publicUrl")
        
    if not upload_url or not public_url:
        raise ValueError(f"Gagal mendapatkan presigned URL Zernio: {presign_data}")
        
    print(f"[Zernio] Mengunggah {content_type} binary ({file_size / (1024*1024):.2f} MB)...")
    with open(file_path, "rb") as f:
        media_bytes = f.read()
        
    put_req = urllib.request.Request(
        upload_url,
        data=media_bytes,
        headers={"Content-Type": content_type},
        method="PUT"
    )
    with urllib.request.urlopen(put_req) as put_resp:
        if put_resp.status not in [200, 204]:
            raise RuntimeError(f"Gagal upload binary ke R2: status {put_resp.status}")
            
    print(f"[Zernio] Binary berhasil terunggah ke Cloudflare R2: {public_url}")
    return public_url

def upload_to_zernio(video_path, caption, thumbnail_path=None):
    z_key = ENV.get("ZERNIO_API_KEY")
    tiktok_id = ENV.get("TIKTOK_ACCOUNT_ID") or "6ad8acf3c24aa78753a651ef"
    ig_id = ENV.get("INSTAGRAM_ACCOUNT_ID") or "6ad8acd9aad76462b1a71e23"
    
    if not z_key:
        raise ValueError("ZERNIO_API_KEY belum diset")
        
    video_url = upload_file_to_zernio(video_path, content_type="video/mp4")
    
    # Optional cover image upload via presign
    cover_url = None
    if thumbnail_path and os.path.exists(thumbnail_path):
        try:
            print("[Zernio] Uploading thumbnail cover...")
            cover_url = upload_file_to_zernio(thumbnail_path, content_type="image/jpeg")
        except Exception as e:
            print(f"[Zernio] Warning: thumbnail upload dilewati: {e}")

    platforms = []
    if tiktok_id:
        p_tt = {"platform": "tiktok", "accountId": tiktok_id}
        if cover_url:
            p_tt["platformSpecificData"] = {"videoCoverImageUrl": cover_url}
        platforms.append(p_tt)
        
    if ig_id:
        p_ig = {"platform": "instagram", "accountId": ig_id}
        if cover_url:
            p_ig["platformSpecificData"] = {"instagramThumbnail": cover_url}
        platforms.append(p_ig)
        
    post_payload = {
        "title": caption.split("\n")[0][:80],
        "content": caption,
        "mediaItems": [{"type": "video", "url": video_url}],
        "platforms": platforms,
        "publishNow": True
    }
    
    post_req = urllib.request.Request(
        "https://api.zernio.com/v1/posts",
        data=json.dumps(post_payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {z_key}",
            "Content-Type": "application/json"
        },
        method="POST"
    )
    with urllib.request.urlopen(post_req) as post_resp:
        post_res = json.loads(post_resp.read().decode())
        post_obj = post_res.get("post") or post_res.get("data") or post_res
        post_id = post_obj.get("_id") or post_obj.get("id")
        
    print(f"[Zernio] ✅ POST BERHASIL DIBUAT (ID: {post_id})")
    return {"platform": "zernio", "ok": True, "postId": post_id, "data": post_obj}

# -------------------------------------------------------------
# 3. STATUS & HEALTH CHECK
# -------------------------------------------------------------
def check_status():
    print("="*60)
    print("  STATUS INTEGRASI MULTI-PLATFORM DITA-04 (@ditafable)")
    print("="*60)
    
    # Check YouTube
    yt_token_set = bool(ENV.get("YT_REFRESH_TOKEN"))
    if yt_token_set:
        try:
            token = get_yt_access_token()
            req = urllib.request.Request(
                "https://www.googleapis.com/youtube/v3/channels?part=snippet,statistics&mine=true",
                headers={"Authorization": f"Bearer {token}"}
            )
            with urllib.request.urlopen(req) as resp:
                data = json.loads(resp.read().decode())
                items = data.get("items", [])
                if items:
                    ch = items[0]
                    print(f" [YouTube]   OK -> Channel: '{ch['snippet']['title']}' ({ch['snippet'].get('customUrl', 'no-custom-url')})")
                    print(f"             ID: {ch['id']} | Videos: {ch['statistics'].get('videoCount', 0)} | Views: {ch['statistics'].get('viewCount', 0)}")
                else:
                    print(" [YouTube]   WARNING -> Token valid tapi tidak ada channel")
        except Exception as e:
            print(f" [YouTube]   ERROR -> {e}")
    else:
        print(" [YouTube]   PENDING -> YT_REFRESH_TOKEN belum diset")
        
    # Check Zernio
    z_key = ENV.get("ZERNIO_API_KEY")
    if z_key:
        try:
            req = urllib.request.Request(
                "https://api.zernio.com/v1/accounts",
                headers={"Authorization": f"Bearer {z_key}"}
            )
            with urllib.request.urlopen(req) as resp:
                data = json.loads(resp.read().decode())
                accs = data.get("accounts", [])
                print(f" [Zernio]    OK -> Terhubung {len(accs)} akun:")
                for a in accs:
                    plat = a.get("platform")
                    u = a.get("username", a.get("name"))
                    acc_id = a.get("id") or a.get("_id")
                    print(f"    - [{plat.upper()}] @{u} (ID: {acc_id})")
        except Exception as e:
            print(f" [Zernio]    ERROR -> {e}")
    else:
        print(" [Zernio]    ERROR -> ZERNIO_API_KEY tidak ada")

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "status":
        check_status()
        return

    import argparse
    parser = argparse.ArgumentParser(description="Multi-platform publisher for DITA-04")
    parser.add_argument("--day", type=int, default=None, help="Day index to publish")
    parser.add_argument("--video", type=str, default=None, help="Custom video path")
    parser.add_argument("--dry-run", action="store_true", help="Dry run without real upload")
    args = parser.parse_args()

    day_num = args.day
    if day_num is None:
        if os.path.exists(CAMPAIGN_STATE_PATH):
            try:
                with open(CAMPAIGN_STATE_PATH, "r", encoding="utf-8") as f:
                    cs = json.load(f)
                    day_num = cs.get("next_day") or (cs.get("active_day", 1) + 1)
            except Exception:
                day_num = 1
        else:
            day_num = 1

    day_str = f"{day_num:03d}"
    packet_file = os.path.join(ROOT_DIR, "curriculum", f"content_packet_day_{day_str}.json")
    video_file = args.video or os.path.join(ROOT_DIR, "output", f"dita_fable_day_{day_str}_master.mp4")

    print("="*60)
    print(f"  DITA-04 PUBLISHER: DAY {day_str}")
    print(f"  Target Video: {video_file}")
    print("="*60)

    if not os.path.exists(video_file):
        print(f"Error: Video file not found: {video_file}")
        sys.exit(1)

    # Load metadata from packet
    title = f"Dongeng Fabel Day {day_num}"
    caption = "Dongeng fabel pengantar tidur penuh pesan moral ramah anak dan keluarga. #DitaDongeng #FabelAnak #CeritaAnak #KidsStories"
    tags = ["dongeng", "fabel", "cerita anak", "bedtime story", "moral value", "kak dita"]
    
    if os.path.exists(packet_file):
        with open(packet_file, "r", encoding="utf-8") as pf:
            p_data = json.load(pf)
            dist_meta = p_data.get("social_fleet_distribution_metadata", {})
            title = dist_meta.get("title") or title
            caption = dist_meta.get("caption") or caption
            tags = dist_meta.get("tags") or tags

    thumb_file = os.path.join(ROOT_DIR, "output", "preview_frames", "frame_05_kakek_beruang_memeluk.jpg")
    if not os.path.exists(thumb_file):
        thumb_file = os.path.join(ROOT_DIR, "output", "preview_frames", "frame_42s_moral_hug.jpg")
    if not os.path.exists(thumb_file):
        thumb_file = None

    if args.dry_run:
        print("[DRY-RUN] Title:", title)
        print("[DRY-RUN] Caption:", caption[:100] + "...")
        print("[DRY-RUN] Video size:", os.path.getsize(video_file))
        print("[DRY-RUN] Success (simulated)!")
        return

    # Real publication
    results = {}

    # Check if YouTube already published successfully in prior run
    existing_yt = None
    if os.path.exists(PUBLISHED_PATH):
        try:
            with open(PUBLISHED_PATH, "r", encoding="utf-8") as f:
                past = json.load(f)
                for p in past:
                    if p.get("day") == day_num and p.get("outcomes", {}).get("youtube", {}).get("ok"):
                        existing_yt = p["outcomes"]["youtube"]
                        break
        except Exception:
            pass

    if existing_yt:
        print(f"[YouTube] Day {day_num} sudah pernah terbit ({existing_yt.get('url')}), skip re-upload.")
        results["youtube"] = existing_yt
    else:
        try:
            results["youtube"] = upload_to_youtube(video_file, title, caption, tags=tags, thumbnail_path=thumb_file)
        except Exception as e:
            print(f"[YouTube] Publish failed: {e}")
            results["youtube"] = {"platform": "youtube", "ok": False, "error": str(e)}

    try:
        results["zernio"] = upload_to_zernio(video_file, caption, thumbnail_path=thumb_file)
    except Exception as e:
        print(f"[Zernio] Publish failed: {e}")
        results["zernio"] = {"platform": "zernio", "ok": False, "error": str(e)}

    # Append to published receipts
    published_records = []
    if os.path.exists(PUBLISHED_PATH):
        try:
            with open(PUBLISHED_PATH, "r", encoding="utf-8") as f:
                published_records = json.load(f)
        except Exception:
            published_records = []

    receipt = {
        "channel_id": "DITA-04",
        "day": day_num,
        "title": title,
        "video_file": video_file,
        "video_hash": compute_file_hash(video_file),
        "timestamp": datetime.now().isoformat(),
        "outcomes": results
    }
    published_records.append(receipt)
    with open(PUBLISHED_PATH, "w", encoding="utf-8") as f:
        json.dump(published_records, f, indent=2)

    print(f"[Receipts] Updated {PUBLISHED_PATH}")

if __name__ == "__main__":
    main()
