import cv2

pic = cv2.imread("./720/right_wink.jpg")
cv2.namedWindow("vision",1) #1 代表窗口大小等于图片大小,不可以被拖动改变大小.   
cv2.imshow("vision",pic)
cv2.moveWindow("vision",0,100)
cv2.waitKey(1000)
cv2.destroyAllWindows()#结束所有打开窗口