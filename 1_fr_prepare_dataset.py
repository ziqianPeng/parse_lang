import os, random, sys
from pathlib import Path
import numpy as np

# define project path and gold data path
fr_path = 'fr_sud_nomwt'  #'fr_sud2_11'
raw_docpath = os.path.join(fr_path, 'raw_data')  #'fr_all')

# create structure
to_parse_path = os.path.join(fr_path, 'input_conllus', 'to_parse')
Path(to_parse_path).mkdir(parents = True, exist_ok = True)

# modify it if use other parser, e.g. hopsParser_res
# must in the format '{xxx}_res', and specify it when run the parser (e.g. in 2_trankit_fr_jour.py) 
project_path = os.path.join(fr_path, 'trankitParser_res') 
train_datapath = os.path.join(project_path, 'conllus')
Path(train_datapath).mkdir(parents = True, exist_ok = True)

# uncomment if trankit_fpath in 2_trankit_fr_jour.py is specified to the script located in djangoBootParser
# with open(os.path.join(fr_path,'progress.txt' ), 'w') as f:
#     f.write('french parser')

# the .tsv stores names (without .conllu) of files to parse
# please check if file ends with '.conllu'
to_parse_ls =[fname[:-7] for fname in os.listdir(to_parse_path) if fname.endswith('conllu')] # filename without .conllu
with open(os.path.join(fr_path, 'to_parse_fnames.tsv'), 'w') as f:
    f.write('\t'.join(to_parse_ls))



def make_data_lang(raw_docpath, train_datapath, dev_ratio = 0.1):
    """prepare dataset"""
    data_list = []
    # read data
    doc_list = [d for d in os.listdir(raw_docpath) if d[:3]=='SUD'\
            and d!='SUD_French-FTB' and d.split('.')[-1] not in ['zip', 'tgz'] ]
    print(doc_list)
    for doc_name in doc_list:
        print(doc_name)
        for f in os.listdir(os.path.join(raw_docpath, doc_name)):
            if f.endswith('.conllu'):
                print('   ', f)
                data_list.append(open(os.path.join(raw_docpath, doc_name, f)).read().strip())
    # split into train and dev
    dataset = '\n\n'.join(data_list).split('\n\n')
    idx_dev = random.sample( range(len(dataset)), k = int( len(dataset)*dev_ratio))
    idx_train = list(set(np.arange(len(dataset))) - set(idx_dev))
    random.shuffle(idx_train)
    dev_set_list = [dataset[d] for d in idx_dev ]
    train_set_list = [dataset[t] for t in idx_train ]

    with open( os.path.join(train_datapath, 'train.conllu'), 'w'  ) as f:
        f.write( '\n\n'.join(train_set_list) + '\n\n'  )

    with open( os.path.join(train_datapath, 'dev.conllu' ), 'w' ) as f:
        f.write( '\n\n'.join(dev_set_list) + '\n\n'  )


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: 1_fr_prepare_dataset.py is_to_train")
        sys.exit(-1)

    prepare_train = True if sys.argv[1].lower() == 'true' else False
    if prepare_train:
        make_data_lang(raw_docpath, train_datapath)