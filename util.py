from math import radians, degrees, tan, atan

# 전제조건
# FOV = 90 # degree (라디안이 아닙니다)
# (yaw_, pitch_) = (0,0) ~ (7,7)
# WIDTH, HEIGHT

# example setting
FOV = 90
THETA = FOV/2
TAN_THETA = tan(radians(THETA))
WIDTH = 640
HEIGHT = 480
ROUND_COUNTS = 8

def getYawPitch(yaw_index, pitch_index, x, y):
    if yaw_index < 0\
    or pitch_index < 0\
    or yaw_index >= ROUND_COUNTS\
    or pitch_index >= ROUND_COUNTS:
        return (yaw_index, pitch_index)
    
    w = WIDTH/2
    h = HEIGHT/2

    center = {
        x: w,
        y: h,
    }

    dist = {}

    dist['x'] = x - center['x']
    dist['y'] = y - center['y']

    raw_alpha = atan((dist['x']/w)*TAN_THETA)
    alpha = degrees(raw_alpha)

    raw_beta = atan((dist['y']/h)*TAN_THETA)
    beta = degrees(raw_beta)

    return (alpha, beta)

