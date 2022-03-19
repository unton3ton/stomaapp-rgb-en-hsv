# https://www.notabug.org/Tonypythony/

# conda create -n STOMAAPP ### C:\Users\123\miniconda3\envs
### conda activate STOMAAPP

# pip install matplotlib
# pip install Pillow
# pip install --upgrade cx_Freeze

### conda deactivate

from pathlib import Path
from tkinter import filedialog
from tkinter import *
from PIL import ImageTk, Image 
from time import time

from pylab import imshow, array, ginput, close # Matplotlib по умолчанию использует формат RGB

d = 10 # mm

def get_d():
	while True:
		try:
			d = int(input("Please input d = "))
			return d
		except ValueError:
			print("It's not a number!")

def get_modecode():
	while True:
		modecode = input("Please input mode for your image (RGB or HSV): ")
		if modecode == 'RGB' or modecode == 'HSV':
			return modecode
		else:
			print("It's not a modecode for image!")

def get_imagemode(mesMode):
	global image
	while True:
		try:
			if mesMode == 'RGB':
				image = Image.open(filename).convert('RGB')
			elif mesMode == 'HSV':
				image = Image.open(filename).convert('HSV')
			return image
		except ValueError:
			print("It's not a code of imagemode!")

mes = input("Size of scale = 10 mm = 1 cm? If 'yes' press 'Enter', if 'not' print 'not'? ")

if mes == 'not':
	get_d()

mesMode = get_modecode() # выбор режима открытия и работы с изображением

d_sqr = d**2

root = Tk()

current_dir = Path.cwd() # путь текущей директории
filename = filedialog.askopenfilename(initialdir = current_dir, # initialdir = "/run/media/rick/DATA/Kazahi"
 title = "Select imagefile", filetypes = (("JPG files", "*.JPG"),("jpeg files", "*.jpeg"),
 										("jpg files", "*.jpg"),("png files", "*.png"),
 										("bmp files", "*.bmp"),("all files", "*.*")))

x_size_screen = int(root.winfo_screenwidth()/3)
y_size_screen = int(root.winfo_screenheight()/3)

get_imagemode(mesMode) # выбор режима открытия/работы изображения

def color_of_points(img):
	im = array(image)
	imshow(im)
	print('\nPlease click 2 points to determine the scale of the image')
	x = ginput(2)
	y = [(int(p), int(q)) for p, q in x]
	a = [y[0][0], y[0][1], y[1][0], y[1][1]]
	clr1 = img.getpixel(y[0])
	clr2 = img.getpixel(y[1])
	print('Color 1 point {} is'.format((a[0],a[1])), clr1) # color of the first selected pixel
	print('Color 2 point {} is'.format((a[2],a[3])), clr2) # color of the second selected pixel
	global D_sqr
	D_sqr = int((a[0]-a[2])**2+(a[1]-a[3])**2) # distance^2 between selected pixels

	print('\nPlease click 2 points to crop colors: (left, upper, right, lower)')
	x = ginput(2)
	y = [(int(p), int(q)) for p, q in x]

	a = [y[0][0], y[0][1], y[1][0], y[1][1]]
	print(a)
	
	im_crop = image.crop((a[0], a[1], a[2], a[3]))
	global x_crop, y_crop
	x_crop, y_crop = im_crop.size[0], im_crop.size[1]

	imshow(im_crop)

	print('\nPlease click 2 points to for detect colors')
	x = ginput(2)
	y = [(int(p), int(q)) for p, q in x]
	
	clr1 = image.getpixel(y[0])
	clr2 = image.getpixel(y[1])
	close() # закрыть окно с выбором точек
	print('Color 1 point is', clr1) # color of the first selected pixel
	print('Color 2 point is', clr2) # color of the second selected pixel

	return im_crop

image = color_of_points(image)

k = d_sqr / D_sqr # коэффициент масштаба для перевода пикселей в мм

s_1 = image.size[0]*image.size[1]

image = image.resize((x_size_screen,y_size_screen)) 
s_resize = image.size[0]*image.size[1]

x_size_root = int(x_size_screen*1.5)
y_size_root = int(y_size_screen*2.1)

root.geometry('{}x{}'.format(x_size_root,y_size_root)) 

canvas = Canvas(root,width=x_size_screen,height=y_size_screen)

canvas.pack()

pilimage = ImageTk.PhotoImage(image)

imagesprite = canvas.create_image(0,0,image=pilimage, anchor=NW)

container = Frame() # создаём контейнер на главном окне для расположения кнопок и полей ввода
container.pack(side='top', fill='both', expand=True)

redM = 255 # max
redL = 0 # min
greenM = 255 # max
greenL = 0 # min
blueM = 255 # max
blueL = 0 # min

########################################################################

lbl1 = Label(container, text="RedMax = ")  
lbl1.grid(column=6, row=1) 

def get_val_motion1(event):
	global redM
	redM = scal1.get()
	
scal1 = Scale(container, orient=HORIZONTAL, length=int(image.size[0]), from_=0, to=255,
			tickinterval=20, resolution=1)
scal1.bind("<B1-Motion>", get_val_motion1)
scal1.grid(column=7, row=1)

########################################################################

lbl2 = Label(container, text="RedMin = ")  
lbl2.grid(column=6, row=2) 

def get_val_motion2(event_1):
	global redL
	redL = scal2.get()
	
scal2 = Scale(container, orient=HORIZONTAL, length=int(image.size[0]), from_=0, to=255,
			tickinterval=20, resolution=1)
