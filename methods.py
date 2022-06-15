from huffman import *
import numpy as np
from PIL import Image
import time
def Level1_Compress(path):

    # reading file
    content = read_txt_file(path)
    # constructing huffman
    reverse_mapping = {}
    huff = construct_huffman(path,reverse_mapping)

    # calculating probabilities of each item
    probs = huff.make_probability_dict(content)

    print("Probabilities of each item :\n", probs)  # probability dict is printed
    entropi = huff.calculateEntropy(content)
    compressed_path, codes = huff.compress()
    aver_len = huff.calculateAverageCodeLength(content, codes)

    original_size, compressed_size, compression_ratio = huff.calculateCompressionRatio(compressed_path)
    # encode the file content and save the compressed file.
    dictTotxt(huff.reverse_mapping, "reverse_mapping.txt")

    return compressed_path ,codes,entropi,aver_len,original_size,compressed_size,compression_ratio


def Level1_Decompress(compressed_path, reverse_mapping_txt):

    #converting reverse_mapping info from txt
    reverse_mapping = txtTodict(reverse_mapping_txt)

    #construct huffman
    huff1 = construct_huffman(compressed_path,reverse_mapping)

    #obtaining decompressed path
    decompressed_path = huff1.decompress(compressed_path)
    filename, file_extension = os.path.splitext(decompressed_path)
    original_path = filename + ".txt"
    difference = calculate_difference_txt(decompressed_path, original_path)
    return decompressed_path,difference

def Level2_compress(path):
    #reading image
    image =read_image(path)
    #changing color to gray
    img_gray = color2gray(image)

    #2d array of gray image
    img_gray_arr=PIL2np(img_gray)

    row_size=img_gray_arr.shape[0]
    col_size=img_gray_arr.shape[1]

    main_image_arr = np.array(img_gray_arr.flatten().tolist())
    main_image_arr = np.append(main_image_arr,row_size)
    main_image_arr=np.append(main_image_arr,col_size)

    image_arr_file = write_arr_to_txt_L2(main_image_arr)

    #construct huffman
    reverse_mapping = {}
    huffman = construct_huffman(image_arr_file,reverse_mapping)

    prob_dict = huffman.make_probability_dict(main_image_arr)


    # encode the file content and save the compressed file.
    compressed_file_path,codes = huffman.compress()

    entropy = huffman.calculateEntropy(main_image_arr)

    original_size,compressed_size,compression_ratio=huffman.calculateCompressionRatio(compressed_file_path)

    #this is for calculating average code length
    #file = write_arr_to_txt_L2(main_image_arr) #file name of  array's name
    average_code_length=huffman.calculateAverageCodeLength(read_txt_file(image_arr_file),huffman.codes) #reads content of array file and calculates average code length

    dictTotxt(huffman.reverse_mapping, "reverse_mapping_level2.txt") #creates reverse_mapping dicts in a txt for using in decompress operation

    return compressed_file_path,codes,entropy,original_size,compressed_size,compression_ratio,average_code_length

def Level2_decompress(compressed_path,reverse_mapping_path):
    #it is getting to construct huffman with reverse mappings which came from compress operation --> it contains the values and connections with their codes
    reverse_mapping = txtTodict(reverse_mapping_path)
    #construct huffman
    huffman = construct_huffman(compressed_path, reverse_mapping)
    #obtaining decompressed path
    decompressed_file_path = huffman.decompress(compressed_path)

    filename, file_extension = os.path.splitext(compressed_path)
    original_path = filename + ".txt"
    arr_rc = txtToArr(original_path)
    column = arr_rc[-1]
    row = arr_rc[-2]
    original_arr = arr_rc[:-2]
    original_image = np2PIL(original_arr.reshape(row, column))
    arr_de_rc = txtToArr(decompressed_file_path)
    column_dec = arr_de_rc[-1]
    row_dec = arr_de_rc[-2]
    decompressed_arr_last = arr_de_rc[:-2]
    decompressed_image = np2PIL(decompressed_arr_last.reshape(row_dec, column_dec))
    decompressed_image.save("decompressed_image_level2.png")
    difference=calculate_diff_arr(original_arr,decompressed_arr_last)
    return decompressed_file_path,decompressed_image,original_image,difference

