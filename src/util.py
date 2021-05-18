import json
import os

project_path = os.getcwd()
docs_path = project_path.replace("src", "docs")


def get_all_doc_list():
    files = os.listdir(docs_path)
    file_list = []
    for file in files:
        file_list.append(file.split('.')[0])
    return sorted(file_list)


def write2JSON(content, file_name):
    file = open(file_name, 'w')
    content_str = json.JSONEncoder().encode(content)
    file.write(content_str)
    file.close()
