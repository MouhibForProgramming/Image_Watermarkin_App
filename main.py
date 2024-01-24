# -------------------Image Watermarking App-------------------------------
from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk, ImageDraw, ImageFont
import time
# ----------------------Application Functionality----------------------------------------

edit_text = None
image_file_path = None
new_image_file = ""
updated_image = []


def upload_image():
    global image_file_path
    f_types = [("Jpg files", "*.jpg"), ("PNG files", "*.png")]
    image_file_path = filedialog.askopenfile(filetypes=f_types, title="Select a image file")
    if image_file_path:
        image = Image.open(image_file_path.name)

        image_file.insert(0, image_file_path.name)
        new_image = ImageTk.PhotoImage(image)
        image_container.config(image=new_image)
        image_container.image = new_image
        # image_file.delete(0, END)
        updated_image.append(image_file_path.name)
        print(updated_image)

def add_watermark_text():
    global image_file_path
    number_image = 0
    original_image = Image.open(image_file_path.name)

    # define Font
    font = ImageFont.truetype("arial.ttf", size=28)
    # get the text to added
    watermark_text = text_box.get()
    # Edit image
    draw = ImageDraw.Draw(original_image)
    # ad text to the image
    x = original_image.size[0] / 2
    y = original_image.size[1] / 2
    draw.text((int(x), int(y)), watermark_text, fill="#FFF", font=font, stroke_fill="#222", anchor="ms")
    number_image += 1
    new_image_file = image_file_path.name[:image_file_path.name.find(".")] + str(
        number_image) + "." + original_image.format
    original_image.save(fp=f'{new_image_file}')
    display_updated_pc(new_image_file)

    updated_image.append(new_image_file)


def display_updated_pc(file_path):
    modified_image = Image.open(file_path)
    update_image = ImageTk.PhotoImage(modified_image)
    image_container.config(image=update_image)
    image_container.image = update_image


def reset_text():
    global image_file_path
    image = Image.open(image_file_path.name)
    new_image = ImageTk.PhotoImage(image)
    image_container.config(image=new_image)
    image_container.image = new_image


def apply_changes():
    global image_file_path
    size_selected = edit_font_size.get()

    selected_color = current_value.get()
    new_image = Image.open(image_file_path.name)
    draw_image = ImageDraw.Draw(new_image)
    font = ImageFont.truetype("arial.ttf", int(size_selected))
    x = (new_image.size[0] / 2)
    y = (new_image.size[1] / 2)
    if selected_color == "select a color":
        selected_color = "#FFF"

    draw_image.text((int(x), int(y)), text_box.get(), fill=selected_color, font=font, stroke_fill="#222", anchor="ms")

    new_image_file = image_file_path.name[:image_file_path.name.find(".")] + str(
        2) + "." + new_image.format

    new_image.save(new_image_file)
    display_updated_pc(new_image_file)
    updated_image = new_image_file


def add_image_watermark():
    global updated_image
    logo_file_path = filedialog.askopenfile(filetypes=[("Png files", ".*png")])
    if logo_file_path:
        # overlay image(logo) over another image
        fp = open(updated_image[0], mode="rb")
        main_image = Image.open(fp)
        logo = Image.open(logo_file_path.name)
        add_logo.insert(index=0,string=logo_file_path.name)
        # x = main_image.width - logo.size[0]
        # y = main_image.width - logo.size[1]
        main_image.paste(logo, (0, 0))
        name_file_path = "new_image.png"
        main_image.save(name_file_path)
        display_updated_pc(name_file_path)

def save_image():
    global updated_image
    new_image = Image.open(updated_image[0])
    new_image.save("image_saved.png")


# -------------------GUI DESIGN(layout)---------------------------------------


window = Tk()
window.config(padx=50, pady=100, bg="skyblue")
window.title("Imager Watermarking App")

primary_right_frame = Frame(window, width=500, height=700, bg="purple")
primary_right_frame.grid(row=0, column=1, padx=10, pady=5)
add_watermark_to_image_text = Label(primary_right_frame, text="Add Watermark", fg="#789461", bg="purple",
                                    font=("arial", 20, "bold"))
