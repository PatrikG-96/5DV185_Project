from framework.recognition import Recognition
from skimage.segmentation import clear_border
import pytesseract
import numpy as np
import imutils
import cv2
from paddleocr import PaddleOCR


class ANPR:

    LICENSE_PLATE_WIDTH = 13
    LICENSE_PLATE_HEIGHT = 5

    def __init__(self, minAspectRatio:int = 4, maxAspectRatio : int = 5, debugMode : bool = False) -> None:
        self.minAr = minAspectRatio
        self.maxAr = maxAspectRatio
        self.debug = debugMode
        pytesseract.pytesseract.tesseract_cmd = r"C:/Program Files/Tesseract-OCR/tesseract.exe"

    def __debug_show_image(self, title, image, wait=False):

        if self.debug:
            cv2.imshow(title,image)

            if wait:
                cv2.waitKey(0)

    def make_gray(self, image):

        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


    def licence_plate_candidates(self, image, keep = 5):

        # we want to find a license plate, therefore we use a rectangular shape the size/ratio of an international license plate as the structuring element
        # used to define how to perform morphological operations
        rect_structuring_element = cv2.getStructuringElement(cv2.MORPH_RECT, (ANPR.LICENSE_PLATE_WIDTH, ANPR.LICENSE_PLATE_HEIGHT)) 

        # perform blackhat morhology - highlights dark objects with a light background (like black text in a white box...)
        blackhat = cv2.morphologyEx(image, cv2.MORPH_BLACKHAT, rect_structuring_element)

        self.__debug_show_image("After blackhat", blackhat)

        # use close morphology - fills in smaller holes in the image and preserving the larger holes
        square_structuring_element = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        light = cv2.morphologyEx(image, cv2.MORPH_CLOSE, square_structuring_element)

        # In essence - splits image in foreground and background using Otsu's algorithm
        _,light = cv2.threshold(light,0,255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)

        self.__debug_show_image("Light", light)

        # Edge detection using Scharr gradient - only on x-axis as most character edges are horizontal
        gradX = cv2.Sobel(blackhat, ddepth=cv2.CV_32F, dx=1, dy=0, ksize=-1)
        gradX = np.absolute(gradX)

        # Scale the gradient values back to the range [0,255] and convert to 8 bit integer
        (minVal, maxVal) = (np.min(gradX), np.max(gradX))
        gradX = 255 * ((gradX-minVal)/ (maxVal - minVal))
        gradX = gradX.astype("uint8")

        self.__debug_show_image("Scharr", gradX)

        # Reduce noise in the image - makes it smoother 
        gradX = cv2.GaussianBlur(gradX, (5,5), 0)

        # Apply close and otsu again - fill in hole and split into background7foreground
        gradX = cv2.morphologyEx(gradX, cv2.MORPH_CLOSE, rect_structuring_element)
        _, threshold = cv2.threshold(gradX, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

        self.__debug_show_image("Grad thresh", threshold)

        # Reduce noise by removing smaller white areas - erosion removes edges objects, dilate adds to the edges of objects
        # erode - remove small clutter
        # dilate - add back the eroded pixels to the bigger white areas
        threshold = cv2.erode(threshold, None, iterations=2)
        threshold = cv2.dilate(threshold, None, iterations=2)

        self.__debug_show_image("Grad erode/dilate", threshold)

        # Combine threshold with light image with bitwise and, get our candidates for licence plates
        threshold = cv2.bitwise_and(threshold, threshold, mask = light)
        threshold = cv2.dilate(threshold, None, iterations=2)
        threshold = cv2.erode(threshold, None, iterations=1)

        self.__debug_show_image("Final", threshold, wait=True)

        contours = cv2.findContours(threshold.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours = imutils.grab_contours(contours)
        contours = sorted(contours, key=cv2.contourArea, reverse=True)[:keep]

        return contours

    def most_likely_candidate(self, gray_image, candidates, clear_border_flag = False):
        
        license_plate_contour = None

        region = None

        for candidate in candidates:

            (x, y, width, heigth) = cv2.boundingRect(candidate)
            aspect_ratio = width / float(heigth)

            print(f"aspect_ratio: {aspect_ratio}")

            if aspect_ratio >= self.minAr and aspect_ratio <= self.maxAr:

                license_plate_contour = candidate

                license_plate = gray_image[y:y+heigth, x:x+width]

                _, region = cv2.threshold(license_plate, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

                if clear_border_flag:
                    region = clear_border(region)

                self.__debug_show_image("plate", license_plate)
                self.__debug_show_image("roi", region, wait=True)
                break
        return (region, license_plate_contour)

    def tesseract_options(self, psm=7):

        whitelist = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        options = "-c tessedit_char_whitelist={}".format(whitelist)
        options += " --psm {}".format(psm)
        return options

    def find_license_plate(self, image, psm=7, clear_border = False):

        license_plate_text = None

        gray_image = self.make_gray(image)

        candidates = self.licence_plate_candidates(gray_image)

        license_plate, contour = self.most_likely_candidate(gray_image, candidates, clear_border)

        if license_plate is not None:

            options = self.tesseract_options(psm = psm)
            license_plate_text = pytesseract.image_to_string(license_plate, config=options)
            
        cv2.destroyAllWindows()
        return license_plate_text


class RegPlateRecognition(Recognition):

    def __init__(self) -> None:
        super().__init__()
        self.anpr = ANPR(debugMode=False)

    def debug_mode(self, mode : bool) -> None:
        self.anpr.debug = mode

    def predict(self, data : dict) -> str:
        
        if not data.get("image"):
            return

        return self.anpr.find_license_plate(image=data['image'])