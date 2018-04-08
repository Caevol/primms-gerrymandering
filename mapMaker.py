from random import randint
from math import ceil, pow, sqrt

def getEuclideanDistance(p1x, p1y, p2x, p2y):
	return sqrt(pow(p1x - p2x, 2) + pow(p1y - p2y, 2))

##### center generator #####
def getRandomCenters(region, radius, centerCount):
	centers = []
	sizeY = len(region)
	sizeX = len(region[0])
	for i in xrange(centerCount):
		repeat =True
		while repeat == True:
			repeat = False
			pos = randint(0, sizeY * sizeX - 1)
			posX = pos % sizeX
			posY = pos / sizeY
			for center in centers:
				if getEuclideanDistance(posX, posY, center['x'], center['y']) < radius:
					repeat = True
		centers.append({'x' : posX, 'y' : posY})

	return centers

def getManualCenters(region):
	print 'How many districts?'
	districtNum = int(raw_input())
	
	centers = []
	
	for i in xrange(districtNum):
		print 'Center', i
		print 'x:'
		x = int(raw_input())
		print 'y:'
		y = int(raw_input())
		centers.append({'x':x,'y':y})

	return centers
		
##### Map creators #####

#parties should be a list of single character party ids
def generateRandomMap(sizeX, sizeY, parties):
	
	region = [['_' for x in xrange(sizeX)] for y in xrange(sizeY)]
	
	positions = [x for x in xrange(sizeX * sizeY)]
	
	membersPerParty = (sizeX * sizeY) // len(parties)
	
	for party in parties:
		for x in xrange(membersPerParty):
			pos = randint(0, len(positions) - 1)
			posX = positions[pos] % sizeX
			posY = positions[pos] // sizeX
			region[posY][posX] = party
			positions.remove(positions[pos])
	
	for x in xrange((sizeX * sizeY) % len(parties)):
		posX = positions[x] % sizeX
		posY = positions[x] // sizeX
		region[posY][posX] = party[0]
		positions.remove(positions[x])

	return region

def scatterRemainder(region, count, party):
	
	positions = []
	for y in xrange(len(region)):
		for x in xrange(len(region[y])):
			if region[y][x] != party:
				positions.append([y, x])
					
	for i in xrange(count):
		pos = randint(0, len(positions) - 1)
		region[positions[pos][0]][positions[pos][1]] = party
		del positions[pos]
		
# Generate parties lines so b tends to form clusters and red forms the rest.
def generateClusteredMap(sizeX, sizeY, clusters, parties):
	from sklearn.datasets import make_blobs

	region = [[parties[0] for x in xrange(sizeX)] for y in xrange(sizeY)]
	
	x,_ = make_blobs(n_samples = (sizeX * sizeY // 2), 
		n_features = 2, centers = clusters, 
		cluster_std = sizeX / (clusters * 2), center_box = (0, sizeX))
	
	x = [[ceil(x0[0]), ceil(x0[1])] for x0 in x]
	
	count = (sizeX * sizeY) // 2
	
	for val in x:
		posX, posY = int(val[0]), int(val[1])
		if posX < sizeX and posY < sizeY and region[posY][posX] == parties[0]:
			region[posY][posX] = parties[1]
			count -= 1
	
	scatterRemainder(region, count, parties[1])
			
	return region
	
	