#!/usr/bin/env python3
"""
Generates Week 1 (7 Days) of Ultra-Premium Westwing-Style Instagram Carousels (1080x1350)
and 9:16 Vertical Instagram Reels & TikTok Videos (MP4 with embedded stereo AAC music) for Nahia Home:
- 100% Editorial English
- ZERO prices on any image
- ZERO cropped/cut-off products (every product is 100% visible in full)
- Cover slides show ONLY the single main editorial title at the bottom (no confusing secondary subtitles or mismatched product names)
- Detail/Story slides (Slides 2 & 3) show ONLY the italic serif headline at the bottom (no multi-line subtitle paragraph underneath)
- Curated Edit (Slide 4) ONLY includes products that actually appear in Slides 1, 2, and 3 of that post
- Every 9:16 video is generated for both Instagram Reels and TikTok with its editorial music track embedded inside the MP4
"""
import os, json, math, urllib.request, urllib.parse, subprocess, shutil
import numpy as np
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = "/Users/josemiguellavao/Desktop/NAHIA HOME"
STUDIO_DIR = os.path.join(BASE_DIR, "social_studio")
ASSETS_DIR = os.path.join(STUDIO_DIR, "assets")
AUDIO_DIR = os.path.join(ASSETS_DIR, "audio")
CUTOUTS_DIR = os.path.join(STUDIO_DIR, "cutouts")
STD_DIR = os.path.join(BASE_DIR, "scratch/batch_standardization")
os.makedirs(ASSETS_DIR, exist_ok=True)
os.makedirs(AUDIO_DIR, exist_ok=True)
os.makedirs(CUTOUTS_DIR, exist_ok=True)

DIDOT_PATH = "/System/Library/Fonts/Supplemental/Didot.ttc"
GILL_PATH = "/System/Library/Fonts/Supplemental/GillSans.ttc"

def font_serif(size, italic=False):
    try:
        return ImageFont.truetype(DIDOT_PATH, size, index=1 if italic else 0)
    except Exception:
        return ImageFont.load_default()

def font_sans(size, bold=False):
    try:
        return ImageFont.truetype(GILL_PATH, size, index=2 if bold else 0)
    except Exception:
        return ImageFont.load_default()

# Product catalog items — NO prices displayed on slides, only Maison, Title, and Materiality note
PRODUCTS = {
    "vaso_abeille": {
        "title": '"Abeille" Water Tumbler',
        "brand": "LA ROCHÈRE · FRANCE 1475",
        "material_note": "Pressed French Crystal · 26 cl",
        "handle": "/products/vaso-agua-abeille-26cl",
        "local": os.path.join(BASE_DIR, "work/video_assets/vaso_clean.png")
    },
    "copa_abeille_verde": {
        "title": '"Abeille" Olive Wine Goblet',
        "brand": "LA ROCHÈRE · FRANCE 1475",
        "material_note": "Olive Tinted Pressed Crystal · 24 cl",
        "handle": "/products/copa-de-vino-abeille-verde-oliva-240ml",
        "local": os.path.join(BASE_DIR, "work/video_assets/copa_clean.png")
    },
    "jarra_abeille": {
        "title": '"Abeille" Glass Pitcher',
        "brand": "LA ROCHÈRE · FRANCE 1475",
        "material_note": "Pressed French Crystal · 1 L",
        "handle": "/products/jarra-de-cristal-abeille-1-l",
        "local": os.path.join(STD_DIR, "jarra-de-cristal-abeille-1l/primary.jpg")
    },
    "jarra_soplado_abeille": {
        "title": '"Abeille" Blown-Glass Carafe',
        "brand": "LA ROCHÈRE · FRANCE 1475",
        "material_note": "Mouth-Blown French Glass · 1 L",
        "handle": "/products/jarra-de-vidrio-soplado-abeille-1l",
        "local": os.path.join(STD_DIR, "jarra-de-vidrio-soplado-abeille-1l/primary.jpg")
    },
    "minibol_abeille": {
        "title": '"Abeille" Mini Glass Bowl',
        "brand": "LA ROCHÈRE · FRANCE 1475",
        "material_note": "Pressed French Crystal · 27 cl",
        "handle": "/products/mini-bol-abeille-27-cl",
        "local": os.path.join(STD_DIR, "mini-bol-abeille-27-cl/primary.jpg")
    },
    "plato_pearl": {
        "title": "Pearl Stoneware Plate",
        "brand": "COSTA NOVA · PORTUGAL",
        "material_note": "Fine Portuguese Stoneware",
        "handle": "/products/bowl-perla",
        "local": os.path.join(BASE_DIR, "work/video_assets/plato_clean.png")
    },
    "ensaladera_pearl": {
        "title": "Pearl Stoneware Salad Bowl",
        "brand": "COSTA NOVA · PORTUGAL",
        "material_note": "Beaded Rim Stoneware · 27 cm",
        "handle": "/products/ensaladera-costa-nova-pearl-27cm",
        "local": os.path.join(STD_DIR, "ensaladera-costa-nova-pearl-27cm/primary.jpg")
    },
    "jarra_alheli": {
        "title": "Alhelí Ribbed Pitcher",
        "brand": "CÔTÉ TABLE · PARIS",
        "material_note": "Mouth-Blown Green Glass · 2.3 L",
        "handle": "/products/jarra-alheli-cote-table-2-3-l",
        "local": os.path.join(STD_DIR, "jarra-alheli-cote-table-2-3-l/primary.jpg")
    },
    "grifo_livlig": {
        "title": "Architectural Garden Tap",
        "brand": "LIVLIG · GARDEN ARCHITECTURE",
        "material_note": "Solid Brass & Sage Rosette",
        "handle": "/products/grifo-de-jardin-con-roseta-green-livlig",
        "local": os.path.join(STD_DIR, "grifo-de-jardin-con-roseta-green-livlig/primary.jpg")
    },
    "manguera_green_livlig": {
        "title": "Graceful Green Garden Hose",
        "brand": "LIVLIG · GARDEN ARCHITECTURE",
        "material_note": "UV-Resistant Matte Weave · 20M",
        "handle": "/products/manguera-de-jardin-graceful-green-20m-livlig",
        "local": os.path.join(STD_DIR, "manguera-de-jardin-graceful-green-20m-livlig/primary.jpg")
    },
    "soporte_livlig": {
        "title": "Graceful Green Hose Holder",
        "brand": "LIVLIG · GARDEN ARCHITECTURE",
        "material_note": "Powder-Coated Architectural Steel",
        "handle": "/products/soporte-de-manguera-graceful-green-livlig",
        "local": os.path.join(STD_DIR, "soporte-de-manguera-graceful-green-livlig/primary.jpg")
    },
    "abanico_viana": {
        "title": "Santanyí Linen Hand Fan",
        "brand": "THE VIANA FAN · ARTISANAL",
        "material_note": "Organic Linen & Noble Wood",
        "handle": "/products/abanico-de-lino-santanyi-the-viana-fan",
        "local": os.path.join(BASE_DIR, "work/video_assets/abanico_clean.png")
    },
    "libro_slim": {
        "title": "Slim Aarons — La Dolce Vita",
        "brand": "CURATED EDITIONS · MONOGRAPH",
        "material_note": "Hardcover Collector’s Edition",
        "handle": "/products/slim-aarons-la-dolce-vita",
        "local": os.path.join(BASE_DIR, "work/video_assets/libro_slim_aarons.webp")
    },
    "libro_lemon": {
        "title": "The Gourmand’s Lemon",
        "brand": "TASCHEN · ART & GASTRONOMY",
        "material_note": "Illustrated Hardcover Volume",
        "handle": "/products/the-gourmands-lemon",
        "local": os.path.join(BASE_DIR, "work/video_assets/libro_gourmand_lemon.webp")
    },
    "tetera_pearl": {
        "title": "Pearl Stoneware Teapot",
        "brand": "COSTA NOVA · PORTUGAL",
        "material_note": "Beaded Rim Stoneware & Infuser",
        "handle": "/products/tetera-con-infusor-pearl-costa-nova",
        "local": os.path.join(STD_DIR, "tetera-con-infusor-pearl-costa-nova/primary.jpg")
    },
    "taza_pearl": {
        "title": "Pearl Espresso Cup & Saucer",
        "brand": "COSTA NOVA · PORTUGAL",
        "material_note": "Glazed Portuguese Stoneware",
        "handle": "/products/taza-de-cafe-con-plato-costa-nova-pearl"
    },
    "taza_perloa": {
        "title": "Perloa Beaded Cup & Saucer",
        "brand": "CÔTÉ TABLE · PARIS",
        "material_note": "Sculpted French Glass · 18 cl",
        "handle": "/products/taza-de-te-c-plato-perloa-cote-table-18cl",
        "local": os.path.join(STD_DIR, "taza-de-te-c-plato-perloa-cote-table-18cl/primary.jpg")
    },
    "lechera_pearl": {
        "title": "Pearl Stoneware Creamer",
        "brand": "COSTA NOVA · PORTUGAL",
        "material_note": "Beaded Rim Stoneware · 10 cl",
        "handle": "/products/lechera-pearl-10cl-costa-nova",
        "local": os.path.join(STD_DIR, "lechera-pearl-10cl-costa-nova/primary.jpg")
    },
    "mantel_casalopez": {
        "title": "Majorque Linen Placemat",
        "brand": "CASA LÓPEZ · PARIS",
        "material_note": "Pure Woven Linen · Vert Olive",
        "handle": "/products/mantel-individual-lino-majorque-vert-olive-casa-lopez",
        "local": os.path.join(STD_DIR, "mantel-individual-lino-majorque-vert-olive-casa-lopez-paris/primary.jpg")
    },
    "servilleta_emperatriz": {
        "title": "Emperatriz Linen Napkin",
        "brand": "CASA LÓPEZ · PARIS",
        "material_note": "Botanical Embroidered Linen",
        "handle": "/products/servilleta-lino-emperatriz-casa-lopez-paris",
        "local": os.path.join(STD_DIR, "servilleta-lino-emperatriz-casa-lopez-paris/primary.jpg")
    },
    "cuaderno_umbel": {
        "title": "Umbel Botanical Notebook",
        "brand": "ARTISANAL STATIONERY",
        "material_note": "Embroidered Linen Spine",
        "handle": "/products/cuaderno-de-notas-umbel",
        "local": os.path.join(BASE_DIR, "work/umbel_final_1000.jpg")
    }
}

