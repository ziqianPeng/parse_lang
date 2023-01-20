# Parse by language with trankit


## scripts

- 0_preprocessing.py (fast): 

  preprocess data if necessary. 
- 1_fr_prepare_dataset.py (fast)
  
  make folder and prepare dataset with several gold .conllu 
- 2_trankit_fr_jour.py (train and parse, take time)
    + run ```train_pred_trankit_final.py``` with custom hyperparam
        + ```train_pred_trankit_final.py``` is copied from djangoBootParser, with logging process commented.

        it make use of ```processData.py``` copied from djangoBootParser to combine output of trankit pipeline etc.
- 3_get_conf_matrix.py (fast)

  compute confusion matrix of precision, recall, f1-score for different DEPREL


## Usage

1. mkdir folder_name
2. create `folder_name/input_conllus/to_parse` and copy files to parse under it, 
you can define the "folder_name" as you wish
3. modify necessary variables, adapt and run (optional `0_preprocessing.py` and ) `1_fr_prepare_dataset.py` 
to prepare project folder
4. modify necessary variables and run `2_trankit_fr_jour.py` with nohup 
5. modify necessary variables and run `3_get_conf_matrix.py` to get confusion matrix

## Presentation
### 0_preprocessing.py: 

  preprocess data if necessary. 
  
  current function: 
  ```
  def maj2lower(conll_fpath):
    """Replace the first token of # text by the Form of the token with ID 1 """
  def min2maj(conll_fpath):
    """Replace the Form the token with ID 1 by the first token of # text"""
  ```
  *usage:* modify the main function part to call the function you want and run:
  ```
  python3 0_preprocessing.py conll_dir
  ```
### 1_fr_prepare_dataset.py 

  make folder and prepare dataset with several gold .conllu 
  
  The folder structure should be as follows, where progress.txt is optional: 
  it's only necessary if you run the trankit script located in djangoBootparser 

  ```
  folder_example/
  ├── input_conllus
  │   └── to_parse
  ├── progress.txt # optional
  ├── to_parse_fnames.tsv
  └── trankitParser_res
      └── conllus
          ├── dev.conllu
          └── train.conllu
  ```
  
  #### usage
  modify the `fr_path` and `raw_docpath` , 
  put files to parse under the folder `{fr_path}/input_conllus/to_parse`
  make sure that the `project_path` is consistent with what you will specified in `2_trankit_fr_jour.py `
  
  adapte `make_data_lang` to read gold files if necessary
  
  ```python3 1_fr_prepare_dataset.py```
  

### 2_trankit_fr_jour.py (train and parse, take time)
  this file run `train_pred_trankit_final.py` with custom hyperparam
    
  `project_path` should be the same as `fr_path` in 1_fr_prepare_dataset.py   
      
      # train the parser if need_train, otherwise directly parse files.
      need_train = true
      # consider the tokenisation of files to parse is gold
      tokenized = True
      # don't parse gold files directly under folder `input_conllus`
      # so if parse_train, please copy gold files under `input_conllus` folder
      parse_train = False
      # parser_id used to create model folder in the format '{parser_id}_res' 
      # must be the same as what you defined in `project_path` of script 1_fr_prepare_dataset
      parser_id = 'trankitParser'
    
  + `train_pred_trankit_final.py` is copied from djangoBootParser, with logging process commented, so that progress.txt won't be used.
        
    it make use of `processData.py` copied from djangoBootParser to combine output of trankit pipeline etc.
        
    the most important function is `train_trankit` that is called in `train_pred_trankit`. 
    the function train tokenizer(token+mwt), posdep(pos+head+deprel) tagger and lemmatizer(lemma) for the pipeline, 
     
    if there is already tokenizer etc. ready-to-use under `trankitParser_res/xlm-roberta-large/customized`, 
    you can comment the `train_tok` and `train_mwt` part to begin with parser training 

    run in background and write output into `nohup_name.out`. 
    ```
    conda activate base
    nohup python3 2_trankit_fr_jour.py >> nohup_name.out 2>&1 &
    ```

    *Information*: I got CUDA memory error when I run 5 language in the same time for datasize in [10,30,50,100,300,500] under the account `arboratorgrew`, so maybe avoid training 4 or more parser in parallel according to the datasize.

### 3_get_conf_matrix.py

compute confusion matrix of precision, recall, f1-score for different DEPREL

  *usage:* modify the main function part to adapt the `project_path` and run
  ```
  python3 3_get_conf_matrix.py
  ```

