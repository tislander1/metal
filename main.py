import cv2
import numpy as np

im_gray = cv2.imread('celeron_detail.png', cv2.IMREAD_GRAYSCALE)
(threshold, im_bw) = cv2.threshold(im_gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

kernel_strength = 3
kernel = np.ones((kernel_strength, kernel_strength), np.uint8) 
im_bw_eroded = cv2.erode(im_bw, kernel)
im_bw_dilated = cv2.dilate(im_bw_eroded, kernel)  
cv2.imwrite('bw_image.png', im_bw)
#cv2.imwrite('bw_image_eroded.png', im_bw_eroded)
cv2.imwrite('bw_image_dilated.png', im_bw_dilated)
print('Threshold: '+str(threshold))

