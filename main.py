import cv2
from screeninfo import get_monitors
from tkinter import filedialog, Tk, Button, Label


def sketch(image):
    gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    blur_gray = cv2.GaussianBlur(gray,(5,5),900)
    edges = cv2.Canny(blur_gray,45,90)
    ret,thre = cv2.threshold(edges,70,255,cv2.THRESH_BINARY_INV)
    return thre

cam = cv2.VideoCapture(0)

def live():
    while 1:
        ret,frame = cam.read()
        screen = get_monitors()[0]
        frame_resized = cv2.resize(frame, (screen.width, screen.height))  
        sketch_resized = sketch(frame_resized)
        cv2.imshow('Live Sketch', sketch_resized)
        if cv2.waitKey(1)==27:
            break
        if cv2.waitKey(1)==13:
            cv2.imwrite('live_Captured_sketch.jpg',sketch_resized)
            print('Image Saved!!!')

def load_image():
    root = Tk()
    root.withdraw()  # Hide the root window
    file_path = filedialog.askopenfilename()
    if file_path:
        image = cv2.imread(file_path)
        sketch_image = sketch(image)
        cv2.imshow('Live Sketch', sketch_image)
        cv2.imwrite('local_Img_sketch.jpg', sketch_image)
        return
    else:
        return None


option = input("Enter your choice:\n\n 1. Capture a live snapshot and save it as a sketch\n 2. Start a live stream\n 3. Select an image file from your device\nPlease enter the number of your chosen action: ")


if option == '1':
    ret, frame = cam.read()
    if ret:
        cv2.imwrite('Captured_sketch.jpg', sketch(frame))
        print('Image Saved!!!')
    else:
        print("Failed to grab frame")
elif option == '2':
    live()
elif option == '3':
    root = Tk()
    root.title("Select Image")
    root.geometry("300x200")
    
    def on_button_click():
        global image
        image = load_image()
        root.destroy()

    Label(root, text="Click the button to select an image file").pack(pady=20)
    Button(root, text="Select Image", command=on_button_click).pack(pady=10)
    
    root.mainloop()
else:
    print("Invalid option selected")



cam.release()
cv2.destroyAllWindows()