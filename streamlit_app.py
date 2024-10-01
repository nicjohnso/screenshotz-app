import streamlit as st
import pyautogui
from PIL import Image, ImageDraw, ImageFilter
import random
import numpy as np
import colorsys

# Function to generate analogous or complementary colors based on a base color
def generate_harmonious_colors(scheme='analogous', num_colors=5):
    # Randomly select a base hue (value between 0 and 1)
    base_hue = random.random()
    colors = []

    # Generate colors in HSL, then convert to RGB
    for i in range(num_colors):
        if scheme == 'analogous':
            # For analogous, slightly shift the hue
            hue = (base_hue + (i * 0.1)) % 1.0
        elif scheme == 'complementary':
            # For complementary, alternate between base hue and complement
            hue = (base_hue + (i % 2) * 0.5) % 1.0  # Shift by 180 degrees (0.5 in HSL)
        
        # Convert HSL (Hue, Saturation, Lightness) to RGB
        rgb = colorsys.hls_to_rgb(hue, 0.6, 0.7)  # Fixed saturation and lightness
        # Convert to 8-bit RGB
        rgb = tuple(int(x * 255) for x in rgb)
        colors.append(rgb)
    
    return colors

# Function to create a background with mixed colors in a swirl pattern
def create_attractive_background(width, height, color_scheme='analogous', num_colors=5, blur_radius=20):
    # Generate harmonious colors (either analogous or complementary)
    colors = generate_harmonious_colors(scheme=color_scheme, num_colors=num_colors)

    # Create an empty image
    background = Image.new("RGB", (width, height))

    # Create a swirl pattern by drawing circles with random colors and positions
    draw = ImageDraw.Draw(background)

    for _ in range(300):  # Draw 300 random circles
        color = random.choice(colors)
        # Random position and size of circles
        radius = random.randint(50, 200)
        x = random.randint(0, width)
        y = random.randint(0, height)
        # Draw an ellipse (circle-like shape)
        draw.ellipse((x - radius, y - radius, x + radius, y + radius), fill=color)

    # Apply a swirl pattern effect (a rudimentary swirl effect using numpy)
    # Convert the image to a numpy array for manipulation
    img_array = np.array(background)
    
    # Random shifts to create a swirl-like effect
    center_x, center_y = width // 2, height // 2
    for i in range(height):
        for j in range(width):
            offset_x = int(30 * np.sin(2 * np.pi * (i / height)))
            offset_y = int(30 * np.cos(2 * np.pi * (j / width)))
            if 0 <= i + offset_x < height and 0 <= j + offset_y < width:
                img_array[i, j] = img_array[i + offset_x, j + offset_y]

    # Convert back to an image
    swirl_background = Image.fromarray(img_array)

    # Apply a blur to smooth the color transitions
    blurred_background = swirl_background.filter(ImageFilter.GaussianBlur(blur_radius))

    return blurred_background

# Function to add a thin black border around the screenshot
def add_border_to_screenshot(screenshot, border_size=5):
    # Calculate the new image size with the border
    new_width = screenshot.width + 2 * border_size
    new_height = screenshot.height + 2 * border_size

    # Create a new image with a black background (border)
    bordered_image = Image.new("RGB", (new_width, new_height), "black")

    # Paste the original screenshot onto the black background (centered)
    bordered_image.paste(screenshot, (border_size, border_size))

    return bordered_image

# Function to add a background based on the screenshot size
def add_background_to_screenshot(screenshot, color_scheme='analogous'):
    # Get the screenshot dimensions
    screenshot_with_border = add_border_to_screenshot(screenshot)

    # Create an attractive background image based on the screenshot size
    background_image = create_attractive_background(screenshot_with_border.width, screenshot_with_border.height, color_scheme=color_scheme)

    # Calculate position to center the screenshot on the background
    x_offset = (background_image.width - screenshot_with_border.width) // 2
    y_offset = (background_image.height - screenshot_with_border.height) // 2

    # Paste the screenshot with the border onto the background
    background_image.paste(screenshot_with_border, (x_offset, y_offset))

    return background_image

# Streamlit app title
st.title("Screenshot Capture App with Harmonious Artistic Background and Border")

# Let user choose the color scheme
color_scheme = st.selectbox("Select Color Scheme", options=['analogous', 'complementary'])

# Button to capture screenshot
if st.button("Take Screenshot"):
    # Capture the screenshot
    screenshot = pyautogui.screenshot()

    # Add attractive background with color swirl and blur, based on the selected color scheme
    background_image = add_background_to_screenshot(screenshot, color_scheme=color_scheme)

    # Save the screenshot with background to a BytesIO object
    img_buffer = io.BytesIO()
    background_image.save(img_buffer, format="PNG")
    img_buffer.seek(0)

    # Display the screenshot with background in the Streamlit app
    st.image(background_image, caption=f"Screenshot with {color_scheme.capitalize()} Background and Border", use_column_width=True)

    # Provide a download link for the screenshot with background
    st.download_button(
        label="Download Screenshot with Artistic Background and Border",
        data=img_buffer,
        file_name="screenshot_with_artistic_background_and_border.png",
        mime="image/png"
    )
