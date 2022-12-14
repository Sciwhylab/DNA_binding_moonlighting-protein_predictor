# DNA_Binding_moonlighting_predictor

This predictor is trained to predict Moonlighting DNA binding proteins using the averaged ensemble of predictions from the 5 features sets generated as mentioned below. 

This repository includes the following source codes:

1. moonlighting_catboost_prediction.py     
    To predict moonlighting proteins from all 5 feature sets compiled as provided in the dataset
    
2. averaged_ensemble_prediction.py  
    To generate the predictions by ensembling the predictions from individual models.
    
3. To generate predictions from individual features:
      
      - Evolutionary_feature_model.py    
        Can be used to generate predictions from evolutionary features.
      
      - Geneexpression_feature_model.py     
        Can be used to generate predictions from Gene expression features.
      
      - PPInetwork_feature_model.py   
        Can be used to generate predictions from Protein network features.
      
      - Secondarystructure_feature_model.py  
        Can be used to generate predictions from Secondary structure features.
      
      - Sequence_feature_model.py   
        Can be used to generate predictions from Sequence features.


## Feature generation

### Evolutionary Features

Position specific scoring matrix (PSSM) can be generated using PSI-BLAST in the locally installed BLAST with default parameters and 3 iterations against the nr database available in NCBI.
To generate the evolutionary features the average  of the log odds score values for all amino acids(20 features) and the average of the log odds score for each of the 20 amino acids were taken(20*20 features).
There will be 420 evolutionary features.

### Predicted Structural Features

The structural features were extracted from the predictions made using locally installed Raptor X. 
The 3 state secondary structural features , the solvent accessability and the order, disorder content from the predictions were taken as features.  
There will be 8 structural features.

### PPI-Network features

The network features were extracted from Targetmine using API.
For each gene using the High confidence direct physical protein protein Ineractions the three network properties like the number of pathways involved and whether a protein is a bottleneck, or hub were extracted.
There will be 3 network features.

### Protein sequence and predicted binding site features

Amino acid composition, length of the proteins, and the binding site prediction scores for carbohydrates, DNA,RNA, adenosine triphosphate(ATP) and proteins can be calculated using (http://gigeasa-bs.sciwhylab.org/).The human sequence features used for the study is included in the folder GIGEASA_human_dataset.
There will be 40 sequence features.

### Gene Expression Features

For each gene the frequency of occurence of expression values can be binned into 5 equal probability bins.(http://www.sciwhylab.org/gigeasa/)
There will be 10 gene expression features when using 5 equal probability bins.The human gene expression features used for the study is included in the folder GIGEASA_human_dataset.


## Running the model

### Prediction model

The model was built on python version 3 and above.Libraries for catboost,pickle and sklearn have to be installed.
The input file should be in the format provided in the dataset.tsv as tab seperated file. The input file path and the path of the folder for the output file to be written can be provided as arguments.
The outputs will be written in the folder mentioned.

### Ensemble model

The ouputs of the prediction model are used as inputs for ensembling. The path to these files can be provided and the path for the ensemble output can also be provided.  

## STEPS

1. Extract the features and create a tab seperated file for input as shown in the dataset.tsv file to generate predictions for all features together.

2. To extract all the feature based predictions together run "python moonlighting_catboost_prediction.py path\inputfile path\outputfolder" in the terminal 
   and provide the path for the input file and output folder as input to get the prediction score.
   To create predictions for each feature set seperately run the respective feature model in the following format "python feature_model.py path\inputfile   
   path\outputfolder".

3. Run "python averaged_ensemble_prediction.py path\outputfile_of_individual_models path\outputfolder path\inputfile_of_initial_model" in the terminal and 
   provide the path for the input file and output folder as input to get the maximum and averaged ensemble score.
