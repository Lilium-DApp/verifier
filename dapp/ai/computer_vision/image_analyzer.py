import numpy as np
from PIL import ImageDraw
from .image_decode import ImageDecode
from tflite_runtime.interpreter import Interpreter

class ImageAnalyzer:
    """
    A class to analyze images using a pre-trained tflite model. 

    Attributes:
        min_confidence (float): The minimum confidence score to consider a detection as valid. 
        max_iou (float): The maximum Intersection over Union (IoU) threshold to discard overlapping boxes.
        interpreter (tflite_runtime.interpreter.Interpreter): The TensorFlow Lite model interpreter.
        input_details (dict): Details of the input tensor for the model.
        output_details (dict): Details of the output tensor for the model.
        image_decoder (ImageDecode): An instance of the ImageDecode class to handle image decoding.
    """

    def __init__(self, model_path, min_confidence=0.2, max_iou=0.5):
        """
        Initializes an ImageAnalyzer instance.

        Args:
            model_path (str): The path to the tflite model file. Defaults to 'model/best_float32_v1.tflite'.
            min_confidence (float): The minimum confidence score to consider a detection as valid. Defaults to 0.2.
            max_iou (float): The maximum IoU threshold to discard overlapping boxes. Defaults to 0.5.
        """
        self.min_confidence = min_confidence
        self.max_iou = max_iou
        self.interpreter = Interpreter(model_path)
        self.interpreter.allocate_tensors()
        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()
        self.image_decoder = ImageDecode()

    @staticmethod
    def bbox_iou(box_a, box_b, box_a_area, box_b_area):
        """Calculates the Intersection over Union (IoU) of two bounding boxes."""
        inter_x_1 = max(box_a[0], box_b[0])
        inter_y_1 = max(box_a[1], box_b[1])
        inter_x_2 = min(box_a[2], box_b[2])
        inter_y_2 = min(box_a[3], box_b[3])

        inter_area = max(0, inter_x_2 - inter_x_1 + 1) * max(0, inter_y_2 - inter_y_1 + 1)
        iou = inter_area / (box_a_area + box_b_area - inter_area)
        return iou

    @staticmethod
    def xywh2xyxy(xywh):
        """Converts bounding box format from xywh to xyxy."""
        dw = xywh[2] / 2
        dh = xywh[3] / 2
        return [
            xywh[0] - dw,
            xywh[1] - dh,
            xywh[0] + dw,
            xywh[1] + dh,
        ]

    def process_image(self, base64_str):
        """Processes the input image and returns the annotated image along with detected bounding boxes."""
        img = self.image_decoder.from_base64(base64_str)
        img_resized_and_padded = self.image_decoder.resize_and_pad(img)
        
        data = np.array(img_resized_and_padded).astype(np.float32) / 255
        data = np.expand_dims(data, axis=0)
        
        input_idx = self.input_details[0]['index']
        output_idx = self.output_details[0]['index']
        
        self.interpreter.set_tensor(input_idx, data)
        self.interpreter.invoke()
        output = self.interpreter.get_tensor(output_idx)

        confidence = output[:, 4:84].max(axis=1)
        cand_mask = confidence > self.min_confidence

        cand_boxes = output[0, :, cand_mask[0, :]]
        final_boxes = []

        for box_i, box_i_pred in enumerate(cand_boxes):
            discard_i = False
            box_i_xyxy = self.xywh2xyxy(box_i_pred[:4]*640)
            box_i_prob = box_i_pred[4:].max()
            box_i_class = box_i_pred[4:].argmax()
            box_i_area = (box_i_xyxy[2] - box_i_xyxy[0] + 1) * (box_i_xyxy[3] - box_i_xyxy[1] + 1)

            for box_j, box_j_pred in enumerate(cand_boxes):
                if box_i == box_j:
                    continue
                
                box_j_xyxy = self.xywh2xyxy(box_j_pred[:4]*640)
                box_j_prob = box_j_pred[4:].max()
                box_j_area = (box_j_xyxy[2] - box_j_xyxy[0] + 1) * (box_j_xyxy[3] - box_j_xyxy[1] + 1)
                
                iou = self.bbox_iou(box_i_xyxy, box_j_xyxy, box_i_area, box_j_area)
                if (iou > self.max_iou) and (box_j_prob > box_i_prob):
                    discard_i = True
                    break

            if not discard_i:
                final_boxes.append(
                    {
                        'xyxy': box_i_xyxy,
                        'class': box_i_class,
                        'prob': box_i_prob,
                    }
                )

        new_img = img_resized_and_padded.copy()
        draw = ImageDraw.Draw(new_img)

        for box in final_boxes:
            label = f'{box["class"]} ({box["prob"]*100:.1f}%)'
            coords = [int(round(x)) for x in box["xyxy"]]
            draw.rectangle(coords, outline='red')
            textbox = draw.textbbox(
                xy=(coords[0], coords[1]),
                text=label,
                anchor="lt",
            )
            draw.rectangle(
                xy=[textbox[0], textbox[1], textbox[2] + 2, textbox[3] + 2],
                fill='red',
            )
            draw.text(
                xy=(coords[0] + 2, coords[1] + 1),
                text=label,
                anchor="lt",
                fill='white',
            )
        
        return new_img, final_boxes

# Example usage:
# analyzer = ImageAnalyzer()
# annotated_image, detections = analyzer.process_image(base64_str)