import os
from PIL import Image
import imagehash
import shutil


def move_duplicate_images(source_directory, target_directory):
    """
    Moves duplicate images from the source directory to the target directory.

    Args:
    - source_directory: Path to the directory containing the original images.
    - target_directory: Path to the directory where duplicates will be moved.
    """
    # Create the target directory if it doesn't exist
    if not os.path.exists(target_directory):
        os.makedirs(target_directory)

    hashes = {}
    duplicates = []

    # Iterate through all image files in the source directory
    for image_file in os.listdir(source_directory):
        if not image_file.lower().endswith(('.jpg', '.jpeg', '.png')):
            continue  # Skip non-image files

        image_path = os.path.join(source_directory, image_file)

        # Open and hash the image
        try:
            with Image.open(image_path) as img:
                img_hash = imagehash.average_hash(img)
        except Exception as e:
            print(f"Error processing {image_file}: {e}")
            continue

        # Check if the hash already exists
        if img_hash in hashes:
            duplicates.append(image_path)
            print(f"Duplicate found: {image_file} and {hashes[img_hash]}")
        else:
            hashes[img_hash] = image_file

    # Move duplicates to the target directory
    for duplicate in duplicates:
        target_path = os.path.join(target_directory, os.path.basename(duplicate))
        shutil.move(duplicate, target_path)
        print(f"Moved {duplicate} to {target_path}")

    print("Duplicate image moving process completed.")
    print(f"Total moved duplicate images: {len(duplicates)}")


# Adjust these paths if necessary to match your directory structure
move_duplicate_images('downloaded_images', 'Confusion Image')
