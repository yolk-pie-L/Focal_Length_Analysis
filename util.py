import torch
import cv2
from PIL import Image
import numpy as np

# 加载预训练的 YOLOv5 模型
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)


def is_central(x1, y1, x2, y2, image_width, image_height):
    position_x = (x1 + x2) / image_width / 2
    position_y = (y1 + y2) / image_height / 2
    return 0.15 < position_x < 0.85 and 0.15 < position_y < 0.85


def is_person(image_path):
    image = Image.open(image_path)
    image_width, image_height = image.size

    # 使用模型进行预测
    results = model(image)
    # results.show()

    # 获取预测结果的数据
    predictions = results.xyxy[0].cpu().numpy()  # [x1, y1, x2, y2, confidence, class]

    # 解析预测结果并标记图像中的主体
    for prediction in predictions:
        x1, y1, x2, y2, confidence, cls = prediction

        label = model.names[int(cls)]
        if label != 'person' or confidence <= 0.55:
            continue

        # 计算人物框的宽度和高度
        box_width = x2 - x1
        box_height = y2 - y1
        box_area = box_width * box_height

        # 计算人物在图像中的占比
        image_area = image_width * image_height
        person_area_ratio = box_area / image_area

        # print(f'Label: {label}, Confidence: {confidence:.2f}')
        # print(f'Bounding box: ({x1}, {y1}), ({x2}, {y2})')
        # print(f'Width: {box_width}, Height: {box_height}')
        # print(f'Person area: {box_area} pixels, Area ratio: {person_area_ratio:.2%}')

        # 如果人物占比大于 20%，则认为这是一张人物照片
        if person_area_ratio > 0.2:
            return True
        # 如果人物占比大于1%，并且人物位于图像中央，则认为这是一张人物照片
        if person_area_ratio > 0.01 and \
                (is_central(x1, y1, x2, y2, image_width, image_height)):
            return True

    return False




