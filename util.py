from math import pi
half_pi = 0.5 * pi
quarter_pi = 0.25 * pi

# example setting
PAGINATION = 8

WIDTH = 1440
HEIGHT = 720
w = WIDTH//2
h = HEIGHT//2
center = {
    'x': w,
    'y': h,
}

def getYawPitch(x, y, i=None, j=None):
    constX, constY = pi, half_pi
    yaw, pitch = 0, 0
    if i and j:
        if i not in range(PAGINATION)\
        or j not in range(PAGINATION):
            return None
        constX = constY = 0.5 * quarter_pi
        yaw = quarter_pi * i
        pitch = quarter_pi * j

    diff = {
        'x': x-center['x'],
        'y': y-center['y'],
    }

    yaw_ = (diff['x']/w) * constX + yaw
    pitch_ = (diff['y']/h) * constY + pitch

    return (yaw_, pitch_)

# example
# print(getYawPitch(970,392))

