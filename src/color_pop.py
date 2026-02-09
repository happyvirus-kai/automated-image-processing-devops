def color_pop(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)

    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lower = np.array([35, 50, 50])   # green range
    upper = np.array([85, 255, 255])

    mask = cv2.inRange(hsv, lower, upper)
    result = image.copy()
    result[mask == 0] = gray[mask == 0]

    return result