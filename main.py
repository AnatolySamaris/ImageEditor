import cv2
import numpy as np
from tkinter import Tk, Label, Scale, Canvas, Button, Frame, LEFT, RIGHT
from tkinter.filedialog import askopenfilename, asksaveasfilename
from PIL import ImageTk, Image, ImageGrab


def open_image():
    global image
    path = askopenfilename(filetypes=[('Image Files', ('.png', '.jpg', '.jpeg'))])
    image = Image.open(path)
    image = np.array(image)
    canvas.delete('all')
    canvas.image = ImageTk.PhotoImage(Image.fromarray(image))
    canvas.create_image(0, 0, image=canvas.image, anchor='nw')


def display_image(image):
    canvas.delete('all')
    canvas.image = ImageTk.PhotoImage(Image.fromarray(image))
    canvas.create_image(0, 0, image=canvas.image, anchor='nw')


def save_image():
    global canvas
    img = ImageGrab.grab(bbox=(canvas.winfo_rootx() + 50, canvas.winfo_rooty() + 60,
                         canvas.winfo_rootx() + canvas.winfo_width() + 160,
                         canvas.winfo_rooty() + canvas.winfo_height() + 170))
    filepath = asksaveasfilename(defaultextension='.jpeg', filetypes=(('PNG', '*.png'), ('JPEG', '*.jpg;*.jpeg')))
    if filepath:
        img.save(filepath)


def brightness_adjust(image, value):
    brightness = value
    if brightness > 0:
        shadow = brightness
        highlight = 255
    else:
        shadow = 0
        highlight = 255 + brightness
    alpha_b = (highlight - shadow)/255
    gamma_b = shadow
    adjusted_image = cv2.addWeighted(image, alpha_b, image, 0, gamma_b)
    return adjusted_image


def contrast_adjust(image, value):
    alpha_c = value / 100
    adjusted_image = cv2.convertScaleAbs(image, alpha=alpha_c, beta=0)
    return adjusted_image


def negative(image):
    inverted_img = cv2.bitwise_not(image)
    return inverted_img


def blur(image, value):
    ksize = (value, value)
    blur_image = cv2.blur(image, ksize)
    return blur_image


def sharpen(image, value):
    kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
    sharpen_image = cv2.filter2D(image, -1, kernel)
    return sharpen_image


app = Tk()
app.title("Image Processing App")
app.geometry("750x650")

# Разметка рабочего окна
canvas_frame = Frame(app)
canvas_frame.pack(side=LEFT)
control_frame = Frame(app)
control_frame.pack(side=RIGHT)

canvas_spacer = Frame(canvas_frame, width=20)
control_spacer = Frame(control_frame, height=20)

canvas = Canvas(canvas_frame, width=600, height=600)
canvas.pack()

# Кнопки загрузки и сохранения изображения
button_save = Button(canvas_frame, text="Сохранить", command=save_image)
button_save.pack(side='right')

canvas_spacer.pack(side='right')

button_open = Button(canvas_frame, text="Открыть", command=open_image)
button_open.pack(side='right')

# Интерфейс фильтров
brightness_control = Scale(control_frame, from_=-100, to=100, orient="horizontal")
brightness_control.bind("<B1-Motion>",
                        lambda x: display_image(brightness_adjust(image, brightness_control.get())))
brightness_control.pack()
label_brightness = Label(control_frame, text="Яркость")
label_brightness.pack()

contrast_control = Scale(control_frame, from_=0, to=300, orient="horizontal")
contrast_control.bind("<B1-Motion>",
                       lambda x: display_image(contrast_adjust(image, contrast_control.get())))
contrast_control.pack()
label_contrast = Label(control_frame, text="Контрастность")
label_contrast.pack()

blur_control = Scale(control_frame, from_=1, to=50, orient="horizontal")
blur_control.bind("<B1-Motion>",
                lambda x: display_image(blur(image, blur_control.get())))
blur_control.pack()
label_blur = Label(control_frame, text="Размытие")
label_blur.pack()

sharpen_control = Scale(control_frame, from_=1, to=100, orient="horizontal")
sharpen_control.bind("<B1-Motion>",
                    lambda x: display_image(sharpen(image, sharpen_control.get())))
sharpen_control.pack()
label_sharpen = Label(control_frame, text="Резкость")
label_sharpen.pack()

control_spacer.pack()

button_negative = Button(control_frame, text="Негатив",
                        command=lambda: display_image(negative(image)))
button_negative.pack()


app.mainloop()