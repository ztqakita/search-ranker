import cmath
import os
import json
import numpy as np
import src.util as util


def create_query_vector(word_list, word_set):
    word_vector = []
    for word in word_list:
        if word not in word_set:
            word_vector.append(0)
        else:
            word_vector.append(1)
    return word_vector


def createVSM(index, word_list, file_num, path):
    docs = os.listdir(path)
    VSM = {}
    for doc in docs:
        doc_id = doc.split('.')[0]
        tf_idf_list = []
        for word in word_list:
            if doc_id not in index[word]:
                tf_idf_list.append(0)
                continue

            tf = len(index[word][doc_id])
            df = len(index[word])
            idf = cmath.log10(file_num / df).real
            # idf =  float("%.3f" % cmath.log(10 , fileNum / df).real)
            tf_idf = float(tf * idf)

            tf_idf_list.append(tf_idf)

        VSM[doc_id] = tf_idf_list
    # util.write2JSON(VSM, util.project_path + 'VSM.json')
    return VSM


def get_VSM():
    with open(util.project_path + 'VSM.json', 'r') as f:
        vsm_str = f.read()
        vsm = json.JSONDecoder().decode(vsm_str)
        return vsm


def calculate_cos(vsm, word_vector):
    score_list = []
    for doc_id in vsm.keys():
        A = np.mat(vsm[doc_id])
        B = np.mat(word_vector)
        num = float(A * B.T)  # 若为行向量则 A * B.T
        denom = np.linalg.norm(A) * np.linalg.norm(B)
        if denom == 0.0:
            print(doc_id)
        cos = num / denom  # 余弦值
        sim = 0.5 + 0.5 * cos  # 归一化
        if sim > 0.5:
            score_list.append([sim, doc_id])
    sorted_score_list = sorted(score_list, reverse=True)
    return sorted_score_list



def get_wfidf_score(index, file_num, doc_id, word_set):
    score = 0
    doc_id = str(doc_id)
    for word in word_set:
        if word not in index or doc_id not in index[word]:
            continue
        tf = len(index[word][doc_id])
        df = len(index[word])
        wf = 1 + cmath.log10(tf).real
        idf = cmath.log10(file_num / df).real
        # add up all the wfidf of each key word
        score += wf * idf
    return score


def get_sorted_score_list(index, file_num, doc_list, word_set):
    score_list = []
    for doc in doc_list:
        score = get_wfidf_score(index, file_num, doc, word_set)
        score_list.append([score, doc])
    sorted_score_list = sorted(score_list, reverse=True)
    return sorted_score_list
