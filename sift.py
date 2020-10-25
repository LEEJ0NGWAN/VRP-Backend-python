
from PIL import Image
import os
import numpy as np
import cv2
from matplotlib import pyplot as plt
import subprocess
from util import getYawPitch

def init(data_list):

    # popen = subprocess.Popen("extract_panorama_partial.exe", shell=True)
    # output = popen.wait()

    # print(output)

    call = subprocess.call([
        "/usr/bin/open", "-W", "-n", "-a", 
        os.getcwd()+"/extract_panorama_partial.app"])


def work(sinput='./sinput.jpg'):

    for cnt in range(0,8):
        for cnt2 in range(0,8):
            print(str(cnt)+" "+str(cnt2)+":================")
            dir_file=str.format('./extract_panorama_partial.app/Contents/screenShots/screen_{0}_{1}.png',cnt,cnt2)
            img1 = cv2.imread(dir_file,0) #big
            img2 = cv2.imread(sinput,0) #small

            sift = cv2.xfeatures2d.SIFT_create()
            
            kp1, des1 = sift.detectAndCompute(img1,None)
            kp2, des2 = sift.detectAndCompute(img2,None)

            bf = cv2.BFMatcher()
            matches = bf.knnMatch(des1,des2, k=2)

            good = []

            for i, (m,n) in enumerate(matches):
                if m.distance < 0.5*n.distance:
                    good.append([m])
                    # img1_idx = m.queryIdx
                    # img2_idx = m.trainIdx

                    # x - columns
                    # y - rows
                    # Get the coordinates
                    # print(kp1[i].pt)
                    # print(kp2[i].pt)

            for goodie in good:
                a = goodie[0].imgIdx
                b = goodie[0].queryIdx
                c = goodie[0].trainIdx

                # print(kp1[b].pt)
                x, y = kp1[b].pt
                print(getYawPitch(x,y,cnt,cnt2))