def Level3_compress(path):
    image = read_image(path)
    img_gray = color2gray(image)
    img_gray_arr=PIL2np(img_gray)
    row_size=img_gray_arr.shape[0]
    col_size=img_gray_arr.shape[1]
    img_gray_arr_diffed, pivot = difference(img_gray_arr)
    img_gray_arr_diffed_1d = img_gray_arr_diffed.flatten().tolist()
    img_gray_arr_diffed_1d=np.append(img_gray_arr_diffed_1d,row_size)
    img_gray_arr_diffed_1d=np.append(img_gray_arr_diffed_1d,col_size)
    img_gray_arr_diffed_1d=np.append(img_gray_arr_diffed_1d,pivot)

    reverse_mapping={}
    file_to_compress = write_arr_to_txt_L3(img_gray_arr_diffed_1d)
    huffman = construct_huffman(file_to_compress,reverse_mapping)
    prob_dict = huffman.make_probability_dict(img_gray_arr_diffed_1d)
    # print("probs = ", prob_dict)
    compressed_path,codes = huffman.compress()
    dictTotxt(huffman.reverse_mapping,"reverse_mapping_level3.txt")
    entropy = huffman.calculateEntropy(img_gray_arr_diffed_1d)
    original,compressed,compression_ratio=huffman.calculateCompressionRatio(compressed_path)
    average_code_length=huffman.calculateAverageCodeLength(read_txt_file(file_to_compress),codes)

    return compressed_path,codes,entropy,original,compressed,compression_ratio,average_code_length,

def Level3_decompress(compressed_path,reverse_mapping_txt):
    reverse_mapping = txtTodict(reverse_mapping_txt)

    huff=construct_huffman(compressed_path,reverse_mapping)

    decompressed_file_path = huff.decompress(compressed_path)
    filename, file_extension = os.path.splitext(compressed_path)
    original_path = filename + ".txt"

    # converts txt to arr to obtain image from this array but it contains row and column sizes as well
    np_arr = txtToArr(decompressed_file_path)
    row_size = np_arr[-3]
    col_size = np_arr[-2]
    pivot = np_arr[-1]
    # row size and column size are deleted and the last form of the array
    np_arr_decompressed = np_arr[:-3]
    np_arr_decompressed = np_arr_decompressed.reshape(row_size, col_size)
    np_decompressed_reverse_diffed = reverse_difference(np_arr_decompressed, row_size, col_size, pivot)
    decompressed_image = np2PIL(np_decompressed_reverse_diffed)
    or_arr = txtToArr(original_path)
    row_or = or_arr[-3]
    col_or = or_arr[-2]
    pivot_or = or_arr[-1]
    original_arr = or_arr[:-3]
    original_arr = original_arr.reshape(row_or, col_or)
    original_arr_reverse_diffed = reverse_difference(original_arr, row_or, col_or, pivot_or)
    original_image = np2PIL(original_arr_reverse_diffed)
    difference = calculate_diff_arr(np_decompressed_reverse_diffed, original_arr_reverse_diffed)
    decompressed_image.save("decompressed_level3_image.png")

    return decompressed_file_path,decompressed_image,original_image,difference

