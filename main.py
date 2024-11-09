import os
from PIL import Image
from PIL.ExifTags import TAGS
import matplotlib
import matplotlib.pyplot as plt
from util import is_person
import numpy as np
import math

matplotlib.use("TkAgg")


def get_focal_length(image_path):
    try:
        image = Image.open(image_path)
        exif_data = image._getexif()
        if not exif_data:
            return None

        for tag, value in exif_data.items():
            decoded = TAGS.get(tag, tag)
            if decoded == "FocalLength":
                # Focal length is stored as a tuple (numerator, denominator)
                return value[0] / value[1] if isinstance(value, tuple) else value
    except Exception as e:
        print(f"Error reading {image_path}: {e}")
    return None


def get_all_focal_lengths(directories):
    person_focal_lengths = []
    scenery_focal_lengths = []
    for directory in directories:
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.lower().endswith('.jpg'):
                    image_path = os.path.join(root, file)
                    focal_length = get_focal_length(image_path)
                    if focal_length:
                        if is_person(image_path):
                            person_focal_lengths.append(focal_length)
                        else:
                            scenery_focal_lengths.append(focal_length)
    return person_focal_lengths, scenery_focal_lengths


def plot_focal_length_distribution(focal_lengths, subject):
    plt.clf()
    plt.hist(focal_lengths, bins=range(int(min(focal_lengths)), int(max(focal_lengths)) + 1, 1), edgecolor='black')
    # 设置x轴刻度
    start_x = min(focal_lengths) // 10 * 10
    end_x = math.ceil(max(focal_lengths) / 10) * 10
    xticks = np.arange(start_x, end_x + 1, step=10)
    plt.xticks(xticks)
    # 大写subject首字母
    subject = subject[0].upper() + subject[1:]
    plt.title(subject + ' Focal Length Distribution')
    plt.xlabel('Focal Length (mm)')
    plt.ylabel('Frequency')
    plt.savefig(subject + '_focal_length_distribution.png')


# 使用示例
directory = ["E:/两个人/2024园博园佳能r10/", "E:/两个人/2024深圳南科大5月", "G:/照片2024/新加坡吉隆坡",
             "G:/20240607/调色",
             "G:/20240616", "G:/北京2024", "G:/毕业照", "G:/飞盘/100CANON", "G:/上海丽水台州", "G:/深圳",
             "G:/照片2024/202407老家",
             "G:/20240723随舞/随舞", "G:/20240724沙面约拍/修图"]  # 替换为你的图片目录
person_focal_lengths, scenery_focal_lengths = get_all_focal_lengths(directory)
if person_focal_lengths:
    print("number of person images: ", len(person_focal_lengths))
    plot_focal_length_distribution(person_focal_lengths, "person")
else:
    print("No person focal lengths found in the specified directory.")

if scenery_focal_lengths:
    print("number of scenery images: ", len(scenery_focal_lengths))
    plot_focal_length_distribution(scenery_focal_lengths, "scenery")
else:
    print("No scenery focal lengths found in the specified directory.")