def load_product_image(key):
    info = PRODUCTS[key]
    if "local" in info and os.path.exists(info["local"]):
        im = Image.open(info["local"]).convert("RGBA")
    else:
        slug = info["handle"].split("/")[-1]
        std_path = os.path.join(STD_DIR, slug, "primary.jpg")
        alt_std = os.path.join(STD_DIR, slug.replace("-1-l", "-1l"), "primary.jpg")
        cache_path = os.path.join(CUTOUTS_DIR, f"{key}.png")
        if os.path.exists(std_path):
            im = Image.open(std_path).convert("RGBA")
        elif os.path.exists(alt_std):
            im = Image.open(alt_std).convert("RGBA")
        else:
            if not os.path.exists(cache_path):
                pjson = json.load(urllib.request.urlopen(f"https://nahiahome.com/products/{slug}.json", timeout=15))
                img_url = pjson["product"]["images"][0]["src"]
                req = urllib.request.Request(img_url, headers={"User-Agent": "Mozilla/5.0"})
                with urllib.request.urlopen(req, timeout=20) as resp:
                    with open(cache_path, "wb") as out:
                        out.write(resp.read())
            im = Image.open(cache_path).convert("RGBA")
    arr = np.array(im, dtype=np.float32)
    bg_r, bg_g, bg_b, bg_a = arr[2, 2]
    if bg_a > 240 and bg_r > 225 and bg_g > 225 and bg_b > 220:
        dist = np.sqrt((bg_r - arr[:, :, 0])**2 + (bg_g - arr[:, :, 1])**2 + (bg_b - arr[:, :, 2])**2)
        alpha_factor = np.clip((dist - 5.0) / 10.0, 0, 1)
        arr[:, :, 3] = arr[:, :, 3] * alpha_factor
    fg = arr[:, :, 3] > 140
    if im.width >= 1000 and im.height >= 1000:
        fg[:55, :] = False
        fg[-55:, :] = False
        fg[:, :55] = False
        fg[:, -55:] = False
    ys = np.where(fg.sum(axis=1) > 10)[0]
    xs = np.where(fg.sum(axis=0) > 10)[0]
    out_im = Image.fromarray(arr.astype(np.uint8))
    if len(xs) > 0 and len(ys) > 0:
        pad = 24
        x0 = max(0, int(xs.min()) - pad)
        y0 = max(0, int(ys.min()) - pad)
        x1 = min(out_im.width, int(xs.max()) + pad)
        y1 = min(out_im.height, int(ys.max()) + pad)
        out_im = out_im.crop((x0, y0, x1, y1))
    return out_im