def Level4_compression(path):
    # read image
    image = read_image(path)

    # change color to gray
    image_RGB = color2RGB(image)

    # creating numpy array of image
    image_arr = PIL2np(image_RGB)  # 3D array because of for each red,green and blue

    # row and size values of arr
    arr_row = image_arr.shape[0]
    arr_column = image_arr.shape[1]

    # red,green and blue arrays separately
    r, g, b = getting_r_g_b_arrs_L4(image_RGB)

    reverse_r,reverse_g,reverse_b={},{},{}
    # constructs of huffman
    hr = construct_huffman(r,reverse_r)
    hg = construct_huffman(g,reverse_g)
    hb = construct_huffman(b,reverse_b)

    # probabilities for each color separetly

    image_arr_1d=image_arr.flatten()
    image_arr_1d=np.append(image_arr_1d,arr_row)
    image_arr_1d=np.append(image_arr_1d,arr_column)

    filename = write_arr_to_txt_L4(image_arr_1d)

    # constructing huffman with txt which contains content of 3d array(rgb)
    reverse_mapping={}
    h = construct_huffman(filename,reverse_mapping)

    # Encode the difference image and save into file
    compressed_path,codes = h.compress()

    dictTotxt(h.reverse_mapping,"reverse_mapping_level4.txt")

    entropy=h.calculateEntropy(image_arr_1d)

    # giving compression ratio
    original,compressed,compresssion_ratio=h.calculateCompressionRatio(compressed_path)


    average_code_length=h.calculateAverageCodeLength(read_txt_file(filename),codes)  # reads content of array file and calculates average code length

    return compressed_path,codes,entropy,average_code_length,original,compressed,compresssion_ratio
def Level4_decompress(compressed_path,reverse_mapping_path):
    reverse_mapping=txtTodict(reverse_mapping_path)
    h=construct_huffman(compressed_path,reverse_mapping)
    # to restore image, decompressed path is obtained
    decompressed_path = h.decompress(compressed_path)
    filename, file_extension = os.path.splitext(compressed_path)
    original_path = filename + ".txt"
    or_arr = txtToArr(original_path)
    or_row = or_arr[-2]
    or_col = or_arr[-1]
    original_arr = or_arr[:-2]
    original_3d = original_arr.reshape(or_row, or_col, 3)
    original_image = np2PIL(original_3d)
    np_arr = txtToArr(decompressed_path)
    column_size = np_arr[-1]
    row_size = np_arr[-2]
    np_arr_last = np_arr[:-2]
    np_3darr = np_arr_last.reshape(row_size, column_size, 3)
    # converting array to PIL
    decompressed_image = np2PIL(np_3darr)
    decompressed_image.save("decompressed_color_image_L4.png")
    difference=calculate_diff_arr(original_3d,np_3darr)

    return decompressed_path,decompressed_image,original_image,difference

def Level5_compress(path):
    # read image
    image = read_image(path)

    image_color=color2RGB(image)

    # creating numpy array of image
    image_arr = PIL2np(image_color)

    # row, column and dim values of arr
    arr_row = image_arr.shape[0]
    arr_column = image_arr.shape[1]
    arr_dim=image_arr.shape[2]

    #getting 2d rgb arrays separately
    red,green,blue=getting_r_g_b_arrs_v2(image)

    #difference taken arrays
    red_diff,pivotR=difference(red)
    green_diff,pivotG=difference(green)
    blue_diff,pivotB=difference(blue)
    #huffman constructs to calculate probability
    reverse_r,reverse_g,reverse_b={},{},{}
    hr=construct_huffman(red_diff.flatten(),reverse_r)
    hg=construct_huffman(green_diff.flatten(),reverse_g)
    hb=construct_huffman(blue_diff.flatten(),reverse_b)

    #connecting 2d red,green,blue arrays in a 3d array
    rgb_diff_arr=obtaining3d_diff_arr(image_arr,red_diff,green_diff,blue_diff)
    rgb_diff_arr=rgb_diff_arr.flatten()
    rgb_diff_arr=np.append(rgb_diff_arr,arr_row)
    rgb_diff_arr=np.append(rgb_diff_arr,arr_column)
    rgb_diff_arr=np.append(rgb_diff_arr,pivotR)
    rgb_diff_arr=np.append(rgb_diff_arr,pivotG)
    rgb_diff_arr=np.append(rgb_diff_arr,pivotB)

    rgb_diff_arr_1d=rgb_diff_arr.flatten()
    #getting file path which contains 3d array's items with separeting ','
    filename=write_arr_to_txt_L5(rgb_diff_arr_1d)

    #constructs of huffman
    reverse_mapping={}
    h=construct_huffman(filename,reverse_mapping)


    #Encode the difference image and save into file
    compressed_path,codes=h.compress()

    dictTotxt(h.reverse_mapping,"reverse_mapping_level5.txt")
    entropy=h.calculateEntropy(image_arr.flatten())


    #giving compression ratio
    original,compressed,compression_ratio=h.calculateCompressionRatio(compressed_path)

    # calculating average code length
    average_code_length=h.calculateAverageCodeLength(read_txt_file(filename),codes)  # reads content of array file and calculates average code length

    return compressed_path,codes,entropy,average_code_length,original,compressed,compression_ratio

