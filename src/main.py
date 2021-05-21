import os
import util
from SpellingCorrect import spell
from InvertedIndex import constructIndex, getIndex
from AnalyzeRank import analyzeInput, calculateRank
from PreprocessText import stemming


FILE_NUM = len(os.listdir(util.docs_path))

if __name__ == "__main__":
    # constructIndex.construct_index(util.docs_path)
    inverted_index = getIndex.get_index()
    word_list = getIndex.get_word_list()
    VSM = calculateRank.createVSM(inverted_index, word_list, FILE_NUM, util.docs_path)
    loop = True

    while loop:
        print("input the query statement:")
        raw_query = input()
        print("stemming...")
        query = stemming.lemmatize_sentence(raw_query, True)
        print(str(query))
        print("spelling correcting...")
        query = spell.correctSentence(query)
        print(str(query))

        word_set = set(query)

        word_vector = calculateRank.create_query_vector(word_list, word_set)
        print("VSM method:")
        sorted_doc_list = calculateRank.calculate_cos(VSM, word_vector)
        vsm_doc_list = []
        for doc in sorted_doc_list:
            vsm_doc_list.append(int(doc[1]))
            print("doc id:", doc[1], "score:", "%.4f" % doc[0])

        doc_list = analyzeInput.analyze_input(inverted_index, word_set)
        sorted_doc_list_2 = calculateRank.get_sorted_score_list(inverted_index, FILE_NUM, doc_list, word_set)
        print("wf-idf method:")
        wfidf_doc_list = []
        for doc in sorted_doc_list_2:
            wfidf_doc_list.append(int(doc[1]))
            print("doc id:", doc[1], "score:", "%.4f" % doc[0])

        sum = 0
        diff = 0
        for doc in vsm_doc_list:
            sum += 1
            if doc not in wfidf_doc_list:
                diff += 1
        accuracy = (sum-diff)/sum
        print("accuracy:", accuracy)



