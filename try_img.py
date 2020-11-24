import cv2

image = cv2.imread('/home/pi/share/slideimage3.jpg')
overlay = image.copy()
dimensions = image.shape
print(dimensions)
x, y, w, h = 0, 0, 100, dimensions[0]  # Rectangle parameters
cv2.rectangle(overlay, (x, y), (w, y+h), (0, 200, 0), -1)  # A filled rectangle
x, y, w, h = 0, 0, dimensions[1], 80  # Rectangle parameters
cv2.rectangle(overlay, (x, y), (w+h, h), (0, 200, 0), -1)  # A filled rectangle

alpha = 0.15  # Transparency factor.

# Following line overlays transparent rectangle over the image
image_new = cv2.addWeighted(overlay, alpha, image, 1 - alpha, 0)
cv2.imshow('img',image_new)
cv2.waitKey(0)