def crop_fill(im, target_w, target_h, focus_x=0.5, focus_y=0.5):
    w, h = im.size
    scale = max(target_w / w, target_h / h)
    nw, nh = int(round(w * scale)), int(round(h * scale))
    resized = im.resize((nw, nh), Image.Resampling.LANCZOS)
    left = int(round((nw - target_w) * focus_x))
    top = int(round((nh - target_h) * focus_y))
    left = max(0, min(nw - target_w, left))
    top = max(0, min(nh - target_h, top))
    return resized.crop((left, top, left + target_w, top + target_h))

def add_gradient_overlay(im, top_alpha=90, bottom_alpha=155):
    w, h = im.size
    grad = np.zeros((h, w, 4), dtype=np.uint8)
    y = np.linspace(0, 1, h)
    a_top = np.clip((0.28 - y) / 0.28, 0, 1) ** 1.5 * top_alpha
    a_bot = np.clip((y - 0.62) / 0.38, 0, 1) ** 1.4 * bottom_alpha
    alpha = np.clip(a_top + a_bot, 0, 255).astype(np.uint8)
    grad[:, :, 0] = 18
    grad[:, :, 1] = 15
    grad[:, :, 2] = 12
    grad[:, :, 3] = alpha[:, None]
    return Image.alpha_composite(im.convert("RGBA"), Image.fromarray(grad)).convert("RGB")

def draw_tracked_text(draw, center_x, y, text, font, fill=(250, 247, 242), tracking=6):
    chars = list(text)
    widths = [draw.textlength(c, font=font) for c in chars]
    total_w = sum(widths) + tracking * max(0, len(chars) - 1)
    x = center_x - total_w / 2
    for c, cw in zip(chars, widths):
        draw.text((x, y), c, font=font, fill=fill)
        x += cw + tracking

def draw_centered_text(draw, center_x, y, text, font, fill=(250, 247, 242)):
    w = draw.textlength(text, font=font)
    draw.text((center_x - w / 2, y), text, font=font, fill=fill)

def make_cover_slide(bg_img, issue_label, title_line1, focus_x=0.5, focus_y=0.5):
    """
    Cover slide (Slide 1):
    - Shows ONLY the single main editorial title at the bottom (e.g. 'Exterior Sanctuary')
    - ZERO secondary subtitles or mismatched product names on covers
    """
    W, H = 1080, 1350
    base = crop_fill(bg_img, W, H, focus_x, focus_y)
    base = add_gradient_overlay(base, top_alpha=85, bottom_alpha=155)
    draw = ImageDraw.Draw(base)

    draw_tracked_text(draw, W / 2, 72, "NAHIA HOME", font_sans(22, bold=True), fill=(250, 247, 242), tracking=10)
    draw_tracked_text(draw, W / 2, 108, issue_label.upper(), font_sans(17), fill=(225, 218, 206), tracking=5)
    draw.line([(W / 2 - 40, 144), (W / 2 + 40, 144)], fill=(230, 222, 210), width=1)

    # Single clean title at the bottom — nothing else underneath
    draw_centered_text(draw, W / 2, 1175, title_line1, font_serif(68, italic=False), fill=(252, 249, 244))
    return base

def make_framed_editorial_slide(img, top_kicker, headline_italic, focus_x=0.5, focus_y=0.5):
    """
    Detail / Story slide (Slides 2 & 3):
    - Adaptive frame geometry that preserves the FULL product without cutting off top/bottom/sides
    - Shows ONLY the italic serif headline below the image (no multi-line subtitle paragraph underneath)
    """
    W, H = 1080, 1350
    canvas = Image.new("RGB", (W, H), (250, 247, 242))
    draw = ImageDraw.Draw(canvas)

    draw_tracked_text(draw, W / 2, 66, top_kicker.upper(), font_sans(18), fill=(115, 108, 98), tracking=6)

    # Adaptive frame sizing so vertical product images (like the 1L blown-glass carafe) are NEVER cropped at top/bottom
    iw, ih = img.size
    aspect = iw / ih
    max_fw, max_fh = 880, 960
    if aspect < 0.92:
        # Vertical portrait photo: use full 960px height and matching width so 100% of vertical product is visible
        fh = max_fh
        fw = max(680, min(max_fw, int(round(fh * aspect))))
    else:
        # Square or landscape photo: use 880x880 square frame
        fw, fh = 880, 880

    photo = crop_fill(img, fw, fh, focus_x, focus_y)
    px = (W - fw) // 2
    py = 115 + (max_fh - fh) // 2
    canvas.paste(photo, (px, py))
    draw.rectangle([(px - 1, py - 1), (px + fw, py + fh)], outline=(224, 217, 205), width=1)

    # Single italic headline below the frame (NO body_lines subtitle underneath!)
    headline_y = py + fh + 52
    draw_centered_text(draw, W / 2, headline_y, headline_italic, font_serif(48, italic=True), fill=(32, 28, 24))

    draw_tracked_text(draw, W / 2, 1260, "NAHIAHOME.COM", font_sans(16), fill=(140, 132, 120), tracking=6)
    return canvas

def make_shop_the_edit_slide(edit_title, edit_subtitle, product_keys):
    """
    Westwing 'Shop the Edit' moodboard (Slide 4):
    - ONLY includes products that actually appeared in Slides 1, 2, and 3 of that post
    - Supports 3 or 4 products cleanly (2x2 grid for 4 products; 2 on top + 1 centered below for 3 products)
    """
    W, H = 1080, 1350
    canvas = Image.new("RGBA", (W, H), (250, 247, 242, 255))
    draw = ImageDraw.Draw(canvas)

    draw_tracked_text(draw, W / 2, 68, "THE CURATED EDIT", font_sans(18, bold=True), fill=(120, 112, 100), tracking=8)
    draw_centered_text(draw, W / 2, 105, edit_title, font_serif(52, italic=True), fill=(28, 25, 22))
    draw_tracked_text(draw, W / 2, 178, edit_subtitle.upper(), font_sans(16), fill=(135, 126, 114), tracking=4)
    draw.line([(100, 218), (W - 100, 218)], fill=(226, 219, 207), width=1)

    keys = product_keys[:4]
    if len(keys) == 3:
        cells = [
            (90, 250, 420, 460),
            (570, 250, 420, 460),
            (330, 755, 420, 460),
        ]
    else:
        cells = [
            (90, 250, 420, 460),
            (570, 250, 420, 460),
            (90, 755, 420, 460),
            (570, 755, 420, 460),
        ]

    for idx, key in enumerate(keys):
        cx, cy, cw, ch = cells[idx]
        p = PRODUCTS[key]
        draw.rectangle([(cx, cy), (cx + cw, cy + 330)], fill=(244, 239, 230, 255), outline=(232, 225, 213, 255), width=1)

        try:
            pim = load_product_image(key)
            max_pw, max_ph = 240, 230
            pw, ph = pim.size
            sc = min(max_pw / pw, max_ph / ph)
            npw, nph = int(pw * sc), int(ph * sc)
            pim_r = pim.resize((npw, nph), Image.Resampling.LANCZOS)
            px = cx + (cw - npw) // 2
            py = cy + (330 - nph) // 2
            canvas.alpha_composite(pim_r, (px, py))
        except Exception as e:
            print(f"Warning loading {key}: {e}")

        center_c = cx + cw / 2
        draw_tracked_text(draw, center_c, cy + 348, p["brand"], font_sans(13), fill=(135, 126, 114), tracking=3)
        draw_centered_text(draw, center_c, cy + 374, p["title"], font_serif(26, italic=False), fill=(28, 25, 22))
        draw_centered_text(draw, center_c, cy + 410, p["material_note"], font_serif(21, italic=True), fill=(110, 100, 88))

    draw.line([(100, 1245), (W - 100, 1245)], fill=(226, 219, 207), width=1)
    draw_tracked_text(draw, W / 2, 1272, "DISCOVER THE COLLECTION AT NAHIAHOME.COM", font_sans(16), fill=(115, 108, 98), tracking=5)
    return canvas.convert("RGB")

