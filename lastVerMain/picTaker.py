import cv2


def captureImage():
    
    # Start the video camera
    vc = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    # Function to save the image
    def saveImage(image):

        # Save the images inside the  folder
        cv2.imwrite("F:/2_studiocode/lastVerMain/myImages/takenImage.jpg", image)
        print("[INFO] Image has been saved in folder")

    print("[INFO] Video Capture is now starting please stay still...")

    while True:
        # Capture the frame/image
        _, img = vc.read()

        # Show the image
        cv2.imshow("Press s to save and q to exit the window", img)

        # Wait for user keypress
        key = cv2.waitKey(1) & 0xFF

        # Check if the pressed key is 'k' or 'q'
        if key == ord('s'):
            saveImage(img)
            break

    print("[INFO] Picture Captured")

    # Stop the video camera
    vc.release()
    # Close all Windows
    cv2.destroyAllWindows()

