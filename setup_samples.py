import os
import shutil

# Paths
dataset_dir = r"C:\Users\rattu\Downloads\6_Celebrity Detector QA\Celebrity Faces Dataset"
samples_dir = r"C:\Users\rattu\Downloads\6_Celebrity Detector QA\Local\samples"

# Ensure samples dir exists
os.makedirs(samples_dir, exist_ok=True)

# Iterate through celebrity folders
for cel_name in os.listdir(dataset_dir):
    cel_path = os.path.join(dataset_dir, cel_name)
    if os.path.isdir(cel_path):
        # Find first image
        images = [f for f in os.listdir(cel_path) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
        if images:
            first_image = images[0]
            src = os.path.join(cel_path, first_image)
            
            # Create destination filename (e.g., "Angelina_Jolie.jpg")
            safe_name = cel_name.replace(" ", "_")
            dst_name = f"{safe_name}.jpg"
            dst = os.path.join(samples_dir, dst_name)
            
            # Copy
            shutil.copy2(src, dst)
            print(f"Copied {cel_name} -> {dst_name}")

print("All samples populated.")
