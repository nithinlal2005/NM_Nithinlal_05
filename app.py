from flask import Flask, request, render_template
import numpy as np
import pickle
import os

app = Flask(__name__)

# ---- Load trained model ----
# Replace 'model.pkl' with your trained model file if available.
# For now, let's use a dummy model for demonstration.

class DummyModel:
    def predict(self, X):
        # Rule: if Amount > 1000 or V1 < -3, flag as fraud
        return [1 if (row[5] > 1000 or row[0] < -3) else 0 for row in X]

# Uncomment below to load actual model
# with open('model.pkl', 'rb') as f:
#     model = pickle.load(f)

model = DummyModel()

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        try:
            # Get form data
            v1 = float(request.form['V1'])
            v2 = float(request.form['V2'])
            v3 = float(request.form['V3'])
            v4 = float(request.form['V4'])
            v5 = float(request.form['V5'])
            amount = float(request.form['Amount'])

            # Prepare data for model
            input_data = np.array([[v1, v2, v3, v4, v5, amount]])
            prediction = model.predict(input_data)[0]

            if prediction == 1:
                result = "⚠️ Fraudulent Transaction Detected!"
            else:
                result = "✅ Legitimate Transaction"

        except Exception as e:
            result = f"Error: {str(e)}"

    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
