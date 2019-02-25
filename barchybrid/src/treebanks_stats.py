import utils
from optparse import OptionParser

#taken directly from 18 conll eval
CONTENT_DEPRELS = {
    "nsubj", "obj", "iobj", "csubj", "ccomp", "xcomp", "obl", "vocative",
    "expl", "dislocated", "advcl", "advmod", "discourse", "nmod", "appos",
    "nummod", "acl", "amod", "conj", "fixed", "flat", "compound", "list",
    "parataxis", "orphan", "goeswith", "reparandum", "root", "dep"
}

def get_stats(treebanks):
    traindata = list(utils.read_conll_dir(treebanks, "train"))
    #do countings here
    d = {}
    d['rh'] = 0
    d['lh'] = 0
    tot = 0
    for sentence in traindata:
        conll_sentence = [entry for entry in sentence if isinstance(entry, utils.ConllEntry)]
        for item in conll_sentence:
            if item.relation.split(":")[0] in CONTENT_DEPRELS:
                tot += 1
                if item.id < item.parent_id:
                    d['rh'] += 1
                else:
                    d['lh'] += 1
    d['rh'] /= float(tot)
    d['lh'] /= float(tot)
    d['rh'] *= 100
    d['lh'] *= 100
    print treebanks[0].iso_id
    print "Right-headed rels: " + str(d['rh'])
    print "Left-headed rels: " + str(d['lh'])

def get_stats_b(treebanks):
    traindata = list(utils.read_conll_dir(treebanks, "train"))
    n_sen = 0.
    sen_len = 0.
    n_dep = 0.
    dep_len = 0.
    for sentence in traindata:
        conll_sentence = [entry for entry in sentence if isinstance(entry, utils.ConllEntry)]
        sen_len += len(conll_sentence)
        n_sen += 1
        for item in conll_sentence:
            dep_len += abs(item.id - item.parent_id)
            n_dep += 1

    av_len = sen_len/n_sen
    av_dep = dep_len/n_dep

    print treebanks[0].iso_id
    print "Average sentence length:" + str(av_len)
    print "Average dependency length:" + str(av_dep)

def get_dep_len(item, depth):
    if item.parent_id == 0:
        return depth
    else:
        #I should not have to look over sentence
        #parent = [token for token in sentence if token.id == item.parent_id][0]
        #parent = token.parent_entry
        depth+=1
        return get_dep_len(item.parent_entry, depth)


def get_stats_c(treebanks):
    traindata = list(utils.read_conll_dir(treebanks, "train"))
    n_dep = 0.
    depth = 0.
    for sentence in traindata:
        conll_sentence = [entry for entry in sentence if isinstance(entry, utils.ConllEntry)]
        for item in conll_sentence:
            if item.id != 0:
                depth_tok = get_dep_len(item, sentence, 1)
                depth += depth_tok
                n_dep += 1

    av_dep = depth/n_dep

    print treebanks[0].iso_id
    print "Average distance to root:" + str(av_dep)


if __name__=="__main__":
    parser = OptionParser()
    parser.add_option("--include", metavar="LIST", help="List of languages by ISO code to be run \
                     if using UD. If not specified need to specify trainfile at least. When used in combination with \
                     --multiling, trains a common parser for all languages. Otherwise, train monolingual parsers for \
                     each")
    parser.add_option("--datadir", metavar="PATH",
                      help="Input directory with UD train/dev/test files; obligatory if using --include")
    (options, args) = parser.parse_args()
    #ugly but necessary
    options.shared_task = False
    options.golddir = None
    iso_ids = utils.parse_list_arg(options.include)

    iso_dict = utils.load_iso_dict()
    treebank_metadata = [(name, iso_id) for (name, iso_id) in iso_dict.items()
                         if iso_id in iso_ids]

    treebanks = [utils.UDtreebank(ele, options) for ele in treebank_metadata]
    for treebank in treebanks:
        #get_stats([treebank])
        get_stats_c([treebank])


