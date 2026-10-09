### Handwritten Character Recognition Using CNN



##### **Project Overview**



This project uses a Convolutional Neural Network (CNN) to recognize handwritten digits from images. The application provides a simple web interface where users can submit a handwritten digit image and receive a prediction with a confidence score.



**Features**



* Handwritten digit image upload
* CNN-based digit prediction
* Prediction confidence display
* ##### Web interface built with Flask
* Image preprocessing before prediction



##### **Technologies Used**



Python

TensorFlow / Keras

CNN (Convolutional Neural Network)

Flask

NumPy

Pillow (PIL)



##### **Project Structure**



* app.py — Flask application and prediction logic
* templates — HTML templates for the web interface
* requirements.txt — Python dependencies
* Trained model file — saved CNN model used for prediction



##### **Installation and Setup**



1\. Install Python on your computer.



2\. Download or clone this repository.



3\. Open a terminal in the project directory.



4\. Create and activate a virtual environment.



5\. Install the required libraries:



&#x20;  'pip install -r requirements.txt`



6\. Ensure that the trained model file is present at the path expected by `app.py`.



7\. Start the Flask application:



&#x20;  `python app.py`



8\. Open the local URL shown in the terminal in your web browser.



##### **How to Use**



1\. Open the web application.

2\. Upload an image containing a handwritten digit.

3\. Submit the image for prediction.

4\. View the predicted digit and confidence score.



##### **Model**



The application uses a trained CNN model. The model processes the input image and predicts the most likely digit class.



##### **Internship Project**



Prepared as part of the CodeAlpha Machine Learning Internship.



##### **Disclaimer**



Predictions depend on image quality and preprocessing. The confidence score is a model output and should not be interpreted as a guarantee of correctness.



