# Import required libraries
import numpy as np
import streamlit as st
import cv2
import keras
import sys
from keras.models import load_model

# Loading the model
model = load_model('./TrafficSignClassification/tf_model.h5')

# Name of Classes
all_labels = ['Speed limit (20km/h)','Speed limit (30km/h)','Speed limit (50km/h)','Speed limit (60km/h)',
              'Speed limit (70km/h)','Speed limit (80km/h)','End of speed limit (80km/h)','Speed limit (100km/h)',
              'Speed limit (120km/h)','No passing','No passing for vechiles over 3.5 metric tons',
              'Right-of-way at the next intersection','Priority road','Yield','Stop','No vechiles',
              'Vechiles over 3.5 metric tons prohibited','No entry','General caution','Dangerous curve to the left',
              'Dangerous curve to the right','Double curve','Bumpy road','Slippery road','Road narrows on the right',
              'Road work','Traffic signals','Pedestrians','Children crossing','Bicycles crossing','Beware of ice/snow',
              'Wild animals crossing','End of all speed and passing limits','Turn right ahead','Turn left ahead',
              'Ahead only','Go straight or right','Go straight or left','Keep right','Keep left','Roundabout mandatory',
              'End of no passing','End of no passing by vechiles over 3.5 metric']

# Title of the app
st.title(":blue[Traffic Sign Prediction]")
st.markdown("Upload image of any traffic sign")

# Uploading input image (traffic sign)
traffic_sign = st.file_uploader("Choose an image...", type=["png", "jpeg", "jpg"])
submit = st.button('Predict')

# If the user clicks on submit, do this:
if submit:
    if traffic_sign is not None:

        # Convert the file to an opencv image
        file_bytes = np.asarray(bytearray(traffic_sign.read()), dtype=np.uint8)
        opencv_image = cv2.imdecode(file_bytes, 1)

        # Display the image
        st.image(opencv_image, channels="BGR")
        # Resizing the image
        opencv_image = cv2.resize(opencv_image, (50,50))
        # Convert image to 4 dimension
        opencv_image.shape = (1,50,50,3)

        try:
            # Make Prediction
            with st.spinner('Predicting...'):
                Y_pred = model.predict(opencv_image)
                st.title(f"The Traffic Sign is :blue[{all_labels[np.argmax(Y_pred)]}]")
                st.markdown("Sorry for the very bad prediction. I'll surely work on the accuracy of this model...soon :grimacing:")
            sys.stdout.flush()

        except Exception as e:
            st.error("An error occurred during prediction.")
            st.error(str(e))

