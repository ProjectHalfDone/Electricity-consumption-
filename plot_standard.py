def graf():
    #30 for single figures, 60 for side-by-side figures
    size = 30
    y = list(cdi.keys())

    fig = plt.figure()
    ax = fig.add_subplot(111)

    
    ax.plot(y, list(cdi.values()),'k', label= 'CDI Index')
    ax.plot(y, list(dbi.values()),'b', label = 'DBI Index')
    #plt.plot(y, list(sil.values()),'g', label = 'Silhouette Index')
    ax.plot(y, list(mia.values()),'r', label = 'MIA Index')

    ax.xaxis.set_major_locator(MaxNLocator(integer=True))


    plt.title('Index Development - Normalized Data', fontsize = size)

    plt.xlabel('# of Clusters', fontsize=size*(5/6))
    plt.ylabel('Index Value', fontsize=size*(5/6))

    plt.legend(fontsize=size*(4/6))
    plt.tick_params(axis='both', which='major', labelsize=size/2)

    plt.grid()
    plt.show(block=False)




def plott():
    '''label er fra rdy_date.index

    over <== hh = gg[(gg < 0.5)] indicating consumption increase +200%

    '''
    
    size = 30
    fig = plt.figure()
    ax = fig.add_subplot(111)
    plt.plot(label, rdy_date[over.index[0]].values, color = 'r', linewidth=2)
    plt.plot(label, rdy_date[over.index[25]].values, color = 'b', linewidth=2)
    plt.plot(label, rdy_date[over.index[51]].values, color = 'g', linewidth=2)
    plt.plot(label, rdy_date[over.index[76]].values, color = 'k', linewidth=1.25)
    
    ax.text('2011-01-12', 2.5, "Week 1", color='k', fontsize = size, fontweight='bold', style ='italic')
    ax.text('2011-01-20', 2.5, "Week 2", color='k', fontsize = size, fontweight='bold', style ='italic')
    plt.title('200% Consumption Increase week-on-week', fontsize=size)
    plt.xlabel('Date', fontsize=size*(5/6))
    plt.ylabel('Consumption Index', fontsize=size*(5/6))
    plt.tick_params(axis='both', which='major', labelsize=size/2)
    plt.grid()
    plt.show(block=False)








def nfold(lst, splits):

    '''
    nfold is a method for splitting a list into n splits for cross-validation.
    it takes as input a list randomizes the list and removes n equally sized sublists from the list like n fold cross validation
    the output is dictionary with n different sub lists ready for input for clustering. 

    Syntax:

    final_list = nfold(lst, splits)
    
    input:
        lst = list to be split into sublists

        splits = number of splits to perform

    output:
        final_list = dictionary with all sublists ready for clustering. 


    '''

    #initialize sets
    rlst =  np.random.permutation(lst)
    lst = set(lst)
    size = len(rlst)

    #initialize variables
    final_list = {}
    pcs = int(round(size/splits, 0))
    start = 0

    #create sublists using sets. created by moving a window across the list. 
    for i in range(splits):
        end = pcs+start
        drop = set(rlst[start:end])
        
        start = end
        final_list[i] = lst.difference(drop)
        #print(drop, 'Remainder',lst.difference(drop))
        #print(drop, 'Remainder',final_list[i])
    return final_list


def acf_plot(meter):
    size = 30
    fig = plt.figure()
    ax1 = fig.add_subplot(131)
    ax2 = fig.add_subplot(132)
    ax3 = fig.add_subplot(133)

    [auto, conf, qstat, pvalues] = acf(se[meter], qstat=True, alpha=0.05, nlags=48)

    ax1.plot(se[meter])
    ax1.set_title('Original Consumption', fontsize=size*(5/6))
    
    plt.sca(ax1)
    plt.xticks(rotation=45)
    
    ax2.plot(auto, color = 'b', linewidth=2)
    ax2.plot(conf[:,0], color = 'b', linestyle = '--', linewidth = 1)
    ax2.plot(conf[:,1], color = 'b', linestyle = '--', linewidth = 1)
    ax2.axhline(0, color = 'k')
    ax2.set_title('Series Autocorrelation', fontsize=size*(5/6))

    #significanse correction
    if conf.min()<=0:
            auto[conf[:,0]<=0]=0
    
    ax3.plot(auto)
    ax3.set_title('Retained Significant Features', fontsize=size*(5/6))

    ax2.set_xlabel('Lag', fontsize=size*(5/6))
    ax3.set_xlabel('Lag', fontsize=size*(5/6))
    
    ax1.set_ylabel('Consumption kWh', fontsize=size*(5/6))
    ax1.tick_params(axis='both', which='major', labelsize=size/2)
    ax2.tick_params(axis='both', which='major', labelsize=size/2)
    ax3.tick_params(axis='both', which='major', labelsize=size/2)

    
    plt.show(block=False)
    



