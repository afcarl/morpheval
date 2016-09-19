# -*- coding: utf-8 -*-
'''
calcurating F-measure score for evaluation word segmentation

TODO
* loop in evaluation function can be made more easy
'''


import argparse


def transform(sent):
    """
    Args:
            sent : word-segmented sentence, and at each word POS is attached
              (e.g "私 は 大学生 です")
    Return:
            posits : words in sent are substituted into positions in sent
              (e.g "[1:1, 2:2, 3:5, 6:7]")
    """
    word_list = sent.split(' ')
    posits = []
    start = 1
    for word in word_list:
        end = start + len(word) - 1
        # change word into position
        posits.append('{}:{}'.format(start, end))
        start = end + 1
    return posits


def evaluation(gold_file, pred_file):
    with open(gold_file) as fg, open(pred_file) as fp:
        n_correct = 0
        n_goldw = 0
        n_predw = 0
        for g_sent, p_sent in zip(fg, fp):
            assert g_sent.replace(' ', '') == p_sent.replace(' ', '')
            gold_list = transform(g_sent.strip('\n'))
            pred_list = transform(p_sent.strip('\n'))
            n_goldw += len(gold_list)
            n_predw += len(pred_list)
            # calcurating the number of words correctly predicted
            n_correct += len(set(gold_list).intersection(pred_list))
    precision = n_correct / n_predw
    recall = n_correct / n_goldw
    f_measure = 2 * precision * recall / (precision + recall)
    print('Precision : {}/{} = {}'.format(n_correct, n_predw, precision))
    print('Recall    : {}/{} = {}'.format(n_correct, n_goldw, recall))
    print('F-measure : {}'.format(f_measure))


def test_evaluation():
    gold_tmp_filepath = 'tmp/pos/test_eval_gold.tmp'
    pred_tmp_filepath = 'tmp/pos/test_eval_pred.tmp'
    evaluation(gold_tmp_filepath, pred_tmp_filepath)


if __name__ == '__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument('--gold', help='gold file')
    argparser.add_argument('--pred', help='predicted file')
    args = argparser.parse_args()
    evaluation(args.gold, args.pred)
