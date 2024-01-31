class Player:

    def __init__(self, _name, _color, _pos):

        self.Name = _name

        self.Color = _color

        self.Rect = None

    @property
    def name(self):
        return self.Name

    @name.setter
    def name(self, value):
        self.Name = value

    @property
    def color(self):
        return self.Color

    @color.setter
    def color(self, value):
        self.Color = value

