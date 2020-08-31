# Code for computing, data, models and Graphs for Paper 3.
#
#
# @ Alexander Tureczek, Technical University of Denmark, 2017
#
# Description: Statistical functions for cluster significance check.

import scipy.stats.mstats as sci


aacf = acf_prep(ava)
[mean, model] = clustering.classify(aacf, 7, rs=12345, threshold = 2, plotting= 'Yes', titel = 'ACF clustering')

ploting.class_mean_plot(model, aacf, mean, threshold=2)

aacf.shape

#Select all meters from same class. (0)
aa = aacf[aacf.columns[model.labels_==0]]




#---------------------------------------------------
#           Significance ACF clusters           
#---------------------------------------------------
#identify cluster members.
clust_members = {}
for i in np.unique(model.labels_):
	clust_members['Cluster '+str(i)] = list(aacf.columns[model.labels_==i])

#/AACF test
def non_par_test(data, clust_members):
    for i in range(data.shape[0]-1):
        [test, p] = sci.kruskalwallis(
        list(data[clust_members['Cluster 0']].ix[i+1]),
        list(data[clust_members['Cluster 1']].ix[i+1]),
        list(data[clust_members['Cluster 2']].ix[i+1]),
        list(data[clust_members['Cluster 3']].ix[i+1]),
        list(data[clust_members['Cluster 4']].ix[i+1]),
        list(data[clust_members['Cluster 5']].ix[i+1]))
        #list(data[clust_members['Cluster 6']].ix[i+1]))

        if p < 0.05:
            print('Lag: '+str(i)+' Significant')
        else:
            print('Lag: '+str(i)+' ---***---')



#---------------------------------------------------
#           Significance Noorm clusters       
#---------------------------------------------------


norm_members = {}
for i in np.unique(model.labels_):
	norm_members['Cluster '+str(i)] = list(aacf.columns[model.labels_==i])


#/NORM test
def non_par_test(data, clust_members):
    for i in range(data.shape[0]-1):
        [test, p] = stats.f_oneway(
        list(data[clust_members['Cluster 0']].ix[i+1]),
        list(data[clust_members['Cluster 1']].ix[i+1]),
        list(data[clust_members['Cluster 2']].ix[i+1]),
        list(data[clust_members['Cluster 3']].ix[i+1]))
        #list(data[clust_members['Cluster 4']].ix[i+1]),
        #list(data[clust_members['Cluster 5']].ix[i+1]),
        #list(data[clust_members['Cluster 6']].ix[i+1]))

        if p < 0.05:
            print('Lag: '+str(i)+' Significant')
        else:
            print('Lag: '+str(i)+' ---***---')


	




#/NORM samle gruppe 0 og 1.
def non_par_test(data, clust_members):
    for i in range(data.shape[0]-1):
        [test, p] = sci.kruskalwallis(
        list(data[clust_members['Cluster 0']].ix[i+1])+
        list(data[clust_members['Cluster 1']].ix[i+1]),
        list(data[clust_members['Cluster 2']].ix[i+1]),
        list(data[clust_members['Cluster 3']].ix[i+1]))
        #list(data[clust_members['Cluster 4']].ix[i+1]),
        #list(data[clust_members['Cluster 5']].ix[i+1]),
        #list(data[clust_members['Cluster 6']].ix[i+1]))

        if p < 0.05:
            print('Lag: '+str(i)+' Significant')
        else:
            print('Lag: '+str(i)+' ---***---')
