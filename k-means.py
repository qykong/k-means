#!/usr/bin/env python
import csv
import math
import random
import sys

def readCsv(filename):
    i = 0
    dataset = {}
    with open(filename, 'rb') as csvfile:
        data = csv.reader(csvfile, delimiter=',')
        for row in data:
            dataset[i] = row
            i=i+1
    return dataset

def Euclidean(p1,p2):
    total = 0.0
    for idx,number1 in enumerate(p1):
        #if this is not numerical value, then jump to another iteration
        try:
            number2 = p2[idx]
            total += math.pow(float(number1)-float(number2),2)
        except:
            continue
    return math.sqrt(total)

def Manhatten(p1,p2):
    total = 0.0
    for idx,number1 in enumerate(p1):
        try:
            number2 = p2[idx]
            total += math.fabs(float(number1)-float(number2))
        except:
            continue
    return total

def Cosine(p1,p2):
    p1p2 = 0
    p1Euclidean = 0
    p2Euclidean = 0
    for idx,number1 in enumerate(p1):
        try:
            number2 = p2[idx]
            n1f = float(number1)
            n2f = float(number2)
        except:
            continue
        p1p2 += n1f*n2f
        p1Euclidean += math.pow(n1f,2)
        p2Euclidean += math.pow(n2f,2)
    return 1-(p1p2/(math.sqrt(p1Euclidean)*math.sqrt(p2Euclidean)))

def randomInit(dataset,k):
    kcentroids = {}
    randindices = random.sample(range(len(dataset)),k)
    i = 0
    for index in randindices:
        kcentroids[i] = dataset[index][:]
        i += 1
    return kcentroids

def ffInit(dataset,distanceFunction,k):
    firstIndex = random.sample(range(len(dataset)),1)[0]
    kcentroids = {}
    kcentroids[0] = dataset[firstIndex][:]
    isInKCentroids = [firstIndex]
    for j in range(k-1):
        maxDis = 0
        maxIdx = 0
        for dIdx in dataset:
            dis = 0
            if dIdx in isInKCentroids:
                continue
            for i in kcentroids:
                if distanceFunction == 1:
                    dis += Manhatten(kcentroids[i],dataset[dIdx])
                elif distanceFunction == 2:
                    dis += Euclidean(kcentroids[i],dataset[dIdx])
                elif distanceFunction == 3:
                    dis += Cosine(kcentroids[i],dataset[dIdx])
            if dis>maxDis:
                maxDis = dis
                maxIdx = dIdx
        kcentroids[j+1] = dataset[maxIdx][:]
        isInKCentroids.append(maxIdx)
    return kcentroids

def kMeans(dataset,k,distanceFunction,maxIterations,initFunction):
    if initFunction == 1:
        kCentroids = randomInit(dataset,k)
    elif initFunction == 2:
        kCentroids = ffInit(dataset,distanceFunction,k)
    else:
        print "Unknown initial function."
    unChanged = False
    global iterations #used to count current number of iterations
    while iterations<maxIterations and not unChanged:
        kClusters = {}
        for t in range(k):
            kClusters[t] = []
            kClusters[t].append(kCentroids[t])#avoid the case when there are centrods share same distances
        unChanged = True
        #(re)assign each object to clusters
        for dIdx in dataset:
            minIdx = 0
            minDis = sys.float_info.max
            for idx in range(k):
                if distanceFunction == 1:
                    dis = Manhatten(kCentroids[idx],dataset[dIdx])
                elif distanceFunction == 2:
                    dis = Euclidean(kCentroids[idx],dataset[dIdx])
                elif distanceFunction == 3:
                    dis = Cosine(kCentroids[idx],dataset[dIdx])
                if dis < minDis:
                    minIdx = idx
                    minDis = dis
            kClusters[minIdx].append(dataset[dIdx])
        #calculate the mean value of every class
        for cIdx in kClusters:
            s = kClusters[cIdx][0][:] #must pass by value instead of reference
            #s is defined to calculate mean value
            for idx,attribute in enumerate(s):
                try:
                    float(attribute)
                except:
                    continue
                s[idx] = 0
            for j,o in enumerate(kClusters[cIdx]):
                if j==0:#ignore the first value which is the centroid
                    continue
                for idx,attribute in enumerate(o):
                    try:
                        float(attribute)
                    except:
                        continue
                    s[idx] += float(attribute)
            if j!=0:#if there is only one value, then no need to calculate centroids
                for idx,attribute in enumerate(s):
                    try:
                        float(attribute)
                    except:
                        continue
                    s[idx] = float(attribute)/len(kClusters[cIdx])
                    if unChanged and kCentroids[cIdx][idx] != s[idx]:
                        unChanged = False
                    kCentroids[cIdx][idx] = s[idx]
        iterations += 1
    for x in range(k):
        del kClusters[x][0]#remove the centroids which is the first values in clusters
    return kClusters

if __name__ == '__main__':
    # filename = raw_input('Enter a filename:')
    # k = raw_input('Enter the value of k:')
    # maxIterations = raw_input("Enter the maximum iterations:")
    # distanceFunction = raw_input("Choose a distance function\n1.Manhatten\n2.Euclidean\n3.Cosine\nEnter the number:")
    # initFunction = raw_input("Choose a initial function\n1.Random initial function\n2.Farthest first initial function\nEnter the number:")
    # dataset = readCsv(filename)
    # iterations = 0
    # Centroids = kMeans(dataset,int(k),int(distanceFunction),int(maxIterations),int(initFunction))
    # print "The k centrods are listed as following:"
    # for idx in Centroids:
        # sys.stdout.write("%3s "%(idx+1))
        # for attribute in Centroids[idx]:
            # try:
                # float(attribute)
            # except:
                # continue
            # sys.stdout.write("%.5f "%(attribute))
        # sys.stdout.write("\n")
    # print "\nThe number of iterations is %s."%(iterations)
    filename = "abalone3.csv"#raw_input('Enter a filename:')
    # k = raw_input('Enter the value of k:')
    k = 3
    maxIterations = 400#raw_input("Enter the maximum iterations:")
    distanceFunction = raw_input("Choose a distance function\n1.Manhatten\n2.Euclidean\n3.Cosine\nEnter the number:")
    initFunction = raw_input("Choose a initial function\n1.Random initial function\n2.Farthest first initial function\nEnter the number:")
    dataset = readCsv(filename)
    iterations =0
    Clusters = kMeans(dataset,int(k),int(distanceFunction),int(maxIterations),int(initFunction))
    for idx in Clusters:
        sys.stdout.write('%s, '%(len(Clusters[idx])))
    for t in range(3):
        m = 0
        f = 0
        i = 0
        for j,o in enumerate(Clusters[t]):
            if o[0] == 'M':
                m+=1
            elif o[0] == 'F':
                f+=1
            elif o[0] == 'I':
                i+=1
        sys.stdout.write('m=%s f=%s i=%s, '%(m,f,i))
