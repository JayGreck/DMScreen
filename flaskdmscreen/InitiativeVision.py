import cv2
import pytesseract
import random
import numpy as np


class InitiativeVision:
    pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

    def __init__(self, image):
        self.img1 = cv2.imread("flaskdmscreen/static/statblocks/" + image)
        self.img = cv2.resize(self.img1, None, fx=2, fy=2,  interpolation=cv2.INTER_CUBIC)
        self.thresh, self.im_bw = cv2.threshold(self.img, 127, 255, cv2.THRESH_BINARY) #was 210, 230

    
        image1 = cv2.bitwise_not(self.im_bw)
        kernel = np.ones((2,2),np.uint8)
        image1 = cv2.erode(image1, kernel, iterations=1)
        image1 = cv2.bitwise_not(image1)


    
        self.imgRGB = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY) # Pytesseract only accepts RGB, originally pasing in self.img
       
        
    
    
    def detectWord(self):
        imgHeight, imgWidth, _ = self.img.shape
        boxes = pytesseract.image_to_data(self.imgRGB)
        word_row = False
        statblock_name_list = []
        for x,b in enumerate(boxes.splitlines()):
            
            if x != 0: # Not equal to the first row

                b = b.split()
                if len(b) == 12: # Length of 12 indicates that there is a word
                    
                


                    if b[11] == "Tiny" or b[11] == "Small" or b[11] == "Medium" or b[11] == "Large" or b[11] == "Huge" or b[11] == "Gargantuan":
                        word_row = True
                    elif word_row != True:
                        
                        statblock_name_list.append(str(b[11]))
                        
                       
                   
                        
                
                    x,y,w,h = int(b[6]), int(b[7]), int(b[8]), int(b[9]) # used for our bounding box values
                    if b[11] == 'DEX':
                        
                        rows, cols, _ = self.img.shape

                        roi = self.img[y: h*4+y, x: w+x+30]
                        cv2.imwrite("roi.jpg", roi)
                        cropped = cv2.imread("roi.jpg")
                        resize = cv2.resize(cropped, None, fx=3, fy=3) # was 2, 2
                        croppedRGB = cv2.cvtColor(resize, cv2.COLOR_BGR2GRAY)
                        break
            
                    ### Create Rectangle
                    else:
                        cv2.rectangle(self.img, (x,y), (w+x,h+y), (255, 0, 0), 1)
                       
                

        name = ' '.join(statblock_name_list).lower()
        print(name)
        
    
        try:
            boxes = pytesseract.image_to_data(croppedRGB, config='--psm 6')
            numbers_detected = []
            for z,bx in enumerate(boxes.splitlines()):
                if z != 0:
                
                    bx = bx.split()
                    
                    if len(bx) == 12:
                    
                        
                        if bx[11].find('-') == True:
                            number_append = ''.join(filter(str.isdigit, bx[11]))
                            add_minus_sign = "-"
                            number_append = add_minus_sign + number_append
                        else:
                            number_append = ''.join(filter(str.isdigit, bx[11]))
                            print(number_append)
                        if number_append != "":
                            numbers_detected.append(int(number_append))
                            initiative_modifier = min(numbers_detected)

            print("Initiative Bonus = " + str(initiative_modifier))
            initiative_roll = random.randint(1,20) + initiative_modifier
            print(initiative_roll)

            return initiative_modifier, initiative_roll, name 
        except:
            return 1, 1, 1    







#print(pytesseract.image_to_boxes(imgRGB))


#### Detecting characters
#imgHeight, imgWidth, _ = img.shape
#boxes = pytesseract.image_to_boxes(imgRGB)
#for b in boxes.splitlines():
    #b = b.split(' ')
    #print(b)
    #x,y,w,h = int(b[1]), int(b[2]), int(b[3]), int(b[4])

    ### Create Rectangle
    #cv2.rectangle(img, (x,imgHeight-y), (w,imgHeight-h), (255, 0, 0), 1)
    #cv2.putText(img, b[0], (x,imgHeight-y+25), cv2.FONT_HERSHEY_COMPLEX, 1, (255,0,0), 1)

# #### Test
# img_w = 1000 # = cvImage.width
# img_h = 1000 # = cvImage.height
# tl_x = 10.0 / 100.0
# tl_y = 10.0 / 100.0
# br_x = 90.0 / 100.0
# br_y = 90.0 / 100.0

# print (tl_x, tl_y, br_x, br_y)

# rect_tl = (int(tl_x * img_w), int(tl_y * img_h))
# rect_br = (int(br_x * img_w), int(br_y * img_h))

# print (rect_tl, rect_br)

#cv.rectangle(cvImage, rect_tl, rect_br, (255,0,0), 2)

#### Detecting words

                

# cv2.imshow("Test", self.cropped)
# cv2.imshow("Image", self.img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()