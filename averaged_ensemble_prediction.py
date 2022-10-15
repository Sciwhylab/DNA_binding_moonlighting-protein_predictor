#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd 
import numpy as np
import os
from sys import argv

input_dir = argv[1] # give the path and name of the input file.
output_dir =argv[2] ### give the path for the output file

#data=pd.read_csv(input_file,sep='\t')

a1=pd.read_csv(os.path.join(input_dir, "CatboostPrediction_score_Evolutionary.txt"),sep="\t")
a2=pd.read_csv(os.path.join(input_dir, "CatboostPrediction_score_Gene_expression.txt"),sep="\t")
a3=pd.read_csv(os.path.join(input_dir, "CatboostPrediction_score_PPI_Network.txt"),sep="\t")
a4=pd.read_csv(os.path.join(input_dir, "CatboostPrediction_score_Secondary_structure.txt"),sep="\t")
a5=pd.read_csv(os.path.join(input_dir, "CatboostPrediction_score_Sequence.txt"),sep="\t")

input_file = argv[3] # give the path and name of the input file used to train the model to get a list of the unique proteins.
data=pd.read_csv(input_file,sep='\t')

p1=list(data['Proteins'])

l=["Protein","Evolutionary","Gene_exp","PPI","SECstruct","Seq","True label"]
averaged_pred=pd.DataFrame(columns=l)

label, prt=[], []
seqa, stra, evoa, ppia, gea=[], [], [], [], []
seqi, stri, evoi, ppii, gei=[], [], [], [], []
for p in p1:
    #### predicted probability for averaging
    seqa.extend(a5.loc[a5['indices']==p,'predicted probability1'])
    stra.extend(a4.loc[a4['indices']==p,'predicted probability1'])
    evoa.extend(a1.loc[a1['indices']==p,'predicted probability1'])
    gea.extend(a2.loc[a2['indices']==p,'predicted probability1'])
    ppia.extend(a3.loc[a3['indices']==p,'predicted probability1'])
    
    ##true label
    label.extend(a3.loc[a3['indices']==p,'true label'])
    prt.extend(a3.loc[a3['indices']==p,'indices'])
    
averaged_pred['Evolutionary']=evoa
averaged_pred['Gene_exp']=gea
averaged_pred['PPI']=ppia
averaged_pred['SECstruct']=stra
averaged_pred['Seq']=seqa
averaged_pred['True label']=label
averaged_pred['Protein']=prt
averaged_pred['averaged_prob']=averaged_pred.iloc[:,1:6].mean(axis=1)
    
DF_ensemble_fold_avg = averaged_pred.groupby('Protein').mean().reset_index(drop=False)
#DF_ensemble_fold_avg = DF_ensemble.groupby('Protein').mean().reset_index(drop=False)
DF_avg=DF_ensemble_fold_avg.drop(['Evolutionary', 'Gene_exp', 'PPI', 'SECstruct', 'Seq'],axis=1)

DF_ens_max=averaged_pred.groupby('Protein').max().reset_index(drop=False)
#DF_ens_max=DF_ensemble.groupby('Protein').max().reset_index(drop=False)
DF_max=DF_ens_max.drop(['Evolutionary', 'Gene_exp', 'PPI', 'SECstruct', 'Seq','True label'],axis=1)
#DF_max.rename({'averaged_probability':'Maximum_probability'},axis=1,inplace=True)
DF_max.columns=['Protein','Maximum_probability']

merged_df=DF_avg.merge(DF_max,how='inner',on='Protein')

merged_df.to_csv(os.path.join(output_dir, "Ensembled_prediction_scores.tsv"),sep="\t",index=False)



