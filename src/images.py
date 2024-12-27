#!../.venv/bin/python3
import random
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import os

# Function to generate random colors
def random_color():
    return tuple(random.randint(50, 255) for _ in range(3))

# Function to create a background with geometric shapes and a grain effect
def create_background_image():
    width, height = 1920, 1080
    background = Image.new("RGB", (width, height), random_color())  # Random background color
    draw = ImageDraw.Draw(background)

    # Add some geometric shapes (circles, rectangles, etc.)
    for _ in range(random.randint(5, 10)):
        shape_type = random.choice(['circle', 'rectangle'])
        color = random_color()
        if shape_type == 'circle':
            x1, y1 = random.randint(0, width), random.randint(0, height)
            x2, y2 = x1 + random.randint(50, 300), y1 + random.randint(50, 300)
            draw.ellipse([x1, y1, x2, y2], fill=color, outline=color)
        else:
            x1, y1 = random.randint(0, width), random.randint(0, height)
            x2, y2 = x1 + random.randint(50, 300), y1 + random.randint(50, 300)
            draw.rectangle([x1, y1, x2, y2], fill=color, outline=color)

    # Apply grain effect to the background
    background_np = np.array(background)
    noise = np.random.normal(0, 10, background_np.shape).astype(np.uint8)
    background_np = np.clip(background_np + noise, 0, 255)
    background = Image.fromarray(background_np)

    return background

# Function to add text to the image
def add_text_to_image(image, text="Jebus Productions"):
    draw = ImageDraw.Draw(image)
    
    # Load a large font
    font = ImageFont.truetype("/Library/Fonts/Arial.ttf", 100)
    
    # Calculate text size using textbbox (bounding box method)
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    
    # Position text in the center
    width, height = image.size
    text_x = (width - text_width) // 2
    text_y = (height - text_height) // 2
    draw.text((text_x, text_y), text, font=font, fill=(255, 255, 255))

# Main loop to create 100 unique images
def generate_images(num_images=100):
    os.makedirs("generated_images", exist_ok=True)

    for i in range(num_images):
        background_image = create_background_image()
        add_text_to_image(background_image, "Jebus Productions")
        background_image.save(f"../tmp/generated_images/lowfi_image_{i + 1}.png")
        print(f"Image {i + 1} saved!")

# Run the image generation
generate_images(100)