def Level5_decompress(compressed_path,reverse_mapping_path):
    reverse_mapping = txtTodict(reverse_mapping_path)
    huffman = HuffmanCoding(compressed_path, reverse_mapping)
    decompress_path = huffman.decompress(compressed_path)
    filename, file_extension = os.path.splitext(compressed_path)
    original_path = filename + ".txt"
    np_arr = txtToArr(decompress_path)
    pivotB = np_arr[-1]
    pivotG = np_arr[-2]
    pivotR = np_arr[-3]
    column = np_arr[-4]
    row = np_arr[-5]

    np_arr_last = np_arr[:-5]
    np_arr_decompress = np_arr_last.reshape(row, column, 3)
    img = np2PIL(np_arr_decompress)
    data = img.getdata()
    r = [(d[0], 0, 0) for d in data]
    g = [(0, d[1], 0) for d in data]
    b = [(0, 0, d[2]) for d in data]

    """FOR RED TO BE REVERSE DIFFERENCE"""
    tempR = np.array(r)
    listR = np.zeros([tempR.shape[0]], dtype=int)
    for i in range(0, tempR.shape[0]):
        listR[i] = tempR[i][0]
    mainR = listR.reshape(row, column)
    rev_diffR = reverse_difference(mainR, row, column, pivotR)
    to1darrayR_REVERSE = rev_diffR.flatten()
    """FOR GREEN TO BE REVERSE DIFFERENCE"""
    tempG = np.array(g)
    listG = np.zeros([tempG.shape[0]], dtype=int)
    for i in range(0, tempG.shape[0]):
        listG[i] = tempG[i][1]
    mainG = listG.reshape(row, column)
    rev_diffG = reverse_difference(mainG, row, column, pivotG)
    to1darrayG_REVERSE = rev_diffG.flatten()
    """FOR BLUE TO BE REVERSE DIFFERENCE"""
    tempB = np.array(b)
    listB = np.zeros([tempB.shape[0]], dtype=int)
    for i in range(0, tempB.shape[0]):
        listB[i] = tempB[i][2]
    mainB = listB.reshape(row, column)
    rev_diffB = reverse_difference(mainB, row, column, pivotB)
    to1darrayB_REVERSE = rev_diffB.flatten()

    to3darray = np.zeros([row, column, 3], dtype=int)
    for i in range(0, row):
        for j in range(0, column):
            to3darray[i][j][0] = to1darrayR_REVERSE[i * column + j]
            to3darray[i][j][1] = to1darrayG_REVERSE[i * column + j]
            to3darray[i][j][2] = to1darrayB_REVERSE[i * column + j]

    decompressed_image = np2PIL(to3darray)
    decompressed_image.save("decompressed_color_image_L5.png")
    or_arr = txtToArr(original_path)
    pivotB_or = or_arr[-1]
    pivotG_or = or_arr[-2]
    pivotR_or = or_arr[-3]
    column_or = or_arr[-4]
    row_or = or_arr[-5]
    or_arr_last = or_arr[:-5]
    original_arr_3d = or_arr_last.reshape(row_or, column_or, 3)
    original_image = np2PIL(original_arr_3d)

    data_or = original_image.getdata()
    r_or = [(d[0], 0, 0) for d in data_or]
    g_or = [(0, d[1], 0) for d in data_or]
    b_or = [(0, 0, d[2]) for d in data_or]

    """FOR RED TO BE REVERSE DIFFERENCE"""
    tempR_or = np.array(r_or)
    listR_or = np.zeros([tempR_or.shape[0]], dtype=int)
    for i in range(0, tempR_or.shape[0]):
        listR_or[i] = tempR_or[i][0]
    mainR_or = listR_or.reshape(row_or, column_or)
    rev_diffR_or = reverse_difference(mainR_or, row_or, column_or, pivotR_or)
    to1darrayR_REVERSE_or = rev_diffR.flatten()

    """FOR GREEN TO BE REVERSE DIFFERENCE"""
    tempG_or = np.array(g_or)
    listG_or = np.zeros([tempG_or.shape[0]], dtype=int)
    for i in range(0, tempG_or.shape[0]):
        listG_or[i] = tempG_or[i][1]
    mainG_or = listG_or.reshape(row_or, column_or)
    rev_diffG_or = reverse_difference(mainG_or, row_or, column_or, pivotG_or)
    to1darrayG_REVERSE_or = rev_diffG_or.flatten()

    """FOR BLUE TO BE REVERSE DIFFERENCE"""
    tempB_or = np.array(b_or)
    listB_or = np.zeros([tempB_or.shape[0]], dtype=int)
    for i in range(0, tempB_or.shape[0]):
        listB_or[i] = tempB_or[i][2]
    mainB_or = listB_or.reshape(row_or, column_or)
    rev_diffB_or = reverse_difference(mainB_or, row_or, column_or, pivotB_or)
    to1darrayB_REVERSE_or = rev_diffB_or.flatten()

    to3darray_or = np.zeros([row_or, column_or, 3], dtype=int)
    for i in range(0, row_or):
        for j in range(0, column_or):
            to3darray_or[i][j][0] = to1darrayR_REVERSE_or[i * column_or + j]
            to3darray_or[i][j][1] = to1darrayG_REVERSE_or[i * column_or + j]
            to3darray_or[i][j][2] = to1darrayB_REVERSE_or[i * column_or + j]
    original_image = np2PIL(to3darray_or)
    difference=calculate_diff_arr(to3darray_or,to3darray)
    return decompress_path,decompressed_image,original_image,difference


