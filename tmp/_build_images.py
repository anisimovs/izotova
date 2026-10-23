"""Convert the 12 raw PNG covers into lightweight WebP for the landing.

Mapping is derived from the contact sheet (tmp/_contact_sheet.png), where every
cover's printed title was read directly — not guessed from filename order.
"""
from pathlib import Path

from PIL import Image

TMP = Path(__file__).parent
SRC = TMP / "images"
DST = TMP.parent / "site" / "assets" / "img"

# slug -> (source png, product title, subtitle, age, pages)
MAPPING = {
    "bimbom": ("Обложка.png", "Бим и Бом", "Твердые и мягкие согласные звуки", None, 76),
    "bukvy-zaplatki": ("Обложка_1.png", "Буквы заплатки", "Все буквы русского алфавита", None, 34),
    "myshonok-poverenok": ("mouse.png", "Мышонок поваренок", "Шаблоны для малышей", None, 20),
    "azbuka-vasiliya-1": ("Обложка1.png", "Азбука кота Василия", "Звуки и буквы от А до Й", "4–5 лет", 70),
    "azbuka-vasiliya-2": ("Обложка2.png", "Азбука кота Василия", "Звуки и буквы от К до Ф", "4–5 лет", 70),
    "azbuka-vasiliya-3": ("Обложка3.png", "Азбука кота Василия", "Звуки и буквы от Х до Я", "4–5 лет", 70),
    "zvuki-i-bukvy-1": ("Обложка1_1.png", "Звуки и буквы", "Гласные звуки и буквы", "5–6 лет", 64),
    "zvuki-i-bukvy-2": ("Обложка2_1.png", "Звуки и буквы", "Согласные звуки и буквы", "5–6 лет", 70),
    "zvuki-i-bukvy-3": ("Обложка3_1.png", "Звуки и буквы", "Согласные звуки и буквы", "5–6 лет", 76),
    "azbuka-grammatika-1": ("Обложка1_2.png", "Азбука грамматика", "Фонетика, грамматика, чтение", "6–7 лет", 61),
    "azbuka-grammatika-2": ("Обложка2_2.png", "Азбука грамматика", "Фонетика, грамматика, чтение", "6–7 лет", 58),
    "hochu-chitat-1": ("Обложка1_3.png", "Хочу читать", "От чтения слогов к тексту", "6–7 лет", 80),
    "hochu-chitat-2": ("Обложка2_3.png", "Хочу читать", "От чтения слогов к тексту", "6–7 лет", 80),
}

DST.mkdir(parents=True, exist_ok=True)

total_before = total_after = 0
rows = []
for slug, (src_name, title, subtitle, age, pages) in MAPPING.items():
    src = SRC / src_name
    if not src.exists():
        raise SystemExit(f"missing source: {src}")
    before = src.stat().st_size
    im = Image.open(src).convert("RGB")
    im.thumbnail((900, 1100), Image.LANCZOS)
    out = DST / f"{slug}.webp"
    im.save(out, "WEBP", quality=84, method=6)
    after = out.stat().st_size
    total_before += before
    total_after += after
    rows.append((slug, src_name, title, subtitle, age or "—", pages, before, after))

print(f"{'slug':<22}{'source':<18}{'pages':>7}{'KB before':>11}{'KB after':>10}")
for slug, src_name, title, subtitle, age, pages, before, after in rows:
    print(f"{slug:<22}{src_name:<18}{pages:>7}{before / 1024:>11.0f}{after / 1024:>10.0f}")
print(f"\nTOTAL {total_before / 1024 / 1024:.2f} MB -> {total_after / 1024:.0f} KB")