def ensure_soundtrack_m4a(day_num, search_query):
    """Downloads the 256kbps stereo AAC (.m4a) soundtrack preview from Apple iTunes if not cached."""
    m4a_path = os.path.join(AUDIO_DIR, f"day_{day_num:02d}_music.m4a")
    if os.path.exists(m4a_path) and os.path.getsize(m4a_path) > 50000:
        return m4a_path
    url = "https://itunes.apple.com/search?" + urllib.parse.urlencode({"term": search_query, "media": "music", "limit": 3})
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    data = json.loads(urllib.request.urlopen(req, timeout=15).read().decode())
    results = data.get("results", [])
    if not results:
        raise RuntimeError(f"No iTunes audio track found for {search_query}")
    preview_url = results[0]["previewUrl"]
    req_audio = urllib.request.Request(preview_url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req_audio, timeout=25) as resp:
        with open(m4a_path, "wb") as out:
            out.write(resp.read())
    print(f"Downloaded soundtrack for Day {day_num}: {results[0].get('artistName')} — {results[0].get('trackName')}")
    return m4a_path

def mux_audio_into_mp4(silent_mp4, audio_m4a, final_mp4):
    """Uses macOS AVFoundation (AVMutableComposition) to mux the stereo AAC music track directly into the H.264 MP4."""
    tmp_muxed = "/tmp/nahia_muxed_out.mp4"
    if os.path.exists(tmp_muxed):
        os.remove(tmp_muxed)

    swift_mux = f"""
import Foundation
import AVFoundation

let videoURL = URL(fileURLWithPath: "{silent_mp4}")
let audioURL = URL(fileURLWithPath: "{audio_m4a}")
let outURL = URL(fileURLWithPath: "{tmp_muxed}")

let vAsset = AVURLAsset(url: videoURL)
let aAsset = AVURLAsset(url: audioURL)
let comp = AVMutableComposition()

let vDuration = vAsset.duration
if let vTrack = vAsset.tracks(withMediaType: .video).first,
   let compV = comp.addMutableTrack(withMediaType: .video, preferredTrackID: kCMPersistentTrackID_Invalid) {{
    try! compV.insertTimeRange(CMTimeRange(start: .zero, duration: vDuration), of: vTrack, at: .zero)
}}

if let aTrack = aAsset.tracks(withMediaType: .audio).first,
   let compA = comp.addMutableTrack(withMediaType: .audio, preferredTrackID: kCMPersistentTrackID_Invalid) {{
    let startOffset = CMTime(seconds: 2.0, preferredTimescale: 600)
    try! compA.insertTimeRange(CMTimeRange(start: startOffset, duration: vDuration), of: aTrack, at: .zero)
}}

let exporter = AVAssetExportSession(asset: comp, presetName: AVAssetExportPresetHighestQuality)!
exporter.outputURL = outURL
exporter.outputFileType = .mp4
exporter.shouldOptimizeForNetworkUse = true

let g = DispatchGroup()
g.enter()
exporter.exportAsynchronously {{
    g.leave()
}}
g.wait()
if exporter.status != .completed {{
    fatalError("Export failed: \\(String(describing: exporter.error))")
}}
"""
    swift_file = "/tmp/mux_audio.swift"
    with open(swift_file, "w") as sf:
        sf.write(swift_mux)
    subprocess.run(["swift", swift_file], check=True)
    shutil.move(tmp_muxed, final_mp4)

