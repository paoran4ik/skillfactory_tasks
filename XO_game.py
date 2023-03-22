field = [
    ["-", "-", "-"],
    ["-", "-", "-"],
    ["-", "-", "-"]
]

gamer = "x"
move = []
win = 0
count = 0


def win_check():
    win_rule = [[[0, 0], [0, 1], [0, 2]], [[1, 0], [1, 1], [1, 2]], [[2, 0], [2, 1], [2, 2]],
                [[0, 2], [1, 1], [2, 0]], [[0, 0], [1, 1], [2, 2]], [[0, 0], [1, 0], [2, 0]],
                [[0, 1], [1, 1], [2, 1]], [[0, 2], [1, 2], [2, 2]]]
    global win
    for cell in win_rule:
        cords = []
        for c in cell:
            cords.append(field[c[0]][c[1]])
            if cords == ["x", "x", "x"] or cords == ["o", "o", "o"]:
                win += 1
    return win


def gamer_swap():
    global gamer
    if gamer == "x":
        gamer = "o"
    else:
        gamer = "x"
    return gamer


def game_step_display(field):
    print("   0 1 2")
    print("   _____")

    for i in range(len(field)):
        print(i, end="| ")
        for j in range(len(field[i])):
            print(field[i][j], end=" ")
        print()
    return "   _____"


def x_cord():
    while True:
        x = input("Введите номер клетки по вертикали (от 0 до 2): ")
        if len(x) != 1:
            print("Введите координату!")
            continue
        if not x.isdigit():
            print("Нужно вводить числа из списка: 0, 1, 2.")
            continue
        x = int(x)
        return x


def y_cord():
    while True:
        y = input("Введите номер клетки по горизонтали (от 0 до 2): ")
        if len(y) != 1:
            print("Введите координату!")
            continue
        if not y.isdigit():
            print("Нужно вводить числа из списка: 0, 1, 2. ")
            continue
        y = int(y)
        return y


def game_step(gamer):
    global move
    x = x_cord()
    y = y_cord()
    if 0 > x + y > 4:
        print("Вы ввели неверные координаты, попробуйте ещё раз)")
        game_step(gamer)
    else:
        move = [x, y]
    return move


print("-----------------")
print("Добро пожаловать!")
print("   Это игра в    ")
print(" крестики-нолики ")
print("-----------------")
print()
print(game_step_display(field))

while not win or count != 9:
    game_step(gamer)

    if field[move[0]][move[1]] == "-":
        field[move[0]][move[1]] = gamer_swap()
        win_check()
        count += 1

        if count == 9:
            print(game_step_display(field))
            print("Ничья!")
            break

        if win:
            print(game_step_display(field))
            print(f"Победил игрок игравший за '{gamer}'")

            break

        print(game_step_display(field))
        print()
        print("Ход переходит к следующему игроку.")
        print()

    else:
        print("Эта клетка уже занята! Попробуйте ещё раз)")
        print(game_step_display(field))
