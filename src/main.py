from SpellingCorrect import spell
from InvertedIndex import constructIndex, getIndex


if __name__ == "__main__":
    # constructIndex.construct_index("D:\D\BUPT_projects\IR\search-ranker\search-ranker\docs")
    inverted_index = getIndex.get_index()
    word_list = getIndex.get_word_list()
    doc_info_list = getIndex.get_doc_info()


