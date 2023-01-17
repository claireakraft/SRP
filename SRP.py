# -*- coding: utf-8 -*-
"""
Created on Tue Aug  2 10:47:01 2022

@author: 13096
"""

import pandas as pd
import os 
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA

os.chdir('C:\\Users\\13096\\Documents\\SRP\\FormatedEcoPlateExcelData')

data = pd.read_csv('ecoplatedataforplotting.csv')

##data = pd.read_csv('WFS3.csv')

data['category'].replace({'carbohydrate ': 'carbohydrate',
              'amino acid ': 'amino acid',
              'carboxylic or ketonic acid ': 'carboxylic or ketonic acid',
              'phenolics ': 'phenolics'},
             inplace=True)

data['drought'].replace({'ambient ': 'ambient'},
             inplace=True)

data['insects'].replace({'control ': 'control'},
             inplace=True)

avgdata = data.groupby(['month', 'site', 'plot', 'drought', 'insects', 'enzyme', 'category', 'time'])['OD'].mean().reset_index() 
sgaug = avgdata.loc[(avgdata['site']=='Spring Green') & (avgdata['month']=='July')]

 
def transform(group):
    water0 = group.loc[(group['enzyme']=='Water') & (group['time']==0), 'OD']
    group['OD'] = group['OD'] - water0.values
    group.loc[group['OD'] < 0, 'OD'] = 0.00
    return group
    
 #enames = avgdata['enzyme'].unique()
 #tnames = avgdata['time'].unique()


subdata = sgaug.groupby(['month', 'site', 'plot', 'drought', 'insects']).apply(transform)
    

#testgroupby = avgdata.groupby(['month', 'site', 'plot', 'drought', 'insects'])
#testgroup = testgroupby.get_group(list(testgroupby.groups.keys())[0])
#water0 = testgroup.loc[(testgroup['enzyme']=='Water') & (testgroup['time']==0), 'OD']
#testgroup['OD'] = testgroup['OD'] - water0.values
#testgroup.loc[testgroup['OD'] < 0, 'OD'] = 0.00



#HEAT MAPS



def heat(group):
    mname = group['month'].unique()[0]
    sname = group['site'].unique()[0]
    tname = group['time'].unique()[0]
    group['condition']= group['drought'] +'\n' + group['insects']
    plotavgdata = group.groupby(['category','condition', 'plot'])['OD'].sum().reset_index()
    overallavg = plotavgdata.groupby(['category', 'condition'])['OD'].mean().reset_index()
    maxvalue = overallavg.max()
    #overallavg = 
    #testdata = avgdata.sort_values(by = ['category'])
    fdata = overallavg.pivot("category", "condition", "OD")
    # fdata = fdata.reindex(['Phenylethyl-amine', 'Putrescine', 'D-Glucosaminic Acid',
    #             'Glycyl-L-Glutamic Acid', 'L-Arginine', 'L-Asparagine',
    #             'L-Phenylalanine', 'L-Serine', 'L-Threonine', 'a-D-Lactose',
    #             'B-Methyl-D-Glucoside', 'D,L-a-Glycerol Phosphate', 'D-Cellobiose',
    #             'D-Galactonic Acid g-Lactone', 'D-Mannitol', 'D-Xylose', 
    #             'Glucose-1-Phosphate', 'I-Erythritol', 'N-Acetyl-D-Glucosamine',
    #             'a-Keto Butyric Acid', 'D-Galacturonic Acid', 'D-Malic Acid',
    #             'g-Amino Butyric Acid', 'Itaconic Acid', 'Pyruvic Acid Methyl Ester',
    #             '2-Hydroxy Benzoic Acid', '4-Hydroxy Benzoic Acid', 
    #             'a-Cyclodextrin', 'Glycogen', 'Tween 40', 'Tween 80', 'Water'])
    
    fdata = fdata.reindex(['amine or amide', 'amino acid', 'carbohydrate', 
                'carboxylic or ketonic acid', 'phenolics', 'polymers', 'water'])

    f, ax = plt.subplots(figsize=(6, 12))
    sns.heatmap(fdata, vmin= 0.1, vmax= 15, annot=True, linewidths=.5, ax=ax)
    ax.set_title(f'{sname }' +' '+ f'{mname }'+' ' + f'{tname}' + 'hours', fontsize = 20)
    return

heatdata = subdata.groupby(['month', 'site', 'time']).apply(heat)

#PCAs



def princ(group):
    data72 = group.loc[(group['time'] == 72)]  
    sname = group['site'].unique()[0]
    PCAdata = data72.pivot_table(
                values = 'OD',
                index = ['plot', 'month', 'drought','insects'],
                columns = 'category').reset_index()
    PCAdata['condition']= PCAdata['drought'] +'\n' + PCAdata['insects']
  
    # features = ['Phenylethyl-amine', 'Putrescine', 'D-Glucosaminic Acid',
    #                 'Glycyl-L-Glutamic Acid', 'L-Arginine', 'L-Asparagine',
    #                 'L-Phenylalanine', 'L-Serine', 'L-Threonine', 'a-D-Lactose',
    #                 'B-Methyl-D-Glucoside', 'D,L-a-Glycerol Phosphate', 'D-Cellobiose',
    #                 'D-Galactonic Acid g-Lactone', 'D-Mannitol', 'D-Xylose', 
    #                 'Glucose-1-Phosphate', 'I-Erythritol', 'N-Acetyl-D-Glucosamine',
    #                 'a-Keto Butyric Acid', 'D-Galacturonic Acid', 'D-Malic Acid',
    #                 'g-Amino Butyric Acid', 'Itaconic Acid', 'Pyruvic Acid Methyl Ester',
    #                 '2-Hydroxy Benzoic Acid', '4-Hydroxy Benzoic Acid', 
    #                 'a-Cyclodextrin', 'Glycogen', 'Tween 40', 'Tween 80', 'Water']
    
    features = ['amine or amide', 'amino acid', 'carbohydrate', 
                'carboxylic or ketonic acid', 'phenolics', 'polymers', 'water']
    
    
    x = PCAdata.loc[:, features].values
    pca = PCA(n_components=4)
    principalComponents = pca.fit_transform(x)
    print(pca.explained_variance_ratio_)
    principalDf = pd.DataFrame(data = principalComponents
                  , columns = ['PC1', 'PC2', 'PC3', 'PC4'])
    fulldf = pd.concat((PCAdata.reset_index(), principalDf), axis=1)
    fig = plt.figure(figsize = (8,8))
    ax = fig.add_subplot(1,1,1) 
    ax.set_xlabel('Principal Component 1', fontsize = 15)
    ax.set_ylabel('Principal Component 2', fontsize = 15)
    ax.set_title(f'2 component PCA {sname}', fontsize = 20)
    
    # targets = ['ambient\ncontrol', 'ambient\nexclosure', 'drought\ncontrol', 
    #             'drought\nexclosure']
    # colors = ['r', 'g', 'b', 'm']
    # for target, color in zip(targets,colors):
    #     indicesToKeep = fulldf['condition'] == target
        
    targets = ['June', 'July']
    colors = ['r', 'g']
    for target, color in zip(targets,colors):
        indicesToKeep = fulldf['month'] == target  
        
        ax.scatter(fulldf.loc[indicesToKeep, 'PC1']
                    , fulldf.loc[indicesToKeep, 'PC2']
                    , c = color
                    , s = 50)
    ax.legend(targets)
    ax.grid()
    return

pdata = avgdata.groupby(['site']).apply(princ)
