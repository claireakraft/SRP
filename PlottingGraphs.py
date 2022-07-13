# -*- coding: utf-8 -*-
"""
Created on Wed Jun 29 10:47:24 2022

@author: 13096
"""
import pandas as pd
import os 

os.chdir('C:\\Users\\13096\\Documents\\SRP\\FormatedEcoPlateExcelData')

data = pd.read_csv('ecoplatedataforplotting.csv')

avgdata = data.groupby(['date', 'site', 'plot', 'drought', 'insects', 'enzyme', 'category'])['OD'].mean().reset_index()


import matplotlib.pyplot as plt
import seaborn as sns

test = avgdata.loc[avgdata['enzyme']=='Glycogen']

sns.catplot(x='drought',
            y='OD',
            hue='insects',
            data= test,
            kind= 'bar',
            ci= 68)

enames = avgdata['enzyme'].unique()
cnames = avgdata['category'].unique()

for e in enames:
    test = avgdata.loc[avgdata['enzyme']== e]
    f,ax = plt.subplots()
    sns.barplot(x='drought',
                y='OD',
                hue='insects',
                data= test,
                ci= 68,
                ax= ax)
    ax.set_title(e)
    plt.ylim(0,3.5)
    plt.savefig(f'{e}.pdf')
    plt.show()
    
for c in cnames:
    test = avgdata.loc[avgdata['category']== c]
    f,ax = plt.subplots()
    sns.barplot(x='drought',
                y='OD',
                hue='insects',
                data= test,
                ci= 68,
                ax= ax)
    ax.set_title(c)
    plt.ylim(0,1.5)
    plt.savefig(f'{c}.pdf')
    plt.show()   



"""
Heat Graphs:
"""



avgdata['condition']=avgdata['drought'] +'\n' + avgdata['insects']

avgavgdata = avgdata.groupby(['enzyme','condition'])['OD'].mean().reset_index()

testdata = avgdata.sort_values(by = ['category'])


fdata = avgavgdata.pivot("enzyme", "condition", "OD")

fdata = fdata.reindex(['Phenylethyl-amine', 'Putrescine', 'D-Glucosaminic Acid',
                'Glycyl-L-Glutamic Acid', 'L-Arginine', 'L-Asparagine',
                'L-Phenylalanine', 'L-Serine', 'L-Threonine', 'a-D-Lactose',
                'B-Methyl-D-Glucoside', 'D,L-a-Glycerol Phosphate', 'D-Cellobiose',
                'D-Galactonic Acid g-Lactone', 'D-Mannitol', 'D-Xylose', 
                'Glucose-1-Phosphate', 'I-Erythritol', 'N-Acetyl-D-Glucosamine',
                'a-Keto Butyric Acid', 'D-Galacturonic Acid', 'D-Malic Acid',
                'g-Amino Butyric Acid', 'Itaconic Acid', 'Pyruvic Acid Methyl Ester',
                '2-Hydroxy Benzoic Acid', '4-Hydroxy Benzoic Acid', 
                'a-Cyclodextrin', 'Glycogen', 'Tween 40', 'Tween 80', 'Water'])



f, ax = plt.subplots(figsize=(6, 12))
sns.heatmap(fdata, annot=True, linewidths=.5, ax=ax)




"""
PCA:
    
"""

PCAdata = avgdata.pivot_table(
            values = 'OD',
            index = ['plot', 'drought','insects'],
            columns = 'enzyme')

fdata = avgavgdata.pivot("condition", "enzyme", "OD")

from sklearn.preprocessing import StandardScaler

features = ['Phenylethyl-amine', 'Putrescine', 'D-Glucosaminic Acid',
                'Glycyl-L-Glutamic Acid', 'L-Arginine', 'L-Asparagine',
                'L-Phenylalanine', 'L-Serine', 'L-Threonine', 'a-D-Lactose',
                'B-Methyl-D-Glucoside', 'D,L-a-Glycerol Phosphate', 'D-Cellobiose',
                'D-Galactonic Acid g-Lactone', 'D-Mannitol', 'D-Xylose', 
                'Glucose-1-Phosphate', 'I-Erythritol', 'N-Acetyl-D-Glucosamine',
                'a-Keto Butyric Acid', 'D-Galacturonic Acid', 'D-Malic Acid',
                'g-Amino Butyric Acid', 'Itaconic Acid', 'Pyruvic Acid Methyl Ester',
                '2-Hydroxy Benzoic Acid', '4-Hydroxy Benzoic Acid', 
                'a-Cyclodextrin', 'Glycogen', 'Tween 40', 'Tween 80', 'Water']

# Separating out the features
x = PCAdata.loc[:, features].values


# Standardizing the features
x_std = StandardScaler().fit_transform(x)


from sklearn.decomposition import PCA

pca = PCA(n_components=2)

principalComponents = pca.fit_transform(x_std)

principalDf = pd.DataFrame(data = principalComponents
             , columns = ['PC11', 'PC2'])

fulldf = pd.concat((PCAdata.reset_index(), principalDf), axis=1)
fulldf['condition']=fulldf['drought'] +'\n' + fulldf['insects']




fig = plt.figure(figsize = (8,8))
ax = fig.add_subplot(1,1,1) 
ax.set_xlabel('Principal Component 1', fontsize = 15)
ax.set_ylabel('Principal Component 2', fontsize = 15)
ax.set_title('2 component PCA', fontsize = 20)
targets = ['ambient \ncontrol ', 'ambient \nexclosure', 'drought\ncontrol ', 
           'drought\nexclosure']

colors = ['r', 'g', 'b', 'm']
for target, color in zip(targets,colors):
    indicesToKeep = fulldf['condition'] == target
    ax.scatter(fulldf.loc[indicesToKeep, 'PC11']
               , fulldf.loc[indicesToKeep, 'PC2']
               , c = color
               , s = 50)
ax.legend(targets)
ax.grid()



pca.explained_variance_ratio_


