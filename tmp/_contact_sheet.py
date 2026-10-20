"""Build a labeled contact sheet so covers can be matched to products by eye."""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

SRC = Path(__file__).parent / "images"
OUT = Path(__file__).parent / "_contact_sheet.png"

files = sorted(SRC.glob("*.png"))
print("found:", len(files))
for f in files:
    print("  ", f.name, Image.open(f).size)

CELL_W, CELL_H = 420, 560
LABEL_H = 46
COLS = 4
ROWS = (len(files) + COLS - 1) // COLS

sheet = Image.new("RGB", (COLS * CELL_W, ROWS * (CELL_H + LABEL_H)), "white")
draw = ImageDraw.Draw(sheet)

try:
    font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 26)
except OSError:
    font = ImageFont.load_default()

for i, f in enumerate(files):
    col, row = i % COLS, i // COLS
    x, y = col * CELL_W, row * (CELL_H + LABEL_H)

    im = Image.open(f).convert("RGB")
    im.thumbnail((CELL_W - 20, CELL_H - 20), Image.LANCZOS)
    ox = x + (CELL_W - im.width) // 2
    oy = y + (CELL_H - im.height) // 2
    sheet.paste(im, (ox, oy))
    draw.rectangle([x, y, x + CELL_W - 1, y + CELL_H - 1], outline="#bbbbbb", width=2)

    label = f"{i + 1}. {f.name}"
    draw.text((x + 10, y + CELL_H + 6), label, fill="#111111", font=font)

sheet.save(OUT)
print("wrote", OUT, sheet.size)