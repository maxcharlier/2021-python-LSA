import math

"""
Class initaly created by Virgil Brouillard in 2019
""" 
class Point:
    def __init__(self, x, y):
        """
        Class representing a point in 2D space
        :param x: The x value
        :param y: The y value
        """
        self.x = x
        self.y = y

    def distance(self, point):
        """
        Returns the distance between the current point and the point passed as parameter.
        :param point: The point
        :return: The distance
        """
        return math.sqrt((self.x - point.x) ** 2 + (self.y - point.y) ** 2)

    def __str__(self):
        """
        String representation of the point
        :return: String representation
        """
        return "({}, {})".format(self.x, self.y)

    def __eq__(self, other):
        """
        Comparator function
        :param other: The other object
        :return: True if the objects are equal, False otherwise
        """
        if isinstance(other, Point):
            return self.x == other.x and \
                   self.y == other.y
        return False


    def from_str(pos):
        # print("pos " + str(pos)+ " - " + str(pos.replace('(', '').replace(')', '')))
        (x, y) = pos.replace('(', '').replace(')', '').split(', ')
        return Point(float(x), float(y))
