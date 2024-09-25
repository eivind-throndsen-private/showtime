from PIL import Image, ImageDraw, ImageFilter
import datetime
import os
import math
import argparse

# =======================
# Configuration Parameters
# =======================

# Day Mode Colors
DAY_BACKGROUND_COLOR = (230, 240, 250)      # Very light, subtle pale sky blue
DAY_OUTER_RING_FILL = "lightgray"
DAY_OUTER_RING_OUTLINE = "darkgray"
DAY_INNER_CLOCK_FACE_FILL = "white"
DAY_INNER_CLOCK_FACE_OUTLINE = "gray"
DAY_HOUR_HAND_COLOR = "black"
DAY_MINUTE_HAND_COLOR = "black"
DAY_TICK_MARK_COLOR = "black"
DAY_CENTER_CIRCLE_COLOR = '#C23132'       # Red circle at center

# Night Mode Colors
NIGHT_BACKGROUND_COLOR = (0, 0, 0)         # Black
NIGHT_OUTER_RING_FILL = (66, 66, 66)    # Subtle dark gray
NIGHT_OUTER_RING_OUTLINE = (66, 66, 66)    # Subtle dark gray
NIGHT_INNER_CLOCK_FACE_FILL = (0, 0, 0)    # Black
NIGHT_INNER_CLOCK_FACE_OUTLINE = (66, 66, 66)  # Subtle dark gray
NIGHT_HOUR_HAND_COLOR = (66, 66, 66)       # Subtle dark gray
NIGHT_MINUTE_HAND_COLOR = (66, 66, 66)     # Subtle dark gray
NIGHT_TICK_MARK_COLOR = (66, 66, 66)       # Subtle dark gray
NIGHT_CENTER_CIRCLE_COLOR = (66, 66, 66)   # Subtle dark gray

# Default Mode (True for Night Mode, False for Day Mode)
DEFAULT_MODE = 'day'

# Aspect Ratio
ASPECT_RATIO_WIDTH = 16
ASPECT_RATIO_HEIGHT = 9

# =======================
# Helper Functions
# =======================

def polar_to_cartesian(center_x, center_y, radius, angle_degrees):
    angle_radians = math.radians(angle_degrees)
    x = center_x + radius * math.cos(angle_radians)
    y = center_y + radius * math.sin(angle_radians)
    return x, y

def get_hand_coordinates(center_x, center_y, length, angle_degrees, base_width, tip_width, stick_out, hand_color):
    angle_radians = math.radians(angle_degrees)
    angle_perp = angle_radians + math.pi / 2  # Perpendicular angle

    # Tip of the hand
    x_tip = center_x + length * math.cos(angle_radians)
    y_tip = center_y + length * math.sin(angle_radians)

    # Base of the hand (considering stick_out)
    x_base = center_x - stick_out * math.cos(angle_radians)
    y_base = center_y - stick_out * math.sin(angle_radians)

    # Left and right positions at the base
    x_base_left = x_base + (base_width / 2) * math.cos(angle_perp)
    y_base_left = y_base + (base_width / 2) * math.sin(angle_perp)
    x_base_right = x_base - (base_width / 2) * math.cos(angle_perp)
    y_base_right = y_base - (base_width / 2) * math.sin(angle_perp)

    # Left and right positions at the tip
    x_tip_left = x_tip + (tip_width / 2) * math.cos(angle_perp)
    y_tip_left = y_tip + (tip_width / 2) * math.sin(angle_perp)
    x_tip_right = x_tip - (tip_width / 2) * math.cos(angle_perp)
    y_tip_right = y_tip - (tip_width / 2) * math.sin(angle_perp)

    # Return the coordinates in order to make a polygon
    return [
        (x_base_left, y_base_left),
        (x_tip_left, y_tip_left),
        (x_tip_right, y_tip_right),
        (x_base_right, y_base_right),
    ]

