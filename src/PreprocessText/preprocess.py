import os
import src.util as util
import stemming


def preprocess(filename):
    with open(filename, 'r', encoding='GBK') as f:
        content = f.read()
        words = stemming.lemmatize_sentence(content, False)
        return words


def process_directory(path):
    files = os.listdir(path)
    result = []
    for file in files:
        content = preprocess(path + '/' + file)
        result.append(content)
        print(content)
    return result


if __name__ == "__main__":
    process_directory("D:/D/BUPT_projects/IR/search-ranker/search-ranker/docs")
