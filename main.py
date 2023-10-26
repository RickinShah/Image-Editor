#!/usr/bin/env python3

import tkinter as tk
from tkinter import ttk, filedialog
from datetime import datetime
import os
from PIL import Image, ImageTk, ImageEnhance, ImageFilter

class Main(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry('900x650')
        self.withdraw()
        self.file_explorer()
        self.deiconify()
        MainPage(self, self.img)
        self.mainloop()

    def file_explorer(self):
        try:
            try:
                self.tk.call('tk_getOpenFile', '-foobarbaz')
            except tk.TclError:
                pass
            self.tk.call('set', '::tk::dialog::file::showHiddenBtn', '1')
            self.tk.call('set', '::tk::dialog::file::showHiddenVar', '0')
        except:
            pass

        self.filename = filedialog.askopenfilename(initialdir="/home/rickin",
                                            title="Select an image",
                                            filetypes=[("Image files", "*.jpg *.jpeg *.png *.gif *.bmp *.tif *.tiff"),
                                                        ("All files", "*.*")])
        self.img = Image.open(self.filename)

class MainPage(ttk.Frame):
    def __init__(self, parent, img):
        super().__init__(parent, width = 900, height = 650)

        self.imgs = []
        self.img = img
        self.WIDTH_IMAGE = 550
        self.WIDTH_PAGES = 350
        self.X_PAGE = 600
        self.HEIGHT = 650
        self.rotate_var = 0
        self.edit_img = None
        self.is_width_more()
        self.insert_img()
        self.get_thumbnail()
        self.sty = ttk.Style()
        self.sty.configure('TFrame', background = '#1B1B1B')
        #self.sty.configure('TButton', background = 'green', foreground = 'white', font = ("FiraCode Nerd Font Mono", 14))
        #self.sty.configure('TButton', background = 'green', width = 30, foreground = 'white', font = ("FiraCode Nerd Font Mono", 14), borderwidth = 0, relief = "flat", padding = (10, 5), focuscolor = self.sty.map("TButton", fieldbackground=[("active", "blue")]))
        self.style = ttk.Style()
        self.style.configure('mp.TButton', relief = 'flat', width = 15, font = ("CaskaydiaCove NFM SemiLight", 10), borderwidth = 0)
        self.style.map('TButton',
                       foreground = [('pressed', 'black'), ('active', 'green'), ('!active', 'white')],
                       background = [('pressed', 'white'), ('active', 'white'), ('!active', 'green')]
        )
        self.style.configure('undo.TButton', relief = "flat", width = 4, font = ("CaskaydiaCove Nerd Font", 10), borderwidth = 0)
        self.style.configure('img_btn.TButton', relief = "flat", width = 8, font = ("CaskaydiaCove Nerd Font", 10), borderwidth = 0)
        self.style.configure('label.TLabel', background = "green", font = ("CaskaydiaCove Nerd Font", 12), foreground = 'white', padding = (10, 5))

        self.img_page_frame()
        self.main_page_frame()
        self.brightness_page_frame()
        self.contrast_page()
        self.saturation_page()
        self.sharpness_page()
        self.filter_img_page()
        self.flip_img_page()

        self.pack()

    def img_page_frame(self):
        self.img_frame = ttk.Frame(self, width = self.WIDTH_IMAGE, height = self.HEIGHT)

        self.picture = ttk.Label(self.img_frame)
        self.change_thumb()

        undo_button = ttk.Button(self.img_frame, text = "  ", command = self.undo_action, style = "undo.TButton")
        undo_button.place(x = 40, y = 50)

        save_button = ttk.Button(self.img_frame, text = "Save", command = lambda: self.insert_img(self.edit_img), style = "img_btn.TButton")
        save_button.place(x = 200, y= 50)

        self.home_button = ttk.Button(self.img_frame, text = "Home", command = self.go_to_home, style = "img_btn.TButton")
        self.home_button.place(x = 100, y = 50)

        self.img_frame.place(x = 0, y = 0)


    def main_page_frame(self):
        self.main_X = 50
        self.main_Y = 50
        self.main_page = ttk.Frame(self, width = self.WIDTH_PAGES, height = self.HEIGHT)

        save_button_image = ttk.Button(self.main_page, text = "Export  ", command = self.save_image)
        save_button_image.place(x = 200, y = 25)

        grayscale_button = ttk.Button(self.main_page, text = "B&W", command = self.convert_to_grayscale, style = "mp.TButton")
        grayscale_button.place(x = self.main_X, y = self.main_Y + 100)

        brightness_button = ttk.Button(self.main_page, text = "Brightness 🔆", command = self.change_to_brightness, style = "mp.TButton")
        brightness_button.place(x = self.main_X, y = self.main_Y + 150)

        saturation_button = ttk.Button(self.main_page, text = "Saturation", command = self.change_to_saturation, style = "mp.TButton")
        saturation_button.place(x = self.main_X, y = self.main_Y + 200)

        contrast_button = ttk.Button(self.main_page, text = "Contrast ", command = self.change_to_contrast, style = "mp.TButton")
        contrast_button.place(x = self.main_X, y = self.main_Y + 250)

        sharpness_button = ttk.Button(self.main_page, text = "Sharpness", command = self.change_to_sharpness, style = "mp.TButton")
        sharpness_button.place(x = self.main_X, y = self.main_Y + 300)

        rotate_img_button = ttk.Button(self.main_page, text = "Rotate ↺", command = self.rotate_90_degree, style = "mp.TButton")
        rotate_img_button.place(x = self.main_X, y = self.main_Y + 350)

        flip_img = ttk.Button(self.main_page, text = "Flip ←→", command = self.go_to_flip_page, style = "mp.TButton")
        flip_img.place(x = self.main_X, y = self.main_Y + 400)

        img_filter_button = ttk.Button(self.main_page, text = "Filter", command = self.go_to_filter_page, style = "mp.TButton")
        img_filter_button.place(x = self.main_X, y = self.main_Y + 450)

        self.main_page.place(x = self.X_PAGE, y = 0)

    def flip_img_page(self):
        self.flip_img_frame = ttk.Frame(self, width = self.WIDTH_PAGES, height = self.HEIGHT)
        flip_img_hor_button = ttk.Button(self.flip_img_frame, text = "Horizontal ←→", command = self.flip_image_horizontally, style = "mp.TButton")
        flip_img_hor_button.place(x = self.main_X, y = 280)

        flip_img_vert_button = ttk.Button(self.flip_img_frame, text = "Vertical ↑↓", command = self.flip_image_vertically, style = "mp.TButton")
        flip_img_vert_button.place(x = self.main_X, y = 330)

    def brightness_page_frame(self):
        self.brightness_page = ttk.Frame(self, width = self.WIDTH_PAGES, height = self.HEIGHT)
        self.brightness_label = ttk.Label(self.brightness_page, text = "Brightness 🔆", style = "label.TLabel")
        self.brightness_label.place(x = 70, y = 200)
        self.brightness_var = tk.DoubleVar()
        self.brightness_scale = tk.Scale(self.brightness_page, var = self.brightness_var, from_ = -100, to = 100, orient = 'horizontal', resolution = 1, command = self.adjust_brightness, length = 200, background= '#1B1B1B', sliderrelief = 'flat', fg = "white", sliderlength = 10, activebackground = "green", troughcolor= 'grey', highlightthickness=0)
        self.brightness_scale.set(0)
        self.brightness_scale.place(x = 50, y = 300)

        #self.home_button = ttk.Button(self.brightness_page, text = "Home", command = self.go_to_home)
        #self.home_button.place(x = 200, y = 500)

    def saturation_page(self):
        self.saturation_frame = ttk.Frame(self, width = self.WIDTH_PAGES, height = self.HEIGHT)
        self.saturation_label = ttk.Label(self.saturation_frame, text = "Saturation", style = "label.TLabel")
        self.saturation_label.place(x = 70, y = 200)
        self.saturation_var = tk.DoubleVar()
        self.saturation_scale = tk.Scale(self.saturation_frame, var = self.saturation_var, from_ = -100, to = 100, orient = 'horizontal', resolution = 1, command = self.adjust_saturation, length = 200, background= '#1B1B1B', sliderrelief = 'flat', fg = "white", sliderlength = 10, activebackground = "green", troughcolor= 'grey', highlightthickness=0)
        self.saturation_scale.set(0)
        self.saturation_scale.place(x = 50, y = 300)

    def contrast_page(self):
        self.contrast_frame = ttk.Frame(self, width = self.WIDTH_PAGES, height = self.HEIGHT)
        self.contrast_label = ttk.Label(self.contrast_frame, text = "Contrast", style = "label.TLabel")
        self.contrast_label.place(x = 70, y = 200)
        self.contrast_var = tk.DoubleVar()
        self.contrast_scale = tk.Scale(self.contrast_frame, var = self.contrast_var, from_ = -100, to = 100, orient = 'horizontal', resolution = 1, command = self.adjust_contrast, length = 200, background= '#1B1B1B', sliderrelief = 'flat', fg = "white", sliderlength = 10, activebackground = "green", troughcolor= 'grey', highlightthickness=0)
        self.contrast_scale.set(0)
        self.contrast_scale.place(x = 50, y = 300)

    def sharpness_page(self):
        self.sharpness_frame = ttk.Frame(self, width = self.WIDTH_PAGES, height = self.HEIGHT)
        self.sharpness_label = ttk.Label(self.sharpness_frame, text = "Sharpness", style = "label.TLabel")
        self.sharpness_label.place(x = 70, y = 200)
        self.sharpness_var = tk.DoubleVar()
        self.sharpness_scale = tk.Scale(self.sharpness_frame, var = self.sharpness_var, from_ = -100, to = 100, orient = 'horizontal', resolution = 1, command = self.adjust_sharpness, length = 200, background= '#1B1B1B', sliderrelief = 'flat', fg = "white", sliderlength = 10, activebackground = "green", troughcolor= 'grey', highlightthickness=0)
        self.sharpness_scale.set(0)
        self.sharpness_scale.place(x = 50, y = 300)

    def filter_img_page(self):
        filter_X = 50
        self.filter_img_frame = ttk.Frame(self, width = self.WIDTH_PAGES, height = self.HEIGHT)

        self.filter2 = ttk.Button(self.filter_img_frame, text = "Enhance Edges", command = self.enhance_edges_filter, style = "mp.TButton")
        self.filter2.place(x = filter_X, y = 200)

        self.filter3 = ttk.Button(self.filter_img_frame, text = "Emboss", command = self.emboss_filter, style = "mp.TButton")
        self.filter3.place(x = filter_X, y = 250)

        self.filter4 = ttk.Button(self.filter_img_frame, text = "Sharpen", command = self.sharpen_filter, style = "mp.TButton")
        self.filter4.place(x = filter_X, y = 300)

        self.filter5 = ttk.Button(self.filter_img_frame, text = "Contour", command = self.contour_filter, style = "mp.TButton")
        self.filter5.place(x = filter_X, y = 350)

        self.filter6 = ttk.Button(self.filter_img_frame, text = "Detail", command = self.detail_filter, style = "mp.TButton")
        self.filter6.place(x = filter_X, y = 400)

        self.filter7 = ttk.Button(self.filter_img_frame, text = "Blur", command = self.blur_filter, style = "mp.TButton")
        self.filter7.place(x = filter_X, y = 450)

    def get_img(self):
        return self.imgs[-1]

    def insert_img(self, img = None):
        self.rotate_var = 0
        if img is None:
            img = self.img

        print(img)
        print(self.edit_img)
        self.img = img
        self.imgs.append(img)

    def undo_action(self):
        self.rotate_var = 0
        if len(self.imgs) > 1:
            print(len(self.imgs))
            self.imgs.pop()
            self.img = self.imgs[-1]
            self.change_thumb()
        elif len(self.imgs) == 1:
            self.img = self.imgs[-1]
            self.change_thumb()

    def get_thumbnail(self, img = None):
        if img is None:
            img = self.img
        img_copy = img.copy()
        img_copy.thumbnail((450, 450), Image.LANCZOS)
        self.pic_thumb = ImageTk.PhotoImage(img_copy)

    def convert_to_grayscale(self):
        self.edit_img = self.img.convert("L")
        self.change_thumb(self.edit_img)

    def change_thumb(self, img = None):
        if img is None:
            img = self.img
        print(img)
        width, height = img.size
        ratio = min(400/ width, 400 / height)
        print(ratio)
        max_width = width * ratio
        max_height = height * ratio
        print(max_width)
        print(max_height)

        self.get_thumbnail(img)
        if width > height:
            img_X = 650 - max_width - 190
            self.picture.place(x = img_X, y = 220)
        else:
            img_X = 650 - max_width - 250
            self.picture.place(x = img_X, y = 150)
        self.picture.configure(image = self.pic_thumb)
        self.picture.image = self.pic_thumb

    def change_to_brightness(self):
        #print(bool(self.main_page.winfo_ismapped()))
        self.main_page.place_forget()
        self.brightness_page.place(x = self.X_PAGE, y = 0)
        #print(bool(self.main_page.winfo_ismapped()))

    def go_to_flip_page(self):
        self.main_page.place_forget()
        self.flip_img_frame.place(x = self.X_PAGE, y = 0)

    def go_to_home(self):
        self.main_page.place(x = self.X_PAGE, y = 0)
        self.brightness_page.place_forget()
        self.saturation_frame.place_forget()
        self.contrast_frame.place_forget()
        self.sharpness_frame.place_forget()
        self.filter_img_frame.place_forget()
        self.flip_img_frame.place_forget()
        self.img = self.imgs[-1]
        self.change_thumb()

    def rotate_90_degree(self):
        if self.rotate_var == 360:
            self.rotate_var = 0
        self.rotate_var += 90
        print(self.rotate_var)
        self.edit_img = self.img.rotate(self.rotate_var, expand = 1)
        self.is_width_more()
        self.change_thumb(self.edit_img)

    def is_width_more(self):
        width, height = self.img.size
        if width > height:
            self.width_more = True
        else:
            self.width_more = False

    def flip_image_horizontally(self):
        self.edit_img = self.img.transpose(method = Image.FLIP_LEFT_RIGHT)
        self.change_thumb(self.edit_img)

    def flip_image_vertically(self):
        self.edit_img = self.img.transpose(method = Image.FLIP_TOP_BOTTOM)
        self.change_thumb(self.edit_img)

    def crop_page(self):
        self.main_page.place_forget()
        self.crop_image_frame.place(x = 450, y = 0)

    def get_brightness(self, event):
        print(self.brightness_var.get())

    def adjust_brightness(self, event):
        enhancer = ImageEnhance.Brightness(self.img)
        factor = (self.brightness_var.get() / 100) + 1
        self.edit_img = enhancer.enhance(factor)
        self.change_thumb(self.edit_img)

    def change_to_saturation(self):
        self.main_page.place_forget()
        self.saturation_frame.place(x = self.X_PAGE, y = 0)

    def change_to_contrast(self):
        self.main_page.place_forget()
        self.contrast_frame.place(x = self.X_PAGE, y = 0)

    def change_to_sharpness(self):
        self.main_page.place_forget()
        self.sharpness_frame.place(x = self.X_PAGE, y = 0)

    def adjust_saturation(self, event):
        enhancer = ImageEnhance.Color(self.img)
        factor = (self.saturation_var.get()/ 100) + 1
        self.edit_img = enhancer.enhance(factor)
        self.change_thumb(self.edit_img)

    def adjust_contrast(self, event):
        enhancer = ImageEnhance.Contrast(self.img)
        factor = (self.contrast_var.get()/ 100) + 1
        self.edit_img = enhancer.enhance(factor)
        self.change_thumb(self.edit_img)

    def adjust_sharpness(self, event):
        enhancer = ImageEnhance.Sharpness(self.img)
        print(self.sharpness_var.get())
        factor = (self.sharpness_var.get()/ 100) + 1
        self.edit_img = enhancer.enhance(factor)
        self.change_thumb(self.edit_img)

    def save_image(self):
        path = "Edited-Images/"
        if not os.path.exists(path):
            os.mkdir(path)
        file_name = datetime.now().strftime("Edited-Images/Edited-Image-%d-%m-%Y-%H-%M-%S.jpg")
        self.imgs[-1].save(file_name)

    def go_to_filter_page(self):
        self.main_page.place_forget()
        self.filter_img_frame.place(x = self.X_PAGE, y = 0)

    def enhance_edges_filter(self):
        self.edit_img = self.img.filter(ImageFilter.EDGE_ENHANCE)
        self.change_thumb(self.edit_img)

    def emboss_filter(self):
        self.edit_img = self.img.filter(ImageFilter.EMBOSS)
        self.change_thumb(self.edit_img)

    def sharpen_filter(self):
        self.edit_img = self.img.filter(ImageFilter.SHARPEN)
        self.change_thumb(self.edit_img)

    def contour_filter(self):
        self.edit_img = self.img.filter(ImageFilter.CONTOUR)
        self.change_thumb(self.edit_img)

    def detail_filter(self):
        self.edit_img = self.img.filter(ImageFilter.DETAIL)
        self.change_thumb(self.edit_img)

    def blur_filter(self):
        self.edit_img = self.img.filter(ImageFilter.BLUR)
        self.change_thumb(self.edit_img)

Main()
