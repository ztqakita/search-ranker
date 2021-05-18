import os
import src.util as util
from src.PreprocessText import preprocess


def construct_index(path):
    inverted_index = {}
    files = os.listdir(path)
    for file in files:
        print("analyzing file: ", file)
        # 每个文档的词项 list
        content = preprocess.preprocess(path + '/' + file)
        doc_id = file.split('.')[0]

        pos = 0
        for word in content:
            if word not in inverted_index:
                word_list = {doc_id: [pos]}
                inverted_index[word] = word_list
            else:
                if doc_id not in inverted_index[word]:
                    inverted_index[word] = {doc_id: [pos]}
                else:
                    inverted_index[word][doc_id].append(pos)
        pos += 1

    # 给倒排索引中的词项排序
    sorted_inverted_index = sort_index(inverted_index)

    # 获取词项列表
    new_word_list = get_word_list(inverted_index)

    print_index(inverted_index)

    # 将数据写入文件中
    util.write2JSON(sorted_inverted_index, util.project_path + 'invertIndex.json')
    util.write2JSON(new_word_list, util.project_path + 'wordList.json')


def sort_index(index):
    sindex = {k: index[k] for k in sorted(dict.keys())}
    for stem in sindex:
        sindex[stem] = {k: sindex[stem][k] for k in sorted(sindex[stem].keys())}
    return sindex


def get_word_list(inverted_index):
    return list(inverted_index.keys())


def print_index(inverted_index):
    for word in inverted_index:
        print(word)
        for doc in inverted_index[word]:
            print("    ", doc, " : ", inverted_index[word][doc])