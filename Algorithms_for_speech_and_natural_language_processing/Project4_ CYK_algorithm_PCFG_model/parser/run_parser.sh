test_sentences=${1:-'/tmp'}


# Run `chmod u+x run_parser.sh` and pass the path of the output directory as follows:
# `./run_parser.sh /path/to/test_senteces`

# `python3 CYK_parser.py ./sequoia-corpus+fct.mrg_strict.txt ${test_sentences} ./eval_predicted.txt can be replaced by python3 CKY_parser.py ./train_set.txt ${test_sentences} ./eval_predicted.txt if you wanna train the grammar only on a subset of the corpus`


python3 ./Code_PCFG.py ./sequoia-corpus+fct.mrg_strict.txt ./train_set.txt ./dev_set.txt ./eval_grd_truth.txt ./eval_set.txt ./grammar_learnt.txt
python3 CYK_parser.py ./sequoia-corpus+fct.mrg_strict.txt ${test_sentences} ./eval_predicted.txt
python3 Evaluation.py eval_grd_truth.txt eval_predicted.txt evaluation.txt
