from rouge_score import rouge_scorer


def rouge_filter(new_text_list, old_text_list):
    """Compare each word in new_text_list with all words in old_text_list,
       suppose A1...Am is from new_text_list, B1...Bn is from old_text_list
       then we calculate the ROUGE score between Ai and Bj, if the max score
       is greater than 0.7, then we discard Ai
    """

    # similarities = {}
    scorer = rouge_scorer.RougeScorer(["rougeL"], use_stemmer=False)

    results = []
    for new_text in new_text_list:
        rouge_scores = [scorer.score(new_text, old_text)["rougeL"].fmeasure for old_text in old_text_list]
        if max(rouge_scores) > 0.6:
            continue
        results.append(new_text)

    return results


def bert_filter(text, reference):
    """评价text和reference的语义的相似度，使用BERTscore
    """

    return 0.0
