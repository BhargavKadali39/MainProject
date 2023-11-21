
import cv2
import pytesseract
import win32com.client
from nltk.corpus import words
from pytesseract import Output
from textblob import TextBlob

import picTaker as pt


def pre_process_image(texts):
    """This function will pre-process a text with:
    TextBlob & text.correct
    so it can be processed for the further step i.e confidence checking """

    print("[INFO] Text Blob Applied")
    Text = TextBlob(texts)
    return Text.correct()



def is_english_word(word):
    # Move the below two lines as a global scope variables.
    # Only kept here to indicate the functionality and for more readability
    word = word.lower()
    english_words = set(words.words())
    if word in english_words:
        return True
    else:
        return False


def calculate_confidence(text, words_left):
    # try for Divided by 0 exception
    try:
        # Split the text into words
        words = text.split()
        # Calculate the total number of words in the text
        total_words = len(words)
        # Calculate the ratio of words left after processing
        words_left_ratio = words_left / total_words
        # Calculate the confidence as the percentage of words left
        confidence = words_left_ratio * 100
        # Return the confidence value
        return confidence
    except:
        return 0


print("[INFO] Started")
chs = input("Enter 1 to take img through camera\nEnter 2 to give image path\n")

if(chs=="1"):
    pt.captureImage()
    
    # sample_img = "F:/2_studiocode/FinalMainProj/test1/myImages/takenImage.jpg"
    sample_img = "F:/2_studiocode/lastVerMain/myImages/takenImage.jpg"
else:
    sample_img = input("Enter image path and make sure it's in jpg")


# psm 12 is good for digital text
# psm 6 is good for Handwritten text

mconfig  = r"--psm 12 --oem 3 "
mconfig2  = r"--psm 6 --oem 3 "

# Some image paths for testing
imgp="F:/2_studiocode/FinalMainProj/test1/myImages/pic2.jpg"
imgp="F:/2_studiocode/FinalMainProj/test1/myImages/pic1h0.jpg"
imgp="F:/2_studiocode/lastVerMain/myImages/pic4.jpg"

img = cv2.imread(sample_img)
print("[INFO] loaded imgs")
showImg=img
resStr=''
data = pytesseract.image_to_data(img,config=mconfig,output_type=Output.DICT)
for i in range(len(data['text'])):
    if float(data['conf'][i]) > 4 :
        (x , y , w, h ) = (data['left'][i],data['top'][i],data['width'][i],data['height'][i])
        # showImg = cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
        resStr= resStr + data['text'][i]+ " "
# cv2.imshow("img",showImg)
# cv2.waitKey(0)


hypothesis0 = resStr



hypothesis1 = pre_process_image(resStr)
print("[INFO] text pre_processing done")

hypothesis2 = pytesseract.image_to_string(img,config=mconfig2)



print("[INFO] H0")
print(hypothesis0)

print("[INFO] H1")
print(hypothesis1)

print("[INFO] H2")
print(hypothesis2)


print("[INFO] Checking Confidence")
words_left0 = len(hypothesis0.split())
for i in hypothesis0.split():
    if (is_english_word(i) == False):
        words_left0-=1
confidence0 = calculate_confidence(hypothesis0, words_left0)
# print("Confidence: {:.2f}%".format(confidence0))

words_left1 = len(hypothesis1.split())
for i in hypothesis1.split():
    if (is_english_word(i) == False):
        words_left1-=1
confidence1 = calculate_confidence(hypothesis1, words_left1)
# print("Confidence: {:.2f}%".format(confidence1))

words_left2 = len(hypothesis2.split())
for i in hypothesis2.split():
    if (is_english_word(i) == False):
        words_left2-=1
confidence2 = calculate_confidence(hypothesis2, words_left2)
# print("Confidence: {:.2f}%".format(confidence2))


speakText = hypothesis1

# Passing the best hypothesis that we want to convert to audio
if confidence0 > confidence1 and confidence0 > confidence2:
    speakText = hypothesis0
elif confidence1 > confidence0 and confidence1 > confidence2:
    speakText = hypothesis1
else:
    speakText = hypothesis2




# text = hypothesis1
# print(text)
# mytext="".join(c for c in mytext if c.isalpha() or c.isnumeric())


# Create TTS object
tts = win32com.client.Dispatch("SAPI.SpVoice")

# Set properties for voice (optional)
tts.Rate = 2.5  # Speech rate
tts.Volume = 100.0  # Volume level

# Convert text to speech
print("[INFO] Playing the audio")
tts.Speak(speakText)





"""
F:/2_studiocode/lastVerMain/myImages/pic2.jpg

F:/2_studiocode/lastVerMain/myImages/pic1h0.jpg

F:/2_studiocode/lastVerMain/myImages/pic4.jpg

F:/2_studiocode/lastVerMain/myImages/pic2.jpg
2

good combo
mconfig  = r"--psm 12 --oem 3 "
imgp="F:/2_studiocode/FinalMainProj/test1/myImages/pic1h0.jpg"
mconfig  = r"--psm 6 --oem 3 "
imgp="F:/2_studiocode/FinalMainProj/test1/myImages/pic2.jpg"


--------------------------------------------
6 better
text = pytesseract.image_to_string(Image.open("F:/2_studiocode/FinalMainProj/test1/myImages/pic1h0.jpg"),config=mconfig)
text = pytesseract.image_to_string(Image.open(imgp),config=mconfig)
print(f"text {text}") 
--------------------------------------------

for box in boxes.splitlines():
    box = box.split(" ")
    img = cv2.rectangle(img, (int(box[1]),h-int(box[2])),(int(box[3]),h-int(box[4])),(0,255,0),2)
    print(box[0],end='')

boxes = pytesseract.image_to_boxes(img,config=mconfig)
"""


