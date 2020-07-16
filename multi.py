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

images = glob.glob("./images/*.jpg")

for fname in images:
    img = cv2.imread(fname)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Find the chess board corners
    ret, corners = cv2.findChessboardCorners(gray, (7, 7), None)

    # If found, add object points, image points (after refining them)
    if ret == True:
        print("Found corners")
        objpoints.append(objp)
        imgpoints.append(corners)
        # corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
        # imgpoints.append(corners2)

        # Draw and display the corners
        img = cv2.drawChessboardCorners(img, (7, 7), corners, ret)
        cv2.imwrite(fname+".1_pattern.png", img)
        cv2.waitKey(500)
# => 패턴 검출을 통해 객체 지점(objpoints)과 이미지 지점(imgpoints)을 파악

ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(
    objpoints, imgpoints, gray.shape[::-1], None, None
)
print("mtx : ", mtx, "\ndist :", dist)

cv2.destroyAllWindows()

# 경로를 360 승주니이 주신거 하나만
#iimges = glob.glob("./testing/1c.jpg")

img = cv2.imread("./testing/1c.jpg")
# 이미지 크기 반환
h, w = img.shape[:2]
print("height  : ", h, ", width : ", w)
newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w, h), 1, (w, h))
#  => 카메라 왜곡 제거 전 : cv2.getOptimalNewCameraMatrix() 함수를 이용해 카메라 메트릭스를 구함
print("newcameramtx : \n", newcameramtx)
print("roi : \n", roi)


# undistort
dst = cv2.undistort(img, mtx, dist, None, mtx)
# dst = cv2.undistort(img, mtx, dist, None, newcameramtx)
# crop the image
# x, y, w, h = roi
# dst = dst[y : y + h, x : x + w]
cv2.imwrite('./output/1c.png', dst)
dst = cv2.undistort(img, mtx, dist, None, newcameramtx)
cv2.imwrite('./output/2c.png', dst)
"""
for fname in images:
    img = cv2.imread(fname)
    # 이미지 크기 반환
    h, w = img.shape[:2]
    print("height  : ", h, ", width : ", w)
    newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w, h), 1, (w, h))
    #  => 카메라 왜곡 제거 전 : cv2.getOptimalNewCameraMatrix() 함수를 이용해 카메라 메트릭스를 구함
    print("newcameramtx : \n", newcameramtx)
    print("roi : \n", roi)


    # undistort
    dst = cv2.undistort(img, mtx, dist, None, mtx)
    # dst = cv2.undistort(img, mtx, dist, None, newcameramtx)
    # crop the image
    # x, y, w, h = roi
    # dst = dst[y : y + h, x : x + w]
    cv2.imwrite(fname+'.png', dst)

    # tot_error = 0
    # for i in range(len(objpoints)):
    #     imgpoints2, _ = cv2.projectPoints(objpoints[i], rvecs[i], tvecs[i], mtx, dist)
    #     error = cv2.norm(imgpoints[i], imgpoints2, cv2.NORM_L2) / len(imgpoints2)
    #     tot_error += error

    # print("total error: ", tot_error / len(objpoints))
"""