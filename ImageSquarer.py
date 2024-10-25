import os
from PIL import Image, ImageOps

def make_square(image_path, output_path, fill_color=(255, 255, 255)):
    # Open the image
    img = Image.open(image_path).convert("RGB")  # Convert to RGB for JPG format
    
    # Get current dimensions
    width, height = img.size
    print(f"Processing {image_path}: {width}x{height}")
    
    # Find the max dimension to make the image square
    max_dim = max(width, height)
    
    # Create a new image with a white background
    new_img = Image.new('RGB', (max_dim, max_dim), fill_color)
    
    # Paste the original image in the center
    new_img.paste(img, ((max_dim - width) // 2, (max_dim - height) // 2))
    
    # Ensure output is in .jpg format
    output_path_jpg = os.path.splitext(output_path)[0] + '.jpg'
    
    # Save the new image
    new_img.save(output_path_jpg, format="JPEG")
    print(f"Saved squared image as JPG at: {output_path_jpg}")

def process_folder(folder_path):
    # Validate folder path
    if not os.path.isdir(folder_path):
        print("The provided path is not a valid directory.")
        return

    # Acceptable file formats
    image_extensions = {'.jpg', '.jpeg', '.png'}
    
    # Get all image files in the directory with specified formats
    image_files = [f for f in os.listdir(folder_path) if os.path.splitext(f)[1].lower() in image_extensions]

    # If no images found, notify the user
    if not image_files:
        print("No suitable image files found in the folder.")
        return
    
    # Create an output folder for processed images
    output_folder = os.path.join(folder_path, 'squared_images')
    os.makedirs(output_folder, exist_ok=True)

    # Process each image file
    for image_file in image_files:
        input_path = os.path.join(folder_path, image_file)
        output_path = os.path.join(output_folder, os.path.splitext(image_file)[0])  # Base name for output
        make_square(input_path, output_path)

if __name__ == "__main__":
    # Prompt the user for a folder location
    folder_path = input("Please enter the folder path containing the images: ")
    
    # Process the folder and convert images to square and .jpg format
    process_folder(folder_path)