"""
------------------------------------------------HELPFUL METHODS---------------------------------------------------------
"""



def calculate_difference_txt(decompressed_path,original_path):
    original_path_content=read_txt_file(original_path)
    decompressed_path_content=read_txt_file(decompressed_path)
    difference=0
    for i in range(len(original_path_content)):
        if((original_path_content[i])==(decompressed_path_content[i])):
            difference=0
        else:
            difference=-1
    return difference

def write_3darr_to_txt(arr_3d):
    with open("3D_diff_arr.txt", "w+") as file:
        for i in np.ndindex(arr_3d.shape):
            file.write(str(arr_3d[i]))
            if not i == len(arr_3d) - 1:
                file.write(",")
    return file.name

def write_arr_to_txt_L5(image_arr):
    with open("L5.txt", "w+") as file:
        for i in range(0, len(image_arr)):
            file.write(str(image_arr[i]))
            if not i == len(image_arr) - 1:
                file.write(",")
    return file.name

def write_arr_to_txt_L4(image_arr):
    with open("L4.txt", "w+") as file:
        for i in range(0, len(image_arr)):
            file.write(str(image_arr[i]))
            if not i == len(image_arr) - 1:
                file.write(",")
    return file.name

def write_arr_to_txt_L3(image_arr):
    with open("L3.txt", "w+") as file:
        for i in range(0, len(image_arr)):
            file.write(str(image_arr[i]))
            if not i == len(image_arr) - 1:
                file.write(",")
    return file.name

def write_arr_to_txt_L2(image_arr):
    with open("L2.txt", "w+") as file:
        for i in range(0, len(image_arr)):
            file.write(str(image_arr[i]))
            if not i == len(image_arr) - 1:
                file.write(",")
    return file.name

