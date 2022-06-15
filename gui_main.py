from tkinter import *
from tkinter import filedialog as fd
from PIL import ImageTk
from tkinter.ttk import Label, Style
import tkinter as tk
from methods import *
import tkinter.font as font

window=Tk()
button_font=font.Font(size=15, family="Aharoni")
label_font=font.Font(size=30,family="Aharoni", weight="bold")
level_font=font.Font(size=15,family="Aharoni")
open_level_font=font.Font(size=10,family="Aharoni")
window['background']="#5F939A"
window.geometry("600x600")
window.title("COMP204 Project")
style=Style(window)
style.configure("Label",font=("Aharoni",25),bg="#1B2021")
label=Label(window,text="Welcome to the my project!",style="Label",background="#5F939A",foreground="#1B2021")
label['font']=label_font
label.grid(pady=20,padx=30)
def add_slash_path(path):
    last_case = ""
    for i in range(len(path)):
        if (not path[i] == '/'):
            last_case += path[i]
        if (path[i] == '/'):
            last_case += path[i] + '/'
    return last_case

def open_image_file():
    global file_path
    filetypes = (
        ('image files', '*.png'),
        ('image files','*.jpeg')

    )
    file_path = fd.askopenfile(filetypes=filetypes)
    return file_path.name

def open_text_file():
    global file_path
    filetypes = (
        ('text files', '*.txt'),
        ('binary files','*.bin'),
    )
    file_path = fd.askopenfile(filetypes=filetypes)
    return file_path.name
def open_bin_file():
    global file_path
    filetypes = (
        ('binary files', '*.bin'),
    )
    file_path = fd.askopenfile(filetypes=filetypes)
    return file_path.name

def Level1_compress_tk():
    file_path=open_text_file()
    compressed_path, codes,entropi,aver_len,original_size,compressed_size,compression_ratio = Level1_Compress(file_path)
    compress=Tk()
    compress.title("L1-->Compressed")
    compress.geometry("500x300")
    compress['background']="#5F939A"
    results="Compressed File Path: \n\n"+ compressed_path+ "\n\nEntropy: "+ str(entropi)+ "\n\nAverage Code Length: "+ str(aver_len)+ "\n\nOriginal Text Size:"+ str(original_size)+" Bytes"+ "\n\nCompressed Text Size: "+str(compressed_size)+" Bytes"+"\n\nCompression Ratio: "+ str(compression_ratio)
    label=Label(compress,text=results,background="#D8AC9C")
    label['font']=label_font
    label.pack()
    compress.mainloop()


def Level1_decompress_tk():
    file_path = open_bin_file()
    decompress = Tk()
    decompress.title("L1-->Decompressed")
    decompress.geometry("800x100")
    decompress['background'] = "#5F939A"
    decompressed_path,difference = Level1_Decompress(file_path, "reverse_mapping.txt")
    Label_out = Label(decompress,text="Decompressed File Path: " + decompressed_path + "\n" + "Difference: " + str(difference),background="#D8AC9C")
    Label_out['font']=label_font
    Label_out.pack()
    decompress.mainloop()


def Level2_compress_tk():
    image_path=open_image_file()
    a=add_slash_path(image_path)
    compress = Tk()
    compress.title("L2-->Compressed")
    compress.geometry("800x700")
    compress['background'] = "#5F939A"
    make_frame = LabelFrame(compress, text="Original Image", width=200, height=200,bg="#5F939A")
    make_frame.pack()
    temp = ImageTk.PhotoImage(master=make_frame,file=a)
    in_frame=Label(make_frame,image=temp,background="#D8AC9C")
    in_frame['font']=label_font
    in_frame.grid(padx=2,pady=2)
    in_frame.pack()
    compressed_file_path,codes,entropy,original_size,compressed_size,compression_ratio,average_code_length=Level2_compress(a)
    results = "Compressed File Path:" + compressed_file_path + "\n\nEntropy: " + str(entropy) + "\n\nAverage Code Length: " + str(average_code_length) + "\n\nOriginal Image's Size:" + str(original_size) +" Bytes"+ "\n\nCompressed Image Size: " + str(compressed_size) + " Bytes"+ "\n\nCompression Ratio: " + str(compression_ratio)
    label = Label(compress, text=results, font="50",background="#D8AC9C").pack()
    compress.mainloop()
