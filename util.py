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

        constX = constY = quarter_pi

    if base:
        yaw_ = getBaseRadian(yaw_index)
        pitch_ = getBaseRadian(pitch_index)

    else:
        # if pitch_index in [3,4,5,6]:
        #     if x < w:
        #         x = w + (w-x)
        #     else:
        #         x = w - (x-w)

        diff = {
            'x': x-center['x'],
            'y': y-center['y'],
        }

        yaw_ = (diff['x']/w) * constX + getBaseRadian(yaw_index)
        pitch_ = (diff['y']/h) * constY + getBaseRadian(pitch_index)

    return (yaw_, pitch_)

# getYawPitch(x,y,i,j)
# example
# print(getYawPitch(169,210,2,0))

print("/////////////////////")
print("이제 부분 사진에서 특정 좌표를 마지파노 좌표로 변환합니다")
x = int(input("x:"))
y = int(input("y:"))
i = int(input("yaw_index:"))
j = int(input("pitch_index:"))
print(getYawPitch(x, y, i, j))

