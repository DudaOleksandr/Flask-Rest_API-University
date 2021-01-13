from API import Session
from API.models import *

session = Session()


# purchase = Purchase(id=1, quantity=1, userID=1, shipDate='24:23:56', complete=False, status='123')
#
# purchase1 = Purchase(id=2, quantity=1, userID=1, shipDate='24:23:56', complete=False, status='123')
#
# purchase2 = Purchase(id=3, quantity=2, userID=2, shipDate='24:23:56', complete=False, status='123')
#
# product = Product(id=1, name='123', status='123', amount=8, is_bought=False, purchase_r=purchase)
#
# product1 = Product(name='Pet', status='test', amount=8, is_bought=False, purchase_r=purchase1)
#
# product2 = Product(name='Pet', status='test', amount=8, is_bought=False, purchase_r=purchase2)

user = User(id=1, username='Admin', email='1', password='1', user_status='123', status='123')

user1 = User(id=2, username='Test', email='test.test@gamil.com', password='testtest', user_status='123', status='123')


session.add(user)
session.add(user1)
# session.add(purchase)
# session.add(purchase1)
# session.add(purchase2)
#
# session.add(product)
# session.add(product1)
# session.add(product2)

session.commit()
session.query(User).delete()
session.commit()
