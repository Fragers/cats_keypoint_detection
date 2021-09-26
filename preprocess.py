import numpy as np
import cv2
import pandas as pd
import PIL
import os


def make_square(img):
    sz = max(img.shape[0], img.shape[1])
    left = (sz - img.shape[1]) // 2
    right = sz - img.shape[1] - left
    top = (sz - img.shape[0]) // 2
    bottom = sz - img.shape[0] - top
    #         print(top, bottom, left, right)
    return cv2.copyMakeBorder(img, top + 10, bottom + 10, left + 10, right + 10, cv2.BORDER_CONSTANT, None,
                              value=0), left + 10, top + 10, right + 10, bottom + 10


def convert_single_img(img: np.ndarray, points: np.ndarray, new_size=224):
    prev_w = img.shape[1]
    prev_h = img.shape[0]
    points = points.copy()
    img, left, top, right, bottom = make_square(img)
    new_w = prev_w + left + right
    new_h = prev_h + top + bottom
    points[:, 0] += left
    points[:, 1] += top

    points[:, 0] *= (new_size / new_w)
    points[:, 1] *= (new_size / new_h)

    img = cv2.resize(img, (new_size, new_size))
    return img, points


def draw_marks(img, points):
    for i in range(len(points)):
        p = points[i]
        p = [int(p[0]), int(p[1])]
        img = cv2.circle(img, p, 3, (255, 0, 0), 4)

    return img


dataset = {
    "img": [],
    "marks": []
}
base = "cats"
cur_ds = "CAT_04"
p = os.path.join(base, cur_ds)
names = os.listdir(os.path.join(base, cur_ds))

for name in names:
    if not name.endswith(".cat"):
        continue

    img_name = name[:-4]
    # print(img_name)

    img = cv2.imread(os.path.join(p, img_name))
    # s = None
    with open(os.path.join(p, name), "r") as f:
        s = f.readline()
    points = list(map(int, s.split()))
    if points[0] != 9:
        continue

    np_points = np.array(points[1:]).reshape(-1, 2).astype(float)
    img_new, points = convert_single_img(img, np_points)
    # print(points, np_points, img.shape)
    dataset['img'].append(img_new)
    dataset['marks'].append(points)
    # break
    # img_points = draw_marks(img_new, points)
    # cv2.imwrite("./test.png", img_points)
    # break

np.save(os.path.join('new_cats', cur_ds) + ".npy", np.array(dataset))
