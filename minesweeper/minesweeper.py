import pynput
import numpy as np
import PIL
from PIL import Image
from PIL import ImageGrab
import random

import time
# time.sleep(3)

# with pynput.mouse.Events() as events:
#     # Block at most one second
#     event = events.get(10.0)
#     if event is None:
#         print('You did not interact with the mouse within one second')
#     else:
#         print('Received event {}'.format(event))

# mouse = pynput.mouse.Controller()
# mouse.position = (30, 270)

# each square is 24x24
# time.sleep(3)
# mouse = pynput.mouse.Controller()
# mouse.position = (33+16*29, 227+16*15)#first to right, second down.
# keyboard = pynput.keyboard.Controller()
# keyboard.press(' ')
# keyboard.release(' ')

# for i in range(20):
# 	mouse.click(pynput.mouse.Button.left, 1)
# 	print('clicked')
# 	time.sleep(2)
# 	mouse.position = (30+24*i, 270+24*i)


# for i in range(30):
# 	for j in range(16):
# 		mouse = pynput.mouse.Controller()
# 		mouse.position = (30+24*i, 270+24*j)
# 		keyboard = pynput.keyboard.Controller()
# 		keyboard.press(' ')
# 		keyboard.release(' ')
# 		# keyboard.press('a')
# 		# keyboard.release('a')	
# 		time.sleep(0.015) #need a buffer period or else site to slow to process


#keep minesweeper window at 100% zoom
#and all the way up (top of google chrome window touches the finder bar)
#and all the way to the left (left of window = left of screen)
#keep minesweeper window just so you can see the entire grid and a little whitespace
	#around it, but not more than that

# cap2 = ImageGrab.grab(bbox =(40, 516, 40+48*30, 516+48*16))
# print(PIL)
# cap.show() #shows the image

# box1 = cap.crop((0,0,48,48)) #gets the first box ("cap" image is reindexed to 0,0)
# box1arr = np.asarray(box1) #turns image into numpy array
# box1.save('/Users/srinivasansathiamurthy/Desktop/minesweeper/not_cleared.png') #saves image
# not_cleared_box = PIL.Image.open('/Users/srinivasansathiamurthy/Desktop/minesweeper/not_cleared.png') #opens image


#a = 52, b = 436, w = 32
time.sleep(2)
b0 = np.asarray(Image.open('0.png')) #denoted as 0
b1 = np.asarray(Image.open('1.png')) #denoted as 1
b2 = np.asarray(Image.open('2.png')) #denoted as 2
b3 = np.asarray(Image.open('3.png')) #denoted as 3
b4 = np.asarray(Image.open('4.png')) #denoted as 4
b5 = np.asarray(Image.open('5.png')) #denoted as 5
b6 = np.asarray(Image.open('6.png')) #denoted as 6
b7 = np.asarray(Image.open('7.png')) #denoted as 7
bomb = np.asarray(Image.open('bomb.png')) #denoted as 8
flag = np.asarray(Image.open('flag.png')) #denoted as 9
not_cleared_box = np.asarray(Image.open('not_cleared_box.png')) #denoted as 10
red_bomb = np.asarray(Image.open('red_bomb.png')) #denoted as 11
box_list = [b0, b1, b2, b3, b4, b5, b6, b7, bomb, flag, not_cleared_box, red_bomb]
bls = []
for i in box_list:
	bls.append(np.sum(i)-255*32*32)



solving_grid = np.ones((16,30))*12

def get_grid():
	verity = False
	cap = ImageGrab.grab(bbox =(52, 436, 52+32*30, 436+32*16)) #length x height
	# cap.show()
	grid = np.zeros((16,30))
	for i in range(30):
		for j in range(16):
			tempboximg = cap.crop((32*i, 32*j, 32*i+32, 32*j+32))
			tempbox = np.asarray(tempboximg)
			templist = np.array([900000000,900000000,900000000,900000000,900000000,900000000,900000000,900000000,900000000,900000000,900000000,900000000])
			for index, k in enumerate(box_list):
				templist[index] = (np.sum(tempbox)-255*32*32-bls[index])**2
			grid[j,i] = np.argmin(templist)
			if(grid[j,i] == 2):
				if(int(tempbox[15,15,2]) > 8*(int(tempbox[15,15,1]) + int(tempbox[15,15,0]))):
					grid[j,i] = 4
	return grid



areyoudoneyet = True

