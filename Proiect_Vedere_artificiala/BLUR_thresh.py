import cv2


# Load the image
image_path = 'urban4.jpg'  
image = cv2.imread(image_path)

total = 0
min_area_threshold = 2100  
aspect_ratio_range = (0.7, 1) 
blockSize = 87  
C = 2 

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

blurred = cv2.GaussianBlur(gray, (7, 7), 0)  

thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, blockSize, C)

contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

contoured_image = image.copy()
cv2.drawContours(contoured_image, contours, -1, (0, 255, 0), 2)


def could_be_e_scooter(contour, min_area_threshold, aspect_ratio_range):
    area = cv2.contourArea(contour)
    print("Area= ",area)
    if area < min_area_threshold:
        return False
    x, y, w, h = cv2.boundingRect(contour)
    aspect_ratio = float(w) / h
    min_aspect_ratio, max_aspect_ratio = aspect_ratio_range
    return min_aspect_ratio < aspect_ratio < max_aspect_ratio

# Search for the e-scooter in the image
for c in contours:
    if could_be_e_scooter(c, min_area_threshold, aspect_ratio_range):
        print("Found a contour that could be an e-scooter!")
        x, y, w, h = cv2.boundingRect(c)
        print("x= ",x, "y= ",y)
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        total += 1

# Convert image for displaying
marked_image =  image.copy()
# Display the images
cv2.imshow('Gray', gray)
cv2.imshow('Blurred', blurred)
cv2.imshow('Threshold', thresh)
cv2.imshow('Detection', marked_image)
cv2.imshow('Reduced Contours', contoured_image)
print('Total of e-scooters= ', total)
print("min_area_threshold ",min_area_threshold)
# Wait for a key press and then close all image windows
cv2.waitKey(0)
cv2.destroyAllWindows()
