from PIL import Image, ImageDraw, ImageFont
import datetime
import os

def get_current_datetime():
    now = datetime.datetime.now()
    date_text = now.strftime("%a %d %b")
    time_text = now.strftime("%H:%M")
    return date_text, time_text

def create_background_image(width, height, color):
    return Image.new("RGB", (width, height), color=color)

def get_font(font_path, font_size):
    return ImageFont.truetype(font_path, font_size)

def calculate_text_position(draw, text, font, img_width, img_height, y_offset):
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    x = (img_width - text_width) / 2
    y = y_offset
    return x, y

def draw_text_on_image(draw, text, position, font, fill):
    draw.text(position, text, fill=fill, font=font)

def ensure_output_directory(output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

def save_image(img, output_path):
    img.save(output_path)
    print(f"Saved date / time to '{output_path}'.")

def generate_date_time_image(font_path, output_dir):
    # Image settings
    final_img_width, final_img_height = 480, 272
    img_width, img_height = final_img_width * 2, final_img_height * 2  # 4x larger
    background_color = (135, 206, 235)  # Sky blue
    font_size = 96  # Doubled from 48
    text_color = (0, 0, 0)  # Black

    # Get current date and time
    date_text, time_text = get_current_datetime()

    # Create image and drawing context
    img = create_background_image(img_width, img_height, background_color)
    draw = ImageDraw.Draw(img)

    # Set up font
    font = get_font(font_path, font_size)

    # Calculate and draw text positions
    date_pos = calculate_text_position(draw, date_text, font, img_width, img_height, 140)  # Doubled from 70
    time_pos = calculate_text_position(draw, time_text, font, img_width, img_height, 280)  # Doubled from 140
    draw_text_on_image(draw, date_text, date_pos, font, text_color)
    draw_text_on_image(draw, time_text, time_pos, font, text_color)

    # Resize the image
    img_resized = img.resize((final_img_width, final_img_height), Image.LANCZOS)

    # Ensure output directory exists and save image
    ensure_output_directory(output_dir)
    output_path = os.path.join(output_dir, "date_time.png")
    save_image(img_resized, output_path)

def main():
    font_path = "./Arima-VariableFont_wght.ttf"  # Ensure this is a thin/light font
    output_dir = "./output"
    generate_date_time_image(font_path, output_dir)

if __name__ == "__main__":
    main()