def Level2_decompress_tk():
    file_path=open_bin_file()
    decompress = tk.Tk()
    decompress.title("L2-->Decompressed")
    decompress.geometry("800x700")
    decompress['background'] = "#5F939A"
    decompressed_image_path,decompressed_image,original_image,difference=Level2_decompress(file_path,"reverse_mapping_level2.txt")
    make_frame_origin = LabelFrame(decompress, text="Original Image in Gray", width=200, height=200, background="#D8AC9C")
    make_frame_origin.grid(row=100,column=100)
    make_frame_origin.pack()
    temp1 = ImageTk.PhotoImage(master=make_frame_origin,image=original_image)
    in_frame = Label(make_frame_origin, image=temp1,background="#D8AC9C")
    in_frame['font']=label_font
    in_frame.pack()
    make_frame_decom = LabelFrame(decompress, text="Decompressed Image", width=200, height=200, bg="#D8AC9C")
    make_frame_decom.place(x=300,y=300)
    temp = ImageTk.PhotoImage(master=make_frame_decom, image=decompressed_image)
    in_frame = Label(make_frame_decom, image=temp,background="#D8AC9C")
    in_frame.grid(padx=50, pady=50)
    results="Decompressed File Path: " + decompressed_image_path + "\n" + "Difference: " + str(difference)
    label=Label(decompress,text=results,font="50",background="#D8AC9C")
    label['font']=label_font
    label.pack()
    in_frame.pack()
    decompress.mainloop()


def Level3_compress_tk():
    image_path = open_image_file()
    a = add_slash_path(image_path)
    compress = Tk()
    compress.title("L3-->Compressed")
    compress.geometry("800x700")
    compress['background'] = "#5F939A"
    make_frame = LabelFrame(compress, text="Original Image", width=200, height=200,bg="#5F939A")
    make_frame.pack()
    temp = ImageTk.PhotoImage(master=make_frame,file=a)
    in_frame=Label(make_frame,image=temp,background="#D8AC9C")
    in_frame.grid(padx=2,pady=2)
    in_frame.pack()
    compressed_file_path,codes,entropy,original_size,compressed_size,compression_ratio,average_code_length=Level3_compress(a)
    results = "Compressed File Path:" + compressed_file_path + "\n\nEntropy: " + str(entropy) + "\n\nAverage Code Length: " + str(average_code_length) + "\n\nOriginal Image's Size:" + str(original_size) +" Bytes"+ "\n\nCompressed Image Size: " + str(compressed_size)+" Bytes" + "\n\nCompression Ratio: " + str(compression_ratio)
    label = Label(compress, text=results, background="#D8AC9C")
    label['font']=label_font
    label.pack()
    compress.mainloop()
def Level3_decompress_tk():
    file_path=open_bin_file()
    decompress = Tk()
    decompress.title("L3-->Decompressed")
    decompress.geometry("800x700")
    decompress['background'] = "#5F939A"
    decompressed_image_path,decompressed_image,original_image,difference = Level3_decompress(file_path, "reverse_mapping_level3.txt")
    # converts txt to arr to obtain image from this array but it contains row and column sizes as well
    make_frame_origin = LabelFrame(decompress, text="Original Image in Gray", width=200, height=200, background="#D8AC9C")
    make_frame_origin.grid(pady=0,padx=0)
    make_frame_origin.pack()
    temp1 = ImageTk.PhotoImage(master=make_frame_origin, image=original_image)
    in_frame = Label(make_frame_origin, image=temp1,background="#D8AC9C")
    in_frame.grid(padx=50,pady=50)
    in_frame.pack()
    make_frame_decom = LabelFrame(decompress, text="Decompressed Image", width=200, height=200, background="#D8AC9C")
    make_frame_decom.place(x=300, y=300)
    temp = ImageTk.PhotoImage(master=make_frame_decom, image=decompressed_image)
    in_frame_d = Label(make_frame_decom, image=temp,background="#D8AC9C")
    in_frame_d.grid(padx=50, pady=50)
    results = "Decompressed File Path: " + decompressed_image_path + "\n" + "Difference: " + str(difference)
    label = Label(decompress, text=results, font="50",background="#D8AC9C")
    label['font']=label_font
    label.pack()
    in_frame_d.pack()
    decompress.mainloop()
