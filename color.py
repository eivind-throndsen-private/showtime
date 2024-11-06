import colorsys

def rgb_to_hsl(r, g, b):
    """Convert RGB to HSL."""
    # Normalize RGB values to 0-1 range for colorsys
    r, g, b = r / 255.0, g / 255.0, b / 255.0
    return colorsys.rgb_to_hls(r, g, b)

def hsl_to_rgb(h, l, s):
    """Convert HSL back to RGB."""
    r, g, b = colorsys.hls_to_rgb(h, l, s)
    # Convert back to 0-255 range
    return int(r * 255), int(g * 255), int(b * 255)

def adjust_lightness(rgb_color, lightness_increase=0.1):
    """Increase the lightness of an RGB color."""
    r, g, b = rgb_color
    # Convert RGB to HSL
    h, l, s = rgb_to_hsl(r, g, b)
    
    # Increase lightness by the given amount, ensuring it stays in the [0, 1] range
    l = min(1.0, l + lightness_increase)
    
    # Convert back to RGB
    return hsl_to_rgb(h, l, s)

# Define your color tuple as a variable
original_color = (66, 66, 66)  # Dark gray

# Adjust lightness (0.1 is a small increase, you can adjust this value)
lighter_color = adjust_lightness(original_color, lightness_increase=0.2)

print(f"Original color: {original_color}")
print(f"Lighter color: {lighter_color}")
