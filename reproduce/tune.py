from simdeep.simdeep_analysis import SimDeep
from simdeep.extract_data import LoadData
from os.path import abspath
from os.path import split as pathsplit
import numpy as np
# Defining training datasets
from simdeep.config import TRAINING_TSV
from simdeep.config import SURVIVAL_TSV
# Location of the input matrices and survival file
from simdeep.config import PATH_DATA

from simdeep.simdeep_tuning import SimDeepTuning

# AgglomerativeClustering is an external class that can be used as
# a clustering algorithm since it has a fit_predict method
from sklearn.cluster.hierarchical import AgglomerativeClustering
path_file = pathsplit(abspath(__file__))[0]
print(path_file)
path_data = path_file + "/../data/"
print(path_data)
training_tsv = {
    'GE': 'rna_input.tsv',
    'MIR': 'mir.tsv',
    'METH': 'meth.tsv',
}

survival_tsv = 'test_survival.tsv'
# Array of hyperparameters
args_to_optimize = {
    'seed':[0,100,200,300,400,500,600,700,800,900],
    "nb_clusters":[2],
    "use_autoencoders" : [True],
    'cluster_method': ['coxPHMixture'],
    'class_selection': ['weighted_max'],
    "feature_selection_usage" :["individual"]
}
nb_threads = 2 # Number of python threads used to fit survival model
PROJECT_NAME = 'HCC_dataset' # Name
tuning = SimDeepTuning(
    args_to_optimize=args_to_optimize,
    nb_threads=nb_threads,
    survival_tsv=survival_tsv,
    training_tsv=training_tsv,
    path_data=path_data,
    project_name=PROJECT_NAME,
    path_results=path_data,
)
import ray
ray.init(webui_host='0.0.0.0', num_cpus=3 )

tuning.fit(
    # We will use the holdout samples Cox-PH pvalue as objective
    metric='log_test_fold_pvalue',
    num_samples=10,
    # Experiment run concurently using ray as dispatcher
    max_concurrent=2,
    # In addition, each deeprog model will be distributed
    distribute_deepprog=True,
    iterations=1)

# We recommend using large `max_concurrent` and distribute_deepprog=True
# when a large number CPUs and large RAMs are availables

# Results
table = tuning.get_results_table()
print(table)