def openRedImage_L4():
    image_path = "r_L4.png"
    red_screen=Tk()
    red_screen.title("Red Image")
    red_screen['background']="#5F939A"
    red_screen.geometry("400x400")
    make_frame = LabelFrame(red_screen, text="Red Image", width=200, height=200, bg="#5F939A")
    make_frame.pack()
    temp = ImageTk.PhotoImage(master=make_frame, file=image_path)
    in_frame = Label(make_frame, image=temp, background="#D8AC9C")
    in_frame.grid(padx=0, pady=0)
    in_frame.pack()
    red_screen.mainloop()
def openGreenImage_L4():
    image_path = "g_L4.png"
    green_screen = Tk()
    green_screen.title("Green Image")
    green_screen['background'] = "#5F939A"
    green_screen.geometry("400x400")
    make_frame = LabelFrame(green_screen, text="Green Image", width=200, height=200, bg="#5F939A")
    make_frame.pack()
    temp = ImageTk.PhotoImage(master=make_frame, file=image_path)
    in_frame = Label(make_frame, image=temp, background="#D8AC9C")
    in_frame.grid(padx=0, pady=0)
    in_frame.pack()
    green_screen.mainloop()
def openBlueImage_L4():
    image_path = "b_L4.png"
    blue_screen = Tk()
    blue_screen.title("Blue Screen")
    blue_screen['background'] = "#5F939A"
    blue_screen.geometry("400x400")
    make_frame = LabelFrame(blue_screen, text="Blue Image", width=200, height=200, bg="#5F939A")
    make_frame.pack()
    temp = ImageTk.PhotoImage(master=make_frame, file=image_path)
    in_frame = Label(make_frame, image=temp, background="#D8AC9C")
    in_frame.grid(padx=0, pady=0)
    in_frame.pack()
    blue_screen.mainloop()

def Level4_compress_tk():
    image_path = open_image_file()
    a = add_slash_path(image_path)
    compress = Tk()
    compress.title("L4-->Compressed")
    compress.geometry("800x700")
    compress['background'] = "#5F939A"
    make_frame = LabelFrame(compress, text="Original Image", width=200, height=200, bg="#5F939A")
    make_frame.pack()
    temp = ImageTk.PhotoImage(master=make_frame, file=a)
    in_frame = Label(make_frame, image=temp,background="#D8AC9C")
    in_frame.grid(padx=0, pady=0)
    in_frame.pack()
    compressed_file_path, codes, entropy,average_code_length, original_size, compressed_size, compression_ratio,  = Level4_compression(a)
    results = "Compressed File Path:" + compressed_file_path + "\n\nEntropy: " + str(entropy) + "\n\nAverage Code Length: " + str(average_code_length) + "\n\nOriginal Image's Size:" + str(
        original_size)+" Bytes" + "\n\nCompressed Image Size: "+" Bytes" + str(compressed_size) + "\n\nCompression Ratio: " + str(compression_ratio)
    label = Label(compress, text=results, font="50")
    label = Label(compress, text=results, background="#D8AC9C")
    label['font'] = label_font
    label.pack()
    buttonRed = Button(compress, text="Click to see red image", command=openRedImage_L4, width=40, foreground="#1B2021", relief="ridge", bd=5,background="#D8AC9C")
    buttonRed['font'] = button_font
    buttonRed.pack()
    buttonGreen = Button(compress, text="Click to see green image", command=openGreenImage_L4, width=40, foreground="#1B2021",relief="ridge", bd=5, background="#D8AC9C")
    buttonGreen['font'] = button_font
    buttonGreen.pack()
    buttonBlue = Button(compress, text="Click to see blue image", command=openBlueImage_L4, width=40, foreground="#1B2021",relief="ridge", bd=5, background="#D8AC9C")
    buttonBlue['font'] = button_font
    buttonBlue.pack()

    compress.mainloop()

