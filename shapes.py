class Shape(object):
    def __init__(self):
        super(Shape, self).__init__()
        self.color = None

class Line(Shape):
    def __init__(self, color, start_pos, end_pos, width=1):
        super(Line, self).__init__()

        self.color = color
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.width = width

class Rectangle(Shape):
    def __init__(self, color, x, y, width, height):
        super(Rectangle, self).__init__()

        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