#tt = norm.columns[:100]
#cv_rdy = nfold(tt,10)


def cv_nfold(data, cv_rdy, max_clusters=4, size = 30, titel = 'Normalized Data, 10 Fold Pseudo Cross-Validation'):
    #size = 30

    silhouette = pd.DataFrame()
    mia_ind = pd.DataFrame()
    cluster_db = pd.DataFrame()
    davies = pd.DataFrame()


    for i in cv_rdy:
        [sil, mia, cdi, dbi, inerti, models, c_pct] = clusters(data[list(cv_rdy[i])], max_clusters, 12345)

        silhouette[i] = sil.values()
        mia_ind[i] = mia.values()
        cluster_db[i] = cdi.values()
        davies[i] = dbi.values()

    
    x = list(range(2,max_clusters+1,1))

    sil_pm = pd.DataFrame()
    mia_pm = pd.DataFrame()
    cdi_pm = pd.DataFrame()
    dbi_pm = pd.DataFrame()
         
    sil_pm['Upper'] = silhouette.max(axis=1)
    sil_pm['Lower'] = silhouette.min(axis=1)
    sil_pm['Mean'] = silhouette.mean(axis=1)

    mia_pm['Upper'] = mia_ind.max(axis=1)
    mia_pm['Lower'] = mia_ind.min(axis=1)
    mia_pm['Mean'] = mia_ind.mean(axis=1)

    cdi_pm['Upper'] = cluster_db.max(axis=1)
    cdi_pm['Lower'] = cluster_db.min(axis=1)
    cdi_pm['Mean'] = cluster_db.mean(axis=1)

    dbi_pm['Upper'] = davies.max(axis=1)
    dbi_pm['Lower'] = davies.min(axis=1)
    dbi_pm['Mean'] = davies.mean(axis=1)

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))

    ax.plot(x, sil_pm['Mean'], 'b', linewidth=3, label = 'Silhouette Mean')
    ax.plot(x, dbi_pm['Mean'], 'r', linewidth=3, label = 'DBI Mean')
    ax.plot(x, mia_pm['Mean'], 'k', linewidth=3, label = 'MIA Mean')
    ax.plot(x, cdi_pm['Mean'], 'g', linewidth=3, label = 'CDI Mean')
             
    ax.plot(x, sil_pm['Lower'], 'b--', linewidth=1, label='_nolegend_')
    ax.plot(x, sil_pm['Upper'], 'b--', linewidth=1, label='_nolegend_')

    ax.plot(x, mia_pm['Lower'], 'k--', linewidth=1, label='_nolegend_')
    ax.plot(x, mia_pm['Upper'], 'k--', linewidth=1, label='_nolegend_')

    ax.plot(x, cdi_pm['Lower'], 'g--', linewidth=1, label='_nolegend_')
    ax.plot(x, cdi_pm['Upper'], 'g--', linewidth=1, label='_nolegend_')

    ax.plot(x, dbi_pm['Lower'], 'r--', linewidth=1, label='_nolegend_')
    ax.plot(x, dbi_pm['Upper'], 'r--', linewidth=1, label='_nolegend_')

    plt.legend(loc='upper right')

    plt.title(titel, fontsize=size)
    plt.xlabel('# of Clusters', fontsize=size*(5/6))
    plt.ylabel('Index Value', fontsize=size*(5/6))
    plt.legend(fontsize=size*(4/6))
    plt.tick_params(axis='both', which='major', labelsize=size/2)
    plt.grid()

    plt.show(block=False)

    return sil_pm, mia_pm, cdi_pm, dbi_pm

    #[sil_pm, mia_pm, cdi_pm, dbi_pm] = cv_nfold(norm, cv_rdy)





