class BoardException(Exception):
    pass


class BoardWrongShipException(BoardException):
    pass


class BoardOutException(BoardException):
    def __str__(self):
        return 'Нельзя выстрелить за пределы доски!'


class BoardUsedException(BoardException):
    def __str__(self):
        return 'В эту клетку вы уже стреляли!'
