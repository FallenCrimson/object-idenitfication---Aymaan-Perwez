import json
import argparse
import os
import sys
import tkinter as tk
from tkinter import filedialog
from pathlib import Path
from utils.general import update_options
from ultralytics import YOLO
from ultralytics.utils.checks import cv2, print_args
import numpy as np

FILE = Path(__file__).resolve()
ROOT = FILE.parents[0]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))
ROOT = Path(os.path.relpath(ROOT, Path.cwd()))

def predict(opt, image_path):
    opt.source = image_path
    results = model(**vars(opt), stream=True)

    for result in results:
        if opt.save_txt:
            result_json = json.loads(result.tojson())
            print(json.dumps({'results': result_json}))
        else:
            im0 = cv2.imencode('.jpg', result.plot())[1].tobytes()
            yield im0

def choose_file():
    root = tk.Tk()
    root.withdraw()  # This Is To Hide the main window

    file_path = filedialog.askopenfilename(title="Select Image File",
                                           filetypes=[("Image Files", "*.jpg;*.jpeg;*.png;*.gif")])

    if file_path:
        # Performing the prediction
        for image_bytes in predict(opt, file_path):
            # Converting the image bytes to a NumPy array
            nparr = np.frombuffer(image_bytes, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

            # Here, It Is Displaying the image using OpenCV
            cv2.imshow("YOLO Results", img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

        print("Prediction completed.")

if __name__ == '__main__':
    # Inputing the following arguments as follows
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', '--weights', type=str, default=ROOT / 'yolov8s.pt',
                        help='model path or triton URL')
    parser.add_argument('--source', type=str, default=ROOT / 'data/images',
                        help='source directory for images or videos')
    parser.add_argument('--conf', '--conf-thres', type=float, default=0.25,
                        help='object confidence threshold for detection')
    parser.add_argument('--iou', '--iou-thres', type=float, default=0.7,
                        help='intersection over union (IoU) threshold for NMS')
    parser.add_argument('--imgsz', '--img', '--img-size', nargs='+', type=int, default=[640],
                        help='image size as scalar or (h, w) list, i.e. (640, 480)')
    parser.add_argument('--half', action='store_true', help='use half precision (FP16)')
    parser.add_argument('--device', default='', help='device to run on, i.e. cuda device=0/1/2/3 or device=cpu')
    parser.add_argument('--show', '--view-img', default=False, action='store_true',
                        help='show results if possible')
    parser.add_argument('--save', action='store_true', help='save images with results')
    parser.add_argument('--save_txt', '--save-txt', action='store_true', help='save results as .txt file')
    parser.add_argument('--save_conf', '--save-conf', action='store_true',
                        help='save results with confidence scores')
    parser.add_argument('--save_crop', '--save-crop', action='store_true',
                        help='save cropped images with results')
    parser.add_argument('--show_labels', '--show-labels', default=True, action='store_true',
                        help='show labels')
    parser.add_argument('--show_conf', '--show-conf', default=True, action='store_true',
                        help='show confidence scores')
    parser.add_argument('--max_det', '--max-det', type=int, default=300,
                        help='maximum number of detections per image')
    parser.add_argument('--vid_stride', '--vid-stride', type=int, default=1,
                        help='video frame-rate stride')
    parser.add_argument('--stream_buffer', '--stream-buffer', default=False, action='store_true',
                        help='buffer all streaming frames (True) or return the most recent frame (False)')
    parser.add_argument('--line_width', '--line-thickness', default=None, type=int,
                        help='The line width of the bounding boxes. If None, it is scaled to the image size.')
    parser.add_argument('--visualize', default=False, action='store_true',
                        help='visualize model features')
    parser.add_argument('--augment', default=False, action='store_true',
                        help='apply image augmentation to prediction sources')
    parser.add_argument('--agnostic_nms', '--agnostic-nms', default=False, action='store_true',
                        help='class-agnostic NMS')
    parser.add_argument('--retina_masks', '--retina-masks', default=False, action='store_true',
                        help='whether to plot masks in native resolution')
    parser.add_argument('--classes', type=list,
                        help='filter results by class, i.e. classes=0, or classes=[0,2,3]')
    parser.add_argument('--boxes', default=True, action='store_false',
                        help='Show boxes in segmentation predictions')
    parser.add_argument('--exist_ok', '--exist-ok', action='store_true',
                        help='existing project/name ok, do not increment')
    parser.add_argument('--project', default=ROOT / 'runs/detect',
                        help='save results to project/name')
    parser.add_argument('--name', default='exp', help='save results to project/name')
    parser.add_argument('--dnn', action='store_true', help='use OpenCV DNN for ONNX inference')
    

    opt, unknown = parser.parse_known_args()

    # Finally, We are Loading the model
    model = YOLO(str(opt.model))

    # file interactively Chosen as per the user's choice
    choose_file()
