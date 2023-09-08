import os
import base64
from dotenv import load_dotenv
from io import BytesIO
from PIL import Image, ImageDraw
import numpy as np
from tflite_runtime.interpreter import Interpreter
import pathlib

class ImageInput:
    def __init__(self, img: Image.Image):
        self._img = img

    def get_resized_nparray(self) -> np.ndarray:
        resized_img = self._img.resize((640, 640))

        if resized_img.mode != 'RGB':
            resized_img = resized_img.convert('RGB')

        final_arr = np.array(resized_img).astype(np.float32)
        final_arr = np.expand_dims(final_arr, axis=0)
        return final_arr

    def get_image(self) -> Image.Image:
        return self._img

def from_bytes(data: bytes):
    buffer = BytesIO(data)
    pil_img = Image.open(buffer)
    return ImageInput(pil_img)

class TreeDetectionModel:
    model_name = 'tree_detection_model'
    model_version = '1.0'
    model_file = 'computer_vision/model/best_float32_v1.tflite'

    def __init__(self):
        self.interp = None
        self._input_mean = 255.0
        self._input_std = 255.0
        self._input_idx = 0
        self._output_idx = 0

    def _get_full_paths(self):
        project_root = pathlib.Path(__file__).parent.parent
        model_path = (project_root / self.model_file).resolve()
        return model_path

    def load(self):
        if self.interp is not None:
            return

        model_path = self._get_full_paths()
        self.interp = Interpreter(str(model_path))
        self.interp.allocate_tensors()

        input_details = self.interp.get_input_details()
        self._input_idx = input_details[0]['index']

        output_details = self.interp.get_output_details()
        self._output_idx = output_details[0]['index']

    def predict(self, X: ImageInput):
        img_data = X.get_resized_nparray()
        img_data = (img_data - self._input_mean) / self._input_std

        self.interp.set_tensor(self._input_idx, img_data)
        self.interp.invoke()

        output_data = self.interp.get_tensor(self._output_idx)
        
        output_boxes = output_data[0, :, :4]
        output_scores = output_data[0, :, 4]

        results = []

        for i in range(len(output_scores)):
            if output_scores[i] >= 0.1:
                bounding_box = output_boxes[i]
                score = float(output_scores[i])
                label = "tree"
                results.append((label, bounding_box, score))

        original_img = X.get_image()
        draw = ImageDraw.Draw(original_img)

        for result in results:
            box = result[1] * [original_img.width, original_img.height, original_img.width, original_img.height]
            draw.rectangle(box.tolist(), outline="red")
            draw.text((box[0], box[1]), f"{result[0]}: {result[2]*100:.2f}%", fill="red")

        original_img.show()

        return results

def from_base64(base64_str):
    data = base64.b64decode(base64_str)
    return from_bytes(data)

# Exemplo de uso:
load_dotenv()

base64_image_str = os.getenv("BASE64_STRING")  
model = TreeDetectionModel()
model.load()
img_input = from_base64(base64_image_str)
results = model.predict(img_input)
print(results)
