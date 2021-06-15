import json
import src.util as util


def get_index():
    with open(util.project_path + 'invertIndex.json', 'r') as f:
        index_str = f.read()
        index = json.JSONDecoder().decode(index_str)
        return index


def get_Image_Index():
    with open(util.project_path + 'invertImageIndex.json', 'r') as f:
        index_str = f.read()
        index = json.JSONDecoder().decode(index_str)
        return index


def get_word_list():
    with open(util.project_path + 'wordList.json', 'r') as f:
        word_str = f.read()
        word_list = json.JSONDecoder().decode(word_str)
        return word_list


def get_doc_info():
    with open(util.project_path + 'docInfo.json', 'r') as f:
        info_str = f.read()
        doc_info_list = json.JSONDecoder().decode(info_str)
        return doc_info_list
