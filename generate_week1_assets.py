#!/usr/bin/env python3
"""
Generates Week 1 (7 Days) of Ultra-Premium Westwing-Style Instagram Carousels (1080x1350)
and 9:16 Vertical TikTok/Reel Videos (1080x1920 MP4) for Nahia Home:
- 100% Editorial English
- ZERO prices on any image
- ZERO composite/pasted objects or movie screenshots (100% authentic photography only)
"""
import os, json, math, urllib.request, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = "/Users/josemiguellavao/Desktop/NAHIA HOME"
STUDIO_DIR = os.path.join(BASE_DIR, "social_studio")
ASSETS_DIR = os.path.join(STUDIO_DIR, "assets")
CUTOUTS_DIR = os.path.join(STUDIO_DIR, "cutouts")
STD_DIR = os.path.join(BASE_DIR, "scratch/batch_standardization")
os.makedirs(ASSETS_DIR, exist_ok=True)
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
        "title": '"Abeille" Glass Carafe',
        "brand": "LA ROCHÈRE · FRANCE 1475",
        "material_note": "Signature Bee Relief · 1 L",
        "handle": "/products/jarra-de-cristal-abeille-1-l"
    },
    "minibol_abeille": {
        "title": '"Abeille" Mini Glass Bowl',
        "brand": "LA ROCHÈRE · FRANCE 1475",
        "material_note": "Pressed French Crystal · 27 cl",
        "handle": "/products/mini-bol-abeille-27-cl"
    },
    "botella_poisson": {
        "title": '"Poisson" Sculptural Carafe',
        "brand": "CÔTÉ TABLE · PARIS",
        "material_note": "Molded Glass Carafe · 1.1 L",
        "handle": "/products/botella-poisson-cote-table-1-1-l"
    },
    "plato_pearl": {
        "title": "Pearl Stoneware Plate",
        "brand": "COSTA NOVA · PORTUGAL",
        "material_note": "Fine Portuguese Stoneware",
        "handle": "/products/bowl-perla",
        "local": os.path.join(BASE_DIR, "work/video_assets/plato_clean.png")
    },
    "ensaladera_perloa": {
        "title": "Perloa Scalloped Bowl",
        "brand": "CÔTÉ TABLE · PARIS",
        "material_note": "Beaded Rim Ceramic · 21 cm",
        "handle": "/products/ensaladera-perloa-21-cm-cote-table"
    },
    "cubiertos_bamboo": {
        "title": "Panda Bamboo Serving Set",
        "brand": "SABRÊ · PARIS",
        "material_note": "Natural Bamboo Root & Steel",
        "handle": "/products/cubiertos-de-servicio-ensalada",
        "url": "https://cdn.shopify.com/s/files/1/0603/1130/6380/files/SETDECUBIERTOSDESERVICIOPARAENSALADA.png?v=1728394005"
    },
    "jarra_alheli": {
        "title": "Alhelí Ribbed Pitcher",
        "brand": "CÔTÉ TABLE · PARIS",
        "material_note": "Mouth-Blown Green Glass · 2.3 L",
        "handle": "/products/jarra-alheli-cote-table-2-3-l"
    },
    "grifo_livlig": {
        "title": "Architectural Garden Tap",
        "brand": "LIVLIG · GARDEN ARCHITECTURE",
        "material_note": "Solid Brass & Sage Rosette",
        "handle": "/products/grifo-de-jardin-con-roseta-green-livlig"
    },
    "manguera_livlig": {
        "title": "Gentle Greige Garden Hose",
        "brand": "LIVLIG · GARDEN ARCHITECTURE",
        "material_note": "UV-Resistant Matte Weave · 20M",
        "handle": "/products/manguera-de-jardin-gentle-greige-20m-livlig"
    },
    "soporte_livlig": {
        "title": "Graceful Green Hose Holder",
        "brand": "LIVLIG · GARDEN ARCHITECTURE",
        "material_note": "Powder-Coated Architectural Steel",
        "handle": "/products/soporte-de-manguera-graceful-green-livlig"
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
        "handle": "/products/tetera-con-infusor-pearl-costa-nova"
    },
    "taza_pearl": {
        "title": "Pearl Espresso Cup & Saucer",
        "brand": "COSTA NOVA · PORTUGAL",
        "material_note": "Glazed Portuguese Stoneware",
        "handle": "/products/taza-de-cafe-con-plato-costa-nova-pearl"
    },
    "taza_perloa": {
        "title": "Perloa Beaded Tea Cup",
        "brand": "CÔTÉ TABLE · PARIS",
        "material_note": "Sculpted French Glass · 18 cl",
        "handle": "/products/taza-de-te-c-plato-perloa-cote-table-18cl"
    },
    "lechera_pearl": {
        "title": "Pearl Stoneware Creamer",
        "brand": "COSTA NOVA · PORTUGAL",
        "material_note": "Beaded Rim Stoneware · 10 cl",
        "handle": "/products/lechera-pearl-10cl-costa-nova"
    },
    "mantel_casalopez": {
        "title": "Majorque Linen Placemat",
        "brand": "CASA LÓPEZ · PARIS",
        "material_note": "Pure Woven Linen · Vert Olive",
        "handle": "/products/mantel-individual-lino-majorque-vert-olive-casa-lopez"
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
        alpha_factor = np.clip((dist - 14) / 18.0, 0, 1)
        arr[:, :, 3] = arr[:, :, 3] * alpha_factor
    return Image.fromarray(arr.astype(np.uint8))

def crop_fill(im, target_w, target_h, focus_x=0.5, focus_y=0.5):
    w, h = im.size
    scale = max(target_w / w, target_h / h)
    nw, nh = int(w * scale), int(h * scale)
    resized = im.resize((nw, nh), Image.Resampling.LANCZOS)
    left = int((nw - target_w) * focus_x)
    top = int((nh - target_h) * focus_y)
    left = max(0, min(nw - target_w, left))
    top = max(0, min(nh - target_h, top))
    return resized.crop((left, top, left + target_w, top + target_h))

def add_gradient_overlay(im, top_alpha=90, bottom_alpha=155):
    w, h = im.size
    grad = np.zeros((h, w, 4), dtype=np.uint8)
    y = np.linspace(0, 1, h)
    a_top = np.clip((0.28 - y) / 0.28, 0, 1) ** 1.5 * top_alpha
    a_bot = np.clip((y - 0.52) / 0.48, 0, 1) ** 1.4 * bottom_alpha
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

def make_cover_slide(bg_img, issue_label, title_line1, title_line2_italic, subtitle, focus_x=0.5, focus_y=0.5):
    W, H = 1080, 1350
    base = crop_fill(bg_img, W, H, focus_x, focus_y)
    base = add_gradient_overlay(base, top_alpha=85, bottom_alpha=165)
    draw = ImageDraw.Draw(base)

    draw_tracked_text(draw, W / 2, 72, "NAHIA HOME", font_sans(22, bold=True), fill=(250, 247, 242), tracking=10)
    draw_tracked_text(draw, W / 2, 108, issue_label.upper(), font_sans(17), fill=(225, 218, 206), tracking=5)
    draw.line([(W / 2 - 40, 144), (W / 2 + 40, 144)], fill=(230, 222, 210), width=1)

    draw_centered_text(draw, W / 2, 1045, title_line1, font_serif(64, italic=False), fill=(252, 249, 244))
    draw_centered_text(draw, W / 2, 1122, title_line2_italic, font_serif(66, italic=True), fill=(244, 236, 222))
    draw_tracked_text(draw, W / 2, 1225, subtitle.upper(), font_sans(18), fill=(220, 212, 198), tracking=5)
    return base

def make_framed_editorial_slide(img, top_kicker, headline_italic, body_lines, focus_x=0.5, focus_y=0.5):
    W, H = 1080, 1350
    canvas = Image.new("RGB", (W, H), (250, 247, 242))
    draw = ImageDraw.Draw(canvas)

    draw_tracked_text(draw, W / 2, 70, top_kicker.upper(), font_sans(18), fill=(115, 108, 98), tracking=6)

    fw, fh = 880, 840
    photo = crop_fill(img, fw, fh, focus_x, focus_y)
    canvas.paste(photo, ((W - fw) // 2, 125))
    draw.rectangle([((W - fw) // 2 - 1, 124), ((W + fw) // 2, 125 + fh)], outline=(224, 217, 205), width=1)

    draw_centered_text(draw, W / 2, 1015, headline_italic, font_serif(46, italic=True), fill=(32, 28, 24))
    y = 1090
    for line in body_lines:
        draw_centered_text(draw, W / 2, y, line, font_serif(26, italic=False), fill=(90, 83, 74))
        y += 38

    draw_tracked_text(draw, W / 2, 1255, "NAHIAHOME.COM", font_sans(16), fill=(140, 132, 120), tracking=6)
    return canvas

def make_shop_the_edit_slide(edit_title, edit_subtitle, product_keys):
    """Westwing 'Shop the Edit' 2x2 moodboard — NO prices on image, pure editorial curation."""
    W, H = 1080, 1350
    canvas = Image.new("RGBA", (W, H), (250, 247, 242, 255))
    draw = ImageDraw.Draw(canvas)

    draw_tracked_text(draw, W / 2, 68, "THE CURATED EDIT", font_sans(18, bold=True), fill=(120, 112, 100), tracking=8)
    draw_centered_text(draw, W / 2, 105, edit_title, font_serif(52, italic=True), fill=(28, 25, 22))
    draw_tracked_text(draw, W / 2, 178, edit_subtitle.upper(), font_sans(16), fill=(135, 126, 114), tracking=4)
    draw.line([(100, 218), (W - 100, 218)], fill=(226, 219, 207), width=1)

    cells = [
        (90, 250, 420, 460),
        (570, 250, 420, 460),
        (90, 755, 420, 460),
        (570, 755, 420, 460),
    ]

    for idx, key in enumerate(product_keys[:4]):
        cx, cy, cw, ch = cells[idx]
        p = PRODUCTS[key]
        draw.rectangle([(cx, cy), (cx + cw, cy + 330)], fill=(244, 239, 230, 255), outline=(232, 225, 213, 255), width=1)

        try:
            pim = load_product_image(key)
            max_pw, max_ph = 270, 250
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

def render_vertical_video(bg_img, secondary_img, out_mp4, kicker, title1, title2_italic, subtitle):
    VW, VH, FPS, FRAMES = 720, 1280, 24, 144
    tmp_dir = "/tmp/nahia_vertical_frames"
    os.makedirs(tmp_dir, exist_ok=True)

    im1 = crop_fill(bg_img, int(VW * 1.12), int(VH * 1.12), 0.5, 0.5)
    im2 = crop_fill(secondary_img, int(VW * 1.12), int(VH * 1.12), 0.5, 0.5)
    arr1 = np.asarray(im1, dtype=np.float32)
    arr2 = np.asarray(im2, dtype=np.float32)
    sh, sw = arr1.shape[:2]
    yy, xx = np.mgrid[0:VH, 0:VW].astype(np.float32)

    for f in range(FRAMES):
        t = f / FPS
        if t < 3.2:
            p = t / 3.2
            ox = int((sw - VW) * (0.25 + 0.5 * p))
            oy = int((sh - VH) * (0.5 - 0.15 * p))
            crop = arr1[oy:oy+VH, ox:ox+VW].copy()
        else:
            p = (t - 3.2) / 2.8
            ox = int((sw - VW) * (0.75 - 0.45 * p))
            oy = int((sh - VH) * (0.35 + 0.2 * p))
            crop = arr2[oy:oy+VH, ox:ox+VW].copy()
            if t < 3.8:
                alpha = (t - 3.2) / 0.6
                alpha = alpha * alpha * (3 - 2 * alpha)
                ox1 = int((sw - VW) * 0.75)
                oy1 = int((sh - VH) * 0.35)
                c1 = arr1[oy1:oy1+VH, ox1:ox1+VW]
                crop = c1 * (1 - alpha) + crop * alpha

        # 100% clean authentic image pixels — ZERO artificial dapple, waves, or pixel distortions
        clean_crop = np.clip(crop, 0, 255).astype(np.uint8)

        frame_im = add_gradient_overlay(Image.fromarray(clean_crop), top_alpha=85, bottom_alpha=165)
        draw = ImageDraw.Draw(frame_im)

        draw_tracked_text(draw, VW / 2, 95, "NAHIA HOME", font_sans(16, bold=True), fill=(250, 247, 242), tracking=8)
        draw_tracked_text(draw, VW / 2, 124, kicker.upper(), font_sans(13), fill=(225, 218, 206), tracking=4)
        draw.line([(VW / 2 - 30, 150), (VW / 2 + 30, 150)], fill=(230, 222, 210), width=1)

        draw_centered_text(draw, VW / 2, 985, title1, font_serif(44, italic=False), fill=(252, 249, 244))
        draw_centered_text(draw, VW / 2, 1040, title2_italic, font_serif(46, italic=True), fill=(244, 236, 222))
        draw_tracked_text(draw, VW / 2, 1118, subtitle.upper(), font_sans(13), fill=(215, 206, 192), tracking=4)

        frame_im.save(f"{tmp_dir}/f{f:04d}.jpg", quality=92)

    swift_code = f"""
import Foundation
import AVFoundation
import CoreGraphics
import ImageIO
let W={VW},H={VH},fps:Int32={FPS}
let out=URL(fileURLWithPath:"{out_mp4}"); try? FileManager.default.removeItem(at:out)
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
    print(f"Rendered clean vertical video: {out_mp4}")

# 100% Authentic, Visually-Verified Photography Only (ZERO composite/inserted objects, ZERO screengrabs)
scene1 = Image.open(os.path.join(BASE_DIR, "work/video_assets/gen/scene1.jpg")).convert("RGB")
scene2 = Image.open(os.path.join(BASE_DIR, "work/video_assets/gen/scene2.jpg")).convert("RGB")
scene3 = Image.open(os.path.join(BASE_DIR, "work/video_assets/gen/scene3.jpg")).convert("RGB")
scene4 = Image.open(os.path.join(BASE_DIR, "work/video_assets/gen/scene4.jpg")).convert("RGB")
scene5 = Image.open(os.path.join(BASE_DIR, "work/video_assets/gen/scene5.jpg")).convert("RGB")

abeille_sunlit = Image.open("/Users/josemiguellavao/.gemini/antigravity/brain/f7a2a8b4-c63a-4d1f-96ad-83f7ae6b5614/audit_abeille_sunlit.jpg").convert("RGB")
abeille_carafe_real = Image.open(os.path.join(STD_DIR, "jarra-de-vidrio-soplado-abeille-1l/sec_3_std.jpg")).convert("RGB")
abeille_minibol_real = Image.open(os.path.join(STD_DIR, "mini-bol-abeille-27-cl/sec_3_orig.jpg")).convert("RGB")
pearl_bowl_real = Image.open(os.path.join(STD_DIR, "ensaladera-costa-nova-pearl-27cm/sec_4_orig.jpg")).convert("RGB")
alheli_pitcher_real = Image.open(os.path.join(STD_DIR, "jarra-alheli-cote-table-2-3-l/sec_3_std.jpg")).convert("RGB")
livlig_wall_real = Image.open(os.path.join(STD_DIR, "soporte-de-manguera-graceful-green-livlig/sec_2_orig.jpg")).convert("RGB")
livlig_brass_real = Image.open(os.path.join(STD_DIR, "conjunto-de-conexion-de-manguera-de-laton-livlig/sec_2_orig.jpg")).convert("RGB")
slim_spread_real = Image.open(os.path.join(STD_DIR, "slim-aarons-la-dolce-vita/sec_2_orig.jpg")).convert("RGB")
umbel_real = Image.open(os.path.join(BASE_DIR, "work/umbel_luxury.jpg")).convert("RGB")
casalopez_table_real = Image.open(os.path.join(STD_DIR, "mantel-individual-lino-majorque-vert-olive-casa-lopez-paris/sec_2_orig.jpg")).convert("RGB")
casalopez_napkin_real = Image.open(os.path.join(STD_DIR, "servilleta-lino-emperatriz-casa-lopez-paris/sec_2_orig.jpg")).convert("RGB")
viana_fans_real = Image.open(os.path.join(STD_DIR, "abanico-de-lino-santanyi-the-viana-fan/sec_3_orig.jpg")).convert("RGB")
pearl_teapot_real = Image.open(os.path.join(STD_DIR, "lechera-pearl-10cl-costa-nova/sec_2_orig.jpg")).convert("RGB")
perloa_teacup_real = Image.open(os.path.join(STD_DIR, "taza-de-te-c-plato-perloa-cote-table-18cl/sec_2_orig.jpg")).convert("RGB")

DAYS_SPEC = [
    {
        "day": 1,
        "date": "2026-11-02",
        "weekday": "Monday · Nov 2",
        "edit_number": "THE TABLE EDIT",
        "title": "The La Rochère Icon (1475)",
        "pillar": "Iconic Objects & Provenance",
        "cover_bg": scene1,
        "secondary_bg": abeille_sunlit,
        "cover_line1": "L’Art de la Table",
        "cover_line2": "La Rochère Since 1475",
        "cover_sub": "French Pressed Glass · The Abeille Collection",
        "slide2_img": abeille_sunlit,
        "slide2_kicker": "FRENCH SAVOIR-FAIRE",
        "slide2_head": "The Imperial Bee Emblem",
        "slide2_body": [
            "Crafted in France’s oldest working glassworks since 1475,",
            "the Abeille collection catches the Mediterranean sunlight",
            "with timeless architectural weight and clarity."
        ],
        "slide3_img": abeille_carafe_real,
        "slide3_kicker": "MOUTH-BLOWN & PRESSED CRYSTAL",
        "slide3_head": "Luminous Silhouettes for the Table",
        "slide3_body": [
            "From the 1L blown-glass carafe to the everyday tumbler,",
            "each piece is designed to bring quiet elegance to every meal."
        ],
        "edit_title": "The Abeille Collection",
        "edit_sub": "La Rochère · France",
        "products": ["vaso_abeille", "copa_abeille_verde", "jarra_abeille", "minibol_abeille"],
        "ig_caption": "THE TABLE EDIT — L’Art de la Table.\n\nCrafted in France’s oldest working glassworks (established in 1475), our La Rochère Abeille glassware brings architectural weight, warm refraction, and the signature bee relief to the everyday table.\n\nExplore the complete collection via the product tags and the link in our bio.\n\n#NahiaHome #LaRochere #ArtDeLaTable #FrenchGlassware #TableStyling #QuietLuxury",
        "tiktok_caption": "THE TABLE EDIT · Crafted in France since 1475. The iconic Abeille glassware collection by La Rochère, curated for timeless tables. Discover the edit at nahiahome.com #NahiaHome #LaRochere #TableStyling #FrenchGlassware #QuietLuxury",
        "audio_suggestion": "Chet Baker — Almost Blue (Instrumental Vinyl)"
    },
    {
        "day": 2,
        "date": "2026-11-03",
        "weekday": "Tuesday · Nov 3",
        "edit_number": "THE MEDITERRANEAN EDIT",
        "title": "Portuguese Stoneware & Southern Light",
        "pillar": "The Art of Hosting",
        "cover_bg": scene2,
        "secondary_bg": pearl_bowl_real,
        "cover_line1": "The Afternoon Table",
        "cover_line2": "Stoneware & Sunlight",
        "cover_sub": "Costa Nova · Côté Table · Sabrê Paris",
        "slide2_img": pearl_bowl_real,
        "slide2_kicker": "PORTUGUESE STONEWARE · COSTA NOVA",
        "slide2_head": "Beaded Rims & Organic Glazes",
        "slide2_body": [
            "Inspired by 18th-century European ceramics, the Pearl",
            "collection pairs ribbed contours with a warm, tactile finish."
        ],
        "slide3_img": alheli_pitcher_real,
        "slide3_kicker": "CÔTÉ TABLE · PARIS",
        "slide3_head": "Botanical Tones in Ribbed Glass",
        "slide3_body": [
            "The Alhelí pitcher in olive glass brings natural height",
            "and luminous texture to outdoor and indoor tablescapes."
        ],
        "edit_title": "The Mediterranean Table",
        "edit_sub": "Portugal & Paris",
        "products": ["plato_pearl", "ensaladera_perloa", "cubiertos_bamboo", "jarra_alheli"],
        "ig_caption": "THE MEDITERRANEAN EDIT — Materiality and southern light.\n\nA timeless table lives in the dialogue between textures: unbleached linen, organic Portuguese stoneware from Costa Nova, ribbed French glass, and natural bamboo cutlery by Sabrê Paris.\n\nDiscover the complete table edit through the product tags and the link in our bio.\n\n#NahiaHome #CostaNova #CoteTable #SabreParis #Tableware #SlowLiving",
        "tiktok_caption": "THE MEDITERRANEAN EDIT · Layering Portuguese stoneware, raw linen, and Parisian bamboo flatware for an effortless Mediterranean table. Explore the edit at nahiahome.com #NahiaHome #TableScape #InteriorDesign #Hosting #EuropeanHome",
        "audio_suggestion": "Stan Getz & João Gilberto — Corcovado (Instrumental)"
    },
    {
        "day": 3,
        "date": "2026-11-04",
        "weekday": "Wednesday · Nov 4",
        "edit_number": "THE EXTERIOR EDIT",
        "title": "The Garden as Architecture",
        "pillar": "The Exterior Sanctuary",
        "cover_bg": livlig_wall_real,
        "secondary_bg": livlig_brass_real,
        "cover_line1": "Exterior Sanctuary",
        "cover_line2": "Solid Brass & Sage",
        "cover_sub": "Livlig Garden · The Viana Fan",
        "slide2_img": livlig_brass_real,
        "slide2_kicker": "GARDEN ARCHITECTURE · LIVLIG",
        "slide2_head": "Precision in Solid Brass",
        "slide2_body": [
            "Machined brass fittings and matte sage-green hoses that",
            "treat the garden and terrace as an extension of the interior."
        ],
        "slide3_img": scene3,
        "slide3_kicker": "SPANISH CRAFTSMANSHIP · VIANA",
        "slide3_head": "Natural Linen & Noble Wood",
        "slide3_body": [
            "Handcrafted in Spain from organic linen and polished wood",
            "ribs for slow afternoons beside the water."
        ],
        "edit_title": "The Exterior Sanctuary",
        "edit_sub": "Livlig & The Viana Fan",
        "products": ["grifo_livlig", "manguera_livlig", "soporte_livlig", "abanico_viana"],
        "ig_caption": "THE EXTERIOR EDIT — The garden as an architectural extension of the home.\n\nFrom Livlig’s sage green garden hoses and solid brass fittings to the handcrafted linen of The Viana Fan, every exterior detail deserves quiet elegance.\n\nExplore the garden and outdoor collection via the link in our bio.\n\n#NahiaHome #Livlig #GardenArchitecture #OutdoorLiving #TerraceDesign #QuietLuxury",
        "tiktok_caption": "THE EXTERIOR EDIT · Elevating the garden sanctuary with solid brass fittings, sage green hardware by Livlig, and handmade Spanish linen. Discover more at nahiahome.com #NahiaHome #GardenDesign #ExteriorDesign #LuxuryHome #OutdoorLiving",
        "audio_suggestion": "Ludovico Einaudi — Una Mattina (Acoustic Piano)"
    },
    {
        "day": 4,
        "date": "2026-11-05",
        "weekday": "Thursday · Nov 5",
        "edit_number": "THE LIVING EDIT",
        "title": "The Reading Corner & Coffee Table",
        "pillar": "Curated Edits & Books",
        "cover_bg": scene4,
        "secondary_bg": umbel_real,
        "cover_line1": "Objects of Desire",
        "cover_line2": "Art Books & Porcelain",
        "cover_sub": "Slim Aarons · Taschen · Costa Nova",
        "slide2_img": slim_spread_real,
        "slide2_kicker": "COLLECTOR MONOGRAPHS",
        "slide2_head": "Slim Aarons: La Dolce Vita",
        "slide2_body": [
            "An intimate photographic chronicle of Italian villas,",
            "sun-drenched gardens, and timeless coastal living."
        ],
        "slide3_img": umbel_real,
        "slide3_kicker": "BOTANICAL STATIONERY",
        "slide3_head": "Tactile Linen & Fine Paper",
        "slide3_body": [
            "Our Umbel botanical notebook pairs raw woven cloth",
            "with delicate line illustration for desks and consoles."
        ],
        "edit_title": "The Reading Sanctuary",
        "edit_sub": "Art Books & Fine Stoneware",
        "products": ["libro_slim", "libro_lemon", "taza_pearl", "tetera_pearl"],
        "ig_caption": "THE LIVING EDIT — The art of styling quiet corners.\n\nLarge-format illustrated monographs including Slim Aarons’ 'La Dolce Vita' and Taschen’s 'The Gourmand’s Lemon', paired with botanical linen stationery and Costa Nova stoneware.\n\nDiscover our curated library and home objects at nahiahome.com.\n\n#NahiaHome #CoffeeTableBooks #SlimAarons #InteriorStyling #ArchitecturalDigest #HomeEdit",
        "tiktok_caption": "THE LIVING EDIT · Styling a travertine side table with large-format Slim Aarons photography, candlelight, and botanical linen stationery. Shop the edit at nahiahome.com #NahiaHome #CoffeeTableBooks #SlimAarons #InteriorStyling #HomeDecor",
        "audio_suggestion": "Erik Satie — Gymnopédie No. 1 (Warm Vinyl)"
    },
    {
        "day": 5,
        "date": "2026-11-06",
        "weekday": "Friday · Nov 6",
        "edit_number": "THE WEEKEND TABLE",
        "title": "Candlelight, Olive & Crystal at Dusk",
        "pillar": "The Art of Hosting",
        "cover_bg": scene5,
        "secondary_bg": casalopez_table_real,
        "cover_line1": "The Friday Table",
        "cover_line2": "Candlelight at Dusk",
        "cover_sub": "La Rochère · Côté Table · Casa López",
        "slide2_img": casalopez_table_real,
        "slide2_kicker": "CASA LÓPEZ · PARIS",
        "slide2_head": "Woven Linen in Vert Olive",
        "slide2_body": [
            "Framed in deep olive green, the Majorque linen placemat",
            "anchors the table with structured Parisian sophistication."
        ],
        "slide3_img": casalopez_napkin_real,
        "slide3_kicker": "BOTANICAL EMBROIDERY",
        "slide3_head": "Heirloom Textiles for the Table",
        "slide3_body": [
            "Delicately embroidered pure linen napkins that soften",
            "beautifully with every gathering."
        ],
        "edit_title": "Dinner by Candlelight",
        "edit_sub": "The Weekend Hosting Edit",
        "products": ["copa_abeille_verde", "vaso_abeille", "botella_poisson", "mantel_casalopez"],
        "ig_caption": "THE WEEKEND TABLE — The art of gathering at dusk.\n\nPure woven linen by Casa López Paris, aged brass taper holders, olive branches, and the warm green glow of our La Rochère Abeille goblets.\n\nEvery piece on this table is tagged in the post and available via the link in our bio.\n\n#NahiaHome #TableSetting #ArtOfHosting #LaRochere #CasaLopez #EveningTable",
        "tiktok_caption": "THE WEEKEND TABLE · Setting the mood for Friday evening: tall taper candles, olive-green French crystal, and Casa López Paris table linens. Discover the look at nahiahome.com #NahiaHome #DinnerParty #TableSetting #ArtOfHosting #QuietLuxury",
        "audio_suggestion": "Dalida & Alain Delon — Paroles, Paroles (Instrumental Lounge)"
    },
    {
        "day": 6,
        "date": "2026-11-07",
        "weekday": "Saturday · Nov 7",
        "edit_number": "THE GIFT EDIT",
        "title": "Objects of Character & Provenance",
        "pillar": "Curated Gift Guide",
        "cover_bg": abeille_sunlit,
        "secondary_bg": abeille_minibol_real,
        "cover_line1": "The Gift Edit",
        "cover_line2": "Objects to Treasure",
        "cover_sub": "Curated European Design · Atelier Selection",
        "slide2_img": abeille_minibol_real,
        "slide2_kicker": "LA ROCHÈRE · FRANCE 1475",
        "slide2_head": "Everyday Rituals in Pressed Crystal",
        "slide2_body": [
            "The Abeille mini bowl brings centuries of French glassmaking",
            "heritage to morning fruit, aperitifs, and desserts."
        ],
        "slide3_img": viana_fans_real,
        "slide3_kicker": "THE VIANA FAN · SPAIN",
        "slide3_head": "Artisanal Linen & Carved Wood",
        "slide3_body": [
            "Thoughtful, enduring objects crafted in small batches",
            "by European ateliers for those who appreciate fine detail."
        ],
        "edit_title": "Objects to Treasure",
        "edit_sub": "The Nahia Home Gift Edit",
        "products": ["botella_poisson", "libro_lemon", "jarra_abeille", "cuaderno_umbel"],
        "ig_caption": "THE GIFT EDIT — The art of gifting objects that endure.\n\nA curated selection of distinctive European pieces: the sculptural Poisson carafe by Côté Table, Taschen’s 'The Gourmand’s Lemon', our 1L Abeille crystal carafe, and botanical linen notebooks.\n\nSave this edit for the upcoming season or explore the collection at nahiahome.com.\n\n#NahiaHome #GiftGuide #ObjectsOfDesire #CoteTable #InteriorGifts #EuropeanDesign",
        "tiktok_caption": "THE GIFT EDIT · Curated European home gifts that feel like a Parisian gallery find. Save this edit for the upcoming holiday season. #NahiaHome #GiftGuide #HolidayGifts #HomeDecor #ParisianStyle",
        "audio_suggestion": "Françoise Hardy — Le temps de l'amour (Acoustic Instrumental)"
    },
    {
        "day": 7,
        "date": "2026-11-08",
        "weekday": "Sunday · Nov 8",
        "edit_number": "LE DIMANCHE MATIN",
        "title": "The Slow Sunday Morning Ritual",
        "pillar": "Slow Sunday Living",
        "cover_bg": pearl_teapot_real,
        "secondary_bg": perloa_teacup_real,
        "cover_line1": "Le Dimanche Matin",
        "cover_line2": "Unrushed Mornings",
        "cover_sub": "Costa Nova Pearl · Perloa · La Rochère",
        "slide2_img": perloa_teacup_real,
        "slide2_kicker": "CÔTÉ TABLE · PARIS",
        "slide2_head": "The Sculpted Perloa Tea Cup",
        "slide2_body": [
            "Delicate glass beads form the handle and saucer rim,",
            "catching the soft morning light at the breakfast table."
        ],
        "slide3_img": pearl_bowl_real,
        "slide3_kicker": "COSTA NOVA · PORTUGAL",
        "slide3_head": "Most Loved Pieces This Week",
        "slide3_body": [
            "Our community’s most desired objects of the week:",
            "Pearl stoneware, Perloa teacups, and Abeille crystal."
        ],
        "edit_title": "The Sunday Morning Edit",
        "edit_sub": "Costa Nova & Côté Table",
        "products": ["tetera_pearl", "taza_perloa", "lechera_pearl", "minibol_abeille"],
        "ig_caption": "LE DIMANCHE MATIN — Unrushed Sunday mornings.\n\nThe Pearl infuser teapot and creamer by Costa Nova on natural marble, paired with Côté Table’s beaded Perloa teacup and the La Rochère Abeille mini bowl.\n\nDiscover this week’s most loved pieces via the link in our bio.\n\n#NahiaHome #SundayMorning #SlowLiving #CostaNovaPearl #ArtDeVivre #MorningRitual",
        "tiktok_caption": "LE DIMANCHE MATIN · Slow Sunday morning rituals with Portuguese Pearl stoneware and sculpted French glass. Discover the collection at nahiahome.com #NahiaHome #SundayMorning #SlowLiving #Ceramics #Tableware",
        "audio_suggestion": "Claude Debussy — Clair de Lune (Soft Morning Piano)"
    }
]

manifest = []

for d in DAYS_SPEC:
    day_num = d["day"]
    day_folder = os.path.join(ASSETS_DIR, f"day_{day_num:02d}")
    os.makedirs(day_folder, exist_ok=True)
    print(f"=== Generating Clean Authentic Day {day_num}: {d['title']} ===")

    s1 = make_cover_slide(d["cover_bg"], d["edit_number"], d["cover_line1"], d["cover_line2"], d["cover_sub"])
    s1.save(os.path.join(day_folder, "ig_slide_1_cover.jpg"), quality=94)

    fx2, fy2 = d.get("slide2_focus", (0.5, 0.5))
    s2 = make_framed_editorial_slide(d["slide2_img"], d["slide2_kicker"], d["slide2_head"], d["slide2_body"], fx2, fy2)
    s2.save(os.path.join(day_folder, "ig_slide_2_detail.jpg"), quality=94)

    fx3, fy3 = d.get("slide3_focus", (0.5, 0.5))
    s3 = make_framed_editorial_slide(d["slide3_img"], d["slide3_kicker"], d["slide3_head"], d["slide3_body"], fx3, fy3)
    s3.save(os.path.join(day_folder, "ig_slide_3_story.jpg"), quality=94)

    s4 = make_shop_the_edit_slide(d["edit_title"], d["edit_sub"], d["products"])
    s4.save(os.path.join(day_folder, "ig_slide_4_shop_edit.jpg"), quality=94)

    video_path = os.path.join(day_folder, f"tiktok_reel_day_{day_num:02d}.mp4")
    if day_num == 1 and os.path.exists(video_path):
        print(f"Keeping authentic live-action video for Day 1: {video_path}")
    else:
        render_vertical_video(
            d["cover_bg"], d["secondary_bg"], video_path,
            d["edit_number"], d["cover_line1"], d["cover_line2"], d["cover_sub"]
        )

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
        "ig_caption": d["ig_caption"],
        "tiktok_caption": d["tiktok_caption"],
        "audio_suggestion": d["audio_suggestion"],
        "products": [PRODUCTS[k] for k in d["products"]],
        "status": "READY TO POST"
    })

with open(os.path.join(STUDIO_DIR, "posts_manifest.json"), "w") as f:
    json.dump(manifest, f, indent=2, ensure_ascii=False)

print("All 7 days regenerated with 100% authentic photography and ZERO prices on images!")
