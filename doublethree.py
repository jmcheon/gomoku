def is_valid_position(position):
    # Check if the position (x, y) is within the bounds of the board.
    return 0 <= position[0] < 19 and 0 <= position[1] < 19


def get_continuous_three(x, y, direction):
    print("===================")
    print(x, y)
    print(x + direction[0], y + direction[1])
    print(x - direction[0], y - direction[1])
    print("===================")
    test = []
    inside = []
    for i in range(3):
        for j in range(3):
            inside.append((x + i + j, y))
        test.append(inside.copy())
        inside.clear()
    return test


def test(x, y, player):
    print("left\n", get_continuous_three(x - 2, y))
    test = get_continuous_three(x - 2, y)
    # print(test)
    flag = None
    print("--------")
    for i in range(len(test)):
        flag = True
        for j in range(len(test[i])):
            if is_valid_position(test[i][j]) == False:
                flag = False
                print("not valid")
                break
            print(test[i][j])
        if flag == True:
            equal_three(test[i], player)

        print("---------")

    # print("northeast\n", get_continuous_three(x - 2, y + 2))
    # print("up\n", get_continuous_three(x, y + 2))
    # print("northwest\n", get_continuous_three(x + 2, y + 2))
    # print("northeast", x - 2, y - 2)
    # print("up", x + 2, y)
    # print("northwest", x + 2, y + 2)
    # right_3 = []
    # left_3 = []
    # down_3 = []
    # up_3 = []

    # updown = []
    # leftright = []

    # for i in range(3):
    #     right_3.append([x + i, y])

    # for i in range(3):
    #     left_3.append([x - i, y])

    # for i in range(3):
    #     down_3.append([x, y + i])

    # for i in range(3):
    #     up_3.append([x, y - i])

    # for i in range(x - 1, x + 2, 1):
    #     updown.append([i, y])

    # print("right_3", right_3)
    # print("left_3", left_3)
    # print("down_3", down_3)
    # print("up_3", up_3)
    # print("updown", updown)


# test(1, 1)
