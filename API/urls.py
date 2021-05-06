from flask import request, jsonify
from marshmallow.utils import EXCLUDE
from .models import Purchase, Product, User, PurchaseSchema, ProductSchema, UserSchema, check_None
from API import session, app, bcrypt

from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)

app.config['SECRET_KEY'] = '12345678'
jwt = JWTManager(app)


def exception_handler(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(e)

    # Renaming the function name:
    wrapper.__name__ = func.__name__
    return wrapper


@app.route("/product", methods=['POST'])
def product_add():
    data = request.get_json()
    try:
        product = ProductSchema(
            partial=("id", "name", "status", "amount", "is_bought")).load(data, unknown=EXCLUDE)
    except Exception:
        return jsonify({'message': "Invalid ID supplied"}), 400

    session.add(product)
    session.commit()

    return jsonify({'message': "Success"}), 200


@app.route("/product/<int:pk>", methods=['GET'])
def get_product(pk):
    try:
        product = check_None(Product, pk)
    except Exception:
        return jsonify({'message': "Product not found"}), 404

    return ProductSchema().dump(product)


@app.route("/product", methods=['GET'])
def get_products():
    try:
        products = ProductSchema()
    except Exception:
        return jsonify({'message': "Products not found"}), 404

    global_products = session.query(Product).order_by(Product.name).all()
    return jsonify(ProductSchema(many=True).dump(global_products))


@app.route("/product/<int:pk>", methods=['PUT'])
@exception_handler
def update_product(pk):
    data = request.get_json()
    try:
        check_None(Product, pk)
    except Exception:
        return jsonify({'message': "Product not found"}), 404

    session.query(Product).filter(Product.id == pk).update(data)
    session.commit()
    return jsonify({'message': "Success"}), 200


@app.route("/product/<int:pk>", methods=['DELETE'])
def delete_product(pk):
    try:
        product = check_None(Product, pk)
    except Exception:
        return jsonify({'message': "Product not found"}), 404
    if 777 == get_jwt_identity():
        session.delete(product)
        session.commit()
        return jsonify({'message': "Success"}), 200
    else:
        return jsonify({'message': "You have not access to delete products"}), 405


@app.route("/purchase", methods=['POST'])
def purchase_order():
    data = request.get_json()
    try:
        data['userID'] = get_jwt_identity()
        purchase = PurchaseSchema(
            partial=("id", "quantity", "userID", "shipDate", "complete", "status")).load(data, unknown=EXCLUDE)
    except Exception:
        return jsonify({'message': "Invalid id supplied"}), 400

    session.add(purchase)
    session.commit()

    return jsonify({'message': "Success"}), 200


@app.route("/purchase/<int:pk>", methods=['GET'])
def get_purchase(pk):
    pk = int(pk)
    try:
        purchase = check_None(Purchase, pk)
    except Exception:
        return jsonify({'message': "Purchase not found"}), 404
    return PurchaseSchema().dump(purchase)


@app.route("/purchase/<int:pk>", methods=['PUT'])
def update_purchase(pk):
    data = request.get_json()
    try:
        check_None(Purchase, pk)
    except Exception:
        return jsonify({'message': "Purchase not found"}), 404
    if session.query(Purchase).filter(Purchase.id == pk).filter(Purchase.userID == get_jwt_identity()):
        purchase_check = session.query(Purchase).filter(Purchase.id == pk).filter(Purchase.userID == get_jwt_identity())
        purchase_check.update(data)
        session.commit()
        return jsonify({'message': "Success"}), 200
    else:
        return jsonify({'message': "Not your purchase"}), 405


@app.route("/purchase/<int:pk>", methods=['DELETE'])
def cancel_purchase(pk):
    try:
        purchase = check_None(Purchase, pk)
    except Exception:
        return jsonify({'message': "Purchase not found"}), 404
    purchase_check = session.query(Purchase).filter(Purchase.id == pk).filter(Purchase.userID == get_jwt_identity())
    if purchase_check is not None:
        session.delete(purchase)
        session.commit()
        return jsonify({'message': "Success"}), 200
    else:
        return jsonify({'message': "Not your purchase"}), 200


@app.route("/user", methods=["POST"])
def user_add():
    data = request.get_json()
    try:
        user = UserSchema(partial=True).load(data, unknown=EXCLUDE)
    except Exception:
        return jsonify({'message': "Invalid data"}), 405

    session.add(user)
    session.commit()
    return jsonify({'message': "Success"}), 200


@app.route("/user/<int:pk>", methods=['GET'])
def get_user(pk):
    pk = int(pk)
    try:
        user = check_None(User, pk)
    except Exception:
        return jsonify({'message': "User not found"}), 404
    return UserSchema().dump(user), 200


@app.route("/user/<int:pk>", methods=['PUT'])
def update_user(pk):
    data = request.get_json()
    try:
        session.query(User).filter(User.id == pk).update(data)
        session.commit()
    except Exception:
        return jsonify({'message': "Commit was failed"}), 405

    return jsonify({'message': "Success"}), 200


@app.route("/user", methods=['DELETE'])
def delete_user():
    pk = get_jwt_identity()
    user = check_None(User, pk)
    session.delete(user)
    session.commit()
    return jsonify({'message': "Success"}), 200


@app.route("/user/login", methods=["POST"])
def user_login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'Login': "false"}), 400
    user = session.query(User).filter(User.email == email).one()

    if user.password == password:
        return jsonify(login="true"), 200

    return jsonify(login="false"), 400