def Level4_decompress_tk():
    file_path = open_bin_file()
    decompress = Tk()
    decompress.title("L4-->Decompressed")
    decompress.geometry("800x700")
    decompress['background'] = "#5F939A"
    decompressed_image_path,decompressed_image,original_image,difference = Level4_decompress(file_path, "reverse_mapping_level4.txt")

    make_frame_origin = LabelFrame(decompress, text="Original Image", width=200, height=200, background="#D8AC9C")
    make_frame_origin.grid(pady=0, padx=0)
    make_frame_origin.pack()
    temp1 = ImageTk.PhotoImage(master=make_frame_origin, image=original_image)
    in_frame = Label(make_frame_origin, image=temp1,background="#D8AC9C")
    in_frame.grid(padx=0, pady=0)
    in_frame.pack()
    make_frame_decom = LabelFrame(decompress, text="Decompressed Image", width=200, height=200, background="#D8AC9C")
    make_frame_decom.place(x=300, y=300)
    temp = ImageTk.PhotoImage(master=make_frame_decom, image=decompressed_image)
    in_frame_d = Label(make_frame_decom, image=temp,background="#D8AC9C")
    in_frame_d.grid(padx=0, pady=0)
    results = "Decompressed File Path: " + decompressed_image_path + "\n" + "Difference: " + str(difference)
    label = Label(decompress, text=results, font="50",background="#D8AC9C")
    label['font']=label_font
    label.pack()
    decompress.mainloop()
def openRedImage_L5():
    image_path = "r_L5.png"
    red_screen=Tk()
    red_screen.title("Red Image")
    red_screen['background']="#5F939A"
    red_screen.geometry("400x400")
    make_frame = LabelFrame(red_screen, text="Red Image", width=200, height=200, bg="#5F939A")
    make_frame.pack()
    temp = ImageTk.PhotoImage(master=make_frame, file=image_path)
    in_frame = Label(make_frame, image=temp, background="#D8AC9C")
    in_frame.grid(padx=0, pady=0)
    in_frame.pack()
    red_screen.mainloop()
def openGreenImage_L5():
    image_path = "g_L5.png"
    green_screen = Tk()
    green_screen['background'] = "#5F939A"
    green_screen.title("Green Image")
    green_screen.geometry("400x400")
    make_frame = LabelFrame(green_screen, text="Green Image", width=200, height=200, bg="#5F939A")
    make_frame.pack()
    temp = ImageTk.PhotoImage(master=make_frame, file=image_path)
    in_frame = Label(make_frame, image=temp, background="#D8AC9C")
    in_frame.grid(padx=0, pady=0)
    in_frame.pack()
    green_screen.mainloop()
def openBlueImage_L5():
    image_path = "b_L5.png"
    blue_screen = Tk()
    blue_screen['background'] = "#5F939A"
    blue_screen.title("Blue Image")
    blue_screen.geometry("400x400")
    make_frame = LabelFrame(blue_screen, text="Blue Image", width=200, height=200, bg="#5F939A")
    make_frame.pack()
    temp = ImageTk.PhotoImage(master=make_frame, file=image_path)
    in_frame = Label(make_frame, image=temp, background="#D8AC9C")
    in_frame.grid(padx=0, pady=0)
    in_frame.pack()
    blue_screen.mainloop()

