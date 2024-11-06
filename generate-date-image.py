# This script generates a file containing current date and time, suitable for displaying on a small embedded device  
# Initially written for display on Squeezebox Touch 

from PIL import Image, ImageDraw, ImageFont
import datetime
import os
import argparse
import imagequant

# =======================
# Configuration Parameters
# =======================

# Day Mode Colors
DAY_BACKGROUND_COLOR = (135, 206, 235)  # Sky blue
DAY_TEXT_COLOR = (0, 0, 0)  # Black

# Night Mode Colors
NIGHT_BACKGROUND_COLOR = (0, 0, 0)  # Black
NIGHT_TEXT_COLOR = (0, 128, 255)  # Azure

# Default Mode
DEFAULT_MODE = 'day'

def optimize_png(input_file, output_file, quality=(50, 80), colors=8):
    """
    Optimizes a PNG image using imagequant library.
    
    Parameters:
    - input_file (str): Path to the input PNG file.
    - output_file (str): Path to the output PNG file.
    - quality (tuple): Tuple defining the min and max quality (1-100).
    - colors (int): Number of colors to reduce to (1-256).
    
    Returns:
    - bool: True if optimization was successful, False otherwise.
    """
    try:
        # Open input image
        input_image = Image.open(input_file)
        
        # Quantize the image
        output_image = imagequant.quantize_pil_image(
            input_image,
            dithering_level=1.0,     # Maximum dithering for best quality
            max_colors=colors,        # Number of colors to reduce to
            min_quality=quality[0],   # Minimum quality from tuple
            max_quality=quality[1]    # Maximum quality from tuple
        )
        
        # Save the optimized image
        output_image.save(output_file, format="PNG", optimize=True)
        return True
        
    except Exception as e:
        print("Error during optimization:", str(e))
        return False


def get_current_datetime():
    now = datetime.datetime.now()
    date_text = now.strftime("%a %d %b")
    time_text = now.strftime("%H:%M")
    return date_text, time_text

def create_background_image(width, height, color):
    return Image.new("RGB", (width, height), color=color)

def get_font(font_path, font_size):
    try:
        return ImageFont.truetype(font_path, font_size)
    except Exception as e:
        print(f"Error loading font '{font_path}': {e}")
        return ImageFont.load_default()

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

def generate_date_time_image(font_path, output_dir, mode='day'):
    # Image settings
    final_img_width, final_img_height = 480, 272
    img_width, img_height = final_img_width * 2, final_img_height * 2  # 4x larger
    font_size = 96  # Doubled from 48

    # Select colors based on mode
    if mode == 'night':
        background_color = NIGHT_BACKGROUND_COLOR
        text_color = NIGHT_TEXT_COLOR
    else:
        background_color = DAY_BACKGROUND_COLOR
        text_color = DAY_TEXT_COLOR

     # **Debug Print**
    # print(f"Mode: {mode}")
    # print(f"Background Color: {background_color}")
    # print(f"Text Color: {text_color}")
    
        
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
    output_path_tmp = os.path.join(output_dir, "date_time_initial.png")
    output_path = os.path.join(output_dir, "date_time.png")
 
    save_image(img_resized, output_path_tmp)

    # cut down on colors and size
    optimize_png(output_path_tmp, output_path, quality=(50, 80), colors=8)



def main():
    parser = argparse.ArgumentParser(description="Generate date and time image with day and night modes.")
    parser.add_argument('--night-mode', action='store_true', help='Force night mode regardless of the current time.')
    args = parser.parse_args()

    # Determine if night mode should be activated
    now = datetime.datetime.now()
    current_hour = now.hour

    # Night mode hours: 23 (11 PM) to 7 (7 AM)
    is_night_time = current_hour >= 23 or current_hour < 7

    # Activate night mode if either it's night time or the user has forced it via the flag
    if args.night_mode or is_night_time:
        active_mode = 'night'
    else:
        active_mode = 'day'
        
    font_path = "./Arima-VariableFont_wght.ttf"  # Ensure this is a thin/light font
    output_dir = "./output"
    generate_date_time_image(font_path, output_dir, mode=active_mode)

if __name__ == "__main__":
    main()