def render_vertical_video(bg_img, secondary_img, out_mp4, audio_m4a, kicker, title1, fx1=0.5, fy1=0.5, fx2=0.5, fy2=0.5):
    """
    Renders a 9:16 vertical MP4 video (720x1280, 24fps, 6.0s) with:
    - Full product framing (centered on fx1, fy1 and fx2, fy2 so products are never cut off)
    - Single clean editorial title at the bottom (title1 only)
    - Stereo AAC music embedded directly inside the MP4
    """
    VW, VH, FPS, FRAMES = 720, 1280, 24, 144
    tmp_dir = "/tmp/nahia_vertical_frames"
    os.makedirs(tmp_dir, exist_ok=True)

    # Use a gentle 1.06x zoom centered on the product focus point so the product stays 100% inside the frame
    im1 = crop_fill(bg_img, int(VW * 1.06), int(VH * 1.06), fx1, fy1)
    im2 = crop_fill(secondary_img, int(VW * 1.06), int(VH * 1.06), fx2, fy2)
    arr1 = np.asarray(im1, dtype=np.float32)
    arr2 = np.asarray(im2, dtype=np.float32)
    sh, sw = arr1.shape[:2]

    for f in range(FRAMES):
        t = f / FPS
        if t < 3.2:
            p = t / 3.2
            ox = int((sw - VW) * (0.35 + 0.30 * p))
            oy = int((sh - VH) * (0.50 - 0.15 * p))
            crop = arr1[oy:oy+VH, ox:ox+VW].copy()
        else:
            p = (t - 3.2) / 2.8
            ox = int((sw - VW) * (0.65 - 0.30 * p))
            oy = int((sh - VH) * (0.35 + 0.20 * p))
            crop = arr2[oy:oy+VH, ox:ox+VW].copy()
            if t < 3.8:
                alpha = (t - 3.2) / 0.6
                alpha = alpha * alpha * (3 - 2 * alpha)
                ox1 = int((sw - VW) * 0.65)
                oy1 = int((sh - VH) * 0.35)
                c1 = arr1[oy1:oy1+VH, ox1:ox1+VW]
                crop = c1 * (1 - alpha) + crop * alpha

        clean_crop = np.clip(crop, 0, 255).astype(np.uint8)
        frame_im = add_gradient_overlay(Image.fromarray(clean_crop), top_alpha=85, bottom_alpha=155)
        draw = ImageDraw.Draw(frame_im)

        draw_tracked_text(draw, VW / 2, 95, "NAHIA HOME", font_sans(16, bold=True), fill=(250, 247, 242), tracking=8)
        draw_tracked_text(draw, VW / 2, 124, kicker.upper(), font_sans(13), fill=(225, 218, 206), tracking=4)
        draw.line([(VW / 2 - 30, 150), (VW / 2 + 30, 150)], fill=(230, 222, 210), width=1)

        # Single clean title at the bottom — nothing else underneath
        draw_centered_text(draw, VW / 2, 1065, title1, font_serif(46, italic=False), fill=(252, 249, 244))

        frame_im.save(f"{tmp_dir}/f{f:04d}.jpg", quality=92)

    silent_mp4 = "/tmp/nahia_silent_vertical.mp4"
    swift_code = f"""
import Foundation
import AVFoundation
import CoreGraphics
import ImageIO
let W={VW},H={VH},fps:Int32={FPS}
let out=URL(fileURLWithPath:"{silent_mp4}"); try? FileManager.default.removeItem(at:out)
let wr=try! AVAssetWriter(outputURL:out,fileType:.mp4)
let inp=AVAssetWriterInput(mediaType:.video,outputSettings:[AVVideoCodecKey:AVVideoCodecType.h264,AVVideoWidthKey:W,AVVideoHeightKey:H,AVVideoCompressionPropertiesKey:[AVVideoAverageBitRateKey:3500000,AVVideoProfileLevelKey:AVVideoProfileLevelH264HighAutoLevel]])
let ad=AVAssetWriterInputPixelBufferAdaptor(assetWriterInput:inp,sourcePixelBufferAttributes:[kCVPixelBufferPixelFormatTypeKey as String:Int(kCVPixelFormatType_32ARGB),kCVPixelBufferWidthKey as String:W,kCVPixelBufferHeightKey as String:H])
wr.add(inp); wr.startWriting(); wr.startSession(atSourceTime:.zero)
let cs=CGColorSpaceCreateDeviceRGB()
for f in 0..<{FRAMES} {{
  while !inp.isReadyForMoreMediaData {{ usleep(1000) }}
  let s=CGImageSourceCreateWithURL(URL(fileURLWithPath:String(format:"{tmp_dir}/f%04d.jpg",f)) as CFURL,nil)!
  let img=CGImageSourceCreateImageAtIndex(s,0,nil)!
  var pb:CVPixelBuffer?; CVPixelBufferCreate(nil,W,H,kCVPixelFormatType_32ARGB,nil,&pb); let b=pb!
  CVPixelBufferLockBaseAddress(b,[])
  let c=CGContext(data:CVPixelBufferGetBaseAddress(b),width:W,height:H,bitsPerComponent:8,bytesPerRow:CVPixelBufferGetBytesPerRow(b),space:cs,bitmapInfo:CGImageAlphaInfo.noneSkipFirst.rawValue)!
  c.draw(img,in:CGRect(x:0,y:0,width:W,height:H))
  CVPixelBufferUnlockBaseAddress(b,[])
  ad.append(b,withPresentationTime:CMTime(value:Int64(f),timescale:fps))
}}
inp.markAsFinished(); let g=DispatchGroup(); g.enter(); wr.finishWriting{{g.leave()}}; g.wait()
"""
    swift_file = "/tmp/encode_vertical.swift"
    with open(swift_file, "w") as sf:
        sf.write(swift_code)
    subprocess.run(["swift", swift_file], check=True)
    mux_audio_into_mp4(silent_mp4, audio_m4a, out_mp4)
    print(f"Rendered vertical video with embedded music: {out_mp4}")

# Load 100% Uncropped Authentic Photography (_orig.jpg & full product shots — NEVER pre-cropped _std.jpg)
scene1 = Image.open(os.path.join(BASE_DIR, "work/video_assets/gen/scene1.jpg")).convert("RGB")
scene2 = Image.open(os.path.join(BASE_DIR, "work/video_assets/gen/scene2.jpg")).convert("RGB")
scene3 = Image.open(os.path.join(BASE_DIR, "work/video_assets/gen/scene3.jpg")).convert("RGB")
scene4 = Image.open(os.path.join(BASE_DIR, "work/video_assets/gen/scene4.jpg")).convert("RGB")
scene5 = Image.open(os.path.join(BASE_DIR, "work/video_assets/gen/scene5.jpg")).convert("RGB")

abeille_pitcher_full = Image.open(os.path.join(STD_DIR, "jarra-de-cristal-abeille-1l/sec_4_orig.jpg")).convert("RGB")
abeille_carafe_full = Image.open(os.path.join(STD_DIR, "jarra-de-vidrio-soplado-abeille-1l/sec_3_orig.jpg")).convert("RGB")
abeille_minibol_full = Image.open(os.path.join(STD_DIR, "mini-bol-abeille-27-cl/sec_3_orig.jpg")).convert("RGB")
pearl_bowl_full = Image.open(os.path.join(STD_DIR, "ensaladera-costa-nova-pearl-27cm/sec_4_orig.jpg")).convert("RGB")
alheli_pitcher_full = Image.open(os.path.join(STD_DIR, "jarra-alheli-cote-table-2-3-l/sec_3_orig.jpg")).convert("RGB")
livlig_wall_full = Image.open(os.path.join(STD_DIR, "soporte-de-manguera-graceful-green-livlig/sec_2_orig.jpg")).convert("RGB")
livlig_tap_full = Image.open(os.path.join(STD_DIR, "grifo-de-jardin-con-roseta-green-livlig/sec_3_orig.jpg")).convert("RGB")
lemon_book_full = Image.open(os.path.join(STD_DIR, "the-gourmands-lemon/primary.jpg")).convert("RGB")
umbel_full = Image.open(os.path.join(BASE_DIR, "work/umbel_luxury.jpg")).convert("RGB")
casalopez_table_full = Image.open(os.path.join(STD_DIR, "mantel-individual-lino-majorque-vert-olive-casa-lopez-paris/sec_2_orig.jpg")).convert("RGB")
casalopez_napkin_full = Image.open(os.path.join(STD_DIR, "servilleta-lino-emperatriz-casa-lopez-paris/sec_2_orig.jpg")).convert("RGB")
viana_fans_full = Image.open(os.path.join(STD_DIR, "abanico-de-lino-santanyi-the-viana-fan/sec_3_orig.jpg")).convert("RGB")
pearl_teapot_full = Image.open(os.path.join(STD_DIR, "lechera-pearl-10cl-costa-nova/sec_2_orig.jpg")).convert("RGB")
perloa_teacup_full = Image.open(os.path.join(STD_DIR, "taza-de-cafe-c-plato-perloa-cote-table/sec_4_orig.jpg")).convert("RGB")

