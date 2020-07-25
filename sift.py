
from PIL import Image
import numpy as np
import cv2
from matplotlib import pyplot as plt
import subprocess

popen=subprocess.Popen("extract_panorama_partial.exe")
output = popen.wait()

print(output)


for cnt in range(0 , 64):
    row = cnt/8
    col = cnt%8
    dir_file=str.format('./extract_panorama_partial_Data/screenShots/screen_{0}_{1}.png',row,col)
    img1 = cv2.imread(dir_file,0) #big
    img2 = cv2.imread('./feature/partialinput/sinput.jpg',0) #small
 
    sift = cv2.xfeatures2d.SIFT_create()
 
    kp1, des1 = sift.detectAndCompute(img1,None)
    kp2, des2 = sift.detectAndCompute(img2,None)
 
    bf = cv2.BFMatcher()
    matches = bf.knnMatch(des1,des2, k=2)
 
    good = []
    for m,n in matches:
        if m.distance < 0.4*n.distance:
            good.append([m])
 
    img4 = cv2.drawMatchesKnn(img1,kp1,img2,kp2,good,None,flags=2)
 
    plt.imshow(img4),plt.show()

    img = Image.fromarray(img4, 'RGB')
    dir_outfile=str.format('output{0}.png',cnt)
    img.save(dir_outfile)

#크기가 너무 크면 압축해야함. 아니면 졸라게 오래 걸림
#YAW,PITCH,FOV는 최적 구해야 함
#feature matching output도 압축이 가능한지 확인 해봐야함
#비교 결과
#정답에 영향을 주는 변인 요소 : fov, 상수, geometry map(cubemap, 6-sided, panoramic), 화질
#1) fov 90 , 상수 0.5 정확도 : 제일 잘 찾은게 특징점 3개. 특징점 1,2개는 많았고 정확히 찾았으나, 정답이 아닌 특징점도 발생함 
#2) fov 100 , 상수 0.4 정확도 :  거의 못찾음. 제일 잘 찾은게 특징점 1개.
