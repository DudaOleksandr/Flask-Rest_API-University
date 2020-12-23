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

# product routes

@app.route("/product", methods=['POST'])
@jwt_required
def product_add():
    data = request.get_json()

    try:
        product = ProductSchema(
            partial=("id", "name", "status", "amount", "is_bought")).load(data, unknown=EXCLUDE)
    except Exception:
        return jsonify({'message': "Invalid ID "}), 400

    try:
        session.add(product)
        session.commit()
    except Exception:
        return jsonify({'message': "Commit was failed"}), 405

    return jsonify({'message': "Success"}), 200


@app.route("/product/<int:pk>", methods=['GET'])
@jwt_required
def get_product(pk):
    try:
        pk = int(pk)
    except ValueError:
        return jsonify({'message': "Invalid ID "}), 400

    try:
        product = check_None(Product, pk)
    except Exception:
        return jsonify({'message': "Product not found"}), 404

    return ProductSchema().dump(product)


@app.route("/product/<int:pk>", methods=['PUT'])
@jwt_required
def update_product(pk):
    data = request.get_json()
    try:
        pk = int(pk)
    except ValueError:
        return "Invalid ID ", 400

    try:
        product = check_None(Product, pk)
    except Exception:
        return jsonify({'message': "Product not found"}), 404

    session.query(Product).filter(Product.id == pk).update(data)
    session.commit()

    return jsonify({'message': "Success"}), 200


@app.route("/product/<int:pk>", methods=['DELETE'])
@jwt_required
def delete_product(pk):
    try:
        pk = int(pk)
    except ValueError:
        return "Invalid ID ", 400

    try:
        product = check_None(Product, pk)
    except Exception:
        return jsonify({'message': "Product not found"}), 404

    session.delete(product)
    session.commit()
    return jsonify({'message': "Success"}), 200


# purchase

@app.route("/purchase", methods=['POST'])
@jwt_required
def purchase_order():
    data = request.get_json()

    try:
        purchase = PurchaseSchema(
            partial=("id", "quantity", "userID", "shipDate", "complete", "status")).load(data, unknown=EXCLUDE)
    except Exception:
        return jsonify({'message': "Invalid ID "}), 400

    try:
        session.add(purchase)
        session.commit()
    except Exception:
        return jsonify({'message': "Commit was failed"}), 405

    return jsonify({'message': "Success"}), 200


@app.route("/purchase/<int:pk>", methods=['GET'])
@jwt_required
def get_purchase(pk):
    try:
        pk = int(pk)
    except ValueError:
        return jsonify({'message': "Invalid ID "}), 400

    try:
        purchase = check_None(Purchase, pk)
    except Exception:
        return jsonify({'message': "Product not found"}), 404

    return PurchaseSchema().dump(purchase)


@app.route("/purchase/<int:pk>", methods=['PUT'])
@jwt_required
def update_purchase(pk):
    data = request.get_json()
    try:
        pk = int(pk)
    except ValueError:
        return "Invalid ID ", 400

    try:
        check_None(Purchase, pk)
    except Exception:
        return jsonify({'message': "Product not found"}), 404

    session.query(Purchase).filter(Purchase.id == pk).update(data)
    session.commit()

    return jsonify({'message': "Success"}), 200


@app.route("/purchase/<int:pk>", methods=['DELETE'])
@jwt_required
def cancel_purchase(pk):
    try:
        pk = int(pk)
    except ValueError:
        return "Invalid ID ", 400

    try:
        purchase = check_None(Purchase, pk)
    except Exception:
        return jsonify({'message': "Purchase not found"}), 404

    session.delete(purchase)
    session.commit()
    return jsonify({'message': "Success"}), 200


# user

@app.route("/user", methods=["POST"])
def user_add():
    data = request.get_json()
    try:
        data['password'] = bcrypt.generate_password_hash(
            data['password']).decode('utf-8')
        print(data['password'])
        user = UserSchema(partial=True).load(data, unknown=EXCLUDE)
    except Exception:
        return jsonify({'message': "Invalid input"}), 405

    try:
        session.add(user)
        session.commit()
    except Exception:
        return jsonify({'message': "Commit was failed"}), 405

    return jsonify({'message': "Success"}), 200


@app.route("/user/<int:pk>", methods=['GET'])
@jwt_required
def get_user(pk):
    try:
        pk = int(pk)
    except ValueError:
        return jsonify({'message': "Invalid ID "}), 400

    try:
        user = check_None(User, pk)
    except Exception:
        return jsonify({'message': "User not found"}), 404

    return UserSchema().dump(user)


@app.route("/user/<int:pk>", methods=['PUT'])
@jwt_required
def update_user(pk):
    data = request.get_json()
    try:
        pk = int(pk)
    except ValueError:
        return "Invalid ID ", 400

    try:
        check_None(User, pk)
    except Exception:
        return jsonify({'message': "Product not found"}), 404

    session.query(User).filter(User.id == pk).update(data)
    session.commit()

    return jsonify({'message': "Success"}), 200


@app.route("/user/<int:pk>", methods=['DELETE'])
@jwt_required
def delete_user(pk):
    try:
        pk = int(pk)
    except ValueError:
        return "Invalid ID ", 400

    try:
        user = check_None(User, pk)
    except Exception:
        return jsonify({'message': "User not found"}), 404

    session.delete(user)
    session.commit()
    return jsonify({'message': "Success"}), 200


@app.route("/user/login", methods=["POST"])
def user_login():
    data = request.get_json()
    try:
        username = data['username']
        password = str(data['password'])
    except Exception:
        return jsonify({'message': "Invalid input"}), 405

    user = session.query(User).filter(User.username == username).one()
    login_check = bcrypt.check_password_hash(user.password, password)
    if login_check:
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token), 200
    return jsonify({'Login': login_check}), 200


@app.route("/user/logout", methods=["GET"])
@jwt_required
def user_logout():
    return jsonify({'message': "Success"}), 200
