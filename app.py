from tkinter import *
from tkinter import Label,Tk, ttk
from PIL import Image, ImageTk, ImageEnhance, ImageOps, ImageDraw
from tkinter import filedialog
from functools import partial

global window, image, canvas, canvas_img, temp_img

def save():
    temp_img.convert('RGB').save("edited_img.jpg")

def rotate():
    global image, rotations, temp_img
    temp_img = temp_img.rotate(90, expand=True)
    img = ImageTk.PhotoImage(temp_img)

    canvas.image = img
    canvas.itemconfigure(canvas_img, image=img)

def brightness(event):
    global image, temp_img
    temp_img = ImageEnhance.Brightness(temp_img).enhance(int(brightness_scale.get())/100.0)
    img = ImageTk.PhotoImage(temp_img)
    canvas.image = img
    canvas.itemconfigure(canvas_img, image=img)

def contrast(event):
    global image, temp_img
    temp_img = ImageEnhance.Contrast(temp_img).enhance(int(contrast_scale.get())/100.0)
    img      = ImageTk.PhotoImage(temp_img)
    canvas.image = img
    canvas.itemconfigure(canvas_img, image=img)

def saturation(event):
    global image, temp_img
    temp_img = ImageEnhance.Color(temp_img).enhance(int(saturation_scale.get())/100.0)
    img      = ImageTk.PhotoImage(temp_img)
    canvas.image = img
    canvas.itemconfigure(canvas_img, image=img)

def toBW():
    global image, temp_img
    temp_img = image.convert('LA')
    img      = ImageTk.PhotoImage(temp_img)
    canvas.image = img
    canvas.itemconfigure(canvas_img, image=img)

def to_blue():
    global image, temp_img
    temp_img = ImageOps.colorize(ImageOps.grayscale(temp_img), "#000066", "#9999CC")
    img      = ImageTk.PhotoImage(temp_img)
    canvas.image = img
    canvas.itemconfigure(canvas_img, image=img)

def flip_horizontally():
    global image, temp_img
    temp_img = temp_img.transpose(Image.FLIP_LEFT_RIGHT)
    img = ImageTk.PhotoImage(temp_img)

    canvas.image = img
    canvas.itemconfigure(canvas_img, image=img)

def flip_vertically():
    global image, temp_img
    temp_img = temp_img.transpose(Image.FLIP_TOP_BOTTOM)
    img = ImageTk.PhotoImage(temp_img)

    canvas.image = img
    canvas.itemconfigure(canvas_img, image=img)

def invert():
    global image, temp_img
    temp_img = ImageOps.invert(temp_img)
    img      = ImageTk.PhotoImage(temp_img)
    canvas.image = img
    canvas.itemconfigure(canvas_img, image=img)

def reset():
    global original_img, temp_img
    temp_img = image
    img      = ImageTk.PhotoImage(temp_img)
    canvas.image = img
    canvas.itemconfigure(canvas_img, image=img)

def paint(color):
    global canvas
    canvas.bind("<B1-Motion>", partial(pen, color))

def pen(color, event):
    global canvas
    x1, y1 =(event.x - 1), (event.y - 1)
    x2, y2 =(event.x + 1), (event.y + 1)

    draw = ImageDraw.Draw(temp_img)

    canvas.create_oval(x1, y1, x2, y2, outline=color, width=5)
    draw.ellipse([x1, y1, x2, y2], fill=color)


window = Tk()
window.title("Fake photoshop")
window.geometry('800x700')

path = filedialog.askopenfilename(filetypes=[("Image File",'.jpg')])
image = Image.open(path)
width, height = image.size
new_width = int(width / 3)
new_height = int(height / 3)

image = image.resize((new_width, new_height))
img = ImageTk.PhotoImage(image)
temp_img = image

canvas = Canvas(window, width=new_width, height=new_width, bg='black')
canvas_img = canvas.create_image(new_width/2, new_height/2, image=img)
canvas.pack(side="left", expand=True, fill="both")


rotate_button = ttk.Button(text="Rotate", command=rotate)
rotate_button.pack()

bw_button = ttk.Button(text="BlackWhite", command=toBW)
bw_button.pack()

blue_button = ttk.Button(text="Blue filter", command=to_blue)
blue_button.pack()

flip_h_button = ttk.Button(text="Flip horizontally", command=flip_horizontally)
flip_h_button.pack()

flip_v_button = ttk.Button(text="Flip vertically", command=flip_vertically)
flip_v_button.pack()

flip_v_button = ttk.Button(text="Invert colors", command=invert)
flip_v_button.pack()

flip_v_button = ttk.Button(text="Reset", command=reset)
flip_v_button.pack()

save_button = ttk.Button(text="Save", command=save)
save_button.pack()

brightness_scale = Scale(window, from_=0, to=200, orient=HORIZONTAL, label="Brightness", showvalue = 0)
brightness_scale.set(100)
brightness_scale.pack()
brightness_scale.bind("<ButtonRelease-1>", brightness)

contrast_scale = Scale(window, from_=0, to=200, orient=HORIZONTAL, label="Contrast", showvalue = 0)
contrast_scale.set(100)
contrast_scale.pack()
contrast_scale.bind("<ButtonRelease-1>", contrast)

saturation_scale = Scale(window, from_=0, to=200, orient=HORIZONTAL, label="Saturation", showvalue = 0)
saturation_scale.set(100)
saturation_scale.pack()
saturation_scale.bind("<ButtonRelease-1>", saturation)

button1=Button(window, text="", bg='black', command=partial(paint, 'black'))
button1.pack(side = "left")

button2=Button(window, text="", bg="red", command=partial(paint, 'red'))
button2.pack(side = "left")

button3=Button(window,text="", bg="pink", command=partial(paint, 'pink'))
button3.pack(side = "left")

button4=Button(window,text="", bg="yellow", command=partial(paint, 'yellow'))
button4.pack(side = "left")

button5=Button(window,text="", bg="purple", command=partial(paint, 'purple'))
button5.pack(side = "left")

window.mainloop()