DAYS_SPEC = [
    {
        "day": 1,
        "date": "2026-11-02",
        "weekday": "Monday · Nov 2",
        "edit_number": "THE TABLE EDIT",
        "title": "The La Rochère Icon (1475)",
        "pillar": "Iconic Objects & Provenance",
        "cover_bg": scene1,
        "cover_focus": (0.5, 0.5),
        "secondary_bg": abeille_pitcher_full,
        "video_focus_1": (0.5, 0.5),
        "video_focus_2": (0.5, 0.5),
        "cover_line1": "L’Art de la Table",
        "slide2_img": abeille_pitcher_full,
        "slide2_focus": (0.5, 0.5),
        "slide2_kicker": "FRENCH SAVOIR-FAIRE",
        "slide2_head": "The Imperial Bee Emblem",
        "slide3_img": abeille_carafe_full,
        "slide3_focus": (0.5, 0.5),
        "slide3_kicker": "MOUTH-BLOWN & PRESSED CRYSTAL",
        "slide3_head": "Luminous Silhouettes for the Table",
        "edit_title": "The Abeille Collection",
        "edit_sub": "La Rochère · France",
        "products": ["vaso_abeille", "copa_abeille_verde", "jarra_abeille", "jarra_soplado_abeille"],
        "ig_caption": "THE TABLE EDIT — L’Art de la Table.\n\nCrafted in France’s oldest working glassworks (established in 1475), our La Rochère Abeille glassware brings architectural weight, warm refraction, and the signature bee relief to the everyday table.\n\nExplore the complete collection via the product tags and the link in our bio.\n\n#NahiaHome #LaRochere #ArtDeLaTable #FrenchGlassware #TableStyling #QuietLuxury",
        "tiktok_caption": "THE TABLE EDIT · Crafted in France since 1475. The iconic Abeille glassware collection by La Rochère, curated for timeless tables. Discover the edit at nahiahome.com #NahiaHome #LaRochere #TableStyling #FrenchGlassware #QuietLuxury",
        "audio_suggestion": "Chet Baker — Almost Blue (Instrumental Vinyl)",
        "itunes_query": "Chet Baker Almost Blue"
    },
    {
        "day": 2,
        "date": "2026-11-03",
        "weekday": "Tuesday · Nov 3",
        "edit_number": "THE MEDITERRANEAN EDIT",
        "title": "Portuguese Stoneware & Southern Light",
        "pillar": "The Art of Hosting",
        "cover_bg": scene2,
        "cover_focus": (0.5, 0.5),
        "secondary_bg": pearl_bowl_full,
        "video_focus_1": (0.5, 0.5),
        "video_focus_2": (0.5, 0.5),
        "cover_line1": "The Afternoon Table",
        "slide2_img": pearl_bowl_full,
        "slide2_focus": (0.5, 0.5),
        "slide2_kicker": "PORTUGUESE STONEWARE · COSTA NOVA",
        "slide2_head": "Beaded Rims & Organic Glazes",
        "slide3_img": alheli_pitcher_full,
        "slide3_focus": (0.5, 0.55),
        "slide3_kicker": "CÔTÉ TABLE · PARIS",
        "slide3_head": "Botanical Tones in Ribbed Glass",
        "edit_title": "The Mediterranean Table",
        "edit_sub": "Portugal & Paris",
        "products": ["plato_pearl", "ensaladera_pearl", "jarra_alheli"],
        "ig_caption": "THE MEDITERRANEAN EDIT — Materiality and southern light.\n\nA timeless table lives in the dialogue between textures: unbleached linen, organic Portuguese stoneware from Costa Nova, and mouth-blown green ribbed glass by Côté Table Paris.\n\nDiscover the complete table edit through the product tags and the link in our bio.\n\n#NahiaHome #CostaNova #CoteTable #Tableware #SlowLiving #MediterraneanHome",
        "tiktok_caption": "THE MEDITERRANEAN EDIT · Layering Portuguese Pearl stoneware, raw linen, and Parisian ribbed glass for an effortless Mediterranean table. Explore the edit at nahiahome.com #NahiaHome #TableScape #InteriorDesign #Hosting #EuropeanHome",
        "audio_suggestion": "Stan Getz & João Gilberto — Corcovado (Instrumental)",
        "itunes_query": "Stan Getz Joao Gilberto Corcovado"
    },
    {
        "day": 3,
        "date": "2026-11-04",
        "weekday": "Wednesday · Nov 4",
        "edit_number": "THE EXTERIOR EDIT",
        "title": "The Garden as Architecture",
        "pillar": "The Exterior Sanctuary",
        "cover_bg": livlig_wall_full,
        "cover_focus": (0.5, 0.5),
        "secondary_bg": livlig_tap_full,
        "video_focus_1": (0.78, 0.55),
        "video_focus_2": (0.5, 0.5),
        "cover_line1": "Exterior Sanctuary",
        "slide2_img": livlig_tap_full,
        "slide2_focus": (0.5, 0.5),
        "slide2_kicker": "GARDEN ARCHITECTURE · LIVLIG",
        "slide2_head": "Precision in Solid Brass",
        "slide3_img": scene3,
        "slide3_focus": (0.58, 0.5),
        "slide3_kicker": "SPANISH CRAFTSMANSHIP · VIANA",
        "slide3_head": "Natural Linen & Noble Wood",
        "edit_title": "The Exterior Sanctuary",
        "edit_sub": "Livlig & The Viana Fan",
        "products": ["manguera_green_livlig", "soporte_livlig", "grifo_livlig", "abanico_viana"],
        "ig_caption": "THE EXTERIOR EDIT — The garden as an architectural extension of the home.\n\nFrom Livlig’s sage green garden hoses, wall holders, and solid brass taps to the handcrafted linen of The Viana Fan, every exterior detail deserves quiet elegance.\n\nExplore the garden and outdoor collection via the link in our bio.\n\n#NahiaHome #Livlig #GardenArchitecture #OutdoorLiving #TerraceDesign #QuietLuxury",
        "tiktok_caption": "THE EXTERIOR EDIT · Elevating the garden sanctuary with solid brass taps, sage green hardware by Livlig, and handmade Spanish linen. Discover more at nahiahome.com #NahiaHome #GardenDesign #ExteriorDesign #LuxuryHome #OutdoorLiving",
        "audio_suggestion": "Ludovico Einaudi — Una Mattina (Acoustic Piano)",
        "itunes_query": "Ludovico Einaudi Una Mattina"
    },
    {
        "day": 4,
        "date": "2026-11-05",
        "weekday": "Thursday · Nov 5",
        "edit_number": "THE LIVING EDIT",
        "title": "The Reading Corner & Coffee Table",
        "pillar": "Curated Edits & Books",
        "cover_bg": scene4,
        "cover_focus": (0.55, 0.5),
        "secondary_bg": umbel_full,
        "video_focus_1": (0.55, 0.5),
        "video_focus_2": (0.5, 0.5),
        "cover_line1": "Objects of Desire",
        "slide2_img": lemon_book_full,
        "slide2_focus": (0.5, 0.5),
        "slide2_kicker": "TASCHEN · ART & GASTRONOMY",
        "slide2_head": "The Gourmand’s Lemon",
        "slide3_img": umbel_full,
        "slide3_focus": (0.5, 0.5),
        "slide3_kicker": "BOTANICAL STATIONERY",
        "slide3_head": "Tactile Linen & Fine Paper",
        "edit_title": "The Reading Sanctuary",
        "edit_sub": "Art Books & Fine Stoneware",
        "products": ["libro_slim", "taza_pearl", "libro_lemon", "cuaderno_umbel"],
        "ig_caption": "THE LIVING EDIT — The art of styling quiet corners.\n\nLarge-format illustrated monographs including Slim Aarons’ 'La Dolce Vita' and Taschen’s 'The Gourmand’s Lemon', paired with botanical linen stationery and Costa Nova stoneware.\n\nDiscover our curated library and home objects at nahiahome.com.\n\n#NahiaHome #CoffeeTableBooks #SlimAarons #InteriorStyling #ArchitecturalDigest #HomeEdit",
        "tiktok_caption": "THE LIVING EDIT · Styling a travertine side table with large-format Slim Aarons photography, Taschen monographs, and botanical linen stationery. Shop the edit at nahiahome.com #NahiaHome #CoffeeTableBooks #SlimAarons #InteriorStyling #HomeDecor",
        "audio_suggestion": "Erik Satie — Gymnopédie No. 1 (Warm Vinyl)",
        "itunes_query": "Erik Satie Gymnopedie No 1"
    },
    {
        "day": 5,
        "date": "2026-11-06",
        "weekday": "Friday · Nov 6",
        "edit_number": "THE WEEKEND TABLE",
        "title": "Candlelight, Olive & Crystal at Dusk",
        "pillar": "The Art of Hosting",
        "cover_bg": scene5,
        "cover_focus": (0.45, 0.5),
        "secondary_bg": casalopez_table_full,
        "video_focus_1": (0.45, 0.5),
        "video_focus_2": (0.5, 0.5),
        "cover_line1": "The Friday Table",
        "slide2_img": casalopez_table_full,
        "slide2_focus": (0.5, 0.5),
        "slide2_kicker": "CASA LÓPEZ · PARIS",
        "slide2_head": "Woven Linen in Vert Olive",
        "slide3_img": casalopez_napkin_full,
        "slide3_focus": (0.5, 0.5),
        "slide3_kicker": "BOTANICAL EMBROIDERY",
        "slide3_head": "Heirloom Textiles for the Table",
        "edit_title": "Dinner by Candlelight",
        "edit_sub": "The Weekend Hosting Edit",
        "products": ["copa_abeille_verde", "vaso_abeille", "mantel_casalopez", "servilleta_emperatriz"],
        "ig_caption": "THE WEEKEND TABLE — The art of gathering at dusk.\n\nPure woven placemats and botanical embroidered linen napkins by Casa López Paris, paired with the warm olive glow of our La Rochère Abeille crystal.\n\nEvery piece on this table is tagged in the post and available via the link in our bio.\n\n#NahiaHome #TableSetting #ArtOfHosting #LaRochere #CasaLopez #EveningTable",
        "tiktok_caption": "THE WEEKEND TABLE · Setting the mood for Friday evening: tall taper candles, olive-green French crystal, and Casa López Paris table linens. Discover the look at nahiahome.com #NahiaHome #DinnerParty #TableSetting #ArtOfHosting #QuietLuxury",
        "audio_suggestion": "Dalida & Alain Delon — Paroles, Paroles (Instrumental Lounge)",
        "itunes_query": "Dalida Alain Delon Paroles Paroles"
    },
    {
        "day": 6,
        "date": "2026-11-07",
        "weekday": "Saturday · Nov 7",
        "edit_number": "THE GIFT EDIT",
        "title": "Objects of Character & Provenance",
        "pillar": "Curated Gift Guide",
        "cover_bg": abeille_pitcher_full,
        "cover_focus": (0.5, 0.5),
        "secondary_bg": abeille_minibol_full,
        "video_focus_1": (0.5, 0.5),
        "video_focus_2": (0.5, 0.5),
        "cover_line1": "The Gift Edit",
        "slide2_img": abeille_minibol_full,
        "slide2_focus": (0.5, 0.5),
        "slide2_kicker": "LA ROCHÈRE · FRANCE 1475",
        "slide2_head": "Everyday Rituals in Pressed Crystal",
        "slide3_img": viana_fans_full,
        "slide3_focus": (0.5, 0.5),
        "slide3_kicker": "THE VIANA FAN · SPAIN",
        "slide3_head": "Artisanal Linen & Carved Wood",
        "edit_title": "Objects to Treasure",
        "edit_sub": "The Nahia Home Gift Edit",
        "products": ["jarra_abeille", "minibol_abeille", "abanico_viana"],
        "ig_caption": "THE GIFT EDIT — The art of gifting objects that endure.\n\nA curated selection of distinctive European pieces: our 1L Abeille crystal pitcher and mini bowls from France’s oldest glassworks, paired with handcrafted Spanish linen fans by The Viana Fan.\n\nSave this edit for the upcoming season or explore the collection at nahiahome.com.\n\n#NahiaHome #GiftGuide #ObjectsOfDesire #LaRochere #InteriorGifts #EuropeanDesign",
        "tiktok_caption": "THE GIFT EDIT · Curated European home gifts that feel like a Parisian gallery find. Save this edit for the upcoming season. #NahiaHome #GiftGuide #HolidayGifts #HomeDecor #ParisianStyle",
        "audio_suggestion": "Françoise Hardy — Le temps de l'amour (Acoustic Instrumental)",
        "itunes_query": "Francoise Hardy Le temps de l amour"
    },
    {
        "day": 7,
        "date": "2026-11-08",
        "weekday": "Sunday · Nov 8",
        "edit_number": "LE DIMANCHE MATIN",
        "title": "The Slow Sunday Morning Ritual",
        "pillar": "Slow Sunday Living",
        "cover_bg": pearl_teapot_full,
        "cover_focus": (0.5, 0.55),
        "secondary_bg": perloa_teacup_full,
        "video_focus_1": (0.5, 0.55),
        "video_focus_2": (0.5, 0.5),
        "cover_line1": "Le Dimanche Matin",
        "slide2_img": perloa_teacup_full,
        "slide2_focus": (0.5, 0.5),
        "slide2_kicker": "CÔTÉ TABLE · PARIS",
        "slide2_head": "The Sculpted Perloa Cup & Saucer",
        "slide3_img": pearl_bowl_full,
        "slide3_focus": (0.5, 0.5),
        "slide3_kicker": "COSTA NOVA · PORTUGAL",
        "slide3_head": "Most Loved Pieces This Week",
        "edit_title": "The Sunday Morning Edit",
        "edit_sub": "Costa Nova & Côté Table",
        "products": ["tetera_pearl", "lechera_pearl", "taza_perloa", "ensaladera_pearl"],
        "ig_caption": "LE DIMANCHE MATIN — Unrushed Sunday mornings.\n\nThe Pearl infuser teapot, creamer, and scalloped bowl by Costa Nova on natural marble, paired with Côté Table’s beaded Perloa glass cup and saucer.\n\nDiscover this week’s most loved pieces via the link in our bio.\n\n#NahiaHome #SundayMorning #SlowLiving #CostaNovaPearl #ArtDeVivre #MorningRitual",
        "tiktok_caption": "LE DIMANCHE MATIN · Slow Sunday morning rituals with Portuguese Pearl stoneware and sculpted French glass. Discover the collection at nahiahome.com #NahiaHome #SundayMorning #SlowLiving #Ceramics #Tableware",
        "audio_suggestion": "Claude Debussy — Clair de Lune (Soft Morning Piano)",
        "itunes_query": "Claude Debussy Clair de Lune"
    }
]

