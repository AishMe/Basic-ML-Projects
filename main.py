# Import required libraries
import numpy as np
import streamlit as st
import cv2
import keras
import sys
from keras.models import load_model

# Loading the model
model = load_model('dog_breed.h5')

# Name of Classes
BREEDS = ['Scottish Deerhound', 'Maltese Dog', 'Afgan Hound']

# Title of the app
st.title("Dog Breed Prediction")
st.markdown("Upload an image of the dog")

# Uploading input image (dog)
dog_image = st.file_uploader("Choose an image...", type="png")
submit = st.button('Predict')

# If the user clicks on submit, do this:
if submit:
    if dog_image is not None:

        # Convert the file to an opencv image
        file_bytes = np.asarray(bytearray(dog_image.read()), dtype=np.uint8)
        opencv_image = cv2.imdecode(file_bytes, 1)

        # Display the image
        st.image(opencv_image, channels="BGR")
        # Resizing the image
        opencv_image = cv2.resize(opencv_image, (224,224))
        # Convert image to 4 dimension
        opencv_image.shape = (1,224,224,3)

        try:
            # Make Prediction
            with st.spinner('Predicting...'):
                Y_pred = model.predict(opencv_image)
                st.title(f"The Dog Breed is :blue[{BREEDS[np.argmax(Y_pred)]}]")
            sys.stdout.flush()

        except Exception as e:
            st.error("An error occurred during prediction.")
            st.error(str(e))


    