import os
import src.util as util

path = os.getcwd()
print(path)
save_path = util.project_path.replace("\search_ranker_pictures", "")
data_path = path + "\\cifar_100_selected\\"


def construct_index(path):
    inverted_index = {}
    folders = os.listdir(path)
    for folder in folders:
        # 每个文档的词项 list
        if folder not in inverted_index:
            sub_path = path + "\\" + folder
            sub_folders = os.listdir(sub_path)
            folder = folder.replace("_", " ")
            inverted_index[folder] = {}
            for sub_folder in sub_folders:
                min_path = sub_path + "\\" + sub_folder
                min_folder = os.listdir(min_path)
                sub_folder = sub_folder.replace("_", " ")
                inverted_index[folder][sub_folder] = []
                for item in min_folder:
                    image_id = item.split('.')[0]
                    inverted_index[folder][sub_folder].append(image_id)


    # 给倒排索引中的词项排序
    # sorted_inverted_index = sort_index(inverted_index)

    # 获取词项列表
    new_big_label_list = list(inverted_index.keys())

    # print_index(inverted_index)

    # 将数据写入文件中
    util.write2JSON(inverted_index, save_path + 'invertImageIndex.json')

if __name__ == "__main__":
    construct_index(data_path)