def draw_marker(draw, angle_degrees, outer_radius, inner_radius, width, center_x, center_y, tick_color):
    angle_radians = math.radians(angle_degrees)
    angle_perp = angle_radians + math.pi / 2  # Perpendicular angle
    x_outer = center_x + outer_radius * math.cos(angle_radians)
    y_outer = center_y + outer_radius * math.sin(angle_radians)
    x_inner = center_x + inner_radius * math.cos(angle_radians)
    y_inner = center_y + inner_radius * math.sin(angle_radians)
    x_outer_left = x_outer + (width / 2) * math.cos(angle_perp)
    y_outer_left = y_outer + (width / 2) * math.sin(angle_perp)
    x_outer_right = x_outer - (width / 2) * math.cos(angle_perp)
    y_outer_right = y_outer - (width / 2) * math.sin(angle_perp)
    x_inner_left = x_inner + (width / 2) * math.cos(angle_perp)
    y_inner_left = y_inner + (width / 2) * math.sin(angle_perp)
    x_inner_right = x_inner - (width / 2) * math.cos(angle_perp)
    y_inner_right = y_inner - (width / 2) * math.sin(angle_perp)
    coords = [
        (x_outer_left, y_outer_left),
        (x_inner_left, y_inner_left),
        (x_inner_right, y_inner_right),
        (x_outer_right, y_outer_right),
    ]
    draw.polygon(coords, fill=tick_color)

