import cv2
import numpy as np
import random
import colorsys

def write_closed_contours_to_svg(svg_filename, contours):
    with open(svg_filename, 'w') as f:
        f.write('<svg xmlns="http://www.w3.org/2000/svg">\n')
        for contour in contours:
            #print(c[i][0])
            f.write('<path stroke="red" d="')
            last_item = len(contour) - 1
            for ix, point in enumerate(contour):
                if ix == 0:
                    f.write(' M' + str(point[0][0])+  ' ' + str(point[0][1])+' ')
                elif ix >= 0 and ix < last_item:
                    f.write(' L' + str(point[0][0])+  ' ' + str(point[0][1])+' ')
                elif ix > 0 and ix == last_item:
                    f.write(' L' + str(point[0][0])+  ' ' + str(point[0][1])+' Z')
            f.write('"/>\n')
        f.write('</svg>')

#hyperparameters to tune
erosion_dilation_kernel = 3
simplification_kernel = 4
min_allowed_contour_area = 3

scale_factor = 1

im_gray = cv2.imread('celeron_detail.png', cv2.IMREAD_GRAYSCALE)
(threshold, im_bw) = cv2.threshold(im_gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

kernel = np.ones((erosion_dilation_kernel, erosion_dilation_kernel), np.uint8) 
im_bw_eroded = cv2.erode(im_bw, kernel)
im_bw_dilated = cv2.dilate(im_bw_eroded, kernel)  
cv2.imwrite('bw_image.png', im_bw)
#cv2.imwrite('bw_image_eroded.png', im_bw_eroded)
cv2.imwrite('bw_image_dilated.png', im_bw_dilated)

contours, contours_hierarchy = cv2.findContours(im_bw_dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

#import shapely
# shapely_polygons = []
# for contour in contours:
#     poly = shapely.Polygon([(int(item[0][0]), int(item[0][1])) for item in contour])
#     shapely_polygons.append(poly)
# shapely_tolerance = 3
# simplified_polygons = []
# for this_polygon in shapely_polygons:
#     simplified_polygons.append(shapely.simplify(this_polygon, tolerance=shapely_tolerance, preserve_topology=True))


simplified_contours = []
for contour in contours:
    approx_contour = cv2.approxPolyDP(curve=contour, epsilon=simplification_kernel, closed=True)
    simplified_contours.append(approx_contour)


simplified_large_contours = []
for contour in simplified_contours:
    if cv2.contourArea(contour) > min_allowed_contour_area:
        simplified_large_contours.append(contour)
x = 2

# Draw the contours on the original image
color_pic = cv2.cvtColor(im_gray, cv2.COLOR_GRAY2RGB)
for contour in simplified_large_contours:
    #get a random brightly saturated color
    h,s,l = random.random(), 0.5 + random.random()/2.0, 0.4 + random.random()/5.0
    r,g,b = [int(256*i) for i in colorsys.hls_to_rgb(h,l,s)]
    cv2.drawContours(color_pic, [contour], -1, (r,g,b), 1)

cv2.imwrite('color_pic.png', color_pic)

write_closed_contours_to_svg('svg_file.svg', simplified_large_contours)

# Display the image with contours
cv2.imshow('Contours', color_pic)
cv2.waitKey(0)
cv2.destroyAllWindows()

print('Threshold: '+str(threshold))

print('Done!')