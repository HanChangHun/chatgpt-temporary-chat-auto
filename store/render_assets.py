from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont


ROOT = Path(__file__).resolve().parents[1]
ASSET_DIR = ROOT / "store" / "assets"
ICON_DIR = ROOT / "icons"
SOURCE_CAPTURE = ROOT / "store" / "source" / "chatgpt-real-page.png"
LOGO_APP_ICON = ROOT / "store" / "source" / "logo-generated-appicon.png"
SCALE = 3

FONT_FILES = {
    "regular": [
        r"C:\Windows\Fonts\segoeui.ttf",
        r"C:\Windows\Fonts\arial.ttf",
    ],
    "semibold": [
        r"C:\Windows\Fonts\seguisb.ttf",
        r"C:\Windows\Fonts\segoeuib.ttf",
        r"C:\Windows\Fonts\arialbd.ttf",
    ],
    "bold": [
        r"C:\Windows\Fonts\segoeuib.ttf",
        r"C:\Windows\Fonts\arialbd.ttf",
    ],
    "mono": [
        r"C:\Windows\Fonts\consola.ttf",
        r"C:\Windows\Fonts\cour.ttf",
    ],
}

COLORS = {
    "ink": "#172033",
    "muted": "#64748b",
    "line": "#dbe4ea",
    "paper": "#ffffff",
    "wash": "#f5f7f8",
    "sidebar": "#edf3f7",
    "teal": "#0f766e",
    "teal_bright": "#14b8a6",
    "blue": "#2563eb",
    "amber": "#f4b740",
    "green_soft": "#dff7ef",
}


def c(hex_color, alpha=255):
    value = hex_color.lstrip("#")
    return tuple(int(value[i : i + 2], 16) for i in (0, 2, 4)) + (alpha,)


def load_font(size, weight="regular"):
    for candidate in FONT_FILES.get(weight, FONT_FILES["regular"]):
        if Path(candidate).exists():
            return ImageFont.truetype(candidate, size * SCALE)
    return ImageFont.load_default(size * SCALE)


def sc(value):
    return int(round(value * SCALE))


def box(values):
    return tuple(sc(v) for v in values)


def rounded(draw, coords, radius, fill, outline=None, width=1):
    draw.rounded_rectangle(
        box(coords),
        radius=sc(radius),
        fill=fill,
        outline=outline,
        width=sc(width),
    )


def ellipse(draw, coords, fill, outline=None, width=1):
    draw.ellipse(box(coords), fill=fill, outline=outline, width=sc(width))


def line(draw, coords, fill, width=1):
    draw.line([sc(v) for v in coords], fill=fill, width=sc(width))


def text(draw, xy, value, size, fill, weight="regular", anchor=None, align="left"):
    draw.text(
        (sc(xy[0]), sc(xy[1])),
        value,
        font=load_font(size, weight),
        fill=fill,
        anchor=anchor,
        align=align,
    )


def text_size(draw, value, size, weight="regular"):
    bounds = draw.textbbox((0, 0), value, font=load_font(size, weight))
    return (bounds[2] - bounds[0]) / SCALE, (bounds[3] - bounds[1]) / SCALE


def shadow(base, coords, radius, blur=18, offset=(0, 8), alpha=32):
    layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    x1, y1, x2, y2 = coords
    ox, oy = offset
    d.rounded_rectangle(
        box((x1 + ox, y1 + oy, x2 + ox, y2 + oy)),
        radius=sc(radius),
        fill=(15, 23, 42, alpha),
    )
    layer = layer.filter(ImageFilter.GaussianBlur(sc(blur)))
    base.alpha_composite(layer)


def gradient(size, left, right, vertical=False):
    width, height = size
    img = Image.new("RGBA", size, left)
    d = ImageDraw.Draw(img)
    steps = height if vertical else width
    for i in range(steps):
        t = i / max(1, steps - 1)
        color = tuple(int(left[j] * (1 - t) + right[j] * t) for j in range(4))
        if vertical:
            d.line((0, i, width, i), fill=color)
        else:
            d.line((i, 0, i, height), fill=color)
    return img