def create_swiss_clock_image(width=480, mode='day'):
    scale_factor = 4  # Drawing at higher resolution
    # Width and height for drawing
    width_draw = width * scale_factor
    aspect_ratio = ASPECT_RATIO_WIDTH / ASPECT_RATIO_HEIGHT
    height_draw = int(width_draw / aspect_ratio)
    center_x = width_draw // 2
    center_y = height_draw // 2
    clock_radius = int(min(width_draw, height_draw) * 0.40)

    # Define the unit scale (units to pixels)
    # According to measurements, outer edge of tickmarks at 49.5 units
    unit_scale = clock_radius / 49.5

    # Select colors based on mode
    if mode == 'night':
        BACKGROUND_COLOR = NIGHT_BACKGROUND_COLOR
        OUTER_RING_FILL = NIGHT_OUTER_RING_FILL
        OUTER_RING_OUTLINE = NIGHT_OUTER_RING_OUTLINE
        INNER_CLOCK_FACE_FILL = NIGHT_INNER_CLOCK_FACE_FILL
        INNER_CLOCK_FACE_OUTLINE = NIGHT_INNER_CLOCK_FACE_OUTLINE
        HOUR_HAND_COLOR = NIGHT_HOUR_HAND_COLOR
        MINUTE_HAND_COLOR = NIGHT_MINUTE_HAND_COLOR
        TICK_MARK_COLOR = NIGHT_TICK_MARK_COLOR
        CENTER_CIRCLE_COLOR = NIGHT_CENTER_CIRCLE_COLOR
    else:
        BACKGROUND_COLOR = DAY_BACKGROUND_COLOR
        OUTER_RING_FILL = DAY_OUTER_RING_FILL
        OUTER_RING_OUTLINE = DAY_OUTER_RING_OUTLINE
        INNER_CLOCK_FACE_FILL = DAY_INNER_CLOCK_FACE_FILL
        INNER_CLOCK_FACE_OUTLINE = DAY_INNER_CLOCK_FACE_OUTLINE
        HOUR_HAND_COLOR = DAY_HOUR_HAND_COLOR
        MINUTE_HAND_COLOR = DAY_MINUTE_HAND_COLOR
        TICK_MARK_COLOR = DAY_TICK_MARK_COLOR
        CENTER_CIRCLE_COLOR = DAY_CENTER_CIRCLE_COLOR

    # Create the image
    image = Image.new("RGB", (width_draw, height_draw), BACKGROUND_COLOR)

    # Create a drawing object
    draw = ImageDraw.Draw(image)

    # Draw steel frame ring (outer circle)
    outer_radius = clock_radius + 75
    bounding_box = [
        center_x - outer_radius,
        center_y - outer_radius,
        center_x + outer_radius,
        center_y + outer_radius,
    ]
    draw.ellipse(bounding_box, fill=OUTER_RING_FILL, outline=OUTER_RING_OUTLINE, width=4 * scale_factor)

    # Draw inner clock face
    inner_radius = int(clock_radius * 0.95) + 50
    bounding_box = [
        center_x - inner_radius,
        center_y - inner_radius,
        center_x + inner_radius,
        center_y + inner_radius,
    ]
    draw.ellipse(bounding_box, fill=INNER_CLOCK_FACE_FILL, outline=INNER_CLOCK_FACE_OUTLINE)

    # Draw hour markers as rectangles
    for hour in range(12):
        angle_degrees = (hour / 12.0) * 360.0 - 90
        outer_radius_marker = unit_scale * 49.5 * 0.95  # Adjusted outer radius for markers
        inner_radius_marker = outer_radius_marker - unit_scale * 11  # Hour markers are 11 units long
        marker_width = unit_scale * 3  # Hour marker width is 3 units
        draw_marker(draw, angle_degrees, outer_radius_marker, inner_radius_marker, marker_width, center_x, center_y, TICK_MARK_COLOR)

    # Draw minute markers as rectangles
    for minute in range(60):
        if minute % 5 == 0:
            continue  # Skip the hour markers
        angle_degrees = (minute / 60.0) * 360.0 - 90
        outer_radius_marker = unit_scale * 49.5 * 0.95
        inner_radius_marker = outer_radius_marker - unit_scale * 3.2  # Minute markers are 3.2 units long
        marker_width = unit_scale * 1.2  # Minute marker width is 1.2 units
        draw_marker(draw, angle_degrees, outer_radius_marker, inner_radius_marker, marker_width, center_x, center_y, TICK_MARK_COLOR)

    # Get current time
    now = datetime.datetime.now()
    hour = now.hour % 12
    minute = now.minute

    # Calculate angles
    hour_angle = (hour + minute / 60.0) * 30.0 - 90
    minute_angle = minute * 6.0 - 90

    # Draw hour hand as a polygon
    # Using measurements for hour hand: 32 units in the direction of the hour, 12 units in the opposite
    hour_hand_length = unit_scale * 32
    hour_hand_stickout = unit_scale * 12
    base_width = unit_scale * 6  # From original hand parameters
    tip_width = unit_scale * 4.5

    hour_hand_coords = get_hand_coordinates(
        center_x, center_y, hour_hand_length, hour_angle, base_width, tip_width, hour_hand_stickout, HOUR_HAND_COLOR
    )

    draw.polygon(hour_hand_coords, fill=HOUR_HAND_COLOR)

    # Draw minute hand as a polygon
    # Using measurements for minute hand: 46 units in the direction of the minute, 12 units in the opposite
    minute_hand_length = unit_scale * 46
    minute_hand_stickout = unit_scale * 12
    base_width = unit_scale * 5.7
    tip_width = unit_scale * 3.5

    minute_hand_coords = get_hand_coordinates(
        center_x, center_y, minute_hand_length, minute_angle, base_width, tip_width, minute_hand_stickout, MINUTE_HAND_COLOR
    )

    draw.polygon(minute_hand_coords, fill=MINUTE_HAND_COLOR)

    # Draw center circle
    center_circle_radius = unit_scale * 1.5
    bounding_box = [
        center_x - center_circle_radius,
        center_y - center_circle_radius,
        center_x + center_circle_radius,
        center_y + center_circle_radius,
    ]
    draw.ellipse(bounding_box, fill=CENTER_CIRCLE_COLOR)

    # Downscale the image to desired size using a high-quality resampling filter
    image = image.resize((width, int(width / aspect_ratio)), Image.LANCZOS)

    # Ensure the output directory exists
    output_dir = "./output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Save the image
    mode_suffix = "_night" if mode == 'night' else "_day"
    output_path = os.path.join(output_dir, f"swiss-clock.png")
    image = image.convert('RGB')  # Convert back to RGB if not saving with transparency
    image.save(output_path)

    print(f"Saved clock image to '{output_path}'.")

# =======================
# Main Execution
# =======================

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a Swiss clock image with day and night modes.")
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

    create_swiss_clock_image(mode=active_mode)
