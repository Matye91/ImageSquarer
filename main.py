import os
from PIL import Image
from pillow_heif.as_plugin import register_heif_opener

# Allow Pillow to open .heic/.heif files
register_heif_opener()

MAX_DIMENSION = 2400

def make_square(image_path, output_path, fill_color=(255, 255, 255), max_dimension=MAX_DIMENSION, use_webp=False):
    # Open the image
    img = Image.open(image_path)

    # Handle transparency for PNG files
    if img.mode == "RGBA":
        # Create a white background image
        white_bg = Image.new("RGB", img.size, fill_color)
        # Paste the original image onto the white background using the alpha channel as a mask
        img = Image.alpha_composite(white_bg.convert("RGBA"), img).convert("RGB")

    else:
        img = img.convert("RGB")  # Convert to RGB for non-transparent images

    # Get current dimensions
    width, height = img.size
    print(f"Processing {image_path}: {width}x{height}")

    # Find the max dimension to make the image square
    max_dim = max(width, height)

    # Create a new image with a white background
    new_img = Image.new('RGB', (max_dim, max_dim), fill_color)

    # Paste the original image in the center
    new_img.paste(img, ((max_dim - width) // 2, (max_dim - height) // 2))

    # Scale down if the square exceeds the maximum allowed dimension
    if max_dim > max_dimension:
        new_img = new_img.resize((max_dimension, max_dimension), Image.Resampling.LANCZOS)

    # Save as .webp or .jpg depending on user preference
    if use_webp:
        output_path_final = os.path.splitext(output_path)[0] + '.webp'
        new_img.save(output_path_final, format="WEBP")
    else:
        output_path_final = os.path.splitext(output_path)[0] + '.jpg'
        new_img.save(output_path_final, format="JPEG")

    print(f"Saved squared image at: {output_path_final}")

def process_folder(folder_path, use_webp=False):
    # Validate folder path
    if not os.path.isdir(folder_path):
        print("The provided path is not a valid directory.")
        return

    # Acceptable file formats
    image_extensions = {'.jpg', '.jpeg', '.png', '.webp', '.heic', '.heif'}
    
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
        make_square(input_path, output_path, use_webp=use_webp)

if __name__ == "__main__":
    # Prompt the user for a folder location
    folder_path = input("Please enter the folder path containing the images: ")

    # Ask the user whether they want WebP output instead of JPG
    webp_choice = input("Do you want the output images in WebP format? (Y/N): ").strip().lower()
    use_webp = webp_choice == 'y'

    # Process the folder and convert images to square (.webp or .jpg)
    process_folder(folder_path, use_webp=use_webp)