def finalize(img, path):
    path.parent.mkdir(parents=True, exist_ok=True)
    if img.size[0] % SCALE == 0 and img.size[1] % SCALE == 0:
        img = img.resize((img.size[0] // SCALE, img.size[1] // SCALE), Image.Resampling.LANCZOS)
    img.convert("RGBA").save(path)


def draw_capsule(draw, coords, fill):
    x1, y1, x2, y2 = coords
    radius = max(1, int((y2 - y1) / 2))
    draw.rounded_rectangle(coords, radius=radius, fill=fill)


def load_generated_app_icon(size):
    source = Image.open(LOGO_APP_ICON).convert("RGBA")
    rgb = source.convert("RGB")
    mask = Image.new("L", source.size, 0)
    md = ImageDraw.Draw(mask)
    pixels = rgb.load()
    alpha = mask.load()

    for y in range(source.height):
        for x in range(source.width):
            r, g, b = pixels[x, y]
            if not (r > 244 and g > 244 and b > 244):
                alpha[x, y] = 255

    bbox = mask.getbbox() or (0, 0, source.width, source.height)
    crop = source.crop(bbox)
    crop = crop.resize((size, size), Image.Resampling.LANCZOS)

    out = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    rounded_mask = Image.new("L", (size, size), 0)
    rd = ImageDraw.Draw(rounded_mask)
    rd.rounded_rectangle((0, 0, size - 1, size - 1), radius=max(1, int(size * 0.22)), fill=255)
    out.paste(crop, (0, 0), rounded_mask)
    return out


def app_icon(size):
    if LOGO_APP_ICON.exists():
        return load_generated_app_icon(size)

    ss = 6
    n = size * ss
    img = Image.new("RGBA", (n, n), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    def p(value):
        return int(round(value * n))

    shadow = Image.new("RGBA", (n, n), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    sd.ellipse((p(0.14), p(0.10), p(0.86), p(0.82)), fill=(0, 0, 0, 56))
    sd.polygon([(p(0.36), p(0.75)), (p(0.22), p(0.92)), (p(0.52), p(0.78))], fill=(0, 0, 0, 56))
    shadow = shadow.filter(ImageFilter.GaussianBlur(max(1, p(0.024))))
    img.alpha_composite(shadow)

    dark = c("#0f172a")
    bubble_fill = (255, 255, 255, 255)
    d.ellipse((p(0.14), p(0.09), p(0.86), p(0.81)), fill=bubble_fill)
    d.polygon([(p(0.36), p(0.75)), (p(0.22), p(0.93)), (p(0.52), p(0.78))], fill=bubble_fill)

    cx, cy, radius = p(0.50), p(0.45), p(0.29)
    stroke = max(2, p(0.045))
    dash_len = 24
    gap_len = 22
    start = 200
    while start < 520:
        end = min(start + dash_len, 520)
        d.arc((cx - radius, cy - radius, cx + radius, cy + radius), start, end, fill=dark, width=stroke)
        start += dash_len + gap_len

    d.line((p(0.38), p(0.72), p(0.30), p(0.83)), fill=dark, width=stroke)
    d.line((p(0.30), p(0.83), p(0.43), p(0.76)), fill=dark, width=stroke)

    d.rounded_rectangle((p(0.35), p(0.37), p(0.71), p(0.52)), radius=p(0.075), fill=c(COLORS["teal"]))
    d.ellipse((p(0.59), p(0.385), p(0.70), p(0.505)), fill=(255, 255, 255, 255))

    img = img.resize((size, size), Image.Resampling.LANCZOS)
    return img


def paste_icon(base, xy, size):
    icon = app_icon(sc(size))
    base.alpha_composite(icon, (sc(xy[0]), sc(xy[1])))


def real_capture(crop, size):
    if not SOURCE_CAPTURE.exists():
        raise FileNotFoundError(
            f"Missing real ChatGPT source capture: {SOURCE_CAPTURE}. "
            "Open ChatGPT, capture a sanitized top crop, then rerun this script."
        )

    source = Image.open(SOURCE_CAPTURE).convert("RGBA")
    return source.crop(crop).resize((sc(size[0]), sc(size[1])), Image.Resampling.LANCZOS)


def real_capture_contain(crop, size):
    source = Image.open(SOURCE_CAPTURE).convert("RGBA").crop(crop)
    target_w, target_h = sc(size[0]), sc(size[1])
    scale = min(target_w / source.width, target_h / source.height)
    resized = source.resize((int(source.width * scale), int(source.height * scale)), Image.Resampling.LANCZOS)
    out = Image.new("RGBA", (target_w, target_h), (0, 0, 0, 0))
    out.alpha_composite(resized, ((target_w - resized.width) // 2, (target_h - resized.height) // 2))
    return out


def real_capture_cover(crop, size):
    source = Image.open(SOURCE_CAPTURE).convert("RGBA").crop(crop)
    target_w, target_h = sc(size[0]), sc(size[1])
    scale = max(target_w / source.width, target_h / source.height)
    resized = source.resize((int(source.width * scale), int(source.height * scale)), Image.Resampling.LANCZOS)
    left = max(0, (resized.width - target_w) // 2)
    top = 0
    return resized.crop((left, top, left + target_w, top + target_h))


def add_scrim(img, alpha=120):
    overlay = Image.new("RGBA", img.size, (0, 0, 0, alpha))
    img.alpha_composite(overlay)


def draw_toggle(draw, x, y, on=True, scale=1.0):
    width = 42 * scale
    height = 24 * scale
    rounded(draw, (x, y, x + width, y + height), height / 2, c(COLORS["teal"] if on else "#94a3b8"))
    knob = height - 6 * scale
    kx = x + width - knob - 3 * scale if on else x + 3 * scale
    ellipse(draw, (kx, y + 3 * scale, kx + knob, y + 3 * scale + knob), c("#ffffff"))


def draw_browser_scene(draw, include_popup=True):
    # Browser shell
    shadow(canvas, (56, 42, 1224, 758), 22, blur=22, offset=(0, 13), alpha=34)
    rounded(draw, (56, 42, 1224, 758), 22, c(COLORS["paper"]), outline=c(COLORS["line"]))
    rounded(draw, (56, 42, 1224, 110), 22, c("#fbfcfd"))
    line(draw, (56, 110, 1224, 110), c(COLORS["line"]))
    for i, color in enumerate(["#ef6a5b", "#f4b740", "#3fb950"]):
        ellipse(draw, (84 + i * 22, 70, 96 + i * 22, 82), c(color))
    rounded(draw, (178, 63, 706, 89), 13, c("#eef3f7"), outline=c("#d8e1e8"))
    text(draw, (202, 69), "chatgpt.com/?temporary-chat=true", 12, c(COLORS["muted"]), "mono")
    rounded(draw, (732, 63, 836, 89), 13, c(COLORS["green_soft"]))
    text(draw, (784, 70), "Temporary", 12, c(COLORS["teal"]), "semibold", anchor="ma")

    # Sidebar
    rounded(draw, (56, 110, 304, 758), 0, c(COLORS["sidebar"]))
    text(draw, (90, 148), "ChatGPT", 21, c(COLORS["ink"]), "bold")
    rounded(draw, (86, 195, 258, 239), 11, c("#ffffff"), outline=c("#d7e1e8"))
    text(draw, (112, 207), "+ New chat", 15, c(COLORS["ink"]))
    text(draw, (90, 284), "Recent", 13, c(COLORS["muted"]), "semibold")
    rounded(draw, (86, 314, 258, 350), 10, c("#ffffff"))
    text(draw, (108, 323), "Temporary chat", 14, c(COLORS["ink"]), "semibold")
    for index, item in enumerate(["Draft ideas", "Research notes", "Weekly plan"]):
        text(draw, (108, 374 + index * 38), item, 14, c("#506995"))

    # Main ChatGPT-like surface
    text(draw, (384, 150), "Temporary Chat", 14, c(COLORS["muted"]), "semibold")
    rounded(draw, (904, 130, 1042, 164), 17, c("#f3f7f6"), outline=c("#cad8d5"))
    text(draw, (922, 139), "Temporary Chat", 12, c(COLORS["teal"]), "bold")
    rounded(draw, (798, 131, 884, 163), 16, c("#ffffff"), outline=c("#cad8d5"))
    text(draw, (816, 140), "Auto", 12, c(COLORS["ink"]), "bold")
    draw_toggle(draw, 850, 136, True, 0.72)

    text(draw, (384, 224), "Temporary Chat is ready", 34, c(COLORS["ink"]), "bold")
    text(draw, (386, 274), "New chats open with Temporary Chat enabled by default.", 17, c("#506995"))
    shadow(canvas, (382, 330, 876, 404), 14, blur=13, offset=(0, 8), alpha=15)
    rounded(draw, (382, 330, 876, 404), 14, c("#ffffff"), outline=c("#d8e1e8"))
    text(draw, (416, 354), "Ask anything without saving this conversation to history.", 17, c(COLORS["ink"]))
    rounded(draw, (382, 446, 612, 500), 12, c(COLORS["teal"]))
    text(draw, (497, 462), "temporary-chat=true", 15, c("#ffffff"), "bold", anchor="ma")
    rounded(draw, (626, 456, 734, 490), 17, c("#ffffff"), outline=c("#cad8d5"))
    text(draw, (652, 465), "Auto", 13, c(COLORS["ink"]), "bold")
    draw_toggle(draw, 686, 461, True, 0.72)

    if not include_popup:
        return

    # Extension popup overlay
    shadow(canvas, (902, 202, 1184, 502), 20, blur=24, offset=(0, 15), alpha=38)
    rounded(draw, (902, 202, 1184, 502), 20, c("#ffffff"), outline=c("#d8e1e8"))
    paste_icon(canvas, (930, 230), 42)
    text(draw, (986, 226), "Temp Chat Auto", 20, c(COLORS["ink"]), "bold")
    rounded(draw, (986, 258, 1044, 280), 11, c(COLORS["green_soft"]))
    text(draw, (1015, 263), "Saved", 11, c(COLORS["teal"]), "semibold", anchor="ma")
    rounded(draw, (930, 314, 1152, 386), 12, c("#f5f8fb"), outline=c("#d8e1e8"))
    text(draw, (950, 332), "Auto mode", 14, c(COLORS["ink"]), "semibold")
    text(draw, (950, 357), "Temporary by default", 13, c("#506995"))
    draw_toggle(draw, 1100, 338, True, 0.88)
    rounded(draw, (930, 420, 1152, 462), 10, c(COLORS["teal"]))
    text(draw, (1041, 431), "Apply now", 14, c("#ffffff"), "bold", anchor="ma")


def screenshot():
    canvas = real_capture((0, 0, 970, 606), (1280, 800))
    finalize(canvas, ASSET_DIR / "screenshot-1280x800.png")


def promo_small():
    img = real_capture((0, 0, 970, 617), (440, 280))
    d = ImageDraw.Draw(img)
    add_scrim(img, 108)
    grad = gradient(img.size, (0, 0, 0, 220), (0, 0, 0, 20))
    img.alpha_composite(grad)
    paste_icon(img, (28, 34), 44)
    text(d, (86, 34), "Temporary Chat Auto", 25, c("#ffffff"), "bold")
    text(d, (88, 76), "ChatGPT starts in", 16, c("#dbeafe"), "semibold")
    text(d, (88, 102), "Temporary Chat.", 16, c("#dbeafe"), "semibold")
    rounded(d, (28, 184, 246, 226), 12, c(COLORS["teal"]))
    text(d, (137, 196), "temporary-chat=true", 13, c("#ffffff"), "bold", anchor="ma")
    rounded(d, (284, 182, 392, 226), 15, (0, 0, 0, 162), outline=(255, 255, 255, 74))
    text(d, (306, 195), "Auto", 13, c("#ffffff"), "bold")
    draw_toggle(d, 348, 196, True, 0.64)
    finalize(img, ASSET_DIR / "promo-small-440x280.png")


def promo_marquee():
    img = Image.new("RGBA", (1400 * SCALE, 560 * SCALE), c("#050505"))
    d = ImageDraw.Draw(img)
    backdrop = real_capture_cover((0, 0, 970, 617), (1400, 560))
    backdrop = backdrop.filter(ImageFilter.GaussianBlur(sc(7)))
    img.alpha_composite(Image.blend(Image.new("RGBA", img.size, c("#050505")), backdrop, 0.26))
    add_scrim(img, 78)

    paste_icon(img, (84, 88), 72)
    text(d, (178, 88), "Temporary Chat Auto", 42, c("#ffffff"), "bold")
    text(d, (180, 156), "New ChatGPT conversations open in", 24, c("#dbeafe"), "semibold")
    text(d, (180, 192), "Temporary Chat by default.", 24, c("#dbeafe"), "semibold")
    rounded(d, (180, 262, 454, 316), 14, c(COLORS["teal"]))
    text(d, (317, 279), "temporary-chat=true", 17, c("#ffffff"), "bold", anchor="ma")

    shadow(img, (604, 48, 1328, 512), 24, blur=24, offset=(0, 16), alpha=72)
    panel = real_capture_contain((0, 0, 970, 606), (704, 440))
    panel_bg = Image.new("RGBA", panel.size, c("#000000"))
    panel_bg.alpha_composite(panel)
    mask = Image.new("L", panel.size, 0)
    md = ImageDraw.Draw(mask)
    md.rounded_rectangle((0, 0, panel.size[0] - 1, panel.size[1] - 1), radius=sc(18), fill=255)
    img.paste(panel_bg, (sc(614), sc(58)), mask)
    rounded(d, (614, 58, 1318, 498), 18, None, outline=(255, 255, 255, 72))

    finalize(img, ASSET_DIR / "promo-marquee-1400x560.png")


def icons():
    ICON_DIR.mkdir(parents=True, exist_ok=True)
    for size in (16, 32, 48, 128):
        app_icon(size).save(ICON_DIR / f"icon-{size}.png")


if __name__ == "__main__":
    icons()
    screenshot()
    promo_small()
    promo_marquee()
