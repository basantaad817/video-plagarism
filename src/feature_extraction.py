import tensorflow as tf
from tensorflow.keras.applications.mobilenet import MobileNet, preprocess_input # type: ignore
from tensorflow.keras.preprocessing import image #type: ignore
import numpy as np
import os

def extract_features_from_frames(frame_dir):
    """Extract features using MobileNet model for each frame in the specified directory."""
    model = MobileNet(weights='imagenet', include_top=False)
    features_list = []

    for frame_file in sorted(os.listdir(frame_dir)):
        frame_path = os.path.join(frame_dir, frame_file)
        img = image.load_img(frame_path, target_size=(224, 224))
        img_data = image.img_to_array(img)
        img_data = np.expand_dims(img_data, axis=0)
        img_data = preprocess_input(img_data)

        features = model.predict(img_data)
        features_list.append(features.flatten())

    return np.array(features_list)
