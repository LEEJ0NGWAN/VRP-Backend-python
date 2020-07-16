# Reference : http://www.gisdeveloper.co.kr/?p=6868
import numpy as np
import cv2
import glob

# termination criteria
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# 7 * 7 grid 이미지 사용
# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((7 * 7, 3), np.float32)
objp[:, :2] = np.mgrid[0:7, 0:7].T.reshape(-1, 2)
# Arrays to store object points and image points from all the images.
objpoints = []  # 3d point in real world space
imgpoints = []  # 2d points in image plane.

images = glob.glob("./images/1b.jpg")
# TODO: 이미지 resize

for fname in images:
    img = cv2.imread(fname)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Find the chess board corners
    ret, corners = cv2.findChessboardCorners(gray, (7, 7), None)

    # If found, add object points, image points (after refining them)
    if ret == True:
        print("Found corners")
        objpoints.append(objp)

        corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
        imgpoints.append(corners2)

        # Draw and display the corners
        img = cv2.drawChessboardCorners(img, (7, 7), corners2, ret)
        # cv2.imshow("img", img)
        cv2.imwrite("./images/11.png", img)
        cv2.waitKey(500)
# => 패턴 검출을 통해 객체 지점(objpoints)과 이미지 지점(imgpoints)을 파악

# print("imgpoint : ", imgpoints, "\nobjpoint : ", objpoints)

ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(
    objpoints, imgpoints, gray.shape[::-1], None, None
)
print("mtx : ", mtx, "\ndist :", dist)

cv2.destroyAllWindows()

# cropped image
# mtx :  [[557.99558698   0.         208.31247694]
#  [  0.         614.31202123 270.68409783]
#  [  0.           0.           1.        ]]
# dist : [[-0.01001418  0.00541765 `-0.09569414  0.01828405  0.00178755]]
# height  :  1036 , width :  828
# newcameramtx :
#  [[462.24606323   0.         269.85824053]
#  [  0.         419.61282349 166.23924625]
#  [  0.           0.           1.        ]]
# roi :
#  (105, 38, 626, 890)

# whole image
# mtx :  [[654.71221502   0.         704.07921836]
#  [  0.         252.92733638 383.68230819]
#  [  0.           0.           1.        ]]
# dist : [[-0.13909136 -0.02002549  0.01342978  0.01113573  0.02202911]]
# height  :  720 , width :  1440
# newcameramtx :
#  [[527.23638916   0.         739.79329093]
#  [  0.         205.43510437 393.92774307]
#  [  0.           0.           1.        ]]
# roi :
#  (541, 286, 517, 255)
# total error:  0.5078810910700184

img = cv2.imread("./images/11.jpg")
# 이미지 크기 반환
h, w = img.shape[:2]
print("height  : ", h, ", width : ", w)
newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w, h), 1, (w, h))
#  => 카메라 왜곡 제거 전 : cv2.getOptimalNewCameraMatrix() 함수를 이용해 카메라 메트릭스를 구함
print("newcameramtx : \n", newcameramtx)
print("roi : \n", roi)


# # undistort
# dst = cv2.undistort(img, mtx, dist, None, newcameramtx)
# # crop the image
# x, y, w, h = roi
# # dst = dst[y : y + h, x : x + w]
# cv2.imwrite("./images/6_result_2.png", dst)

# undistort
mapx, mapy = cv2.initUndistortRectifyMap(mtx, dist, None, newcameramtx, (w, h), 5)
dst = cv2.remap(img, mapx, mapy, cv2.INTER_LINEAR)
# crop the image
x, y, w, h = roi
if x!=1:
    dst = dst[y : y + h, x : x + w]

cv2.imwrite("./images/11r.png", dst)

tot_error = 0
for i in range(len(objpoints)):
    imgpoints2, _ = cv2.projectPoints(objpoints[i], rvecs[i], tvecs[i], mtx, dist)
    error = cv2.norm(imgpoints[i], imgpoints2, cv2.NORM_L2) / len(imgpoints2)
    tot_error += error

print("total error: ", tot_error / len(objpoints))