def read_txt_file_v2(path):
    file=open(path, "r")
    content=file.read()
    content=content.split(',')
    if('' in content):
        content.remove('')
    return content

def read_txt_file(path):
    file = open(path, "r")
    content = file.read()
    return content

def read_image(path):
    image=Image.open(path)
    return image

def construct_huffman(path,reverse_mapping):
    h=HuffmanCoding(path,reverse_mapping)
    return h

def color2gray(img):
    img_gray = img.convert('L')
    return img_gray

def color2RGB(img):
    img_rgb=img.convert("RGB")
    return img_rgb
def PIL2np(img):
    nrows = img.size[0]
    ncols = img.size[1]
    imgarray = np.array(img)
    return imgarray

def np2PIL(im):
    img = Image.fromarray(np.uint8(im))
    return img

def difference(arr):
    row_size = arr.shape[0]
    col_size = arr.shape[1]
    firstDiffArr = np.zeros(shape=(row_size, col_size), dtype=int)

    for i in range(0, row_size):
        for j in range(0, col_size):
            if j == 0:
                firstDiffArr[i][j] = arr[i][j]
            else:
                firstDiffArr[i][j] = int(arr[i][j]) - int(arr[i][j - 1])
    secondDiffArr = np.copy(firstDiffArr)
    pivot = firstDiffArr[0][0]
    secondDiffArr[0][0] = secondDiffArr[0][0] - pivot
    for i in range(1, row_size):
        secondDiffArr[i][0] = firstDiffArr[i][0] - firstDiffArr[i - 1][0]
    return secondDiffArr, pivot
def calculate_diff_arr(origin_arr,decomp_arr):
    origin_arr_1d=origin_arr.flatten()
    decomp_arr_2d=decomp_arr.flatten()
    diff=0
    for i in range(len(origin_arr_1d)):
            diff+=origin_arr_1d[i]-decomp_arr_2d[i]
    return int(math.pow(diff,2))

def txtToArr(decompressed_path):
    with open(decompressed_path,'r') as decompressed_diff_file:
        decompressed_content=decompressed_diff_file.read()
    decompressed_content = decompressed_content.split(',')
    np_arr_diff = np.array(decompressed_content, dtype=int)
    return np_arr_diff

def reverse_difference(arr, row_size, columun_size, pivot):
    diff_arr_reverse = np.copy(arr)
    diff_arr_reverse[0][0] = pivot
    for i in range(1, row_size):
        diff_arr_reverse[i][0] = diff_arr_reverse[i - 1][0] + arr[i][0]
    decompressed_image_arr = np.copy(diff_arr_reverse)
    for i in range(0, row_size):
        for j in range(0, columun_size):
            if j == 0:
                decompressed_image_arr[i][j] = diff_arr_reverse[i][j]
            else:
                decompressed_image_arr[i][j] = decompressed_image_arr[i][j - 1] + decompressed_image_arr[i][j]
    return decompressed_image_arr
def getting_r_g_b_arrs_v2(image):
    row_size = image.size[1]
    column_size = image.size[0]

    rgb_image = color2RGB(image)
    rgb_image_arr = PIL2np(rgb_image)  # 3d arr
    dim = rgb_image_arr.shape[2]
    data = image.getdata()
    r = [(d[0], 0, 0) for d in data]
    g = [(0, d[1], 0) for d in data]
    b = [(0, 0, d[2]) for d in data]

    image.putdata(r)
    image.save('r_L5.png')
    image.putdata(g)
    image.save('g_L5.png')
    image.putdata(b)
    image.save('b_L5.png')

    tempR = np.array(r)
    listR = np.zeros([tempR.shape[0]], dtype=int)
    for i in range(0, tempR.shape[0]):
        listR[i] = tempR[i][0]
    mainR = listR.reshape(row_size, column_size)

    tempG = np.array(g)
    listG = np.zeros([tempG.shape[0]], dtype=int)
    for i in range(0, tempG.shape[0]):
        listG[i] = tempG[i][1]
    mainG = listG.reshape(row_size, column_size)

    tempB = np.array(b)
    listB = np.zeros([tempB.shape[0]], dtype=int)
    for i in range(0, tempB.shape[0]):
        listB[i] = tempB[i][2]
    mainB = listB.reshape(row_size, column_size)
    return mainR,mainG,mainB

