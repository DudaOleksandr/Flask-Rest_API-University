import requests, pytest
from API import *
from API.models import *

# session = Session()
test_app = app.test_client()
url = 'http://127.0.0.1:5000'

user_log = {'username': '5', 'password': '5'}


class TestClass:

    # @classmethod
    # def setup_class(cls):
    #     global session
    #     engine = create_engine('mysql+pymysql://root@127.0.0.1:3306/lab5')
    #     SessionFactory = sessionmaker(bind=engine)
    #     Session = scoped_session(SessionFactory)
    #     session = Session()

    def teardown_method(self, method):
        # try:
        session.query(Product).delete()
        session.query(Purchase).delete()
        session.query(User).delete()
        session.commit()
        # except Exception:
        #     engine = create_engine('mysql+pymysql://root@127.0.0.1:3306/lab5')
        #     SessionFactory = sessionmaker(bind=engine)
        #     Session = scoped_session(SessionFactory)
        #     session = Session()
        #     session.query(User).delete()
        #     session.query(Product).delete()
        #     session.query(Purchase).delete()
        #     session.commit()

    def login_user(self, user_lo):
        log = test_app.post('/user/login', json=user_lo)
        return log.json['access_token']

    def test_user_add(self):
        user = {'username': '5', 'password': '5'}
        response = test_app.post('/user', json=user)
        assert response.status_code == 200

    def test_user_add_invalid_data(self):
        user = {'username': '5', 'password': '5', 'email': 453}
        response = test_app.post('/user', json=user)
        assert response.status_code == 405

    def test_user_login_success(self):
        user = User(id=1, username='5', password='5')
        user.crypt()
        session.add(user)
        session.commit()
        user = {'username': '5', 'password': '5'}
        response = test_app.post('/user/login', json=user)
        assert response.status_code == 200

    def test_user_get(self):
        user = User(id=1, username='5', password='5')
        user.crypt()
        session.add(user)
        session.commit()
        response = test_app.get('/user', headers={'Authorization': f'Bearer {self.login_user(user_log)}'})
        assert response.status_code == 200

    def test_user_login_false(self):
        user = User(id=1, username='5', password='5')
        user.crypt()
        session.add(user)
        session.commit()
        user = {'username': '5', 'password': '232'}
        response = test_app.post('/user/login', json=user)
        assert response.status_code == 200

    def test_user_update_success(self):
        user = User(id=1, username='5', password='5')
        user.crypt()
        session.add(user)
        session.commit()
        user1 = {'email': '55'}
        response = test_app.put('/user', headers={'Authorization': f'Bearer {self.login_user(user_log)}'}, json=user1)
        assert response.status_code == 200

    def test_user_update_fail(self):
        user = User(id=999, username='Admin', password='1')
        user1 = User(id=1, username='5', password='5')
        user.crypt()
        user1.crypt()
        session.add(user)
        session.add(user1)
        session.commit()
        user1 = {'id': 999}
        response = test_app.put('/user', headers={'Authorization': f'Bearer {self.login_user(user_log)}'}, json=user1)
        assert response.status_code == 405

    def test_user_delete_success(self):
        user = User(id=1, username='5', password='5')
        user.crypt()
        session.add(user)
        session.commit()
        response = test_app.delete('/user', headers={'Authorization': f'Bearer {self.login_user(user_log)}'})
        assert response.status_code == 200

    ################################## PRODUCT ##################################

    def test_product_add(self):
        user = User(id=666, username='3445', password='345345')
        user.crypt()
        session.add(user)
        session.commit()
        user = {'username': user.username, 'password': '345345'}
        product = {'name': '23', 'amount': 123, 'is_bought': False,
                   "status": "32432"}
        k = self.login_user(user)
        response = test_app.post('/product', json=product, headers={'Authorization': f'Bearer {k}'})
        assert response.status_code == 200

    def test_product_add_405(self):
        user = User(id=1, username='3445', password='345345')
        user.crypt()
        session.add(user)
        session.commit()
        user = {'username': user.username, 'password': '345345'}
        product = {'name': '23', 'amount': 123, 'is_bought': False,
                   "status": "32432"}
        k = self.login_user(user)
        response = test_app.post('/product', json=product, headers={'Authorization': f'Bearer {k}'})
        assert response.status_code == 405

    def test_product_add_400(self):
        user = User(id=1, username='3445', password='345345')
        product = Product(id=1, name='2345')
        user.crypt()
        session.add(user)
        session.add(product)
        session.commit()
        user = {'username': user.username, 'password': '345345'}
        product = {'id': 'fgh', 'name': '23', 'amount': 123, 'is_bought': False,
                   "status": "32432"}
        k = self.login_user(user)
        response = test_app.post('/product', json=product, headers={'Authorization': f'Bearer {k}'})
        assert response.status_code == 400

    def test_product_add_405_commit(self):
        user = User(id=1, username='3445', password='345345')
        product = Product(id=666, name='2345')
        user.crypt()
        session.add(user)
        session.add(product)
        session.commit()
        user = {'username': user.username, 'password': '345345'}
        product = {'id': 666, 'name': '23', 'amount': 123, 'is_bought': False,
                   "status": "32432"}
        k = self.login_user(user)
        response = test_app.post('/product', json=product, headers={'Authorization': f'Bearer {k}'})
        assert response.status_code == 405

    def test_product_delete_success(self):
        product = Product(id=9, name='23', amount=123)
        user = User(id=777, username='3445', password='345345')
        user.crypt()
        session.add(product)
        session.add(user)
        session.commit()
        user = {'username': user.username, 'password': '345345'}
        product = {'name': '23', 'amount': 123, 'is_bought': False,
                   "status": "32432"}
        k = self.login_user(user)
        response = test_app.delete('/product/9', json=product, headers={'Authorization': f'Bearer {k}'})
        assert response.status_code == 200

    def test_product_delete_404(self):
        product = Product(id=7, name='23', amount=123)
        user = User(id=777, username='3445', password='345345')
        user.crypt()
        session.add(product)
        session.add(user)
        session.commit()
        user = {'username': user.username, 'password': '345345'}
        product = {'name': '23', 'amount': 123, 'is_bought': False,
                   "status": "32432"}
        k = self.login_user(user)
        response = test_app.delete('/product/9', json=product, headers={'Authorization': f'Bearer {k}'})
        assert response.status_code == 404

    def test_product_delete_405(self):
        product = Product(id=9, name='23', amount=123)
        user = User(id=3, username='3445', password='345345')
        user.crypt()
        session.add(product)
        session.add(user)
        session.commit()
        user = {'username': user.username, 'password': '345345'}
        product = {'name': '23', 'amount': 123, 'is_bought': False,
                   "status": "32432"}
        k = self.login_user(user)
        response = test_app.delete('/product/9', json=product, headers={'Authorization': f'Bearer {k}'})
        assert response.status_code == 405

    def test_product_get_200(self):
        product = Product(id=9, name='23', amount=123)
        user = User(id=777, username='3445', password='345345')
        user.crypt()
        session.add(product)
        session.add(user)
        session.commit()
        user = {'username': user.username, 'password': '345345'}
        product = {'name': '23', 'amount': 123, 'is_bought': False,
                   "status": "32432"}
        k = self.login_user(user)
        response = test_app.get('/product/9', json=product, headers={'Authorization': f'Bearer {k}'})
        assert response.status_code == 200

    def test_product_get_404(self):
        product = Product(id=7, name='23', amount=123)
        user = User(id=777, username='3445', password='345345')
        user.crypt()
        session.add(product)
        session.add(user)
        session.commit()
        user = {'username': user.username, 'password': '345345'}
        product = {'name': '23', 'amount': 123, 'is_bought': False,
                   "status": "32432"}
        k = self.login_user(user)
        response = test_app.get('/product/9', json=product, headers={'Authorization': f'Bearer {k}'})
        assert response.status_code == 404

    def test_product_put_200(self):
        product = Product(id=9, name='23', amount=123)
        user = User(id=777, username='3445', password='345345')
        user.crypt()
        session.add(product)
        session.add(user)
        session.commit()
        user = {'username': user.username, 'password': '345345'}
        product = {'name': '23', 'amount': 123, 'is_bought': False,
                   "status": "32432"}
        k = self.login_user(user)
        response = test_app.put('/product/9', json=product, headers={'Authorization': f'Bearer {k}'})
        assert response.status_code == 200

    def test_product_put_404(self):
        product = Product(id=7, name='23', amount=123)
        user = User(id=777, username='3445', password='345345')
        user.crypt()
        session.add(product)
        session.add(user)
        session.commit()
        user = {'username': user.username, 'password': '345345'}
        product = {'name': '23', 'amount': 123, 'is_bought': False,
                   "status": "32432"}
        k = self.login_user(user)
        response = test_app.put('/product/9', json=product, headers={'Authorization': f'Bearer {k}'})
        assert response.status_code == 404

    def test_product_put_405(self):
        product = Product(id=9, name='23', amount=123)
        user = User(id=3, username='3445', password='345345')
        user.crypt()
        session.add(product)
        session.add(user)
        session.commit()
        user = {'username': user.username, 'password': '345345'}
        product = {'name': '23', 'amount': 123, 'is_bought': False,
                   "status": "32432"}
        k = self.login_user(user)
        response = test_app.put('/product/9', json=product, headers={'Authorization': f'Bearer {k}'})
        assert response.status_code == 405

    ################################## PURCHASE ##################################
    def test_purchase_add_200(self):
        user = User(id=666, username='3445', password='345345')
        user.crypt()
        session.add(user)
        session.commit()
        user = {'username': user.username, 'password': '345345'}
        purchase = {'quantity': 23, 'shipDate': "123"}
        k = self.login_user(user)
        response = test_app.post('/purchase', json=purchase, headers={'Authorization': f'Bearer {k}'})
        assert response.status_code == 200

    def test_purchase_add_400(self):
        user = User(id=1, username='3445', password='345345')
        purchase = Purchase(id=123, quantity=23, shipDate='213', userID=1)
        user.crypt()
        session.add(user)
        session.add(purchase)
        session.commit()
        user = {'username': user.username, 'password': '345345'}
        purchase = {'id': 'vbcv', 'quantity': 23, 'shipDate': "123"}
        k = self.login_user(user)
        response = test_app.post('/purchase', json=purchase, headers={'Authorization': f'Bearer {k}'})
        assert response.status_code == 400

    def test_purchase_get_200(self):
        purchase = Purchase(id=9, quantity=1, userID=777, shipDate='24:23:56', complete=False, status='123')
        user = User(id=777, username='3445', password='345345')
        user.crypt()
        session.add(purchase)
        session.add(user)
        session.commit()
        user = {'username': user.username, 'password': '345345'}
        purchase = {'name': '23', 'amount': 123, 'is_bought': False,
                    "status": "32432"}
        k = self.login_user(user)
        response = test_app.get('/purchase/9', json=purchase, headers={'Authorization': f'Bearer {k}'})
        assert response.status_code == 200

    def test_purchase_get_404(self):
        purchase = Purchase(id=7, quantity=1, userID=777, shipDate='24:23:56', complete=False, status='123')
        user = User(id=777, username='3445', password='345345')
        user.crypt()
        session.add(purchase)
        session.add(user)
        session.commit()
        user = {'username': user.username, 'password': '345345'}
        purchase = {'name': '23', 'amount': 123, 'is_bought': False,
                    "status": "32432"}
        k = self.login_user(user)
        response = test_app.get('/purchase/9', json=purchase, headers={'Authorization': f'Bearer {k}'})
        assert response.status_code == 404

    def test_purchase_put_200(self):
        purchase = Purchase(id=9, quantity=1, userID=777, shipDate='24:23:56', complete=False, status='123')
        user = User(id=777, username='3445', password='345345')
        user.crypt()
        session.add(purchase)
        session.add(user)
        session.commit()
        user = {'username': user.username, 'password': '345345'}
        purchase = {'shipDate': '23'}
        k = self.login_user(user)
        response = test_app.put('/purchase/9', json=purchase, headers={'Authorization': f'Bearer {k}'})
        assert response.status_code == 200

    def test_purchase_put_404(self):
        purchase = Purchase(id=7, quantity=1, userID=777, shipDate='24:23:56', complete=False, status='123')
        user = User(id=777, username='3445', password='345345')
        user.crypt()
        session.add(purchase)
        session.add(user)
        session.commit()
        user = {'username': user.username, 'password': '345345'}
        purchase = {'shipDate': '23'}
        k = self.login_user(user)
        response = test_app.put('/purchase/9', json=purchase, headers={'Authorization': f'Bearer {k}'})
        assert response.status_code == 404

    # def test_purchase_put_405(self):
    #     purchase = Purchase(id=9, userID=1, quantity=1, shipDate='24:23:56', complete=False, status='123')
    #     user = User(id=3, username='3445', password='345345')
    #     user.crypt()
    #     session.add(purchase)
    #     session.add(user)
    #     session.commit()
    #     user = {'username': user.username, 'password': '345345'}
    #     purchase = {'shipDate': '23'}
    #     k = self.login_user(user)
    #     response = test_app.put('/purchase/9', json=purchase, headers={'Authorization': f'Bearer {k}'})
    #     assert response.status_code == 405

    def test_purchase_delete_success(self):
        purchase = Purchase(id=9, userID=1, quantity=1, shipDate='24:23:56', complete=False, status='123')
        user = User(id=777, username='3445', password='345345')
        user.crypt()
        session.add(purchase)
        session.add(user)
        session.commit()
        user = {'username': user.username, 'password': '345345'}
        purchase = {'name': '23', 'amount': 123, 'is_bought': False,
                   "status": "32432"}
        k = self.login_user(user)
        response = test_app.delete('/purchase/9', json=purchase, headers={'Authorization': f'Bearer {k}'})
        assert response.status_code == 200

    def test_purchase_delete_404(self):
        purchase = Purchase(id=7, userID=1, quantity=1, shipDate='24:23:56', complete=False, status='123')
        user = User(id=777, username='3445', password='345345')
        user.crypt()
        session.add(purchase)
        session.add(user)
        session.commit()
        user = {'username': user.username, 'password': '345345'}
        purchase = {'name': '23', 'amount': 123, 'is_bought': False,
                   "status": "32432"}
        k = self.login_user(user)
        response = test_app.delete('/purchase/9', json=purchase, headers={'Authorization': f'Bearer {k}'})
        assert response.status_code == 404

    # def test_purchase_delete_405(self):
    #     purchase = Purchase(id=9, userID=1, quantity=1, shipDate='24:23:56', complete=False, status='123')
    #     user = User(id=3, username='3445', password='345345')
    #     user.crypt()
    #     session.add(purchase)
    #     session.add(user)
    #     session.commit()
    #     user = {'username': user.username, 'password': '345345'}
    #     purchase = {'name': '23', 'amount': 123, 'is_bought': False,
    #                "status": "32432"}
    #     k = self.login_user(user)
    #     response = test_app.delete('/purchase/9', json=purchase, headers={'Authorization': f'Bearer {k}'})
    #     assert response.status_code == 405
