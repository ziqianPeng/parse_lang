import os, re
import numpy as np
import pandas as pd
from pathlib import Path
from sklearn.metrics import ConfusionMatrixDisplay
import matplotlib.pyplot as plt

ID, FORM, LEMMA, UPOS, XPOS, FEATS, HEAD, DEPREL, DEPS, MISC = range(10)

def get_conf_all(conll_gold_path, conll_pred_path, regroup = False, infix = 'fr'):
    conll_gold = open(conll_gold_path).read().strip().split('\n\n')
    conll_parsed = open(conll_pred_path).read().strip().split('\n\n')

    conf_dict = {}
    for idx in range(len(conll_gold)):
        gold_info = [l.split('\t') for l in conll_gold[idx].split('\n') if l[0] != '#' ]
        parsed_info = [l.split('\t') for l in conll_parsed[idx].split('\n') if l[0] != '#' ]
        for tid in range(len(gold_info)):
            if '-' not in gold_info[tid][ID] and '.' not in gold_info[tid][ID]:
                dep = gold_info[tid][DEPREL]
                dep_parsed = parsed_info[tid][DEPREL]

                if regroup:
                    # 'comp:obl$attitude@x' as 'comp'
                    sub_pat = re.compile(r'[:|@|$]')
                    dep = re.split(sub_pat, dep)[0]
                    dep_parsed = re.split(sub_pat, dep_parsed)[0]

                conf_dict[dep] = conf_dict.get(dep, {})
                conf_dict[dep][dep_parsed] = conf_dict[dep].get(dep_parsed, 0) +1
    # make sorted square matrix
    sorted_conf_dict = {}
    for dep, v in conf_dict.items():
        sorted_conf_dict[dep] = {k: v.get(k, 0) for k in sorted(conf_dict)}
    sorted_conf_dict = {k: sorted_conf_dict[k] for k in sorted(sorted_conf_dict) }
    # dict to dataFrame
    conf_df = pd.DataFrame(sorted_conf_dict).fillna(0)
    conf_df.to_csv( os.path.join(store_path, f"conf_count_{infix}.tsv"), sep = '\t' )
    return conf_df


def get_conf_m(conf_count_df, store_path, infix = 'fr', conf_type = 'recall', round_int = 4):
    assert(conf_type.lower() in ['precision', 'recall'])
    if conf_type == 'precision':
        conf_df = conf_count_df.div(conf_count_df.sum(axis = 1), axis = 0).fillna(0).round(round_int)
    else:
        # recall
        conf_df = conf_count_df.div(conf_count_df.sum(axis = 0), axis = 1).round(round_int)
    # store
    conf_df.to_csv( os.path.join(store_path, f"conf_{conf_type.lower()}_{infix}.tsv"), sep = '\t' )
    # figure
    deprel_list = list(conf_df.columns)
    conf_m = conf_df.T.to_numpy()
    print('shape of confusion matrix: ', conf_m.shape)
    cm1 = ConfusionMatrixDisplay(confusion_matrix = conf_m, display_labels = deprel_list)

    fig, ax = plt.subplots( figsize = (30, 30) )
    cm1.plot( ax = ax, cmap = plt.cm.Blues )
    ax.set_title( f"confusion_matrix_{infix}_{conf_type.lower()}" ) #count
    plt.xticks(rotation = 45)
    plt.savefig( os.path.join(store_path, f'confusion_matrix_{infix}_{conf_type.lower()}.png') ) #count
    return conf_df


if __name__ == '__main__':
    project_path = 'fr_sud_nomwt/trankitParser_res'

    gold_path = os.path.join( project_path, 'conllus', 'dev.conllu' )
    pred_path = os.path.join(project_path, 'evalDev', 'dev.conllu')

    store_path = os.path.join(project_path, 'conf_matrix')
    Path(store_path).mkdir(parents = True, exist_ok = True)

    # conf_count_df = get_conf_all(gold_path, pred_path, infix = 'fr')
    # precision_df = get_conf_m(conf_count_df, store_path, infix = 'fr', conf_type = 'precision')
    # recall_df = get_conf_m(conf_count_df, store_path, infix = 'fr', conf_type = 'recall')

    # regroup
    store_path_1 = os.path.join(project_path, 'conf_matrix', 'regroup')
    Path(store_path_1).mkdir(parents = True, exist_ok = True)

    conf_count_df = get_conf_all(gold_path, pred_path, regroup = True, infix = 'regroup_fr')
    precision_df = get_conf_m(conf_count_df, store_path_1, infix = 'fr_regroup', conf_type = 'precision')
    recall_df = get_conf_m(conf_count_df, store_path_1, infix = 'fr_regroup', conf_type = 'recall')