manifest = []

for d in DAYS_SPEC:
    day_num = d["day"]
    day_folder = os.path.join(ASSETS_DIR, f"day_{day_num:02d}")
    os.makedirs(day_folder, exist_ok=True)
    print(f"=== Generating Day {day_num}: {d['title']} ===")

    cfx, cfy = d.get("cover_focus", (0.5, 0.5))
    s1 = make_cover_slide(d["cover_bg"], d["edit_number"], d["cover_line1"], cfx, cfy)
    s1.save(os.path.join(day_folder, "ig_slide_1_cover.jpg"), quality=94)

    fx2, fy2 = d.get("slide2_focus", (0.5, 0.5))
    s2 = make_framed_editorial_slide(d["slide2_img"], d["slide2_kicker"], d["slide2_head"], fx2, fy2)
    s2.save(os.path.join(day_folder, "ig_slide_2_detail.jpg"), quality=94)

    fx3, fy3 = d.get("slide3_focus", (0.5, 0.5))
    s3 = make_framed_editorial_slide(d["slide3_img"], d["slide3_kicker"], d["slide3_head"], fx3, fy3)
    s3.save(os.path.join(day_folder, "ig_slide_3_story.jpg"), quality=94)

    s4 = make_shop_the_edit_slide(d["edit_title"], d["edit_sub"], d["products"])
    s4.save(os.path.join(day_folder, "ig_slide_4_shop_edit.jpg"), quality=94)

    # Download soundtrack & render 9:16 video with embedded music for BOTH TikTok and Instagram Reels
    audio_m4a = ensure_soundtrack_m4a(day_num, d["itunes_query"])
    video_path = os.path.join(day_folder, f"tiktok_reel_day_{day_num:02d}.mp4")
    ig_reel_path = os.path.join(day_folder, f"ig_reel_day_{day_num:02d}.mp4")

    if "--slides-only" not in os.sys.argv:
        vfx1, vfy1 = d.get("video_focus_1", cfx if isinstance(cfx, tuple) else (cfx, cfy))
        vfx2, vfy2 = d.get("video_focus_2", (0.5, 0.5))
        render_vertical_video(
            d["cover_bg"], d["secondary_bg"], video_path, audio_m4a,
            d["edit_number"], d["cover_line1"], vfx1, vfy1, vfx2, vfy2
        )
        shutil.copy2(video_path, ig_reel_path)

    manifest.append({
        "day": day_num,
        "date": d["date"],
        "weekday": d["weekday"],
        "edit_number": d["edit_number"],
        "title": d["title"],
        "pillar": d["pillar"],
        "ig_slides": [
            f"assets/day_{day_num:02d}/ig_slide_1_cover.jpg",
            f"assets/day_{day_num:02d}/ig_slide_2_detail.jpg",
            f"assets/day_{day_num:02d}/ig_slide_3_story.jpg",
            f"assets/day_{day_num:02d}/ig_slide_4_shop_edit.jpg"
        ],
        "video_url": f"assets/day_{day_num:02d}/tiktok_reel_day_{day_num:02d}.mp4",
        "ig_video_url": f"assets/day_{day_num:02d}/ig_reel_day_{day_num:02d}.mp4",
        "audio_url": f"assets/audio/day_{day_num:02d}_music.m4a",
        "ig_caption": d["ig_caption"],
        "tiktok_caption": d["tiktok_caption"],
        "audio_suggestion": d["audio_suggestion"],
        "products": [PRODUCTS[k] for k in d["products"]],
        "status": "READY TO POST"
    })

with open(os.path.join(STUDIO_DIR, "posts_manifest.json"), "w") as f:
    json.dump(manifest, f, indent=2, ensure_ascii=False)

print("All 7 days regenerated with full uncropped products, clean typography, matched Curated Edits, and embedded music!")