def Level5_compress_tk():
    image_path = open_image_file()
    a = add_slash_path(image_path)
    compress = Tk()
    compress.title("L5-->Compressed")
    compress.geometry("800x700")
    compress['background'] = "#5F939A"
    make_frame = LabelFrame(compress, text="Original Image", width=200, height=200, bg="#5F939A")
    make_frame.pack()
    temp = ImageTk.PhotoImage(master=make_frame, file=a)
    in_frame = Label(make_frame, image=temp,background="#D8AC9C")
    in_frame.grid(padx=2, pady=2)
    in_frame.pack()
    compressed_file_path, codes, entropy, average_code_length, original_size, compressed_size, compression_ratio= Level5_compress(a)
    results = "Compressed File Path:" + compressed_file_path + "\n\nEntropy: " + str(entropy) + "\n\nAverage Code Length: " + str(average_code_length) + "\n\nOriginal Image's Size:" + str(original_size) +" Bytes"+ "\n\nCompressed Image Size: " + str(compressed_size) +" Bytes"+ "\n\nCompression Ratio: " + str(compression_ratio)
    label = Label(compress, text=results, font="20")
    label = Label(compress, text=results, background="#D8AC9C")
    label['font'] = label_font
    label.pack()
    buttonRed = Button(compress, text="Click to see red image", command=openRedImage_L5, width=40, foreground="#1B2021",relief="ridge", bd=5, background="#D8AC9C")
    buttonRed['font'] = button_font
    buttonRed.pack()
    buttonGreen = Button(compress, text="Click to see green image", command=openGreenImage_L5, width=40,foreground="#1B2021", relief="ridge", bd=5, background="#D8AC9C")
    buttonGreen['font'] = button_font
    buttonGreen.pack()
    buttonBlue = Button(compress, text="Click to see blue image", command=openBlueImage_L5, width=40, foreground="#1B2021",relief="ridge", bd=5, background="#D8AC9C")
    buttonBlue['font'] = button_font
    buttonBlue.pack()
    compress.mainloop()


def Level5_decompress_tk():
    file_path = open_bin_file()
    decompress = Tk()
    decompress.title("L5-->Decompressed")
    decompress.geometry("800x700")
    decompress['background'] = "#5F939A"
    decompressed_path,decompressed_image,original_image,difference = Level5_decompress(file_path, "reverse_mapping_level5.txt")

    make_frame_origin = LabelFrame(decompress, text="Original Image", width=200, height=200, background="#D8AC9C")
    make_frame_origin.grid(pady=0, padx=0)
    make_frame_origin.pack()
    temp1 = ImageTk.PhotoImage(master=make_frame_origin, image=original_image)
    in_frame = Label(make_frame_origin, image=temp1,background="#D8AC9C")
    in_frame.grid(padx=50, pady=50)
    in_frame.pack()
    make_frame_decom = LabelFrame(decompress, text="Decompressed Image", width=200, height=200, background="#D8AC9C")
    make_frame_decom.place(x=300, y=300)
    temp = ImageTk.PhotoImage(master=make_frame_decom, image=decompressed_image)
    in_frame_d = Label(make_frame_decom, image=temp,background="#D8AC9C")
    in_frame_d.grid(padx=0, pady=0)
    results = "Decompressed File Path: " + decompressed_path + "\n" + "Difference: " + str(difference)
    label = Label(decompress, text=results,background="#D8AC9C")
    label['font']=label_font
    label.pack()
    decompress.mainloop()

def openLevel1():
    Level1 = Toplevel(window)
    Level1.title("Level 1")
    Level1.geometry("400x300")
    Level1['background']="#EAC8AF"
    label=Label(Level1,text="\n\t\tWelcome to Level1 ! \n\n In this level, you can compress and decompress txt files!",background="#EAC8AF")
    label['font']=open_level_font
    label.pack()
    button_c = Button(Level1, text="Compress txt file", command=Level1_compress_tk, width=40,background="#D8AC9C",foreground="#1B2021")
    button_c.pack(pady=30)
    button_d= Button(Level1, text="Decompress bin file", command=Level1_decompress_tk, width=40,background="#D8AC9C",foreground="#1B2021")
    button_d.pack(pady=30)
    Level1.mainloop()
def openLevel2():
    Level2 = Toplevel(window)
    Level2.title("Level 2")
    Level2.geometry("400x300")
    Level2['background']="#EAC8AF"
    label=Label(Level2,text="\n\t\tWelcome to Level2 ! \n\n In this level, you can compress and decompress gray images! ",background="#EAC8AF")
    label['font']=open_level_font
    label.pack()
    button_l2_c = Button(Level2, text="Compress image file", command=Level2_compress_tk, width=40,background="#D8AC9C",foreground="#1B2021")
    button_l2_c.pack(pady=30)
    button_l2_d = Button(Level2, text="Decompress bin file", command=Level2_decompress_tk, width=40,background="#D8AC9C",foreground="#1B2021")
    button_l2_d.pack(pady=30)
