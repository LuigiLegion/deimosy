# Imports
from utils import image, coordinates, find_optimal_path


# Initializations
def main():
    # Create image from image file path
    img = image()
    # Prompt user for starting and target points
    coords = coordinates(img)
    # Find optimal path based on starting and target points
    find_optimal_path(img, coords)


if __name__ == '__main__':
    main()
