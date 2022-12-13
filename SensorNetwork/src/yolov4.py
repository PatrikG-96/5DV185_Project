from darknet.darknet import make_image, network_height, network_width, copy_image_from_bytes, detect_image, bbox2points, load_network
from paddleocr import PaddleOCR
import cv2
import numpy as np
from darknet.darknet_images import load_images, image_detection

def crop_image(image, coordinates):

    return image[coordinates[1]:coordinates[3], coordinates[0]:coordinates[2]]

def yolov4_detection(network, frame, config, data, batch_size, weights, threshold, class_names):

    width = network_width(network)
    height = network_height(network)
    dnet_image = make_image(width, height, 3)

    image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    image_resized = cv2.resize(image_rgb, (width, height))

    copy_image_from_bytes(dnet_image, image_resized.tobytes())
    detections = detect_image(network, class_names, dnet_image, thresh=threshold)

    out_size = frame.shape[:2]
    in_size = image_resized.shape[:2]
    coord, scores = resize_bounding_box(detections, out_size, in_size)

    return coord, scores

def resize_bounding_box(detections, out_size, in_size):
    coord = []
    scores = []

    for detection in detections:
        points = list(detection[0])
        conf = detection[1]

        xmin, ymin, xmax, ymax = bbox2points(points)

        y_scale = float(out_size[0] / in_size[0])
        x_scale = float(out_size[1] / in_size[1])

        ymin = int(y_scale * ymin)
        ymax = int(y_scale * ymax)
        xmin = int(x_scale * xmin) if int(x_scale * xmin) > 0 else 0
        xmax = int(x_scale * xmax)

        final_points = [xmin, ymin, xmax-xmin, ymax-ymin]
        scores.append(conf)
        coord.append(final_points)

    return coord, scores

def alpr(image_path, config_path, data_path, weights_path, batch_size, thresh):

    network, class_names, class_colors = load_network(
        config_file=config_path,
        data_file=data_path,
        weights = weights_path,
        batch_size=batch_size
    )
    
    image = cv2.imread(image_path)
    bounding_boxes, scores = yolov4_detection(network = network, config = config_path, frame = data_path, batch_size=batch_size, weights=weights_path, threshold=thresh)

    for box in bounding_boxes:

        box = [box[0], box[1], box[2]-box[0], box[3]-box[1]]

        cropped_image = crop_image(image, box)

        result = PaddleOCR.ocr(cropped_image, cls=False, det=False)

        ocr_result = result[0][0]

        print(ocr_result)