from wand.color import Color
from wand.drawing import Drawing
from wand.image import Image


out_width = 1920
out_height = 1080
patches = 32

with Image(width=out_width, height=out_height) as pat:
    # draw a black background
    with Drawing() as draw:
        draw.fill_color = Color.from_hsl(0, 0, 0)
        draw.rectangle(left=0, top=0, right=out_width, bottom=out_height)
        draw(pat)

    patch_space_w = int(out_width / patches)
    patch_margin_w = int(patch_space_w * 0.1)
    patch_w = patch_space_w - 2 * patch_margin_w

    patch_space_h = int(out_height / 4)
    patch_margin_h = int(patch_space_h * 0.1)
    patch_h = patch_space_h - 2 * patch_margin_h

    print(f"patch width is {patch_w} with {patch_margin_w} margin")
    print(f"patch height is {patch_h} with {patch_margin_h} margin")

    channels = [
        (1, 1, 1),  # white
        (1, 0, 0),  # red
        (0, 1, 0),  # green
        (0, 0, 1),  # blue
    ]
    for row in range(0, 4):
        channel = channels[row]
        for i in range(0, patches):
            with Drawing() as draw:
                intensity = i / 256.0
                r, g, b = (c * intensity for c in channel)
                draw.fill_color = Color(f"device-rgb({r},{g},{b})")
                patch_left = i * patch_space_w + patch_margin_w
                patch_right = i * patch_space_w + patch_margin_w + patch_w
                patch_top = row * (patch_space_h) + patch_margin_h
                patch_bottom = row * (patch_space_h) + patch_margin_h + patch_h
                draw.rectangle(
                    left=patch_left,
                    top=patch_top,
                    right=patch_right,
                    bottom=patch_bottom,
                )
                draw(pat)

                # use bold arial font to draw the intensity*256 value
                # in the top middle of the patch
                draw.font = "Arial-Bold"
                draw.font_size = 24
                text_intensity = (1 - intensity)*0.2
                r, g, b = (c * text_intensity for c in channel)
                draw.fill_color = Color(f"device-rgb({r},{g},{b})")
                draw.text_alignment = "center"
                # format the intensity value as an integer
                patch_label = f"{int(intensity*256)}"
                draw.text(
                    patch_left + int(patch_w / 2),
                    patch_top + patch_margin_h,
                    patch_label,
                )
                draw(pat)

    pat.save(filename="PNG48:testpat.png")