def getting_r_g_b_arrs_L4(image):
    rgb_image_arr=PIL2np(image)  #3d arr
    dim = rgb_image_arr.shape[2]
    data = image.getdata()

    r = [(d[0], 0, 0) for d in data]
    g = [(0, d[1], 0) for d in data]
    b = [(0, 0, d[2]) for d in data]
    image.putdata(r)
    image.save('r_L4.png')
    image.putdata(g)
    image.save('g_L4.png')
    image.putdata(b)
    image.save('b_L4.png')

    r_im = Image.open('r_L4.png')
    r_im_arr = PIL2np(r_im)

    g_im = Image.open('g_L4.png')
    g_im_arr = PIL2np(g_im)

    b_im = Image.open('b_L4.png')
    b_im_arr = PIL2np(b_im)

    return r_im_arr,g_im_arr,b_im_arr


def getting_r_g_b_arrs_L5(image):
    rgb_image_arr=PIL2np(image)  #3d arr
    dim = rgb_image_arr.shape[2]
    data = image.getdata()

    r = [(d[0], 0, 0) for d in data]
    g = [(0, d[1], 0) for d in data]
    b = [(0, 0, d[2]) for d in data]
    image.putdata(r)
    image.save('r_L5.png')
    image.putdata(g)
    image.save('g_L5.png')
    image.putdata(b)
    image.save('b_L5.png')

    r_im = Image.open('r_L5.png')
    r_im_arr = PIL2np(r_im)

    g_im = Image.open('g_L5.png')
    g_im_arr = PIL2np(g_im)

    b_im = Image.open('b_L5.png')
    b_im_arr = PIL2np(b_im)

    return r_im_arr,g_im_arr,b_im_arr

def obtaining3d_diff_arr(image_arr,r_arr,g_arr,b_arr):
    row_size=image_arr.shape[0]
    column_size=image_arr.shape[1]
    dim=image_arr.shape[2]
    to3darray_DIFFERENCE = np.zeros([row_size, column_size, dim], dtype=int)
    for i in range(0, row_size):
        for j in range(0, column_size):
            to3darray_DIFFERENCE[i][j][0] = r_arr.flatten()[i * column_size + j]
            to3darray_DIFFERENCE[i][j][1] = g_arr.flatten()[i * column_size + j]
            to3darray_DIFFERENCE[i][j][2] = b_arr.flatten()[i * column_size + j]

    return to3darray_DIFFERENCE
def calculating_reverse_diff_for_rgb(np_arr_3d,pivotR,pivotG,pivotB):
    r=np_arr_3d[:,:,0]
    g=np_arr_3d[:,:,1]
    b=np_arr_3d[:,:,2]
    rev_diff_r=reverse_difference(r, r.shape[0], r.shape[1], pivotR).flatten()
    rev_diff_g=reverse_difference(g, g.shape[0], g.shape[1], pivotG).flatten()
    rev_diff_b=reverse_difference(b, b.shape[0], b.shape[1], pivotB).flatten()

    return rev_diff_r,rev_diff_g,rev_diff_b


#dict to txt
def dictTotxt(dict, path):
    with open(path, 'w') as f:
        for key, value in dict.items():
            f.write(key + ' ' + value + '\n')

def txtTodict(path):
    dict = {}
    with open(path, 'r') as f:
        for line in f:
            try:
                line = line.strip('\n')
                key, value = line.split(' ')
                if value == '':
                    value = '\n'
                if key == '':
                    pass
                dict[key] = value
            except:
                line = line.strip('\n')
                line = line.strip()
                dict[line] = ' '
                continue
    try:
        del dict['']
    except:
        pass
    return dict
