from simdeep.simdeep_boosting import SimDeepBoosting
from simdeep.config import PATH_THIS_FILE
from sklearn.preprocessing import RobustScaler
from collections import OrderedDict
from os.path import isfile

# specify your data path
path_data = './data/HCC/'

# assert(isfile(path_data + "/rna_360.tsv"))
# assert(isfile(path_data + "/mir_360.tsv"))
# assert(isfile(path_data + "/meth_360.tsv"))

tsv_files = OrderedDict([
     ('MIR', 'mir.tsv'),
     ('METH', 'meth.tsv'),
    ('RNA', 'rna.tsv'), 
#     ('RNA1', 'rna_input_only.tsv'),
#     ('RNA2', 'rna_input_only_epc.tsv'),
#     ('copy','copy.tsv'),
#     ("drug","drug.tsv"),
    ("wxs","wxs.tsv")
])

# The survival file located also in the same folder
survival_tsv = 'survival.tsv'

assert(isfile(path_data + "survival.tsv"))

# More attributes
PROJECT_NAME = 'HCC_dataset' # Name
EPOCHS = 10# autoencoder fitting epoch
SEED = 1000 # random seed
nb_it = 10 # Number of submodels to be fitted
nb_threads = 2 # Number of python threads used to fit survival model
cluster_method = "coxPHMixture"
class_selection = "weighted_max"
survival_flag = {
    'patient_id': 'Samples',
    'survival': 'days',
    'event': 'event'}
feature_selection_usage = "individual"

import ray
ray.init(webui_host='0.0.0.0', num_cpus=3)

boosting = SimDeepBoosting(
    verbose = True,
    nb_threads=nb_threads,
    nb_it=nb_it,
    split_n_fold=3,
    survival_tsv=survival_tsv,
    training_tsv=tsv_files,
    path_data=path_data,
    project_name=PROJECT_NAME,
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

# # predict labels of the training

boosting.predict_labels_on_full_dataset()
boosting.compute_clusters_consistency_for_full_labels()
boosting.evalutate_cluster_performance()
boosting.collect_cindex_for_test_fold()
print('-------calculating the full dataset----------')
boosting.collect_cindex_for_full_dataset()
print("--------------ending--------------")
# boosting.compute_feature_scores_per_cluster()
# boosting.write_feature_score_per_cluster()

# boosting.load_new_test_dataset(
#     {'RNA': 'rna.tsv'},
#     'test_RNA_only',
#     survival_tsv,
# )

# boosting.predict_labels_on_test_dataset()
# boosting.compute_c_indexes_for_test_dataset()
# boosting.compute_clusters_consistency_for_test_labels()

# boosting.plot_supervised_kernel_for_test_sets()
# boosting.plot_supervised_predicted_labels_for_test_sets()
# ray.shutdown()