from PIL import Image
import numpy
from matplotlib import pyplot
import mplcursors
from threading import Timer
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
from pathfinding.core.diagonal_movement import DiagonalMovement

DEFAULT_IMAGE = 'images/1.png'
TIMEOUT_DURATION = 3.0


def main():
    # Create image from image file path
    img = image()
    # Prompt user for starting and target points
    coords = coordinates(img)
    # Find optimal path based on starting and target points
    find_optimal_path(img, coords)


def image():
    # Prompt user for image file path
    path = input('Please enter image file path (or press enter for default): ')

    # If no specific image file path was chosen
    if path == '':
        # Assign default image file path to path variable
        path = DEFAULT_IMAGE

    # Create image from image file path
    img = Image.open(path)

    print('Selected image file: ', path, '\n')

    return img


def plot(img):
    # Create array from image
    data = numpy.array(img)
    # Create plot from image array
    plt = pyplot.imshow(data)

    return plt


def paint_coordinates(coords):
    # Paint starting point
    pyplot.plot(coords[0][1], coords[0][0], 'og')
    # Paint target point
    pyplot.plot(coords[1][1], coords[1][0], 'or')


def close_plot():
    # Initialize timeout to close plot
    Timer(TIMEOUT_DURATION, pyplot.close).start()


def coordinates(img):
    # Create plot from image
    plt = plot(img)
    # Initialize list to store starting and target coordinates
    coords = []
    # Create plot cursor
    cursor = mplcursors.cursor(plt, hover=False)

    print('Please select starting and target points...')

    # Decorate cursor with mouse click event listener
    @cursor.connect('add')
    def clicked_cursor(sel):
        # Hide plot select annotations
        sel.annotation.set_visible(False)
        # Add current point's coordinates to coordinates list
        coords.append(sel.target.index)
        # Paint current point
        pyplot.plot(sel.target[0], sel.target[1], 'og')

        # If coordinates list has two coordinates after mouse click
        if len(coords) == 2:
            # Paint starting point and target point onto plot
            paint_coordinates(coords)

            print('Selected coordinates: ', coords, '\n')
            print('Calculating optimal path, please wait...\n')

            # Close plot
            close_plot()

    # Display plot
    pyplot.show()

    return coords


def matrix(img):
    # Create grayscale image from image
    grayscale_img = img.convert('L')
    # Create list from grayscale image
    data = list(grayscale_img.getdata())
    # Extract width and height from image
    width, height = grayscale_img.size
    # Create matrix from grayscale image using its data and size
    mtrx = [data[offset:offset + width] for offset in range(0, width * height, width)]

    return mtrx


def optimal_path(mtrx, coords):
    # Create grid from matrix
    grid = Grid(matrix=mtrx)
    # Create starting point node from coordinates
    start = grid.node(coords[0][1], coords[0][0])
    # Create target point node from coordinates
    end = grid.node(coords[1][1], coords[1][0])
    # Initialize finder as instance of AStarFinder that allows for diagonal movement
    finder = AStarFinder(diagonal_movement=DiagonalMovement.always)
    # Find optimal path and number of runs between starting point and target point
    path, runs = finder.find_path(start, end, grid)

    print('Number of runs: ', runs)
    print('Path length: ', len(path), '\n')

    return path


def paint_path(path):
    # Extract x values from all coordinates
    x_vals = [coord[0] for coord in path]
    # Extract y values from all coordinates
    y_vals = [coord[1] for coord in path]
    # Paint path
    pyplot.plot(x_vals, y_vals, '-b')
    # Paint starting point
    pyplot.plot(path[0][0], path[0][1], 'og')
    # Paint target point
    pyplot.plot(path[-1][0], path[-1][1], 'or')


def display_path(img, path):
    # Create plot from image
    plot(img)
    # Paint optimal path onto plot
    paint_path(path)
    # Display plot
    pyplot.show()


def find_optimal_path(img, coords):
    # If user selected starting target points
    if len(coords):
        # Create matrix from image
        mtrx = matrix(img)
        # Find optimal path in matrix
        path = optimal_path(mtrx, coords)
        # Display plot with optimal path
        display_path(img, path)

        print('Done!')

    # Otherwise, display friendly message saying no starting and target points were selected to user
    else:
        print('\nNo starting and target points were selected.')


if __name__ == '__main__':
    main()
