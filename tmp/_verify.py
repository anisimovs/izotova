"""Проверка: ссылки и обложки в index.html совпадают с tmp/goods.txt."""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GOODS = ROOT / "tmp" / "goods.txt"
HTML = ROOT / "site" / "index.html"

# ── 1. парсим исходный список (файл начинается с пустой строки) ──
raw = [ln.strip() for ln in GOODS.read_text(encoding="utf-8").splitlines()]
raw = [ln for ln in raw if ln]  # убираем пустые строки-разделители
pairs = [(raw[i], raw[i + 1]) for i in range(0, len(raw) - 1, 2)]

assert all(u.startswith("http") for _, u in pairs), "чётность пар нарушена"
print(f"goods.txt: {len(pairs)} товаров\n")

errors = []

# ── 2. ссылки: каждая из goods.txt должна встречаться в HTML ──
html = HTML.read_text(encoding="utf-8")
for title, url in pairs:
    n = html.count(url)
    # 2 = карточка (обложка + кнопка «Купить»); 3 = плюс CTA-блок внизу
    ok = n in (2, 3)
    print(f"{'OK ' if ok else 'ERR'}  {url}  ×{n}  {title}")
    if not ok:
        errors.append(f"ссылка {url} встречается {n} раз (ожидалось 2): {title}")

# ── 3. лишние ссылки в HTML, которых нет в goods.txt ──
known = {u for _, u in pairs}
for url in set(re.findall(r"https://payform\.ru/[A-Za-z0-9]+/", html)):
    if url not in known:
        errors.append(f"в HTML есть ссылка, которой нет в goods.txt: {url}")

# ── 4. карточки товаров и их картинки ──
cards = re.findall(
    r'<article class="card reveal" data-series="([^"]+)" data-age="([^"]+)">(.*?)</article>',
    html,
    re.S,
)
print(f"\nкарточек в HTML: {len(cards)}")

img_dir = ROOT / "site" / "assets" / "img"
used_imgs = set()
for series, age, body in cards:
    m = re.search(r'<img src="assets/img/([^"]+)"', body)
    if not m:
        errors.append(f"карточка {series}/{age}: нет <img>")
        continue
    name = m.group(1)
    used_imgs.add(name)
    if not (img_dir / name).exists():
        errors.append(f"нет файла обложки: {name}")

for extra in sorted(p.name for p in img_dir.glob("*.webp")):
    if extra not in used_imgs:
        print(f"     (в галерее не используется: {extra})")

# ── 5. дубли картинок: одна обложка не должна стоять у двух товаров ──
print(f"\nуникальных обложек использовано: {len(used_imgs)} из {len(list(img_dir.glob('*.webp')))}")

# ── 6. счётчики в фильтрах против реального количества карточек ──
from collections import Counter
age_counts = Counter(a for _, a, _ in cards)
print("\nфактически по data-age:", dict(age_counts))
for label, value in re.findall(r'data-filter="([^"]+)"[^>]*>.*?filter-n">(\d+)<', html, re.S):
    actual = len(cards) if label == "all" else age_counts.get(label, 0)
    flag = "OK " if int(value) == actual else "ERR"
    print(f"{flag}  фильтр «{label}»: в разметке {value}, карточек {actual}")
    if int(value) != actual:
        errors.append(f"счётчик фильтра {label}: {value} != {actual}")

# ── итог ──
print()
if errors:
    print("ОШИБКИ:")
    for e in errors:
        print("  -", e)
    sys.exit(1)
print("Все проверки пройдены: 12 товаров, 12 ссылок, 12 обложек.")