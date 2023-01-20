import os, re
import numpy as np
import pandas as pd
from pathlib import Path
from sklearn.metrics import ConfusionMatrixDisplay
import matplotlib.pyplot as plt

ID, FORM, LEMMA, UPOS, XPOS, FEATS, HEAD, DEPREL, DEPS, MISC = range(10)
sub_pat = re.compile(r'[:|@|$]')
sub_pat1 = re.compile(r'[@|$]')


def get_conf_all(conll_gold_path, conll_pred_path, regroup = None, infix = 'fr'):
    """
    confusion matrix by occurency.
    regroup == None (all DEPREL), 0 (remove :,@,$) 1 (consider :)
    """
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

                if regroup is not None:
                    assert(regroup in [0, 1])
                    # 'comp:obl$attitude@x' as 'comp' (case 0) or 'comp:obl' (case 1)
                    sub_pat = re.compile(r'[:|@|$]') if regroup == 0 else re.compile(r'[@|$]')
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


def save_conf_fig(conf_df, fig_name):
    deprel_list = list(conf_df.columns)
    conf_m = conf_df.T.to_numpy()
    print('shape of confusion matrix: ', conf_m.shape)
    cm1 = ConfusionMatrixDisplay(confusion_matrix = conf_m, display_labels = deprel_list)

    fig, ax = plt.subplots( figsize = (30, 30) )
    cm1.plot( ax = ax, cmap = plt.cm.Blues )
    ax.set_title( fig_name) 
    plt.xticks(rotation = 45)
    plt.savefig( os.path.join(store_path, f'{fig_name}.png') ) 


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
    save_conf_fig(conf_df, fig_name = f"confusion_matrix_{infix}_{conf_type.lower()}"  )
    return conf_df

def get_conf_main(gold_path, pred_path, store_path, regroup = None, infix = 'fr'):
    # count
    conf_count_df = get_conf_all(gold_path, pred_path, regroup, infix = infix)
    # precision and recall
    precision_df = get_conf_m(conf_count_df, store_path, infix = infix, conf_type = 'precision')
    recall_df = get_conf_m(conf_count_df, store_path, infix = infix, conf_type = 'recall')

    f1_df = 2 * (precision_df * recall_df /(precision_df + recall_df)).fillna(0)
    f1_df.to_csv(os.path.join(store_path, f'conf_f1score_{infix}.tsv'), sep = '\t' )
    # figure
    save_conf_fig(f1_df, fig_name = f"confusion_matrix_{infix}_f1score"  )



if __name__ == '__main__':
    project_path = 'fr_sud_nomwt/trankitParser_res'

    gold_path = os.path.join( project_path, 'conllus', 'dev.conllu' )
    pred_path = os.path.join(project_path, 'evalDev', 'dev.conllu')

    store_path = os.path.join(project_path, 'conf_matrix')
    Path(store_path).mkdir(parents = True, exist_ok = True)
    get_conf_main(gold_path, pred_path, store_path, regroup = None, infix = 'fr')

    # regroup 0 (remove :,@,$)
    store_path_0 = os.path.join(project_path, 'conf_matrix', 'regroup')
    Path(store_path_0).mkdir(parents = True, exist_ok = True)
    get_conf_main(gold_path, pred_path, store_path_0, regroup = 0, infix = 'fr')

    # regroup 1 (remove @,$)
    store_path_1 = os.path.join(project_path, 'conf_matrix', 'regroup1')
    Path(store_path_1).mkdir(parents = True, exist_ok = True)
    get_conf_main(gold_path, pred_path, store_path_1, regroup = 1, infix = 'fr')


