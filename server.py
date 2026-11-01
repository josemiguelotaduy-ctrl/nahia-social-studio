#!/usr/bin/env python3
"""
Nahia Home — Editorial Social Studio Server (Port 8090)
Serves the interactive Instagram & TikTok Live Preview Dashboard and handles
1-click publishing actions (Clipboard copy, Finder asset reveal, Graph API / Studio launch).
"""
import http.server, json, os, subprocess, urllib.parse, urllib.request, urllib.error

STUDIO_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(STUDIO_DIR)
MANIFEST_PATH = os.path.join(STUDIO_DIR, "posts_manifest.json")
PORT = 8090

def load_env():
    env = {}
    env_path = os.path.join(BASE_DIR, ".env")
    if os.path.exists(env_path):
        for line in open(env_path):
            line = line.strip()
            if "=" in line and not line.startswith("#"):
                k, v = line.split("=", 1)
                env[k] = v.strip().strip('"')
    return env

def copy_to_clipboard(text):
    try:
        p = subprocess.Popen(["pbcopy"], stdin=subprocess.PIPE)
        p.communicate(input=text.encode("utf-8"))
        return True
    except Exception:
        return False

class StudioHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=STUDIO_DIR, **kwargs)

    def _send_json(self, data, status=200):
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path.startswith("/api/posts"):
            with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
            return self._send_json({"posts": data})
        return super().do_GET()

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        raw = self.rfile.read(length).decode("utf-8") if length else "{}"
        payload = json.loads(raw) if raw else {}

        if self.path == "/api/publish/instagram":
            day = int(payload.get("day", 1))
            caption = payload.get("caption", "")
            mode = payload.get("mode", "carousel")  # carousel or reel
            copy_to_clipboard(caption)

            day_folder = os.path.join(STUDIO_DIR, "assets", f"day_{day:02d}")
            target_file = (
                os.path.join(day_folder, f"tiktok_reel_day_{day:02d}.mp4")
                if mode == "reel"
                else os.path.join(day_folder, "ig_slide_1_cover.jpg")
            )

            # Reveal the exact file(s) in Finder and open Instagram Web / Meta Business Suite
            subprocess.Popen(["open", "-R", target_file])
            subprocess.Popen(["open", "https://www.instagram.com/nahiahome/"])

            return self._send_json({
                "ok": True,
                "message": "Caption copied to clipboard! Opened Finder with Day "
                           f"{day:02d} slides highlighted & launched @nahiahome Instagram tab. "
                           "Click '+' on Instagram, drag the 4 slides in, and press Cmd+V to paste the caption."
            })

        elif self.path == "/api/publish/tiktok":
            day = int(payload.get("day", 1))
            caption = payload.get("caption", "")
            mode = payload.get("mode", "video")
            copy_to_clipboard(caption)

            day_folder = os.path.join(STUDIO_DIR, "assets", f"day_{day:02d}")
            target_file = (
                os.path.join(day_folder, f"tiktok_reel_day_{day:02d}.mp4")
                if mode == "video"
                else os.path.join(day_folder, "ig_slide_1_cover.jpg")
            )

            subprocess.Popen(["open", "-R", target_file])
            subprocess.Popen(["open", "https://www.tiktok.com/tiktokstudio/upload"])

            return self._send_json({
                "ok": True,
                "message": "TikTok caption copied to clipboard! Opened Finder with the 9:16 vertical MP4 "
                           "highlighted & launched TikTok Studio Upload. Drag the MP4 in and press Cmd+V!"
            })

        elif self.path == "/api/reveal-folder":
            day = int(payload.get("day", 1))
            day_folder = os.path.join(STUDIO_DIR, "assets", f"day_{day:02d}", "ig_slide_1_cover.jpg")
            subprocess.Popen(["open", "-R", day_folder])
            return self._send_json({"ok": True})

        elif self.path == "/api/update-status":
            day = int(payload.get("day", 1))
            new_status = payload.get("status", "PUBLISHED")
            ig_cap = payload.get("ig_caption")
            tt_cap = payload.get("tiktok_caption")
            with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
                posts = json.load(f)
            for p in posts:
                if p["day"] == day:
                    p["status"] = new_status
                    if ig_cap is not None:
                        p["ig_caption"] = ig_cap
                    if tt_cap is not None:
                        p["tiktok_caption"] = tt_cap
            with open(MANIFEST_PATH, "w", encoding="utf-8") as f:
                json.dump(posts, f, indent=2, ensure_ascii=False)
            return self._send_json({"ok": True, "posts": posts})

        return self._send_json({"error": "Unknown endpoint"}, 404)

if __name__ == "__main__":
    http.server.ThreadingHTTPServer.allow_reuse_address = True
    server = http.server.ThreadingHTTPServer(("127.0.0.1", PORT), StudioHandler)
    print(f"Nahia Home Editorial Social Studio running at http://localhost:{PORT}")
    server.serve_forever()