scal2.bind("<B1-Motion>", get_val_motion2)
scal2.grid(column=7, row=2)

########################################################################

lbl3 = Label(container, text="GreenMax = ")  
lbl3.grid(column=6, row=3) 

def get_val_motion3(event):
	global greenM
	greenM = sca3.get()
	
sca3 = Scale(container, orient=HORIZONTAL, length=int(image.size[0]), from_=0, to=255,
			tickinterval=20, resolution=1)
sca3.bind("<B1-Motion>", get_val_motion3)
sca3.grid(column=7, row=3)

########################################################################

lbl4 = Label(container, text="GreenMin = ")  
lbl4.grid(column=6, row=4) 

def get_val_motion4(event_1):
	global greenL
	greenL = scal4.get()
	
scal4 = Scale(container, orient=HORIZONTAL, length=int(image.size[0]), from_=0, to=255,
			tickinterval=20, resolution=1)
scal4.bind("<B1-Motion>", get_val_motion4)
scal4.grid(column=7, row=4)

########################################################################

lbl5 = Label(container, text="BlueMax = ")  
lbl5.grid(column=6, row=5) 

def get_val_motion5(event):
	global blueM
	blueM = scal5.get()
	
scal5 = Scale(container, orient=HORIZONTAL, length=int(image.size[0]), from_=0, to=255,
			tickinterval=20, resolution=1)
scal5.bind("<B1-Motion>", get_val_motion5)
scal5.grid(column=7, row=5)

########################################################################

lbl6 = Label(container, text="BlueMin = ")  
lbl6.grid(column=6, row=6) 

def get_val_motion6(event_1):
	global blueL
	blueL = scal6.get()
	
scal6 = Scale(container, orient=HORIZONTAL, length=int(image.size[0]), from_=0, to=255,
			tickinterval=20, resolution=1)
scal6.bind("<B1-Motion>", get_val_motion6)
scal6.grid(column=7, row=6)

########################################################################

def my_callback3(): # показывает исходную фотографию
	global pilimage
	pilimage = ImageTk.PhotoImage(image)
	global imagesprite
	imagesprite = canvas.create_image(0,0,image=pilimage, anchor=NW)

button3 = Button(container , text="Source" , command=my_callback3)
button3.grid(row=3 ,column=0)

########################################################################

def my_callback6(): # открыть новое изображение
	global filename
	filename = filedialog.askopenfilename(initialdir = current_dir, 
 				title = "Select imagefile", filetypes = (("JPG files", "*.JPG"),("jpeg files", "*.jpeg"),
 										("jpg files", "*.jpg"),("png files", "*.png"),
 										("bmp files", "*.bmp"),("all files", "*.*")))
	global image
	image = Image.open(filename).convert('RGB')

	image = color_of_points(image)	

	image = image.resize((x_size_screen,y_size_screen)) 
	
	global pilimage
	pilimage = ImageTk.PhotoImage(image)
	global imagesprite
	
	imagesprite = canvas.create_image(0,0,image=pilimage, anchor=NW)

button6 = Button(container , text="Open New Image" , command=my_callback6)
button6.grid(row=4 ,column=0)

########################################################################

def my_callback7(): # главная функция - для расчёта изображения
	N = 0 # счётчик
	new_im = []
	start = time() # для тестирования скорости работы
	for i in range(image.size[0]):
		for j in range(image.size[1]):
			if (image.getpixel((i,j))[0] >= redL) and (image.getpixel((i,j))[0] <= redM) \
			and (image.getpixel((i,j))[1] >= greenL) and (image.getpixel((i,j))[1] <= greenM) \
			and (image.getpixel((i,j))[2] >= blueL) and (image.getpixel((i,j))[2] <= blueM):
				N += 1
				new_im.append((i,j,image.getpixel((i,j))))
	
	area = N*s_1/s_resize

	print("\nApproximate result: {:.2} mm^2 = {:.3} cm^2".format(s_1*k, s_1*k*0.01))
	print("\nAccurate result: {:.2} mm^2 = {:.3} cm^2\n".format(area*k, area*k*0.01))
	print("RedL = {}; RedM = {}, \nGreenL = {}; GreenM = {},\
	 \nBlueL = {}; BlueM = {}".format(redL, redM, greenL, greenM, blueL, blueM))

	print("Time: {0:.3f} s".format(float(round((time()-start)*1e3)/1e3))) # для тестирования скорости работы
	global new_image # нужно для возможности сохранения в дальнейшем
	new_image = Image.new("RGB", (image.size[0], image.size[1]))
	for i in range(len(new_im)):
		new_image.putpixel((new_im[i][0], new_im[i][1]), new_im[i][2])

	
	global pilimage
	pilimage = ImageTk.PhotoImage(new_image)
	global imagesprite
	
	imagesprite = canvas.create_image(0,0,image=pilimage, anchor=NW)

button7 = Button(container , text="Result" , command=my_callback7)
button7.grid(row=1 ,column=0)

########################################################################

def my_callback4(): # сохраняет результат
	file_name = filedialog.asksaveasfilename(initialdir = current_dir,
							filetypes = (("png files", "*.png"),
 										("jpg files", "*.jpg"), 
 										("bmp files", "*.bmp"),("all files", "*.*")), defaultextension="")
	global new_image
	new_image = new_image.resize((x_crop, y_crop)) # сохраняем с исходным размером вырезанного кусочка
	new_image.save(file_name)

button4 = Button(container , text="Save Result" , command=my_callback4)
button4.grid(row=2 ,column=0)

########################################################################

root.mainloop()