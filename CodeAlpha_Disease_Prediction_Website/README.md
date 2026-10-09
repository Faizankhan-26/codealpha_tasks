

### &#x20;          **Disease Prediction from Medical Data Using Machine Learning**



##### &#x20;**Project Overview**



The Disease Prediction from Medical Data project is a machine learning-based web application designed to demonstrate how classification algorithms can analyze medical input data and generate prediction results.



The application provides a simple, user-friendly interface where users can enter medical parameters and view the model's prediction along with its confidence score.



This project was developed as part of a machine learning project portfolio to demonstrate the integration of a trained machine learning model with a Flask-based web application.



##### **Objectives**



* &#x20;Apply machine learning techniques to medical data classification.
* &#x20;Integrate a trained machine learning model into a web application.
* &#x20;Provide an accessible interface for entering medical parameters.
* &#x20;Display prediction results and model confidence.
* &#x20;Demonstrate the practical use of Python, Flask, and Scikit-learn.



##### &#x20;**Key Features**



* User-Friendly Interface: A simple web form for entering medical parameters.
* Machine Learning Integration: Uses a trained classification model to generate predictions.
* Prediction Results: Displays the output based on the provided input data.
* Confidence Score: Presents the model's confidence score where supported by the application.
* Web-Based Access: Runs through a browser using a Flask backend.
* Responsive Design: Provides a clean interface designed for convenient use across different screen sizes.



##### **Technologies Used**



* Programming Language: Python
* Web Framework: Flask
* Machine Learning:  Scikit-learn
* Data Processing: NumPy and Pandas, where used
* Model Serialization: Pickle / Joblib, depending on the saved model format
* Frontend: HTML and CSS



##### **Project Structure**



Disease\_Prediction\_Website



* &#x20;app.py
* &#x20;best\_disease\_prediction\_model.pkl
* &#x20;disease\_prediction\_scaler.pkl
* &#x20;requirements.txt
* &#x20;README.md
* &#x20;templates

&#x20;        index.html



* &#x20;static

&#x20;         style.css





##### &#x20;**Installation and Setup**



Prerequisites



&#x20;Python 3.10 or another Python version compatible with the project's dependencies

&#x20;pip package manager

&#x20;Git (optional, for cloning the repository)



&#x20;Step 1: Clone the Repository



bash

git clone YOUR\_GITHUB\_REPOSITORY\_URL

cd Disease\_Prediction\_Website





Step 2: Create a Virtual Environment



bash

python -m venv venv





Activate it on Windows:



bash

venv\\Scripts\\activate



&#x20;Step 3: Install Dependencies



bash

pip install -r requirements.txt





Step 4: Run the Application



bash

python app.py





Step 5: Open the Website



Open the following address in your browser:



text

http://127.0.0.1:5000/





The application should be running locally while the Flask server remains active.



##### **Machine Learning Workflow**



1\. Collect and prepare the medical input data.

2\. Process the input features in the format expected by the trained model.

3\. Apply the saved preprocessing scaler, if required.

4\. Pass the processed data to the trained classification model.

5\. Generate a prediction and display the result through the web interface.



##### **Limitations**



* &#x20;Prediction quality depends on the training data, preprocessing steps, and model performance.
* &#x20;Results may not generalize to every individual or medical setting.
* &#x20;A confidence score should not be interpreted as the probability that a person has or does not have a disease unless the model has been appropriately calibrated and validated.



##### &#x20;**Medical Disclaimer**



This application is intended for educational and demonstration purposes only.It is not a medical diagnostic tool and must not be used to make medical decisions. Always consult a qualified healthcare professional for medical evaluation and diagnosis.





