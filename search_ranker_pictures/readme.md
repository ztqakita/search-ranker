# 关于search_ranker_pictures

## 图片
CIFAR-100，每一个细分种类保留10张图片
图片按照cifar_100/粗粒度类别/细粒度类别的形式进行存储
每张图片名称为 细粒度类别+数字.png

## 一种可能的排索引方式
直接在粗粒度类别/细粒度类别对应索引后面加上类别锁对应的目录？

## 接口
在`output_fig_in_1_window.py`中
```
output_in_one_dir(route)
```
负责将细粒度类别路径下面的所有图片合成一张图片进行输出。
输入为细粒度图片类别所在路径 e.g. `./cifar100_selected/fish/shark`
```
output_in_all_dirs()
```
负责将粗粒度类别路径下面的所有图片合成一张图片进行输出。
输入为粗粒度图片类别所在路径 e.g. `./cifar100_selected/fish/`
```
