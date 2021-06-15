# A converter to convert the original file into pictures and select 10 figures for each category

import numpy as np
import os
from PIL import Image
import glob

ROOT_PATH= '/'
TO_ROOT='./cifar100_pictures'
def unpickle(file):
    import pickle
    with open(file, 'rb') as fo:
        dict_file = pickle.load(fo, encoding='latin1')
    return dict_file

meta_dict=unpickle(os.path.join(ROOT_PATH,'meta'))
train_dict=unpickle(os.path.join(ROOT_PATH,'train'))
test_dict=unpickle(os.path.join(ROOT_PATH,'test'))

os.mkdir(TO_ROOT)
os.mkdir(os.path.join(TO_ROOT,'train'))
os.mkdir(os.path.join(TO_ROOT,'test'))

print(meta_dict)


for i in range(20):
    os.mkdir(os.path.join(TO_ROOT,'train',meta_dict['coarse_label_names'][i]))
    os.mkdir(os.path.join(TO_ROOT,'test',meta_dict['coarse_label_names'][i]))

data, coarse_label, fine_label = np.array(train_dict['data']).reshape(-1, 3, 32, 32).transpose(0, 2, 3, 1), train_dict['coarse_labels'], train_dict['fine_labels']


for i in range(data.shape[0]):
    route = os.path.join(TO_ROOT,'train', meta_dict['coarse_label_names'][coarse_label[i]], meta_dict['fine_label_names'][fine_label[i]])
    if not os.path.exists(route):
        os.mkdir(route) 
    path_file_number=glob.glob(route+'/*.png')
    if len(path_file_number) < 10:        
        img = Image.fromarray(data[i])
        img.save(os.path.join(TO_ROOT,'train', meta_dict['coarse_label_names'][coarse_label[i]], meta_dict['fine_label_names'][fine_label[i]], meta_dict['fine_label_names'][fine_label[i]]+str(i)+'.png'))


data, coarse_label, fine_label = np.array(test_dict['data']).reshape(-1, 3, 32, 32).transpose(0, 2, 3, 1), test_dict['coarse_labels'], test_dict['fine_labels']
for i in range(data.shape[0]):
    route = os.path.join(TO_ROOT,'test', meta_dict['coarse_label_names'][coarse_label[i]], meta_dict['fine_label_names'][fine_label[i]])
    if not os.path.exists(route):
        os.mkdir(route) 
    path_file_number=glob.glob(route+'/*.png')
    if len(path_file_number) < 10:        
        img = Image.fromarray(data[i])
        img.save(os.path.join(TO_ROOT,'test', meta_dict['coarse_label_names'][coarse_label[i]], meta_dict['fine_label_names'][fine_label[i]], meta_dict['fine_label_names'][fine_label[i]]+str(i)+'.png'))
