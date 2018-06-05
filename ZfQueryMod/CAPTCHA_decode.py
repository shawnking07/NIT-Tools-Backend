from sklearn.externals import joblib
from PIL import ImageFilter
import numpy as np
import os


def get_binarypix(im):
    img = np.array(im)
    rows, cols = img.shape
    for i in range(rows):
        for j in range(cols):
            if img[i, j] <= 128:
                img[i, j] = 0
            else:
                img[i, j] = 1
    binpix = np.ravel(img)
    return binpix


def segment(im):
    s = 5
    w = 12
    h = 24
    t = 0
    im_new = []
    for i in range(4):
        im1 = im.crop((s + w * i, t, s + w * (i + 1), h))
        # im.crop剪裁图片
        im_new.append(im1)
    return im_new


def img_transfer(im):
    im = im.convert('RGB').filter(ImageFilter.DETAIL)
    im = im.filter(ImageFilter.MedianFilter())
    # 滤镜medianfilter是中值滤波器作用是减少噪声
    im = im.convert('L')
    # convert图像模式转换转为L模式 灰度模式
    return im


def cutPic(name):
    im = img_transfer(name)
    pics = segment(im)
    return pics


def load_predict(name):
    clf = joblib.load(os.path.abspath('./ZfQueryMod/train_model.m'))
    predict_value = []

    for pic in cutPic(name):
        binpix = get_binarypix(pic).reshape(1, -1)
        predict_value.append(clf.predict(binpix))

    predict_value = [str(chr(i)) for i in predict_value]
    # print("the CAPTCHA is :", "".join(predict_value))
    return "".join(predict_value)
