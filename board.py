from Battleship.entities import Dot
from Battleship.exceptions import *


class Board:
    def __init__(self, size: int, hid=False):
        self.size = size
        self.hid = hid
        self.field = [['O'] * size for _ in range(size)]
        self.busy = []
        self.ships = []
        self.last_hit = []      # список точек, раненого корабля
        self.count_destr_ships = 0      # счетчик уничтоженных кораблей

    def __str__(self):
        res = '  | ' + ' | '.join(map(str, range(1, self.size + 1))) + ' |'
        for i, row in enumerate(self.field):
            res += f'\n{i + 1} | ' + ' | '.join(row) + ' |'
        if self.hid:
            res = res.replace('■', 'O')
        return res

    def out(self, d: Dot) -> bool:
        return not (0 <= d.x < self.size) or not (0 <= d.y < self.size)

    def contour(self, ship, visible=False):
        AROUND = [(i, j) for i in range(-1, 2) for j in range(-1, 2)]
        for dot in ship.dots:
            for dx, dy in AROUND:
                curr_dot = Dot(dot.x + dx, dot.y + dy)
                if not self.out(curr_dot) and curr_dot not in self.busy:
                    if visible:      # видимость контура
                        self.field[curr_dot.x][curr_dot.y] = '.'
                    self.busy.append(curr_dot)

    def add_ship(self, ship):
        for d in ship.dots:
            if d in self.busy or self.out(d):
                raise BoardWrongShipException()
        for d in ship.dots:
            self.field[d.x][d.y] = '■'
            self.busy.append(d)
        self.ships.append(ship)
        self.contour(ship)

    def shot(self, d: Dot) -> bool:    # возвращает True, если нужно ход переходить
        if d in self.busy:
            raise BoardUsedException()
        if self.out(d):
            raise BoardOutException()

        for ship in self.ships:
            if ship.is_hit(d):
                self.field[d.x][d.y] = ' '
                print('Попадание!')
                ship.lives -= 1
                if ship.lives == 0:
                    self.count_destr_ships += 1
                    self.contour(ship, visible=True)
                    print('Корабль уничтожен!')
                    self.last_hit = []
                    return False
                else:
                    print('Корабль ранен!')
                    self.last_hit.append(d)
                    return True

        self.field[d.x][d.y] = '*'
        print('Мимо!')
        self.busy.append(d)
        return False

    def begin(self):
        self.busy = []

    def defeat(self):
        return self.count_destr_ships == len(self.ships)
