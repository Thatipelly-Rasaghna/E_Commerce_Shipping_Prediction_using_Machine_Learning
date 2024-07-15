import pickle as pkl
from flask import Flask, request, render_template

app = Flask(__name__)

# Load the models
model = pkl.load(open('mode.pkl', 'rb'))
sc = pkl.load(open("norm.pkl", 'rb'))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/prediction')
def predict():
    return render_template('prediction.html')

@app.route('/output', methods=['GET', 'POST'])
def output():
    if request.method == 'POST':
        # Get form data
        Warehouse_block = request.form.get("Warehouse_block", "")
        Mode_of_Shipment = request.form.get("Mode_of_Shipment", "")
        Customer_care_calls = request.form.get("Customer_care_calls", 0, type=int)
        Customer_rating = request.form.get("Customer_rating", 0, type=int)
        Cost_of_the_Product = request.form.get("Cost_of_the_Product", 0, type=float)
        Prior_purchases = request.form.get("Prior_purchases", 0, type=int)
        Product_importance = request.form.get('Product_importance', "")
        Gender = request.form.get('Gender', "")
        Discount_offered = request.form.get("Discount_offered", 0, type=float)
        Weight_in_gms = request.form.get("Weight_in_gms", 0, type=float)

        # Convert categorical data
        warehouse_mapping = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'F': 4}
        shipment_mapping = {'Flight': 0, 'Road': 1, 'Ship': 2}
        importance_mapping = {'high': 0, 'low': 1, 'medium': 2}
        gender_mapping = {'F': 0, 'M': 1}

        Warehouse_block = warehouse_mapping.get(Warehouse_block, -1)
        Mode_of_Shipment = shipment_mapping.get(Mode_of_Shipment, -1)
        Product_importance = importance_mapping.get(Product_importance, -1)
        Gender = gender_mapping.get(Gender, -1)

        # Form the input array for the model
        total = [[Warehouse_block, Mode_of_Shipment, Customer_care_calls, Customer_rating, Cost_of_the_Product, Prior_purchases, Product_importance, Gender, Discount_offered, Weight_in_gms]]
        
        # Make the prediction
        try:
            Pred = model.predict(sc.transform(total))
            xx = Pred[0]
            if int(xx) == 0:
                xx = " Not Reached on time delivery"
            else:
                xx = "Reached on time delivery"
            return render_template('output.html', xx=xx)
        except Exception as e:
            return str(e)
    return render_template('prediction.html')

if __name__ == '__main__':
    app.run(debug=True, port=3000)
