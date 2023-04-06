import cv2

def imgProc(fgndMask):
    structuringElement = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))

    fgndMask = cv2.GaussianBlur(fgndMask, (5, 5), 0)

    ret, fgndMask = cv2.threshold(fgndMask, 128, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    fgndMask = cv2.morphologyEx(fgndMask, cv2.MORPH_CLOSE, structuringElement, iterations=2)
    fgndMask = cv2.morphologyEx(fgndMask, cv2.MORPH_OPEN, structuringElement, iterations=2)

    return fgndMask
