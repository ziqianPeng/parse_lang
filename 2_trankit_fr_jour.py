import os

# trankit_fpath = '/home/arboratorgrew/autogramm/djangoBootParser/djangoBootParser/train_pred_trankit.py'
trankit_fpath = "train_pred_trankit_final.py"
project_path = 'fr_sud_nomwt'  # 'fr_sud2_11'
need_train = True

# to begin, train with epochs_parser = 100, epochs_tok=epochs_lemma = 10
# then decide whether it needs more epochs!
epochs = 100
epochs_tok = 10
tokenized = True
parse_train = False

# used to create model folder in the format '{parser_id}_res' 
# must be the same as what you defined in `project_path` of script 1_fr_prepare_dataset
parser_id = 'trankitParser' 


os.system(f"/home/arboratorgrew/miniconda3/bin/python3 {trankit_fpath} {project_path} {parser_id} \
    {need_train} {epochs} {epochs_tok}  {tokenized} {parse_train}")
