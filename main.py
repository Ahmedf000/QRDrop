import qrcode
from colors.color import Colors
import os


def generate_qrcode_url(url):
    qr = qrcode.QRCode(
        version=1, #autosizing
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10, #box size is 10 for qrcode
        border=4, #writing spaces around the QRcode
    )
    """
    QR codes have built-in redundancy — they store extra data so that even if 
    part of the code is damaged, obscured, 
    or dirty, it can still be read.
    """
    qr.add_data(url)
    qr.make(fit=True)

    try:
        """Generate the image"""
        get_image = qr.make_image(fill_color="black", back_color="white")
        return get_image
    except Exception as e:
        print(Colors.red(f"[!] The image could not be generated {str(e)}"))
        return None



def add_logo_overlay(qr_image, logo_path):
    if not os.path.exists(logo_path):
        print(Colors.red(f"[!] The logo file not found: {logo_path}"))
        return qr_image

    from PIL import Image
    try:
        logo = Image.open(logo_path)
    except Exception as e:
        print(Colors.red(f"[!] Could not open the image {str(e)}"))

    """we gettin the QRcode image and resize the logo for 30% of it"""
    qr_width = qr_image.width
    qr_height = qr_image.height

    logo_resize = int(qr_width * 0.3)
    logo = logo.resize((logo_resize, logo_resize), Image.LANCZOS)
    #same height so only 1 calc, algorithm for high quality
    white_bg = Image.new("RGB", (logo_resize, logo_resize), ('white'))


    if logo.mode == "RGBA":
        white_bg.paste(logo, (0, 0), logo)
        logo = white_bg

    logo_x = (qr_width - logo_resize) // 2
    logo_y = (qr_height - logo_resize) // 2

    qr_image.paste(logo, (logo_x, logo_y))
    return qr_image



def add_text_label(qr_image, text, font_size):
    pass





def main():
    pass




if __name__ == "__main__":
    test_url = "https://www.google.com"
    qrcode = generate_qrcode_url(test_url)
    if qrcode:
        saved = qrcode.save("qrcode.png")
    logo = add_logo_overlay(qrcode, "C:\\Users\\21624\\PycharmProjects\\QRDrop\\wifi_PNG62252-3595169822.png")
    if logo:
        logo.save("logo.png")


