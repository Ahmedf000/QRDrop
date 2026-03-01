import qrcode
from colors.color import Colors
import os


def generate_qrcode_url(url):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=20,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)

    try:
        get_image = qr.make_image(fill_color="black", back_color="white")
        get_image = get_image.convert('RGB')
        return get_image
    except Exception as e:
        print(Colors.red(f"[!] Image generation failed: {str(e)}"))
        return None


def add_logo_overlay(qr_image, logo_path):
    if not os.path.exists(logo_path):
        print(Colors.red(f"[!] Logo file not found: {logo_path}"))
        return qr_image

    from PIL import Image

    try:
        logo = Image.open(logo_path)
        if logo.mode in ('P', 'PA'):  # Fixing palette warning
            logo = logo.convert('RGBA')
    except Exception as e:
        print(Colors.red(f"[!] Could not open image: {str(e)}"))
        return qr_image

    qr_width = qr_image.width
    qr_height = qr_image.height

    if qr_width != qr_height:
        print(Colors.yellow(f"[!] QR not square: {qr_width}x{qr_height}, fixing..."))
        size = max(qr_width, qr_height)
        qr_image = qr_image.resize((size, size), Image.LANCZOS)
        qr_width = qr_height = size

    print(Colors.cyan(f"[*] QR size: {qr_width}x{qr_height}"))

    logo_resize = int(qr_width * 0.25)
    padding = int(qr_height * 0.05)
    logo = logo.resize((logo_resize, logo_resize), Image.LANCZOS)
    print(Colors.cyan(f"[*] Logo resized to: {logo_resize}x{logo_resize}"))

    bg_size = logo_resize + (padding * 2)
    white_bg = Image.new("RGB", (bg_size, bg_size), 'white')

    logo_pos = ((bg_size - logo_resize) // 2, (bg_size - logo_resize) // 2)

    if logo.mode == "RGBA":
        white_bg.paste(logo, logo_pos, logo)
    else:
        white_bg.paste(logo, logo_pos)

    logo = white_bg

    logo_x = (qr_width - bg_size) // 2
    logo_y = (qr_height - bg_size) // 2

    qr_image.paste(logo, (logo_x, logo_y))
    print(Colors.green("[+] Logo pasted onto QR code"))

    return qr_image


def add_text_label(qr_image, text, font_size):
    pass


def main():
    pass


if __name__ == "__main__":


    test_url = "https://www.google.com"
    qr_img = generate_qrcode_url(test_url)

    if qr_img:
        print(f"QR dimensions: {qr_img.width}x{qr_img.height}")
        print(f"QR mode: {qr_img.mode}")

        qr_img.save("qrcode_plain.png")

        qr_with_logo = add_logo_overlay(qr_img, "wifi_PNG62252-3595169822.png")
        qr_with_logo.save("qrcode_with_logo.png")
        print(Colors.green("[+] Done!"))