import pymysql
from flask import Flask, request, jsonify, json
conn = pymysql.connect(host = "sneaker-database-new.c16sew4oi8yj.us-east-1.rds.amazonaws.com", user = "varun", password = "TimAWS98021")
cursor = conn.cursor()
app = Flask(__name__)

@app.route('/check-availability/<product_name>/<color>/<size>')
def check_availability(product_name, color, size):
    filteredProducts = []
    cursor.execute("SELECT model, color, size, quantity_available FROM sneaker_database.product_inventory WHERE model = " + "\'" + product_name + "\'" + " AND color = " + "\'" + color + "\'" + " AND size = " + str(size) + "AND quantity_available > " + str(0))
    for row in cursor :
        filteredProducts.append(row)
    if((len(filteredProducts) > 0)):
        with app.app_context():
            return jsonify({"Available" : True}), 200
    else:
        with app.app_context():
            return jsonify({"Available" : False}), 200

#prods = check_availability('Nike Air Force 1', 'White', 6.0)
#print(prods)
        
@app.route('/check-colors/<product_name>/<size>')
def check_colors(product_name, size):
    filteredProducts = []
    stringConversion = ""
    cursor.execute("SELECT color FROM sneaker_database.product_inventory WHERE model = " + "\'" + product_name + "\'" "AND size = " + str(size) + "AND quantity_available > " + str(0))
    for row in cursor :
        stringConversion = str(row)
        stringConversion = stringConversion[2:len(stringConversion)-3]
        filteredProducts.append(stringConversion)
    with app.app_context():
        return jsonify(filteredProducts), 200

#prods3 = check_colors('Nike Air Force 1', 7.0)
#print(prods3)

@app.route('/check-sizes/<product_name>/<color>')
def check_sizes(product_name, color):
    filteredProducts = []
    stringConversion = ""
    cursor.execute("SELECT size FROM sneaker_database.product_inventory WHERE model = " + "\'" + product_name + "\'" + " AND color = " + "\'" + color + "\'" + "AND quantity_available  > " + str(0))
    for row in cursor :
        stringConversion = str(row)
        stringConversion = stringConversion[1:len(stringConversion)-2]
        stringValue = stringConversion[stringConversion.find("(")+2:stringConversion.find(")")-1]
        filteredProducts.append((float(stringValue)))
    with app.app_context():   
        return jsonify(filteredProducts),200
    
#prods2 = check_sizes('Nike Air Force 1', 'White')
#print(prods2)
    
@app.route('/check-products/<size>')
def check_products(size):
    filteredProducts = []
    stringConversion = ""
    cursor.execute("SELECT model, color FROM  sneaker_database.product_inventory WHERE size = " + str(size) + " AND quantity_available  > " + str(0))
    for row in cursor :
        stringConversion = str(row)
        formattedRow = stringConversion[2:len(stringConversion)-1]
        product = formattedRow.partition(",")[0]
        color = formattedRow.partition(",")[2]
        color = color[2:len(color)-1]
        filteredProducts.append(product[0:len(product)-1] + " in " + color)
    return filteredProducts

print(check_products(7.5))

if (__name__) == "__main__":
    app.run(debug = True)
