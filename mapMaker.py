from random import randint
from math import ceil, pow, sqrt
from logMsg import logMessage

def getEuclideanDistance(p1x, p1y, p2x, p2y):
	return sqrt(pow(p1x - p2x, 2) + pow(p1y - p2y, 2))

def assignIndex(centers):
	for index, center in enumerate(centers):
		center['id'] = index
	return centers

	
def assignCenters(region, centers):
	# get ratio of each party to the whole
	ratios = {}
	partyNumber = {}
	for y in region:
		for x in y:
			if x in ratios:
				ratios[x] += 1
			else:
				ratios[x] = 1
	
	# from number of centers, figure out how many should belong to each party
	partyCount = len(centers)
	size = len(region) * len(region[0])
	
	total = 0
	for key, val in sorted(ratios.iteritems(), key = lambda(k, v) : (v, k), reverse = True)[:-1]:
		if total + ceil(partyCount * (float(val) / size)) > partyCount:
			partyNumber[key] = partyCount - int(total)
			total = partyCount
		else:
			partyNumber[key] = int(ceil(partyCount * (float(val) / size)))
			total += ceil(partyCount * (float(val) / size))
			
	partyNumber[sorted(ratios.iteritems(), key = lambda (k, v): (v,k), reverse = True)[-1][0]] = int(partyCount - total)
	
	
	# Assign centers greedily to give whoever has smallest ratio the first choice based on nearby tiles
	centersCpy = centers[:]
	
	for key, val in sorted(partyNumber.iteritems(), key = lambda(k, v): (v, k)):
		centerCounts = []
		
		if val == 0:
			continue
		
		for index, center in enumerate(centersCpy):
			count = 0
			for y in xrange(max(center['y'] - 3, 0), min(center['y'] + 3, len(region))):
				for x in xrange(max(center['x'] - 3, 0), min(center['x'] + 3, len(region[0]))):
					if region[y][x] == key:
						count += 1
			centerCounts.append([index, count])
				
		
		cen = sorted([c for c in centerCounts if 'alignment' not in centers[c[0]]], key = lambda g: g[1], reverse = True)[:val]

		for c in cen:
			centers[c[0]]['alignment'] = key
		
	return centers	
	
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
def generateRandomMap(sizeX, sizeY, parties, partyRatios):
	
	region = [['_' for x in xrange(sizeX)] for y in xrange(sizeY)]
	
	positions = [x for x in xrange(sizeX * sizeY)]
	
	
	for i in xrange(len(parties)):
		membersPerParty = int((sizeX * sizeY) * partyRatios[i])
		party = parties[i]
		for x in xrange(membersPerParty):
			pos = randint(0, len(positions) - 1)
			posX = positions[pos] % sizeX
			posY = positions[pos] // sizeX
			region[posY][posX] = party
			positions.remove(positions[pos])
	
	for x in xrange(len(positions)):
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
def generateClusteredMap(sizeX, sizeY, clusters, parties, partyRatios):
	logMessage( "Importing sklearn")
	from sklearn.datasets import make_blobs
	logMessage("import complete")
	
	region = [[parties[0] for x in xrange(sizeX)] for y in xrange(sizeY)]
	
	x,_ = make_blobs(n_samples = int(sizeX * sizeY * partyRatios[1]), 
		n_features = 2, centers = clusters, 
		cluster_std = sizeX / (clusters * 2), center_box = (0, sizeX))
	
	x = [[ceil(x0[0]), ceil(x0[1])] for x0 in x]
	
	count = int((sizeX * sizeY) * partyRatios[1])
	
	for val in x:
		posX, posY = int(val[0]), int(val[1])
		if posX < sizeX and posY < sizeY and region[posY][posX] == parties[0]:
			region[posY][posX] = parties[1]
			count -= 1
	
	scatterRemainder(region, count, parties[1])
			
	return region
	
	