from ascii_magic import AsciiArt
from PIL import Image, ImageEnhance
import sys
from pathlib import Path

# ------------------ USER CONFIGURATION ------------------
DEFAULT_COLUMNS = 180       # higher = more horizontal detail
DEFAULT_CHAR_SET = " .'`^\",:;Il!i~+_-?][}{1)(|\\/*tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"
DEFAULT_MONOCHROME = True   # True = no color, cleaner
ENHANCE_CONTRAST = 1.5      # 1.0 = original, higher = sharper ASCII
# --------------------------------------------------------


def main():
    if len(sys.argv) < 2:
        print("Usage: python ascii_convert_detailed.py <image_path>")
        sys.exit(1)

    image_path = Path(sys.argv[1])

    if not image_path.exists():
        print(f"File not found: {image_path}")
        sys.exit(1)

    # Step 1 — open image with Pillow
    img = Image.open(image_path)

    # Step 2 — optional contrast enhancement for more detail
    if ENHANCE_CONTRAST != 1.0:
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(ENHANCE_CONTRAST)

    # Step 3 — create ASCII art object from Pillow image
    art = AsciiArt.from_pillow_image(img)

    # Step 4 — print ASCII to terminal with detailed settings
    art.to_terminal(
        columns=DEFAULT_COLUMNS,
        char=DEFAULT_CHAR_SET,
        monochrome=DEFAULT_MONOCHROME
    )

    # Step 5 — save ASCII output to text file
    output_path = image_path.with_suffix(".txt")
    ascii_string = art.to_ascii(
        columns=DEFAULT_COLUMNS,
        char=DEFAULT_CHAR_SET,
        monochrome=DEFAULT_MONOCHROME
    )

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(ascii_string)

    print(f"\nASCII conversion complete! Saved to: {output_path}")
    print(f"Columns     : {DEFAULT_COLUMNS}")
    print(f"Monochrome  : {DEFAULT_MONOCHROME}")
    print(f"Char set length: {len(DEFAULT_CHAR_SET)}")
    print(f"Contrast enhancer: {ENHANCE_CONTRAST}")


if __name__ == "__main__":
    main()
