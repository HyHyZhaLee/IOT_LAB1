from keras.models import load_model  # TensorFlow is required for Keras to work
import cv2  # Install opencv-python
import numpy as np
import base64

class Camera:
    def __init__(self, IP = 0, debug_flag = 0):
        # Disable scientific notation for clarity
        np.set_printoptions(suppress=True)
        # Load the model
        self.model = load_model("keras_model.h5", compile=False)
        # Load the labels
        self.class_names = open("labels.txt", "r").readlines()
        # CAMERA can be 0 or 1 based on default camera of your computer
        self.setIP(IP)
        self.ai_result = ""
        self.confident = ""
        self.image = ""
        self.debug_flag = debug_flag

    def setIP(self, IP):
        self.IP = IP
        # An ip of your camera can be used as well
        self.IP = IP
        if IP == 0 or IP == 1:
            self.camera = cv2.VideoCapture(0)
        else:
            port = 81
            # URL for streaming
            stream_url = 'http://{}:{}/stream'.format(IP, port)
            # Tạo một đối tượng VideoCapture với URL streaming
            self.camera = cv2.VideoCapture(stream_url)

    def getIP(self, IP):
        return self.IP

    def destroyAllWindows(self):
        cv2.destroyAllWindows()

    def run_ai_detector(self):
        # Grab the web camera's image.
        ret, image = self.camera.read()
        if not ret:
            print("Failed to grab the frame from the camera.")
            return None

        # Optionally show the raw, unprocessed frame
        if self.debug_flag:
            cv2.imshow("Webcam Raw Image", image)
            cv2.waitKey(1)  # Add this line if you're running in a loop to give time for the image to be displayed

        res, frame = cv2.imencode('.jpg', image)
        data = base64.b64encode(frame)

        # Process the image for AI detection
        processed_image = cv2.resize(image, (224, 224), interpolation=cv2.INTER_AREA)
        processed_image = np.asarray(processed_image, dtype=np.float32).reshape(1, 224, 224, 3)
        processed_image = (processed_image / 127.5) - 1

        # Predicts the model
        prediction = self.model.predict(processed_image)
        index = np.argmax(prediction)
        class_name = self.class_names[index].strip()  # Also stripping the newline character
        confidence_score = prediction[0][index]

        if self.debug_flag:
            # If you want to display the processed image, ensure it's converted properly
            # Note: This step is optional and mostly for debugging. It might not be needed or should be adjusted as per your needs.
            # display_image = cv2.cvtColor(processed_image[0], cv2.COLOR_RGB2BGR)
            # cv2.imshow("Processed Image", display_image)
            print(f"Class: {class_name}, Confidence Score: {confidence_score * 100:.2f}%")

        return class_name, f"{confidence_score * 100:.2f}%", data

    # def publishImage(self,dt):
    #     self.ai_result, self.confident, self.image = self.ai_detector()
    #     publish("image", self.image)
    #
    # def publishResult(self,dt):
    #     self.ai_result, self.confident, self.image = self.ai_detector()
    #     publish("ai", self.ai_result)
    #     publish("confident-score", self.confident)

if __name__ == '__main__':
    camera = Camera(0, True)
    
    while cv2.waitKey(1) is -1:
        result, confidence_score, image = camera.run_ai_detector()

    camera.destroyAllWindows()
