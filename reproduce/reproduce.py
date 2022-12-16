import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from simdeep.simdeep_boosting import SimDeepBoosting
from simdeep.config import PATH_THIS_FILE
from sklearn.preprocessing import RobustScaler
from collections import OrderedDict
from os.path import isfile
import numpy as np
import random
import pandas as pd
import os
import scipy.stats as st
import dill
from simdeep.simdeep_utils import save_model
from simdeep.simdeep_utils import load_model
# specify your data path

path_data = './data/PAAD/'

# assert(isfile(path_data + "/rna_360.tsv"))
# assert(isfile(path_data + "/mir_360.tsv"))
# assert(isfile(path_data + "/meth_360.tsv"))

# Add the 
tsv_files = OrderedDict([
     ('MIR', 'mir.tsv'),
     ('METH', 'meth.tsv'),
     ('RNA', 'rna.tsv'), 
    #  ('RNA', 'rna_input.tsv'), 
#     ('RNA', 'rna_input_only.tsv'),
#     ('RNA2', 'rna_input_only_epc.tsv'),
#     ('copy','copy.tsv'),
    # ("drug","drug.tsv"),
    # ("wxs","wxs.tsv"),
    # ('percentage','ablation.csv')
    # ("percentage", "percentage.tsv")
])

# The survival file located also in the same folder
survival_tsv = 'survival.tsv'

assert(isfile(path_data + "survival.tsv"))

# More attributes
# Create the seed list randomly so that in the for loop for implementation, the seed is different.
seed_list = []
for i in range(50):
    seed_list.append(random.randint(0,1000))
#      seed_list.append(i * 100)
print(seed_list)
origin_cindex= []
proba_cindex = []

file = path_data + 'result.csv'
seed_list.remove(632)
# create the result file and delete it if it exists
if(os.path.exists(file) and os.path.isfile(file)):
    os.remove(file)
    print("file deleted")
else:
    pass
df = pd.DataFrame(columns = ['cindex'])
df.to_csv(file, index = False)
# Implement DeepProg for each seed
for SEED in seed_list:
#     PROJECT_NAME = 'UCS_dataset_'+str(SEED) # Name
    EPOCHS = 10# autoencoder fitting epoch

    nb_it = 10 # Number of submodels to be fitted
    nb_threads = 2 # Number of python threads used to fit survival model
    cluster_method = "coxPH"
    class_selection = "weighted_max"
    survival_flag = {
        'patient_id': 'Samples',
        'survival': 'days',
        'event': 'event'}
    feature_selection_usage = "individual"

#     import ray
#     ray.init(webui_host='0.0.0.0', num_cpus=2)

    boosting = SimDeepBoosting(
        verbose = True,
        nb_threads=nb_threads,
        nb_it=nb_it,
        split_n_fold=2,
        survival_tsv=survival_tsv,
        training_tsv=tsv_files,
        path_data=path_data,
#         project_name=PROJECT_NAME,
        path_results=path_data,
        epochs=EPOCHS,
        survival_flag=survival_flag,
         distribute=False,
        seed=SEED,
        nb_clusters = 2,
        use_autoencoders = True,
        cluster_method = cluster_method,
        feature_selection_usage = feature_selection_usage,
        class_selection = class_selection
        )

    boosting.fit()
#     PATH_PRECOMPUTED_LABELS = "./test_saved_model"
    
#     boosting.save_test_models_classes(
#         path_results=PATH_PRECOMPUTED_LABELS # Where to save the labels
#         )
    # # predict labels of the training

    boosting.predict_labels_on_full_dataset()

#     cindex_list = boosting.collect_cindex_for_full_dataset()
#     full_cindex.append(np.mean(cindex_list))
#     boosting.compute_clusters_consistency_for_full_labels()
#     boosting.evalutate_cluster_performance()
#     test_cindex += boosting.collect_cindex_for_test_fold()
#     full_cindex += boosting.collect_cindex_for_full_dataset()
print("------------------------evaluation-----------------------------")

# Get the cindex list for origin and proba method 
result_df = pd.read_csv(file)
print(result_df)
for i in range(len(result_df)):
    if i % 2 == 0:
        origin_cindex.append(result_df.iloc[i].cindex)
    else:
        proba_cindex.append(result_df.iloc[i].cindex)
        
# Calculate the mean, std, max, min and 95% confidence interval
print('c-index results origin method: mean {0} std {1}'.format(np.mean(origin_cindex), np.std(origin_cindex)))
print('c-index results proba method: mean {0} std {1}'.format(np.mean(proba_cindex), np.std(proba_cindex)))
print('max and min c-index results origin method: max {0} min {1}'.format(np.max(origin_cindex), np.min(origin_cindex)))
print('max and min c-index results proba method: max {0} min {1}'.format(np.max(proba_cindex), np.min(proba_cindex)))

confi_origin = st.t.interval(alpha=0.95, df=len(origin_cindex)-1, loc=np.mean(origin_cindex), scale=st.sem(origin_cindex)) 
confi_proba = st.t.interval(alpha=0.95, df=len(proba_cindex)-1, loc=np.mean(proba_cindex), scale=st.sem(proba_cindex)) 
print('95% confidence interval of c-index results origin method: low {0} high {1}'.format(confi_origin[0],confi_origin[1]) )
print('95% confidence interval of c-index results proba method: low {0} high {1}'.format(confi_proba[0],confi_proba[1]) )

# boosting.load_new_test_dataset(
#     {'RNA': 'rna.tsv',
#      'MIR': 'mir.tsv'}, # OMIC file of the test set. It doesnt have to be the same as for training
#     'TEST_DATA_1', # Name of the test test to be used
#     'survival.tsv', # [OPTIONAL] Survival file of the test set. USeful to compute accuracy metrics on the test dataset
# )

# # Predict the labels on the test dataset
# boosting.predict_labels_on_test_dataset()
# # Compute C-index
# boosting.compute_c_indexes_for_test_dataset()
# # See cluster consistency
# boosting.compute_clusters_consistency_for_test_labels()