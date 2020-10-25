from math import pi, radians, tan, atan
half_pi = 0.5 * pi
quarter_pi = 0.25 * pi

# (0,0) ~ (7,7)
PAGINATION = 8

# FOV
HORIZON_FOV = 115
VERTICAL_FOV = 90

# THETA
HORIZON_THETA = radians(HORIZON_FOV/2)
VERTICAL_THETA = radians(VERTICAL_FOV/2)

# FOV_TO_PI
HORIZON_PI = (HORIZON_FOV / 180) * pi
VERTICAL_PI = (VERTICAL_FOV / 180) * pi # half_pi

# 인풋 이미지 사이즈
WIDTH = 3584
HEIGHT = 2240
# WIDTH = 480
# HEIGHT = 360

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

def getBaseRadian(index):
    if index not in range(PAGINATION):
        return None

    if not index:
        return 0

    half_page = PAGINATION//2
    
    baseRadian = pi
    if index < half_page:
        baseRadian = quarter_pi * index
    elif index > half_page:
        baseRadian = quarter_pi * (index-half_page) - pi
    
    return baseRadian

def getYawPitch(x, y, yaw_index=None, pitch_index=None, base=False):
    if not checkRange(x,y):
        return None

    constX, constY = pi, half_pi

    if yaw_index is not None and pitch_index is not None:
        if not checkPage(yaw_index, pitch_index):
            return None

        # constX = constY = quarter_pi
        constX = HORIZON_PI / 2
        constY = VERTICAL_PI / 2

    if base:
        yaw_ = getBaseRadian(yaw_index)
        pitch_ = getBaseRadian(pitch_index)

    else:
        diff = {
            'x': x-center['x'],
            'y': y-center['y'],
        }

        if pitch_index in [3,4,5]:
            diff['x'] = -diff['x']


        # yaw_ = (diff['x']/w) * constX + getBaseRadian(yaw_index)
        alpha = atan((diff['x']/w) * tan(HORIZON_THETA))
        # alpha_ = HORIZON_FOV/MARZIPANO_HFOV * alpha
        yaw_ = alpha + getBaseRadian(yaw_index)

        # pitch_ = (diff['y']/h) * constY + getBaseRadian(pitch_index)
        beta = atan((diff['y']/h) * tan(VERTICAL_THETA))
        pitch_ = beta + getBaseRadian(pitch_index)

    return (yaw_, pitch_)

# 변환 테스트 1
# print(getYawPitch(1888,1724, 0,0))
# print(getYawPitch(1350,830, 0,0))
# print(getYawPitch(1567,722, 0,0))


# 변환 테스트 2
# print(getYawPitch(1792, 1120, 0,0))
# print(getYawPitch(1792, 1120, 1,0))
# print(getYawPitch(1792, 1120, 2,0))
# print(getYawPitch(1792, 1120, 3,0))
# print(getYawPitch(1792, 1120, 4,0))
# print(getYawPitch(1792, 1120, 5,0))
# print(getYawPitch(1792, 1120, 6,0))
# print(getYawPitch(1792, 1120, 7,0))


# 변환 테스트 3
# print(getYawPitch(1792, 1120, 0,0))
# print(getYawPitch(1792, 1120, 0,1))
# print(getYawPitch(1792, 1120, 0,2))
# print(getYawPitch(1792, 1120, 0,3))
# print(getYawPitch(1792, 1120, 0,4))
# print(getYawPitch(1792, 1120, 0,5))
# print(getYawPitch(1792, 1120, 0,6))
# print(getYawPitch(1792, 1120, 0,7))