def openLevel3():
    Level3 = Toplevel(window)
    Level3.title("Level 3")
    Level3.geometry("400x300")
    Level3['background'] = "#EAC8AF"
    label=Label(Level3,text="\n\t\tWelcome to Level3 ! \n\n In this level you can compress and decompress gray images by taken differences! ",background="#EAC8AF")
    label['font'] = open_level_font
    label.pack()
    button_c = Button(Level3, text="Compress image file", command=Level3_compress_tk, width=40,background="#D8AC9C",foreground="#1B2021")
    button_c.pack(pady=30)
    button_d = Button(Level3, text="Decompress bin file", command=Level3_decompress_tk, width=40,background="#D8AC9C",foreground="#1B2021")
    button_d.pack(pady=30)
def openLevel4():
    Level4 = Toplevel(window)
    Level4.title("Level 4")
    Level4.geometry("400x300")
    Level4['background'] = "#EAC8AF"
    label=Label(Level4,text="\n\t\tWelcome to Level4 ! \n\n In this level you can compress and decompress color images!",background="#EAC8AF")
    label['font'] = open_level_font
    label.pack()
    button_c = Button(Level4, text="Compress image file", command=Level4_compress_tk, width=40,background="#D8AC9C",foreground="#1B2021")
    button_c.pack(pady=30)
    button_d = Button(Level4, text="Decompress bin file", command=Level4_decompress_tk, width=40,background="#D8AC9C",foreground="#1B2021")
    button_d.pack(pady=30)
def openLevel5():
    Level5 = Toplevel(window)
    Level5.title("Level 5")
    Level5.geometry("400x300")
    Level5['background'] = "#EAC8AF"
    label=Label(Level5,text="\n\t\tWelcome to Level5 ! \n\n In this level you can compress and decompress color images by taken differences! ",background="#EAC8AF")
    label['font'] = open_level_font
    label.pack()
    button_c = Button(Level5, text="Compress image file", command=Level5_compress_tk, width=40,background="#D8AC9C",foreground="#1B2021")
    button_c.pack(pady=30)
    button_d = Button(Level5, text="Decompress bin file", command=Level5_decompress_tk, width=40,background="#D8AC9C",foreground="#1B2021")
    button_d.pack(pady=30)



buttonL1=Button(window,text="Level 1",command=openLevel1,width=40,foreground="#1B2021",relief="ridge",bd=5,background="#D8AC9C")
buttonL1['font']=button_font
buttonL1.grid(padx=10,pady=15)

buttonL2=Button(window,text="Level 2",command=openLevel2,width=40,foreground="#1B2021",relief="ridge",bd=5,background="#EAC8AF")
buttonL2['font']=button_font
buttonL2.grid(padx=10,pady=15)

buttonL3=Button(window,text="Level 3",command=openLevel3,width=40,foreground="#1B2021",relief="ridge",bd=5,background="#D8AC9C")
buttonL3['font']=button_font
buttonL3.grid(padx=10,pady=15)

buttonL4=Button(window,text="Level 4",command=openLevel4,width=40,foreground="#1B2021",relief="ridge",bd=5,background="#EAC8AF")
buttonL4['font']=button_font
buttonL4.grid(padx=10,pady=15)

buttonL5=Button(window,text="Level 5",command=openLevel5,width=40,foreground="#1B2021",relief="ridge",bd=5,background="#D8AC9C")
buttonL5['font']=button_font
buttonL5.grid(padx=10,pady=15)

button_exit=Button(window,text="Finish Program",command=window.quit,width=40,foreground="#1B2021",relief="ridge",bd=5,background="#EAC8AF")
button_exit['font']=button_font
button_exit.grid(padx=10,pady=15)
window.mainloop()
