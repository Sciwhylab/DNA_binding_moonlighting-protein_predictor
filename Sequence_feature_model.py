#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import numpy as np
import gc
import os
import pickle
from sys import argv

import matplotlib.pyplot as plt
import matplotlib 
from sklearn.model_selection import StratifiedKFold,train_test_split,cross_val_score, LeaveOneOut
from sklearn.metrics import roc_curve, auc, f1_score
from catboost import CatBoostClassifier
#get_ipython().run_line_magic('matplotlib', 'inline')
matplotlib.rcParams.update({'font.size': 20})

import random

def model_clf(s):

    clf = CatBoostClassifier(
        iterations=100,
        learning_rate=0.01,
        max_depth=5,
        #eval_metrics='RMSE',
        random_seed=s,
        auto_class_weights='Balanced',
        colsample_bylevel=0.6,
        min_data_in_leaf=3,
        subsample=0.3
        )
    return clf


def compute_roc_auc(model, index):
    y_predict = model.predict_proba(X.values[index])[:,1]
    fpr, tpr, thresholds = roc_curve(y.values[index], y_predict)
    #print(thresholds)
    auc_score = auc(fpr, tpr)
    return fpr, tpr, auc_score

def adjusted_classes(y_scores, t):
    """
    This function adjusts class predictions based on the prediction threshold (t).
    Will only work for binary classification problems.
    """
    return [1 if y >= t else 0 for y in y_scores]

if __name__=='__main__':
    random.seed(123)
    #input_file = input("Enter the path for the tab seperated input file") # give the path and name of the input file.
    #output_dir = input("Enter the path of the folder to save the output file") ### give the path for the output file
    
    input_file = argv[1]
    output_dir = argv[2]
    os.makedirs(output_dir, exist_ok=True)

    #####  INPUT path  and output path has to be editted
    ### reading the data
    #data=pd.read_csv('feat_formodel_081021_bin5.tsv',sep='\t')
    data=pd.read_csv(input_file,sep='\t')
    data.set_index("Proteins",inplace=True)
    all_data=data.sample(frac=1)
    #names=['Evolutionary','Gene_expression','Sequence','Secondary_structure','PPI_Network']   ### Feature names
    #X_vals=[all_data.loc[:,'all_A':'VV'],all_data.loc[:,'bin1':'binc5'],all_data.loc[:,'q3dna':'countY'],all_data.loc[:,'coil':'order'],all_data.loc[:,'num_pathway':'is_hub']]    #### columns corresponding to Features
    #X_vals=[all_data.loc[:,'bin1':'binc5']]

    #for i,name in enumerate(names):
        ##### ALL FEATURES
    name='Sequence'
    X=all_data.loc[:,'q3dna':'countY']
    #X=all_data.loc[:,'q3dna':'is_hub']  # Features
    y=all_data['Label']  # Labels

    important_all=pd.DataFrame()
    pred_all=pd.DataFrame()
    importance_all, feat_all=[], []

    fprs,tprs, scores=[], [], []
    DF_all=pd.DataFrame()
    df_ind,df_label,df_predictlabel,df_predictprob0,df_predictprob1=[], [], [], [], []
    auc_scores=[]
    y_true,y_pred=[], []

    loo=LeaveOneOut()
    i=0
    for j in range(1,11):
        y_true,y_pred=[], []
        for train_idx,test_idx in loo.split(X):
            #print(X.values[test_idx,:])
            clf=model_clf(j)
            model=clf.fit(X.iloc[train_idx], y.iloc[train_idx])
            df_ind.extend(X.iloc[test_idx].index)
            df_label.extend(list(all_data.loc[X.iloc[test_idx].index,'Label']))
            df_predictlabel.extend(clf.predict(X.iloc[test_idx]))
            df_predictprob0.extend(clf.predict_proba(X.iloc[test_idx])[:,0])
            df_predictprob1.extend(clf.predict_proba(X.iloc[test_idx])[:,1])

            y_predict=clf.predict_proba(X.values[test_idx])[:,1]
            y_true.extend(y.values[test_idx])
            y_pred.extend(y_predict)
            # save the each leave one out model to disk if required!!!! 
            #i+=1
            #filename = 'Pickle_catall_model{}.pkl'.format(i)
            #pickle.dump(model, open('output_path'+filename, 'wb'))

            del clf
            gc.collect()
        fpr,tpr,thresholds=roc_curve(y_true,y_pred)
        fprs.append(fpr)
        tprs.append(tpr)
        auc_score=auc(fpr,tpr)
        auc_scores.append(auc_score)
        print(auc_scores)

    DF_all['indices']=df_ind
    DF_all['true label']=df_label
    DF_all['predicted label']=df_predictlabel
    DF_all['predicted probability0']=df_predictprob0
    DF_all['predicted probability1']=df_predictprob1
    #name='all_leaveoneout'

    out_file = "CatboostPrediction_score_{}.txt".format(name)
    DF_all.to_csv(os.path.join(output_dir, out_file), sep="\t",encoding="utf-8")

