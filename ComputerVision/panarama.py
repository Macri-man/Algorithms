import cv2
import numpy as np
import glob

def stitch_images(image_paths):
    # Load images
    images = [cv2.imread(img) for img in image_paths]

    # Create a Stitcher object
    stitcher = cv2.Stitcher_create()
    
    # Stitch images together
    status, stitched_image = stitcher.stitch(images)

    if status == cv2.Stitcher_OK:
        return stitched_image
    else:
        print("Error during stitching: ", status)
        return None

def main():
    # Specify the path to your images
    image_paths = glob.glob('path/to/your/images/*.jpg')  # Adjust the path and extension accordingly

    # Sort images if necessary (e.g., by filename)
    image_paths.sort()

    # Stitch images
    panorama = stitch_images(image_paths)

    if panorama is not None:
        # Save the resulting panorama
        cv2.imwrite('panorama.jpg', panorama)
        # Display the result
        cv2.imshow('Panorama', panorama)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
