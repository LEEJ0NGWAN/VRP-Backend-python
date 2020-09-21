from math import pi
# example setting
WIDTH = 1440
HEIGHT = 720
w = WIDTH//2
h = HEIGHT//2
center = {
    'x': w,
    'y': h,
}

def getYawPitch(x, y):
    diff = {
        'x': x-center['x'],
        'y': y-center['y'],
    }

    yaw_ = (diff['x']/w) * pi
    pitch_ = 0.5 * (diff['y']/h) * pi

    return (yaw_, pitch_)

# example
# print(getYawPitch(251,244))

