import joblib


class GaussianEnvelopPredictor:
    def __init__(self, model_path):
        self.model = joblib.load(model_path)

    def predict(self, features):
        """
        Predicts using the loaded Gaussian Envelop model.

        Args:
            features (list): List of feature values [temperature, humidity, co].

        Returns:
            prediction: The prediction made by the model.
        """
        if len(features) != 3:
            raise ValueError(
                "Features should contain temperature, humidity, and co.")

        prediction = self.model.predict([features])
        return prediction


# # Usage
# model_path = "./model/gaussian_envelop.sav"
# predictor = GaussianEnvelopPredictor(model_path)
# prediction = predictor.predict([temperature, humidity, air_quality])
# print("Prediction:", prediction)
