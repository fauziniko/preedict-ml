from flask import Flask, request, jsonify
import tensorflow as tf
import numpy as np

# Load pre-trained model
model = tf.keras.models.load_model('model/calories_fitbit_model_optmz.h5')

# Initialize Flask app
app = Flask(__name__)

# Configurable feature keys
REQUIRED_KEYS = ['calories', 'sugar', 'fat', 'salt']

def validate_input(data):
    """
    Validate the input JSON payload to ensure it contains the required keys
    and each key has a list of 7 numerical values.
    """
    if not isinstance(data, dict):
        return "Input data must be a JSON object.", False

    for key in REQUIRED_KEYS:
        if key not in data:
            return f"Missing required key: {key}.", False
        if not isinstance(data[key], list):
            return f"Key '{key}' must be a list.", False
        if len(data[key]) != 7:
            return f"List for '{key}' must contain exactly 7 elements.", False
        if not all(isinstance(i, (int, float)) for i in data[key]):
            return f"All elements in '{key}' must be numbers.", False

    return None, True

@app.route('/predict', methods=['POST'])
def predict():
    """
    Endpoint to predict calories based on input data.
    """
    try:
        # Parse input JSON
        data = request.get_json()

        # Validate input
        error_message, is_valid = validate_input(data)
        if not is_valid:
            return jsonify({'error': error_message}), 400

        # Prepare input data for prediction
        input_data = np.array([data[key] for key in REQUIRED_KEYS]).T  # Shape (7, 4)
        input_data = input_data[:, 0].reshape((1, 7, 1))  # Select 'calories' and reshape

        # Perform prediction
        prediction = model.predict(input_data)
        predicted_value = int(prediction[0][0])

        # Return JSON response
        response = {
            'predicted_calories': predicted_value
        }
        return jsonify(response)

    except Exception as e:
        return jsonify({'error': f"An error occurred: {str(e)}"}), 500

# Run the Flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
