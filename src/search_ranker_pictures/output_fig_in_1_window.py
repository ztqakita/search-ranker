import cv2
import numpy as np
import os


def output_in_one_dir(route):
    images = []
    for root, dirs, image in os.walk(route):
        for img in image:
            fig = cv2.imread(os.path.join(route,img))
            images.append(fig)
            # cv2.imshow("the first 10 results",figure)
            # cv2.waitKey(0)
    # print(images)
    line = []
    line.append(np.hstack(images[:5]))
    line.append(np.hstack(images[5:10]))

    print(line)

    combined = np.vstack(line)
    cv2.imshow("the results", combined)
    cv2.waitKey(0)


def output_in_all_dirs(route):
    images = []
    for _, dirs, image in os.walk(route):
        print(dirs, image)
        if image == []:
            for sub in dirs:
                for _,_, _image in os.walk(os.path.join(route, sub)):
                    for img in _image:
                        fig = cv2.imread(os.path.join(route, sub, img))
                        images.append(fig)
                        # cv2.imshow("the first 10 results",figure)
                        # cv2.waitKey(0)
    
    line = []
    pivot = 0
    while pivot + 5 <= len(images):
        line.append(np.hstack(images[pivot:pivot+5]))
        pivot += 5

    print(line)

    combined = np.vstack(line)
    cv2.imshow("the results", combined)
    cv2.waitKey(0)


if __name__ == "__main__":
    output_in_all_dirs("./cifar100_selected/fish")