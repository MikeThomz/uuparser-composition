# UUParser-compos

This fork of [UUParser](https://github.com/UppsalaNLP/uuparser) contains the code developed for the following paper: 
> Miryam de Lhoneux, Miguel Ballesteros and Joakim Nivre. 2019. Recursive Subtree Composition in LSTM-based Dependency Parsing. To appear at NAACL 2019.

Instructions on how to train the parser can be found on the original repository. Options specific to the paper:

* `--use-recursive-composition`: set `TreeLSTM` to use LSTM composition and `RecNN` to use a recurrent cell.
* `--unidir-lstm`: set to `forward` or `backward` to replace the BiLSTM with a forward or a backward LSTM.

All experiments were run with `--disable-rlmost` and `--k 2`. We set the POS embedding size to 25 by setting `--pos-emb-size` to 25 for the `+pos` models (POS embeddings are disabled by default) and disable character embeddings in the `-char` models by setting `--char-emb-size` to 0.

The statistics for Figure 3. were collected with:
```
python src/treebanks_stats.py --include [treebank iso codes] --datadir [UD data dir]
```

For the ensemble, run
```
python src/ensemble.py outfile file1 file2 file3 ...
```

where file1, file2, etc. are model predictions and the output of the ensemble is written to outfile.

The ensemble uses the [dependency decoder from the LxMLS toolkit](https://github.com/LxMLS/lxmls-toolkit/blob/master/lxmls/parsing/dependency_decoder.py) copied in `src/dependency_decoder.py`. 


#### License

This software is released under the terms of the [Apache License, Version 2.0](http://www.apache.org/licenses/LICENSE-2.0).

#### Contact

For questions and usage issues, please contact miryam dot de underscore lhoneux at lingfil dot uu dot se
