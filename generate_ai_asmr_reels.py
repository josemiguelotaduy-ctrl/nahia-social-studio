#!/usr/bin/env python3
"""
AI Image-to-Video ASMR Reel Generator for Nahia Home (powered by Gemini Omni 1.1 Flash).
Uses your exact authentic product photographs (--first-frame) to synthesize 1080p 9:16
vertical live-action motion & native ASMR soundscapes.

Prerequisite:
  Add GEMINI_API_KEY="your_google_ai_studio_key" to /Users/josemiguellavao/Desktop/NAHIA HOME/.env
"""
import os, sys, subprocess

BASE_DIR = "/Users/josemiguellavao/Desktop/NAHIA HOME"
ENV_PATH = os.path.join(BASE_DIR, ".env")
OMNI_SCRIPT = "/Users/josemiguellavao/.gemini/config/plugins/gemini-api/skills/gemini-omni-flash-api/scripts/video/generate_video.py"

if os.path.exists(ENV_PATH):
    with open(ENV_PATH) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip().strip("\"'"))

AI_ASMR_PROMPTS = [
    {
        "day": 1,
        "name": "Day 01 — La Rochère Abeille Crystal Water Pour ASMR",
        "first_frame": "/Users/josemiguellavao/.gemini/antigravity/brain/f7a2a8b4-c63a-4d1f-96ad-83f7ae6b5614/audit_abeille_sunlit.jpg",
        "output": os.path.join(BASE_DIR, "social_studio/assets/day_01/tiktok_reel_day_01_ai.mp4"),
        "prompt": (
            "Continuous, unbroken close-up shot in warm Mediterranean morning sunlight. "
            "Crystal-clear chilled water is slowly poured from the glass carafe into the pressed French crystal "
            "La Rochère Abeille goblet with the signature bee relief. Golden sunlight refracts through the rising water "
            "and ripples softly on the wooden table. Sound design: Crisp, intimate ASMR sound of chilled water pouring "
            "into heavy crystal glass, soft coastal breeze. No dialogue, no music."
        )
    },
    {
        "day": 5,
        "name": "Day 05 — Dusk Candlelight & Casa López Linen ASMR",
        "first_frame": os.path.join(BASE_DIR, "work/video_assets/gen/scene5.jpg"),
        "output": os.path.join(BASE_DIR, "social_studio/assets/day_05/tiktok_reel_day_05_ai.mp4"),
        "prompt": (
            "Continuous, unbroken cinematic shot of a luxury Mediterranean dinner table at sunset overlooking the sea. "
            "Tall ivory taper candles in brass holders flicker gently in the warm evening breeze, casting dancing golden "
            "reflections inside the olive-green La Rochère crystal wine goblets and across the pure woven linen tablecloth. "
            "Sound design: Soft ASMR candle wick crackle, gentle Mediterranean evening waves, and a delicate crystal goblet clink. No dialogue."
        )
    },
    {
        "day": 7,
        "name": "Day 07 — Le Dimanche Matin: Costa Nova Pearl Tea Pour ASMR",
        "first_frame": os.path.join(BASE_DIR, "scratch/batch_standardization/lechera-pearl-10cl-costa-nova/sec_2_orig.jpg"),
        "output": os.path.join(BASE_DIR, "social_studio/assets/day_07/tiktok_reel_day_07_ai.mp4"),
        "prompt": (
            "Continuous, unbroken slow-motion shot on a sunlit marble breakfast table. "
            "Delicate wisps of warm steam rise from the white beaded Costa Nova Pearl stoneware teapot as morning sunlight "
            "sweeps across the glazed ceramic pearls and linen napkin. "
            "Sound design: Quiet Sunday morning ASMR ambiance, soft porcelain lid clink, gentle morning birdsong. No dialogue."
        )
    }
]

def main():
    if not os.environ.get("GEMINI_API_KEY"):
        print("⚠️  GEMINI_API_KEY is not set in /Users/josemiguellavao/Desktop/NAHIA HOME/.env yet.")
        print("   Add GEMINI_API_KEY=your_key to .env and re-run this script to generate full AI video clips via Gemini Omni 1.1 Flash.")
        sys.exit(1)

    for item in AI_ASMR_PROMPTS:
        print(f"🎬 Generating {item['name']}...")
        cmd = [
            os.path.expanduser("~/nahia_venv/bin/python"), OMNI_SCRIPT,
            item["prompt"],
            "--first-frame", item["first_frame"],
            "--aspect-ratio", "9:16",
            "--resolution", "1080p",
            "--output", item["output"]
        ]
        subprocess.run(cmd, check=True)
        print(f"✅ Saved AI ASMR Reel to {item['output']}")

if __name__ == "__main__":
    main()
