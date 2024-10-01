import streamlit as st
from PIL import Image, ImageDraw, ImageFilter
import io
import random
import numpy as np
import colorsys
from streamlit_paste_button import paste_image_button  # Correct import

# Function to generate analogous or complementary colors based on a base color
def generate_harmonious_colors(scheme, num_colors=5):
    base_hue = random.random()
    colors = []
    for i in range(num_colors):
        if scheme == 'analogous':
            hue = (base_hue + (i * 0.1)) % 1.0
        elif scheme == 'complementary':
            hue = (base_hue + (i % 2) * 0.5) % 1.0  # Shift by 180 degrees
        rgb = colorsys.hls_to_rgb(hue, 0.6, 0.7)  # Convert HSL to RGB
        rgb = tuple(int(x * 255) for x in rgb)
        colors.append(rgb)
    return colors

# Function to create a background with mixed colors in a swirl pattern
def create_attractive_background(width, height, color_scheme, num_colors=5, blur_radius=20):
    colors = generate_harmonious_colors(scheme=color_scheme, num_colors=num_colors)
    # Ensure width and height are integers
    width, height = int(width), int(height)
    background = Image.new("RGB", (width, height))
    draw = ImageDraw.Draw(background)
    
    for _ in range(300):  # Draw 300 random circles
        color = random.choice(colors)
        radius = random.randint(50, 200)
        x = random.randint(0, width)
        y = random.randint(0, height)
        draw.ellipse((x - radius, y - radius, x + radius, y + radius), fill=color)

    # Apply a swirl-like pattern and blur to smooth the transitions
    img_array = np.array(background)
    swirl_background = Image.fromarray(img_array)
    blurred_background = swirl_background.filter(ImageFilter.GaussianBlur(blur_radius))
    
    return blurred_background

# Function to add a thin black border around the image
def add_border_to_image(image, border_size=5):
    new_width = image.width + 2 * border_size
    new_height = image.height + 2 * border_size
    bordered_image = Image.new("RGB", (new_width, new_height), "black")
    bordered_image.paste(image, (border_size, border_size))
    return bordered_image

# Function to add a background based on the image size
def add_background_to_image(image, color_scheme):
    # Add a border around the image
    image_with_border = add_border_to_image(image)

    # Create an attractive background 1.2 times the size of the image
    background_width = int(image_with_border.width * 1.2)
    background_height = int(image_with_border.height * 1.2)
    background_image = create_attractive_background(background_width, background_height, color_scheme=color_scheme)

    # Calculate position to center the image on the background
    x_offset = (background_image.width - image_with_border.width) // 2
    y_offset = (background_image.height - image_with_border.height) // 2

    # Paste the image with the border onto the background
    background_image.paste(image_with_border, (x_offset, y_offset))
    return background_image

# Streamlit app title
st.title("Screenshotz")

# Let user choose the color scheme
color_scheme = st.selectbox("Select Color Scheme", options=['analogous', 'complementary'])

# Use streamlit-paste-button to paste images from the clipboard
pasted_image = paste_image_button(label="Paste Image")

if pasted_image is not None:
    # Open the pasted image
    image = Image.open(io.BytesIO(pasted_image.image_data))

    # Add background with color swirl and blur
    background_image = add_background_to_image(image, color_scheme=color_scheme)

    # Save the image with background to a BytesIO object
    img_buffer = io.BytesIO()
    background_image.save(img_buffer, format="PNG")
    img_buffer.seek(0)

    # Display the image with background in the Streamlit app
    st.image(background_image, caption=f"Image with {color_scheme.capitalize()} Background and Border", use_column_width=True)

    # Provide a download link for the image with background
    st.download_button(
        label="Download Image with Artistic Background and Border",
        data=img_buffer,
        file_name="image_with_artistic_background_and_border.png",
        mime="image/png"
    )
