import utils
import numpy as np
import sys, os
from dependency_decoder import DependencyDecoder
from copy import deepcopy

def ensemble(files, outfile):
    """
    Takes conllu files as input
    """
    conllu_files = []
    for f in files:
        cf = utils.read_conll(f)
        conllu_files.append(cf)
    zipped_sentences = zip(*conllu_files)
    decoder = DependencyDecoder()
    sentences_out = []
    for zipped_sentence in zipped_sentences:
        conll_sentence = [entry for entry in zipped_sentence[0] if isinstance(entry, utils.ConllEntry)]
        n_words = len(conll_sentence)
        m = np.zeros((n_words,n_words))
        for i_sentence in zipped_sentence:
            conll_sen = [entry for entry in i_sentence if isinstance(entry, utils.ConllEntry)]
            for item in conll_sen:
                head = item.parent_id
                dep = item.id
                m[head,dep] += 1

        #NOTE: this takes the label of the first!
        heads = decoder.parse_nonproj(m)
        for entry in zipped_sentence[0]:
            if isinstance(entry,utils.ConllEntry):
                entry.pred_parent_id = heads[entry.id]
        sentences_out.append(zipped_sentence[0])
    utils.write_conll(outfile,sentences_out)

if __name__=='__main__':
    out = sys.argv[1]
    files = [f for f in sys.argv[2:]]
    ensemble(files,out)
