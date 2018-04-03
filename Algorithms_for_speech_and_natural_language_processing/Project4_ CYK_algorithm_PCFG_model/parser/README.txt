The .sh file takes in argument the path of the tokenised text on the standard input (one sentence per line, exactly one whitespace between each word similar to eval_set.txt in the same folder. 


# Run `chmod u+x run_parser.sh` and pass the path of the testset as follows:
# `./run_parser.sh /path/to/test_sentences.txt`

# `python3 CKY_parser.py ./sequoia-corpus+fct.mrg_strict.txt ${test_sentences} ./eval_predicted.txt' CAN BE REPLACED BY 'python3 CKY_parser.py ./train_set.txt ${test_sentences} ./eval_predicted.txt if you wanna train the grammar only on a subset of the corpus` however the grammar should contain the tokens in the test sentences otherwise the returned predictions are None.