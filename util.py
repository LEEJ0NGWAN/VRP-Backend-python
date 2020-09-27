from math import pi
half_pi = 0.5 * pi
quarter_pi = 0.25 * pi

# (0,0) ~ (7,7)
PAGINATION = 8

# 인풋 이미지 사이즈
WIDTH = 480
HEIGHT = 360

# 이미지의 4분의 1 크기
w = WIDTH//2
h = HEIGHT//2

# 이미지의 중심
center = {
    'x': w,
    'y': h,
}

def checkRange(x, y):
    if x < 0 or y < 0\
    or x > WIDTH or y > HEIGHT:
        return False

    return True

def checkPage(i, j):
    if i not in range(PAGINATION)\
    or j not in range(PAGINATION):
        return False

    return True

def getYawPitch(x, y, i=None, j=None):
    if not checkRange(x,y):
        return None

    constX, constY = pi, half_pi
    yaw, pitch = 0, 0

    if i is not None and j is not None:
        if not checkPage(i,j):
            return None

        constX = constY = quarter_pi
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
print(getYawPitch(204,282,0,0))

