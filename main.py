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

contours, contours_hierarchy = cv2.findContours(im_bw_dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
x = 2

# Draw the contours on the original image
color_pic = cv2.cvtColor(im_gray, cv2.COLOR_GRAY2RGB)
cv2.drawContours(color_pic, contours, -1, (0, 255, 0), 1)

# Display the image with contours
cv2.imshow('Contours', color_pic)
cv2.waitKey(0)
cv2.destroyAllWindows()

print('Threshold: '+str(threshold))

