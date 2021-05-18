import os
# import .util
from src.PreprocessText import stemming


def preprocess(filename):
    print(filename)
    with open(filename, 'r', encoding='UTF-8') as f:
        content = f.read()
        words = stemming.lemmatize_sentence(content, False)
        return words


def process_directory(path):
    files = os.listdir(path)
    result = []
    for file in files:
        if (file == '.DS_Store'):
            continue
        content = preprocess(path + '/' + file)
        result.append(content)
        print(content)
    return result


# if __name__ == "__main__":
#     process_directory("../../docs")
