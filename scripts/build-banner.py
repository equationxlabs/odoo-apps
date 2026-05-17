#!/usr/bin/env python3
"""
Build the OdooPilot marketplace banner — static PNG (frame B) and an
animated GIF cycling through three scenes (B → C → D → loop).

Output:
    static/description/icon.png    — static frame B (for fallback / icon)
    static/description/banner.gif  — animated 3-scene banner (10s loop)
"""

from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 880, 440
OUT_DIR = "/Users/muralik/projects/equationx-odoo-apps/pilot_for_odoo_setup/static/description"

# ----------------------------- font loader ------------------------------------

def font(size, bold=True):
    """Try a few system fonts. Fall back gracefully."""
    candidates = [
        ("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 0),
        ("/System/Library/Fonts/Helvetica.ttc", 1 if bold else 0),
        ("/System/Library/Fonts/SFNS.ttf", 0),
        ("/Library/Fonts/Arial Bold.ttf", 0),
    ]
    for path, index in candidates:
        try:
            return ImageFont.truetype(path, size, index=index)
        except (OSError, IOError):
            continue
    return ImageFont.load_default()


def font_regular(size):
    for path in [
        "/System/Library/Fonts/SFNS.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
        "/Library/Fonts/Arial.ttf",
    ]:
        try:
            return ImageFont.truetype(path, size)
        except (OSError, IOError):
            continue
    return ImageFont.load_default()


def text_width(draw, text, fnt):
    bbox = draw.textbbox((0, 0), text, font=fnt)
    return bbox[2] - bbox[0]


def draw_sparkle(img, cx, cy, arm_long, arm_short, color):
    """Two interlocking diamonds = 4-point Claude-style sparkle."""
    draw = ImageDraw.Draw(img)
    draw.polygon(
        [
            (cx, cy - arm_long),
            (cx + arm_short, cy),
            (cx, cy + arm_long),
            (cx - arm_short, cy),
        ],
        fill=color,
    )
    draw.polygon(
        [
            (cx - arm_long, cy),
            (cx, cy - arm_short),
            (cx + arm_long, cy),
            (cx, cy + arm_short),
        ],
        fill=color,
    )


# =============================================================================
# Frame B — "Connect Claude Desktop to your Odoo CRM" + feature pills
# =============================================================================

def make_frame_b():
    img = Image.new("RGB", (W, H), (37, 99, 235))  # #2563eb
    draw = ImageDraw.Draw(img)

    # eyebrow
    draw.text(
        (48, 56),
        "FREE  ·  LGPL-3  ·  BY EQUATIONX",
        font=font_regular(15),
        fill=(191, 219, 254),
    )

    # headline lines
    h1 = font(46)
    draw.text((48, 96), "Connect Claude Desktop", font=h1, fill=(255, 255, 255))
    draw.text((48, 154), "to your Odoo CRM.", font=h1, fill=(191, 219, 254))

    # feature pills
    pill_font = font(18)
    pills = ["2-click setup", "Any MCP client", "2FA-ready", "CE 17 + 18"]
    x = 48
    for label in pills:
        tw = text_width(draw, label, pill_font)
        pill_w = tw + 50
        draw.rounded_rectangle(
            (x, 282, x + pill_w, 332),
            radius=25,
            fill=(255, 255, 255),
        )
        draw.text(
            (x + 25, 293),
            label,
            font=pill_font,
            fill=(29, 78, 216),  # #1d4ed8
        )
        x += pill_w + 14

    # tagline
    draw.text(
        (48, 372),
        "From the makers of OdooPilot",
        font=font_regular(17),
        fill=(219, 234, 254),
    )
    return img


# =============================================================================
# Frame C — "Stop building reports. Start asking your Odoo."
# =============================================================================

def make_frame_c():
    img = Image.new("RGB", (W, H), (250, 250, 250))  # #fafafa
    draw = ImageDraw.Draw(img)

    # eyebrow
    draw.text(
        (48, 56),
        "ODOO MCP CONNECTOR  ·  FREE",
        font=font_regular(15),
        fill=(113, 113, 122),
    )

    # headline — two pairs, vertically stacked
    big = font(58)
    draw.text((48, 92), "Stop building", font=big, fill=(10, 10, 10))
    draw.text((48, 156), "reports.", font=big, fill=(10, 10, 10))
    draw.text((48, 224), "Start asking", font=big, fill=(37, 99, 235))
    draw.text((48, 288), "your Odoo.", font=big, fill=(37, 99, 235))

    # big sparkle in upper-right + small satellite
    draw_sparkle(img, cx=720, cy=140, arm_long=46, arm_short=12, color=(37, 99, 235))
    draw_sparkle(img, cx=800, cy=80, arm_long=12, arm_short=4, color=(37, 99, 235))

    # footer
    draw.text(
        (48, 388),
        "By equationx, makers of OdooPilot",
        font=font_regular(15),
        fill=(113, 113, 122),
    )
    return img


# =============================================================================
# Frame D — "Two clicks. Then ask anything." + 3 numbered step cards
# =============================================================================

def make_frame_d():
    img = Image.new("RGB", (W, H), (15, 23, 42))  # #0f172a
    draw = ImageDraw.Draw(img)

    # eyebrow
    draw.text(
        (48, 56),
        "SETUP WIZARD  ·  FREE",
        font=font_regular(15),
        fill=(96, 165, 250),
    )

    # headline
    big = font(46)
    draw.text((48, 96), "Two clicks.", font=big, fill=(255, 255, 255))
    draw.text((48, 152), "Then ask anything.", font=big, fill=(96, 165, 250))

    # three step cards
    card_y = 226
    card_h = 142
    cards = [
        ("1", "Install in Odoo", "Apps → MCP Connector"),
        ("2", "Generate API key", "One click in the wizard"),
        ("3", "Paste config", "Into Claude Desktop"),
    ]
    gap = 16
    total_w = W - 96  # 48 padding each side
    card_w = (total_w - 2 * gap) // 3
    x = 48
    num_font = font(42)
    title_font = font(17)
    sub_font = font_regular(13)
    for n, title, sub in cards:
        # card bg
        draw.rounded_rectangle(
            (x, card_y, x + card_w, card_y + card_h),
            radius=14,
            fill=(30, 58, 138),
        )
        # number
        nw = text_width(draw, n, num_font)
        draw.text((x + (card_w - nw) / 2, card_y + 14), n, font=num_font, fill=(96, 165, 250))
        # title
        tw = text_width(draw, title, title_font)
        draw.text((x + (card_w - tw) / 2, card_y + 70), title, font=title_font, fill=(255, 255, 255))
        # subtitle
        sw = text_width(draw, sub, sub_font)
        draw.text((x + (card_w - sw) / 2, card_y + 95), sub, font=sub_font, fill=(191, 219, 254))
        x += card_w + gap

    # footer
    draw.text(
        (48, 392),
        "By equationx, makers of OdooPilot  ·  Odoo CE 17 + 18",
        font=font_regular(13),
        fill=(148, 163, 184),
    )
    return img


# =============================================================================
# Assembly
# =============================================================================

def main():
    print("Rendering scenes...")
    b = make_frame_b()
    c = make_frame_c()
    d = make_frame_d()

    # Save individual frames for inspection
    b.save(f"{OUT_DIR}/icon.png", "PNG", optimize=True)
    b.save(f"{OUT_DIR}/banner-b.png", "PNG", optimize=True)
    c.save(f"{OUT_DIR}/banner-c.png", "PNG", optimize=True)
    d.save(f"{OUT_DIR}/banner-d.png", "PNG", optimize=True)
    print(f"  icon.png   = scene B (static fallback)")
    print(f"  banner-b/c/d.png written")

    # Build animated GIF: B (2.4s) → fade → C (2.4s) → fade → D (2.4s) → fade → loop
    frames = []
    durations = []  # ms per frame
    hold = 2400       # ms each scene is held
    transition_steps = 6
    transition_ms = 70  # per fade frame

    def transition_into(prev, nxt):
        for i in range(1, transition_steps + 1):
            alpha = i / (transition_steps + 1)
            yield Image.blend(prev, nxt, alpha)

    scenes = [b, c, d]
    for i, scene in enumerate(scenes):
        frames.append(scene)
        durations.append(hold)
        next_scene = scenes[(i + 1) % len(scenes)]
        for inter in transition_into(scene, next_scene):
            frames.append(inter)
            durations.append(transition_ms)

    # Save GIF
    gif_path = f"{OUT_DIR}/banner.gif"
    frames[0].save(
        gif_path,
        save_all=True,
        append_images=frames[1:],
        duration=durations,
        loop=0,
        optimize=True,
        disposal=2,
    )
    import os
    size_kb = os.path.getsize(gif_path) / 1024
    print(f"\nWrote {gif_path}  ({size_kb:.0f} KB, {len(frames)} frames)")


if __name__ == "__main__":
    main()
