import re


def analyze_union_input(index, query):
    if len(query) == 0:
        return []
    else:
        total_result = []
        for word in query:
            word_result = get_target_doc_id(index, word)
            total_result = list(set(total_result).union(set(word_result)))
        return total_result


def analyze_inter_input(index, query):
    if len(query) == 0:
        return []
    else:
        total_result = []
        cnt = 1
        for word in query:
            word_result = get_target_doc_id(index, word)
            if cnt == 1:
                total_result = word_result
            total_result = list(set(total_result).intersection(set(word_result)))
            cnt += 1
        return total_result


def get_target_doc_id(index, word):
    if word not in index:
        return []
    else:
        result = [int(key) for key in index[word].keys()]
        result.sort()
        return result