add_watermark_to_image_text.grid(row=0, column=1, padx=5, pady=5)
left_frame = Frame(window, width=500, height=800, border=0, bg="#E1F0DA")
right_frame = Frame(primary_right_frame, width=700, height=700, bg="#E6A4B4")
left_frame.grid(row=0, column=0, padx=10, pady=5)
right_frame.grid(row=1, column=1, padx=10, pady=5)
# upload image button
# my_image = Image.open("background (1).png")
# my_image = PhotoImage(file="background (1).png")
image_container = Label(left_frame, text="image is here", bg="#E1F0DA", fg="green", font=("arial", 66, "bold"))
image_container.grid(row=0, column=0, padx=5, pady=22)

# create all the needed widgets to add some watermark to the image(logo/text).
# all widgets within the right frame.
image_text = Label(right_frame, text="Image File:", highlightthickness=0, bg="skyblue", fg="#D04848")
image_text.grid(row=0, column=0, padx=5, pady=30)
image_file = Entry(right_frame, width=100, highlightthickness=0)
image_file.grid(row=0, column=1, padx=5, pady=30)
upload_image_bt = Button(right_frame, text="Upload image", highlightthickness=0, width=25, border=3, bg="#DCFFB7",
                         command=upload_image)
upload_image_bt.grid(row=0, column=2, padx=5, pady=30)
add_text = Label(right_frame, text="Add Text", highlightthickness=0, bg="skyblue", fg="#D04848")
add_text.grid(row=1, column=0, padx=5, pady=30)

text_box = Entry(right_frame, width=50)
text_box.grid(row=1, column=1, padx=5, pady=30)
add_text_button = Button(right_frame, text="add watermark text", bg="#DCFFB7", highlightthickness=0, width=25, border=3,
                         command=add_watermark_text)
add_text_button.grid(row=1, column=2, padx=5, pady=30)
reset_text_bt = Button(right_frame, text="reset text", bg="#DCFFB7", highlightthickness=0, width=10, border=3,
                       command=reset_text)
reset_text_bt.grid(row=1, column=3, padx=5, pady=10)
text_font_size = Label(right_frame, text="font size:", highlightthickness=0, bg="skyblue", fg="#D04848")
text_font_size.grid(row=2, column=0, padx=5, pady=30)
# get hold the current value in the spinbox
value_inside = IntVar(right_frame)
edit_font_size = Spinbox(right_frame, from_=8, to=72, width=25, highlightthickness=0, textvariable=value_inside,
                         wrap=True)
edit_font_size.grid(row=2, column=1, padx=5, pady=30)

text_color = Label(right_frame, text="Choose a color", bg="skyblue", fg="#D04848")
text_color.grid(row=3, column=0, padx=5, pady=30)
current_value = StringVar(window)
current_value.set("select a color")
color_select = OptionMenu(right_frame, current_value,
                          *[color for color in ["red", "blue", "green", "yellow", "grey", "purple", "black", "white"]])
color_select.grid(row=3, column=1, padx=5, pady=30)

# add logo
add_logo_text = Label(right_frame, text="Add Logo", bg="skyblue", fg="#D04848")
add_logo_text.grid(row=4, column=0, padx=5, pady=30)
add_logo = Entry(right_frame, width=50)
add_logo.grid(row=4, column=1, padx=5, pady=5)
upload_log_bt = Button(right_frame, text="upload logo",command=add_image_watermark  , width=25, bg="#DCFFB7", highlightthickness=0, border=3)
upload_log_bt.grid(row=4, column=2, padx=5, pady=30)

save_image_bt = Button(right_frame, text="Save Image", width=20, bg="#AAD9BB", highlightthickness=0, command=save_image)
save_image_bt.grid(row=5, column=1, padx=5, pady=8)
save_image_bt = Button(right_frame, text="Update Image", width=20, bg="#AAD9BB", highlightthickness=0,
                       command=apply_changes)
save_image_bt.grid(row=6, column=1, padx=5, pady=8)
save_image_bt = Button(right_frame, text="Reset Image", width=20, bg="#AAD9BB", highlightthickness=0)
save_image_bt.grid(row=7, column=1, padx=5, pady=8)
window.mainloop()
