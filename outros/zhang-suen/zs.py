import cv2

image = cv2.imread("teste.bmp")
thinned = cv2.ximgproc.thinning(cv2.cvtColor(image, cv2.COLOR_RGB2GRAY))
cv2.imshow('image',thinned)
cv2.waitKey(0)