# if # text = Begin  ... 1\t begin, replace B by b
import os, re, sys

text_pat = re.compile(r'(?<=# text = ).+(?=\n)')
ID, FORM = 0, 1


def maj2lower(conll_fpath):
    """
    Replace the first token of # text by the Form of the token with ID 1 
    for example when first char of text is always maj but that of the 1st token could be minuscule
    """
    conll_sents = open(conll_fpath).read().strip().split('\n\n')
    conll_renew = []
    for conll in conll_sents:
        text = re.findall(text_pat, conll)
        assert(len(text)==1 )
        text_info = text[0].strip().split()
        sent_info = conll.split('\n')

        for l in sent_info:
            if l[0] != '#':
                tok = l.split('\t')
                if tok[FORM] != text_info[0]:
                    text_info[0] = tok[FORM]
                break
        text_renew = ' '.join(text_info)
        sent_renew = re.sub(text_pat, text_renew, conll)
        # sent_renew = '\n'.join(sent_info)
        conll_renew.append( sent_renew)
    
    with open(conll_fpath, 'w') as f:
        f.write( '\n\n'.join(conll_renew) + '\n\n' )



def min2maj(conll_fpath):
    """
    Replace the Form the token with ID 1 by the first token of # text 
    for example when first char of text is always maj but that of the 1st token could be minuscule
    """
    conll_sents = open(conll_fpath).read().strip().split('\n\n')
    conll_renew = []
    for conll in conll_sents:
        text = re.findall(text_pat, conll)
        assert(len(text)==1 )
        text_info = text[0].strip().split()
        sent_info = conll.split('\n')

        for i, l in enumerate(sent_info):
            if l[0] != '#':
                tok = l.split('\t')
                if tok[FORM] != text_info[0]:
                    tok[FORM] = text_info[0]
                    sent_info[i] = '\t'.join(tok)
                break
        sent_renew = '\n'.join(sent_info)
        conll_renew.append( sent_renew)
    
    with open(conll_fpath, 'w') as f:
        f.write( '\n\n'.join(conll_renew) + '\n\n' )

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python3 0_preprocessing.py conll_dir')
        sys.exit(-1)
    doc = sys.argv[1] 
    f_ls = [f for f in os.listdir(doc) if f.endswith('.conllu')]
    print(f_ls)    
    for fp in f_ls:
        print(fp)
        maj2lower(os.path.join(doc, fp))


