from tkinter import *
from tkinter import messagebox as mb
from PIL import Image

# ===================== ENCODING FUNCTION =====================
def generate_data(pixels, data):
    data += "###END###"  # End marker
    binary_data = [format(ord(char), '08b') for char in data]
    data_len = len(binary_data)
    image_data = iter(pixels)

    for i in range(data_len):
        pixels = [val for val in next(image_data)[:3] + next(image_data)[:3] + next(image_data)[:3]]

        for j in range(8):
            if binary_data[i][j] == '0' and pixels[j] % 2 != 0:
                pixels[j] -= 1
            elif binary_data[i][j] == '1' and pixels[j] % 2 == 0:
                if pixels[j] == 0:
                    pixels[j] += 1
                else:
                    pixels[j] -= 1

        if i == data_len - 1:
            if pixels[-1] % 2 == 0:
                if pixels[-1] == 0:
                    pixels[-1] += 1
                else:
                    pixels[-1] -= 1
        else:
            if pixels[-1] % 2 != 0:
                pixels[-1] -= 1

        yield tuple(pixels[:3])
        yield tuple(pixels[3:6])
        yield tuple(pixels[6:9])


def encryption(img, data):
    size = img.size[0]
    (x, y) = (0, 0)

    for pixel in generate_data(img.getdata(), data):
        img.putpixel((x, y), pixel)
        if x == size - 1:
            x = 0
            y += 1
        else:
            x += 1


def main_encryption(img_path, text, new_image_name):
    if not img_path or not text or not new_image_name:
        mb.showerror("Error", 'Please fill all input fields.')
        return

    try:
        image = Image.open(img_path, 'r')
    except FileNotFoundError:
        mb.showerror("Error", "Image file not found.")
        return

    new_image = image.copy()
    encryption(new_image, text)
    new_image.save(new_image_name + ".png", 'PNG')
    mb.showinfo("Success", "Image encoded and saved successfully!")


# ===================== DECODING FUNCTION =====================
def main_decryption(img_path, strvar):
    try:
        image = Image.open(img_path, 'r')
    except FileNotFoundError:
        mb.showerror("Error", "Image not found.")
        return

    binary_data = ""
    image_data = iter(image.getdata())

    try:
        while True:
            pixels = [val for val in next(image_data)[:3] + next(image_data)[:3] + next(image_data)[:3]]

            for i in pixels[:8]:
                binary_data += '0' if i % 2 == 0 else '1'

            if pixels[-1] % 2 != 0:
                break
    except StopIteration:
        pass

    all_bytes = [binary_data[i:i+8] for i in range(0, len(binary_data), 8)]
    decoded_data = ""
    for byte in all_bytes:
        decoded_data += chr(int(byte, 2))
        if decoded_data.endswith("###END###"):
            break

    strvar.set(decoded_data.replace("###END###", ""))


# ===================== GUI FUNCTIONS =====================
def encode_image():
    encode_wn = Toplevel(root)
    encode_wn.title("Encode an Image")
    encode_wn.geometry('600x220')
    encode_wn.resizable(0, 0)
    encode_wn.config(bg='AntiqueWhite')

    Label(encode_wn, text='Encode an Image', font=("Comic Sans MS", 15), bg='AntiqueWhite').place(x=220, rely=0)
    Label(encode_wn, text='Enter the path to the image (with extension):', font=("Times New Roman", 13),
          bg='AntiqueWhite').place(x=10, y=50)
    Label(encode_wn, text='Enter the data to be encoded:', font=("Times New Roman", 13), bg='AntiqueWhite').place(
        x=10, y=90)
    Label(encode_wn, text='Enter the output file name (without extension):', font=("Times New Roman", 13),
          bg='AntiqueWhite').place(x=10, y=130)

    img_path = Entry(encode_wn, width=35)
    img_path.place(x=350, y=50)

    text_to_be_encoded = Entry(encode_wn, width=35)
    text_to_be_encoded.place(x=350, y=90)

    after_save_path = Entry(encode_wn, width=35)
    after_save_path.place(x=350, y=130)

    Button(encode_wn, text='Encode the Image', font=('Helvetica', 12), bg='PaleTurquoise', command=lambda:
    main_encryption(img_path.get(), text_to_be_encoded.get(), after_save_path.get())).place(x=220, y=175)


def decode_image():
    decode_wn = Toplevel(root)
    decode_wn.title("Decode an Image")
    decode_wn.geometry('600x300')
    decode_wn.resizable(0, 0)
    decode_wn.config(bg='Bisque')

    Label(decode_wn, text='Decode an Image', font=("Comic Sans MS", 15), bg='Bisque').place(x=220, rely=0)
    Label(decode_wn, text='Enter the path to the image (with extension):', font=("Times New Roman", 12),
          bg='Bisque').place(x=10, y=50)

    img_entry = Entry(decode_wn, width=35)
    img_entry.place(x=350, y=50)

    text_strvar = StringVar()

    Button(decode_wn, text='Decode the Image', font=('Helvetica', 12), bg='PaleTurquoise', command=lambda:
    main_decryption(img_entry.get(), text_strvar)).place(x=220, y=90)

    Label(decode_wn, text='Text that has been encoded in the image:', font=("Times New Roman", 12), bg='Bisque').place(
        x=180, y=130)

    text_entry = Entry(decode_wn, width=94, textvariable=text_strvar, state='readonly')
    text_entry.place(x=15, y=160, height=100)


# ===================== ROOT GUI =====================
root = Tk()
root.title('Image Steganography By Omkar')
root.geometry('300x200')
root.resizable(0, 0)
root.config(bg='NavajoWhite')

Label(root, text='Steganography By Omkar', font=('Comic Sans MS', 15), bg='NavajoWhite',
      wraplength=300).place(x=40, y=0)

Button(root, text='Encode', width=25, font=('Times New Roman', 13), bg='SteelBlue', command=encode_image).place(
    x=30, y=80)
Button(root, text='Decode', width=25, font=('Times New Roman', 13), bg='SteelBlue', command=decode_image).place(
    x=30, y=130)

root.mainloop()
