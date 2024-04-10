import os
import shutil

# Define the path to the directory containing the images
image_directory_path = 'downloaded_images2'

# Iterate over each file in the image directory
for filename in os.listdir(image_directory_path):
    # Check if it's a file and not a directory
    if os.path.isfile(os.path.join(image_directory_path, filename)):
        # Split the filename on underscore (or choose another appropriate character)
        parts = filename.split('_')
        # The first part of the name, assuming it's the series name
        series_name = parts[0]

        # Create a new directory path for this series
        new_directory_path = os.path.join(image_directory_path, series_name)

        # Check if this directory exists, if not, create it
        if not os.path.exists(new_directory_path):
            os.makedirs(new_directory_path)

        # Move the file to the new directory
        shutil.move(os.path.join(image_directory_path, filename), os.path.join(new_directory_path, filename))

print("Images have been organized into folders.")
