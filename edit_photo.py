import os
from PIL import Image
import shutil

def crop_to_ratio(image_path, output_path, target_ratio=1.5):
    """
    Crop an image to the target ratio (width:height = 1:1.5)
    Args:
        image_path: Path to the input image
        output_path: Path to save the output image
        target_ratio: Desired height-to-width ratio (default 1.5)
    """
    # Open the image
    img = Image.open(image_path)
    width, height = img.size
    
    # Calculate current ratio (height/width)
    current_ratio = height / width
    
    if current_ratio > target_ratio:
        # Image is too tall, crop height
        new_height = int(width * target_ratio)
        # Crop from the center
        top = (height - new_height) // 2
        bottom = top + new_height
        img_cropped = img.crop((0, top, width, bottom))
    else:
        # Image is too wide, crop width
        new_width = int(height / target_ratio)
        # Crop from the center
        left = (width - new_width) // 2
        right = left + new_width
        img_cropped = img.crop((left, 0, right, height))
    
    # Save the cropped image
    img_cropped.save(output_path)
    print(f"Cropped {os.path.basename(image_path)} to 1:1.5 ratio")

def process_directory(input_dir, output_dir):
    """
    Process all images in a directory
    Args:
        input_dir: Directory containing input images
        output_dir: Directory to save cropped images
    """
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Process each file in the input directory
    for filename in os.listdir(input_dir):
        input_path = os.path.join(input_dir, filename)
        output_path = os.path.join(output_dir, filename)
        
        # Skip directories and non-image files
        if os.path.isdir(input_path):
            continue
        
        # Check if file is an image
        try:
            with Image.open(input_path) as img:
                # Process the image
                crop_to_ratio(input_path, output_path)
        except (IOError, OSError):
            print(f"Skipping {filename} - not a valid image file")

if __name__ == "__main__":
    input_directory = "id_photos"
    output_directory = "id_photos_cropped"
    
    # Process all images
    process_directory(input_directory, output_directory)
    
    # Option to replace original files
    replace = input("Replace original files with cropped versions? (y/n): ")
    if replace.lower() == 'y':
        for filename in os.listdir(output_directory):
            cropped_path = os.path.join(output_directory, filename)
            original_path = os.path.join(input_directory, filename)
            shutil.copy2(cropped_path, original_path)
        print("Original files have been replaced with cropped versions.")
    
    print("Done!")