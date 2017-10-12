#!/usr/bin/env python
import matplotlib.pyplot as pyplot
import time
import random

if __name__== "__main__":
    dataX = [];dataY = [];
    #  open file
    f=open('realdata.txt')
    # initilise figures and plots
    fig = pyplot.figure()
    fig1 = pyplot.figure()
    plt = fig.add_subplot(111)
    plt1 = fig1.add_subplot(111)
    plt.set_xlabel('Length')
    plt.set_ylabel('Width')
    plt.set_title('Given data without clustering')
    plt1.set_xlabel('Length')
    plt1.set_ylabel('Width')
    plt1.set_title('K-Means algorithm')
    for line in f:
        data = line.split();
        dataX.append(float(data[1]))
        dataY.append(float(data[2]))
        plt.plot(dataX,dataY,'rs')
    mean_old_1 = {}
    mean_old = {}
    mean_new = {}
    d2 = []
    totCluster = 4
    for noCluster in range(totCluster):
        mean_old.update({noCluster+1:[random.uniform(0,4),random.uniform(-1,1)]})
    mean_new.update(mean_old)
    mean_old_1.update(mean_old)

    clusterInfo = [-1]*len(dataX)
    clusterSize = [0]*len(mean_new)

    print "Initial Mean", mean_new
    time.sleep(2)
    for iterI in range(len(mean_new)):
        d2.append(-1.0)
    while True:
        for i in range(len(dataX)):
            for cluster in range(len(d2)):
                d2[cluster] = pow((dataX[i]-mean_new[cluster+1][0]),2)+pow((dataY[i]-mean_new[cluster+1][1]),2)
            clusterInfo[i] = d2.index(min(d2))+1
        mean = [0]*2*len(mean_new)
        clusterSize = [0]*len(mean_new)
        for i in range(len(dataX)):
            temp = clusterInfo[i]-1
            # print temp
            clusterSize[temp] += 1
            mean[(2*temp)] += dataX[i]
            mean[(2*temp)+1] += dataY[i]
        for i in range(len(mean)/2):
            mean[2*i]/=clusterSize[i]
            mean[(2*i)+1]/=clusterSize[i]
            mean_new[i+1] = [mean[2*i],mean[(2*i)+1]]
        if abs(float(mean_new[1][0])-float(mean_old[1][0])) < 0.01 and abs(float(mean_new[1][1])-float(mean_old[1][1])) < 0.01 and abs(float(mean_new[2][0])-float(mean_old[2][0])) < 0.01 and abs(float(mean_new[2][1])-float(mean_old[2][1])) < 0.01:
            break
        mean_old.update(mean_new)

    print "New Mean", mean_new
    # plotting means of the cluster
    i = 1
    for meanXY in mean_new:
        plt1.scatter(mean_new[meanXY][0],mean_new[meanXY][1],marker='x', s=169, linewidths=3,
        color='k', zorder=10)
        label = 'Cluster ' + str(i)
        i+=1
        plt1.text(mean_new[meanXY][0],mean_new[meanXY][1],label,fontsize=14,style='italic', bbox={'facecolor':'white', 'alpha':0.5, 'pad':3})

    for i in range(len(dataX)):
        if clusterInfo[i] == 1:
            k = plt1.plot(dataX[i],dataY[i],'ro',label = "Cluster 1")
        if clusterInfo[i] == 2:
            z = plt1.plot(dataX[i],dataY[i],'bs',label = "Cluster 2")
        if clusterInfo[i] == 3:
            plt1.plot(dataX[i],dataY[i],'m*',label = "Cluster 3")
        if clusterInfo[i] == 4:
            plt1.plot(dataX[i],dataY[i],'gp',label = "Cluster 4")
        if clusterInfo[i] == 5:
            plt1.plot(dataX[i],dataY[i],'kh',label = "Cluster 5")
        if clusterInfo[i] == 6:
            plt1.plot(dataX[i],dataY[i],'yx',label = "Cluster 6")
        if clusterInfo[i] == 7:
            plt1.plot(dataX[i],dataY[i],'cd',label = "Cluster 7")
        if clusterInfo[i] == 8:
            plt1.plot(dataX[i],dataY[i],'k1',label = "Cluster 8")

    pyplot.show()
