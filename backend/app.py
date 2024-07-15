from flask import Flask, request
from flask import jsonify
import json
from flask_cors import CORS

from db_control import crud, mymodels

import requests

# Azure Database for MySQL
# REST APIでありCRUDを持っている
app = Flask(__name__)
CORS(app)
 

@app.route("/")
def index():
    return "<p>Flask top page!</p>"
 
@app.route("/customers", methods=['POST'])
def create_customer():
    values = request.get_json()
    # values = {
    #     "customer_id": "C005",
    #     "customer_name": "佐藤Aこ",
    #     "age": 64,
    #     "gender": "女"
    # }

    # バリデーション: 必須フィールドのチェック
    if not values.get("customer_name") or not values.get("customer_id") or not values.get("age") or not values.get("gender"):
        return jsonify({"error": "All fields are required"}), 400

    tmp = crud.myinsert(mymodels.Customers, values)
    result = crud.myselect(mymodels.Customers, values.get("customer_id"))
    return result, 200

@app.route("/customers", methods=['GET'])
def read_one_customer():
    model = mymodels.Customers
    target_id = request.args.get('customer_id') #クエリパラメータ
    result = crud.myselect(mymodels.Customers, target_id)
    return result, 200

@app.route("/allcustomers", methods=['GET'])
def read_all_customer():
    model = mymodels.Customers
    result = crud.myselectAll(mymodels.Customers)
    return result, 200

@app.route("/customers", methods=['PUT'])
def update_customer():
    print("I'm in")
    values = request.get_json()
    values_original = values.copy()
    model = mymodels.Customers
    # values = {  "customer_id": "C004",
    #             "customer_name": "鈴木C子",
    #             "age": 44,
    #             "gender": "男"}

    # バリデーション: 必須フィールドのチェック
    if not values.get("customer_id"):
        return jsonify({"error": "customer_id is required"}), 400
    
    tmp = crud.myupdate(model, values)
    result = crud.myselect(mymodels.Customers, values_original.get("customer_id"))
    return result, 200

@app.route("/customers", methods=['DELETE'])
def delete_customer():
    model = mymodels.Customers
    target_id = request.args.get('customer_id') #クエリパラメータ

    #バリデーション？
    if not target_id:
        return jsonify({"error": "customer_id is required"}), 400
    
    result = crud.mydelete(model, target_id)
    return result, 200

@app.route("/fetchtest")
def fetchtest():
    response = requests.get('https://jsonplaceholder.typicode.com/users')
    return response.json(), 200

#??GPT指示
if __name__ == "__main__":
    app.run(debug=True)