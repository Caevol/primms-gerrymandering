from Tkinter import *

HEIGHT = 1000
WIDTH = 1000
colors = {
	'r' : 'red',
	'b' : 'blue',
	'g' : 'green',
	'w' : 'white',
	'c' : 'cyan',
	'y' : 'yellow',
}

def getColor(party):
	try:
		return colors[party]
	except keyError:
		return 'black'

def drawMap(regions, claims, centers):

	top = Tk()
	
	can = Canvas(top, width = WIDTH, height = WIDTH)
	can.pack()

	
	sizeY = len(regions)
	sizeX = len(regions[0])
	
	ratioX = WIDTH / sizeX
	ratioY = HEIGHT / sizeY
	
	#draw squares and claims
	for y in xrange(sizeY):
		for x in xrange(sizeX):
			can.create_rectangle(ratioX * x, ratioY * y, 
				ratioX * (x+1), ratioY * (y + 1), fill = getColor(regions[y][x]))

	#draw centers
	if centers != None:
		for center in centers:
			if 'id' in center:
				can.create_oval(ratioX * (center['x'] + .1), ratioY * (center['y'] + .1), 
					ratioX * (center['x'] + .9), ratioY * (center['y'] + .9), fill = 'magenta')
				can.create_text(ratioX * (center['x'] + .5), ratioY * (center['y'] + .5), text = center['id'])
			else:
				can.create_oval(ratioX * (center['x'] + .1), ratioY * (center['y'] + .1), 
					ratioX * (center['x'] + .9), ratioY * (center['y'] + .9), fill = 'magenta')
	
	#draw boundaries of claims
	if claims != None:
		for y in xrange(sizeY):
			for x in xrange(sizeX):
				#can.create_text(ratioX * (x + .5), ratioY * (y + .5), text = claims[y][x])
				
				if y < sizeY - 1 and claims[y][x] != claims[y + 1][x]:
					can.create_line(ratioX * (x), ratioY * (y + 1), ratioX * (x + 1), ratioY * (y + 1), fill = "magenta", width = 5.0)
	
				if x < sizeX - 1 and claims[y][x] != claims[y][x + 1]:
					can.create_line(ratioX * (x + 1), ratioY * (y), ratioX * (x + 1), ratioY * (y + 1), fill = "magenta", width = 5.0)

	
	top.mainloop()
			
