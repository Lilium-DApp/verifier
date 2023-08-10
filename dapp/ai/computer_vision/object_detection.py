import os
import io
import base64
import numpy as np
from PIL import Image
from .class_dict import class_dict
import tflite_runtime.interpreter as tflite


class ImageVerifier:
    def __init__(self, model_path):
        self.model_path = model_path
        self.interpreter = tflite.Interpreter(model_path=model_path)
        self.interpreter.allocate_tensors()
        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()

    def preprocess_image(self, base64_image) -> np.ndarray:
        image_bytes = base64.b64decode(base64_image)
        pil_image = Image.open(io.BytesIO(image_bytes))
        resized_img = pil_image.resize((224, 224))

        if resized_img.mode != 'RGB':
            resized_img = resized_img.convert('RGB')

        final_arr = np.expand_dims(resized_img, axis=0)
        final_arr = np.float32(final_arr)
        return final_arr

    def verify(self, base64_image) -> str:
        input_data = self.preprocess_image(base64_image)
        self.interpreter.set_tensor(self.input_details[0]['index'], input_data)
        self.interpreter.invoke()

        tflite_model_predictions = self.interpreter.get_tensor(
            self.output_details[0]['index'])
        prediction = np.argmax(tflite_model_predictions[0])

        return class_dict[prediction]

# # Example usage
# if __name__ == "__main__":
#     diretorio_atual = os.path.dirname(os.path.abspath(__file__))
#     # Caminho completo para o arquivo image.txt
#     caminho_arquivo = os.path.join(diretorio_atual, 'image.txt')
#     with open(caminho_arquivo, 'r') as arquivo:
#         conteudo = arquivo.read()
#     model_path = 'image.tflite'
#     image_verifier = ImageVerifier(model_path)

#     base64_image = "your_base64_encoded_image_here"
#     result = image_verifier.verify(conteudo)
#     print("Predicted class:", result)
