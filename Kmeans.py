import numpy as np

def randCent(dataset, k):

	n = dataset.shape[1]
	centerMat = np.zeros(k ,n)

	for i in range(n):
		minJ = min(dateset[:,j])
		rangeJ = float(max(dataset[:,j] -minJ)
		centerMat[:,j] = minJ + rangeJ*random.rand(k,1)
	return centerMat

def distEclud(vecA , vecB):
	return np.sqrt(np.sum(np.power(vecA - vecB , 2)))
	

def K_means(dataset, k):

	m = dataset.shape[0]
	centerMat = np.zeros([m,2])
	center = randCent(dataset,k)
	centerChan = True

	while centerChan:
		centerChan = False
		for i in range(m):
			minDist = inf
			minIdx = -1
			for j in range(k):
				dist = distEclud(dataset[i,:] , center[j,:])
				if dist < minDist:
					minDist = dist
					minIdx = j
			if centerMat[i,0] != minIdx:
				centerChan = True
			centerMat[i,:] = minIdx , minDist

		for cent in range(k):
			pts = dataset[np.nonzero(centerMat[:,0]==cent)[0]]
			center[cent,:] = np.mean(pts, axis = 0)

	return center, centerMat
