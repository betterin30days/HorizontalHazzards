"""Representing movement directions"""
class Direction(object):
    """basic properties for name and deltas for travel"""
    name = ""
    x_delta = 0
    y_delta = 0

    def __init__(self, name, x_delta, y_delta):
        """ensure data requirements met before assignment"""
        assert isinstance(name, str)
        assert len(name) > 0
        self.name = name
        assert isinstance(x_delta, int)
        self.x_delta = x_delta
        assert isinstance(y_delta, int)
        self.y_delta = y_delta

    def __str__(self): 
        """debug output of name"""
        return self.name.rjust(5)