while(areyoudoneyet):
	breakout_verity = False

	solved_idx = []
	unsolved_idx = []
	preops = -1
	curops = 0

	loopcnt=0
	while(len(solved_idx) < 30*16 and curops != preops):
		preops = curops


		solving_grid = np.minimum(solving_grid, get_grid())
		#look through solving_grid for indexes you need to solve, and ones you have visited
		allemps = set()
		allfilled = set()
		for i in range(16):
			for j in range(30):
				#if you haven't visited this one yet and it's not 10:
				if((solving_grid[i,j] != 10) and (solving_grid[i,j] != 0) and ((i,j) not in solved_idx)):
					unsolved_idx.append((i,j))
					curops+=1
				#if it needs to be solved
		for i in range(16):
			for j in range(30):
				if((i,j) in unsolved_idx):
					curnum = solving_grid[i,j]
					curemp = 0
					curflag = 0
					curnotemp = 0
					curempidx = []
					for xl in [-1,0,1]:
						for yl in [-1,0,1]:
							if((i+xl > -1) and (i+xl < 16) and (j+yl > -1) and (j+yl < 30) and (xl*yl+xl+yl != 0) and not breakout_verity):
								if(solving_grid[i+xl, j+yl] == 9):
									curflag+=1
								elif(solving_grid[i+xl, j+yl] == 10):
									curemp+=1
									curempidx.append((i+xl,j+yl))
								elif(solving_grid[i+xl, j+yl] < 8):
									curnotemp+=1
								else:
									print("game over")
									solving_grid = np.ones((16,30))*12
									# unsolved_idx = []
									breakout_verity = True
									break
						if(breakout_verity):
							break
					if(curnum == (curemp+curflag) and (curemp > 0)):
						print('fc: ', (i,j))
						solved_idx.append((i,j))
						unsolved_idx.remove((i,j))
						for k in curempidx:
							allemps.add(k)
					if(curnum == curflag and (curemp > 0)):
						print('sc: ', (i,j))
						allfilled.add((i,j))
						solved_idx.append((i,j))
						unsolved_idx.remove((i,j))
				if(breakout_verity):
					break
			if(breakout_verity):
				break

		if(breakout_verity):
			mouse = pynput.mouse.Controller()
			mouse.position = (27+16*15,227-40)
			mouse.click(pynput.mouse.Button.left, 1)
			mouse.click(pynput.mouse.Button.left, 1)
			time.sleep(2)

			initialguesslist = []
			for i in range(16):
				for j in range(30):
					initialguesslist.append((i,j))
			initialguess_list = random.sample(initialguesslist, 3)
			for k1 in initialguess_list:
				curops+=1
				print(k)
				mouse = pynput.mouse.Controller()
				mouse.position = (33+16*k1[1], 227+16*k1[0])
				mouse.click(pynput.mouse.Button.left, 2)
				# mouse.click(pynput.mouse.Button.left, 1)
				print("OIII")
				time.sleep(0.015)

			break
		# verity = False
		print('allemps: ', allemps)
		print('allfilled: ', allfilled)
		for k in allemps:
			curops+=1
			print(k)
			mouse = pynput.mouse.Controller()
			mouse.position = (33+16*k[1], 227+16*k[0])
			# time.sleep(0.15)
			keyboard = pynput.keyboard.Controller()
			keyboard.press(' ')
			keyboard.release(' ')
			print("OIII")
			time.sleep(0.015)
		for k in allfilled:
			curops+=1
			print(k)
			mouse = pynput.mouse.Controller()
			mouse.position = (33+16*k[1], 227+16*k[0])
			# time.sleep(0.15)
			keyboard = pynput.keyboard.Controller()
			keyboard.press(' ')
			keyboard.release(' ')
			print("OIII")
			time.sleep(0.015)
		mouse = pynput.mouse.Controller()
		mouse.position = (33+16*40, 227+16*40)	
		if(len(allemps)+len(allfilled) == 0):
			tempcnt = 0
			randind = []
			for l1 in range(16):
				for l2 in range(30):
					if(solving_grid[l1,l2] == 10):
						tempcnt+=1
						randind.append((l1,l2))
			guess_list = random.sample(randind, 1)
			if(tempcnt == 0):
				areyoudoneyet = False
				break
			for k in guess_list:
				curops+=1
				print(k)
				mouse = pynput.mouse.Controller()
				mouse.position = (33+16*k[1], 227+16*k[0])
				mouse.click(pynput.mouse.Button.left, 2)
				# mouse.click(pynput.mouse.Button.left, 1)
				print("OIII")
				time.sleep(0.015)


# # print("something happened?")
# print(solving_grid.T)









#turn off terminal's ability to screen record after using this app!


