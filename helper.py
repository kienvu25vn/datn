from PIL import Image
from csbdeep.utils import Path, normalize
import numpy as np
def crop_and_save_image(input_path, output_path, left, top, right, bottom):
    try:
        # Open the image
        img = Image.open(input_path)

        # Crop the image
        img_cropped = img.crop((left, top, right, bottom))

        img_cropped = img_cropped.convert("L")
        print(np.array(img_cropped).shape)
        # Save the cropped image
        img_cropped.save(output_path)

        print("Image cropped and saved successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # X = sorted(Path('imagesBB/').glob('*.tif'))
    X = sorted(Path('masksBB/').glob('*.tif'))
    for i in range(len(X)):
        input_image_path = X[i]
        # output_image_path = "bbImages/M2" + str(input_image_path).split('\\')[-1]
        output_image_path = "bbMasks/M2" + str(input_image_path).split('\\')[-1]
        left, top, right, bottom = 512, 0, 1024, 256
        crop_and_save_image(input_image_path, output_image_path, left, top, right, bottom)
    # input_image_path = "imagesBB/0.png.tif"  # Replace with your input image path
    # output_image_path = "output0.tif"  # Replace with your output image path
    # left, top, right, bottom = 0, 0, 512, 256  # Define the cropping coordinates

    # crop_and_save_image(input_image_path, output_image_path, left, top, right, bottom)
