#!/usr/bin/env python3
"""Build the self-contained video demo for the bounty submission."""
import asyncio
import json
import subprocess
from pathlib import Path

import edge_tts
import imageio_ffmpeg
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
BUILD = ROOT / "video_build"
BUILD.mkdir(exist_ok=True)
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
VOICE = "en-US-AriaNeural"
WIDTH, HEIGHT = 1280, 720

FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
TITLE_FONT = ImageFont.truetype(FONT_BOLD, 54)
BODY_FONT = ImageFont.truetype(FONT_MONO, 29)
SMALL_FONT = ImageFont.truetype(FONT_MONO, 21)


def draw_slide(index, item):
    img = Image.new("RGB", (WIDTH, HEIGHT), (15, 18, 28))
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle((45, 40, 1235, 675), radius=28, outline=(90, 110, 145), width=3)
    draw.text((80, 75), item["title"], font=TITLE_FONT, fill=(245, 245, 248))
    y = 175
    for line in item["lines"]:
        if not line:
            y += 22
            continue
        fill = (195, 225, 255)
        if "BLOCKED" in line or "secret request" in line:
            fill = (255, 195, 195)
        elif "passed" in line or "zero-stated" in line:
            fill = (190, 245, 205)
        draw.text((90, y), line, font=BODY_FONT, fill=fill)
        y += 55
    draw.text(
        (80, 625),
        f"Slide {index + 1}/6  •  github.com/naief9961-tech/mermail-bounty-ops-skill",
        font=SMALL_FONT,
        fill=(150, 160, 180),
    )
    out = BUILD / f"slide_{index:02d}.png"
    img.save(out)
    return out


async def synthesize(item, index):
    out = BUILD / f"audio_{index:02d}.mp3"
    communicate = edge_tts.Communicate(item["narration"], VOICE, rate="-5%")
    await communicate.save(str(out))
    return out


def build_segment(slide, audio, index):
    out = BUILD / f"segment_{index:02d}.mp4"
    cmd = [
        FFMPEG, "-y", "-loop", "1", "-i", str(slide), "-i", str(audio),
        "-c:v", "libx264", "-tune", "stillimage", "-c:a", "aac",
        "-b:a", "128k", "-pix_fmt", "yuv420p", "-shortest",
        "-movflags", "+faststart", str(out),
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return out


async def main():
    items = json.loads((ROOT / "video_script.json").read_text())
    segments = []
    for index, item in enumerate(items):
        slide = draw_slide(index, item)
        audio = await synthesize(item, index)
        segments.append(build_segment(slide, audio, index))

    concat_file = BUILD / "concat.txt"
    concat_file.write_text("".join(f"file '{segment}'\n" for segment in segments))
    output = ROOT / "mermail-bounty-ops-demo.mp4"
    subprocess.run(
        [FFMPEG, "-y", "-f", "concat", "-safe", "0", "-i", str(concat_file),
         "-c", "copy", "-movflags", "+faststart", str(output)],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    print(output)


if __name__ == "__main__":
    asyncio.run(main())
