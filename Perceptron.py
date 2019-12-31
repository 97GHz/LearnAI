import random
import math


def activate(p):
    return 1.0 / (1.0 + math.exp(-p))


if __name__ == '__main__':
    x = [[0, 0], [0, 1], [1, 0], [1, 1]]
    y = [0, 0, 0, 1]
    w = []

    for i in range(3):
        w.append(random.uniform(-1, 1))

    for epoch in range(501):
        if epoch % 100 == 0:
            print('epoch: ', epoch)
            print("w: ", w)
        for x_bar, y_bar in zip(x, y):
            s = x_bar[0] * w[0] + x_bar[1] * w[1] + w[2]
            f = activate(s)
            loss = (f - y_bar)**2
            if epoch % 100 == 0:
                print('Loss: ', loss)
                print(x_bar[0], x_bar[1], round(f, 2))

            dLdf = 2*(f - y_bar)
            dfds = activate(s)*(1-activate(s))
            dsdw0 = x_bar[0]
            dsdw1 = x_bar[1]
            dsdw2 = 1

            w[0] -= dsdw0 * dfds * dLdf
            w[1] -= dsdw1 * dfds * dLdf
            w[2] -= dsdw2 * dfds * dLdf
