import math


class mesh(object):
    def __init__(self, width, height, x, y):
        self._width = width
        self._height = height

        # Coord of the bottom left corner
        self._bottom_left_x = x
        self._bottom_left_y = y

        # Coord of the bottom right
        self._bottom_right_x = x + width
        self._bottom_right_y = y

        # Coord of top left
        self._top_left_x = x
        self._top_left_y = y + height

        # Coord of top right
        self._top_right_x = x + width
        self._top_right_y = y + height

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    @property
    def bottom_left(self):
        return self._bottom_left_x, self._bottom_left_y

    @property
    def bottom_right(self):
        return self._bottom_right_x, self._bottom_right_y

    @property
    def top_left(self):
        return self._top_left_x, self._top_left_y

    @property
    def top_right(self):
        return self._top_right_x, self._top_right_y


if __name__ == "__main__":
    rect = mesh(5, 3, 0, 0)
    print(rect.top_right)