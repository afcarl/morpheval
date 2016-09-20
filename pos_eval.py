"""
This script is calcurate precision, recall and F-score for Japanese
Morphological Analysis

TODO
* loop in evaluation function can be made more easy
"""


import argparse


def transform(sent, separator):
    """
    Args:
            sent : word segmented sentence, and at each word POS is attached
                (e.g "私_名詞 は_助詞 大学生_名詞")
            separator : separator between word and POS tag
    Return:
            pais : words in sent are substituted into positions in sent
                (e.g "1:1_名詞 2:2_助詞 3:5_名詞")
    """
    wordpos_list = [wordpos.split(separator) for wordpos in sent.split(' ')]
    pairs = []
    start = 1
    for word, pos in wordpos_list:
        end = start + len(word) - 1
        # change word into position
        pairs.append('{}:{}{}{}'.format(start, end, separator, pos))
        start = end + 1
    return pairs


def check_pair(sent1, sent2, separator):
    words1 = [wordpos.split(separator)[0] for wordpos in sent1.split(' ')]
    words2 = [wordpos.split(separator)[0] for wordpos in sent2.split(' ')]
    return ''.join(words1) == ''.join(words2)


def evaluation(gold_file, pred_file, separator="_"):
    with open(gold_file) as fg, open(pred_file) as fp:
        n_correct = 0
        n_goldw = 0
        n_predw = 0
        for g_sent, p_sent in zip(fg, fp):
            assert check_pair(g_sent.strip('\n'), p_sent.strip('\n'), separator)
            gold_list = transform(g_sent.strip('\n'), separator)
            pred_list = transform(p_sent.strip('\n'), separator)
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


if __name__ == '__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument('--gold', help='gold file')
    argparser.add_argument('--pred', help='predicted file')
    args = argparser.parse_args()
    evaluation(args.gold, args.pred)
