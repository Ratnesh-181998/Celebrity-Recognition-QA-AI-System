from PIL import Image
import os
import glob

# Base directory for artifacts
artifact_dir = r"C:/Users/rattu/.gemini/antigravity/brain/bd923eda-7026-4a91-8a1b-b4a573c858eb/"

# Specific files we captured (in order)
filenames = [
    "01_demo_home_1767270952256.png",
    "02_sample_selected_1767271302745.png",
    "03_detection_result_1767271413348.png",
    "04_question_typed_1767271474127.png",
    "05_chat_response_1767271531492.png"
]

image_paths = [os.path.join(artifact_dir, f) for f in filenames]

images = []
for path in image_paths:
    if os.path.exists(path):
        print(f"Adding {path}")
        img = Image.open(path)
        # Resize to make the GIF smaller and more manageable, maintaining aspect ratio
        base_width = 800
        w_percent = (base_width / float(img.size[0]))
        h_size = int((float(img.size[1]) * float(w_percent)))
        img = img.resize((base_width, h_size), Image.Resampling.LANCZOS)
        images.append(img)
    else:
        print(f"Warning: File not found: {path}")

if images:
    output_path = "demo_walkthrough.gif"
    # Duration is in milliseconds per frame. 
    # We want a pause on each step, so let's say 2000ms (2 seconds) per frame.
    images[0].save(
        output_path,
        save_all=True,
        append_images=images[1:],
        duration=2000, 
        loop=0
    )
    print(f"Successfully created GIF at: {os.path.abspath(output_path)}")
else:
    print("No images found to create GIF.")
