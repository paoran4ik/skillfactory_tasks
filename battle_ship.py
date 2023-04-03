from random import randint


class BaseForExceptions(Exception):
    pass


class OutFieldException(BaseForExceptions):
    def __str__(self):
        return f"Вы выстрелили за границы поля!"


class OccupiedPosShotException(BaseForExceptions):
    def __str__(self):
        return f"Вы уже стреляли в эту точку!"


class ShipPlacementException(BaseForExceptions):
    pass


class Field:
    def __init__(self, hide=False, size=6):

        self.hide = hide
        self.size = size
        self.dead_ship = 0
        self.field = [
            ["0", "0", "0", "0", "0", "0"],
            ["0", "0", "0", "0", "0", "0"],
            ["0", "0", "0", "0", "0", "0"],
            ["0", "0", "0", "0", "0", "0"],
            ["0", "0", "0", "0", "0", "0"],
            ["0", "0", "0", "0", "0", "0"]
        ]
        self.occupied = []
        self.ship_on_field = []

    def __str__(self):
        res = ""
        res += "  | 1 | 2 | 3 | 4 | 5 | 6 |"
        for i, row in enumerate(self.field):
            res += f"\n{i + 1} | " + " | ".join(row) + " |"
        if self.hide:
            res = res.replace("■", "0")
        return res

    def in_field(self, pos):
        return (0 <= pos.x < self.size) and (0 <= pos.y < self.size)

    def contur(self, ship, const=False):
        near = [
            (-1, 1), (0, 1), (1, 1),
            (-1, 0), (0, 0), (1, 0),
            (-1, -1), (0, -1), (1, -1)
        ]
        for d in ship.ship_cords:
            for dx, dy in near:
                cur = Dot(d.x + dx, d.y + dy)
                if self.in_field(cur) and cur not in self.occupied:
                    if const:
                        self.field[cur.x][cur.y] = "•"
                    self.occupied.append(cur)

    def add_ship(self, ship):
        for d in ship.ship_cords:
            if not self.in_field(d) or d in self.occupied:
                raise ShipPlacementException()
        for d in ship.ship_cords:
            self.field[d.x][d.y] = "■"
            self.occupied.append(d)
        self.ship_on_field.append(ship)
        self.contur(ship)

    def hit(self, d):
        if not self.in_field(d):
            raise OutFieldException()

        if d in self.occupied:
            raise OccupiedPosShotException()

        self.occupied.append(d)

        for ship in self.ship_on_field:
            if d in ship.ship_cords:
                ship.hp -= 1
                self.field[d.x][d.y] = "X"
                if ship.hp == 0:
                    self.dead_ship += 1
                    self.contur(ship, const=True)
                    print("Корабль уничтожен.")
                    return False
                else:
                    print("Корабль ранен.")
                    return True
        self.field[d.x][d.y] = "•"
        print("Мимо.")
        return False

    def start(self):
        self.occupied = []


class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f"Dot {self.x},{self.y}"


class Ships:
    def __init__(self, pos, rotation, ship_size):
        self.rotation = rotation
        self.pos = pos
        self.hp = ship_size
        self.ship_size = ship_size

    @property
    def ship_cords(self):
        ship_cords_list = []
        for i in range(self.ship_size):
            pos_x = self.pos.x
            pos_y = self.pos.y

            if self.rotation == 0:
                pos_x += i
            elif self.rotation == 1:
                pos_y += i
            ship_cords_list.append(Dot(pos_x, pos_y))
        return ship_cords_list

    def hit(self, hit_pos):
        return hit_pos in self.ship_cords()

    def __str__(self):
        return f"Ship: position {self.pos}, rotation {self.rotation}, size {self.ship_size}, hp {self.hp} "


class Player:
    def __init__(self, field, enemy):
        self.field = field
        self.enemy = enemy

    def ask(self):
        raise NotImplementedError()

    def move(self):
        while True:
            try:
                target = self.ask()
                repeat = self.enemy.hit(target)
                return repeat
            except BaseForExceptions as e:
                print(e)


class AI(Player):
    def ask(self):
        d = Dot(randint(0, 5), randint(0, 5))
        print(f"Ход компьютера: {d.x + 1} {d.y + 1}")
        return d


class User(Player):
    def ask(self):
        while True:
            cords = input("Ваш ход: ").split()

            if len(cords) != 2:
                print(" Введите 2 координаты! ")
                continue

            x, y = cords

            if not (x.isdigit()) or not (y.isdigit()):
                print(" Введите числа! ")
                continue

            x, y = int(x), int(y)

            return Dot(x - 1, y - 1)


class Game:
    def __init__(self, size=6):
        self.size = size
        pl = self.random_field()
        co = self.random_field()
        co.hide = True
        self.ai = AI(co, pl)
        self.us = User(pl, co)

    def gen_field(self):
        lens = [3, 2, 2, 1, 1, 1, 1]
        field = Field(size=self.size)
        attempts = 0
        for l in lens:
            while True:
                attempts += 1
                if attempts > 5000:
                    return None
                ship = Ships(Dot(randint(0, self.size), randint(0, self.size)), randint(0, 1), l)
                try:
                    field.add_ship(ship)
                    break
                except ShipPlacementException:
                    pass
        field.start()
        return field

    def random_field(self):
        field = None
        while field is None:
            field = self.gen_field()
        return field

    def greet(self):
        print("--------------------")
        print("  Игра Морской Бой  ")
        print("     Обозначения:   ")
        print("    'X' попадание   ")
        print("     '•' промах     ")
        print("--------------------")
        print(" формат ввода: x y ")
        print(" x - номер строки  ")
        print(" y - номер столбца ")

    def loop(self):
        num = 0
        while True:
            print("-" * 27)
            print("Доска пользователя:")
            print(self.us.field)
            print("-" * 27)
            print("Доска компьютера:")
            print(self.ai.field)
            if num % 2 == 0:
                print("-" * 27)
                print("Ходит пользователь!")
                repeat = self.us.move()
            else:
                print("-" * 27)
                print("Ходит компьютер!")
                repeat = self.ai.move()
            if repeat:
                num -= 1

            if self.ai.field.dead_ship == 7:
                print("-" * 27)
                print("Пользователь выиграл!")
                break

            if self.us.field.dead_ship == 7:
                print("-" * 27)
                print("Компьютер выиграл!")
                break
            num += 1

    def start(self):
        self.greet()
        self.loop()


g = Game()
g.start()
