from app import db
from app.models import User, Fruits

# user = User(name='123', password='123')
# user1 = User(name='666', password='666')
# db.session.add(user)
# db.session.add(user1)


fruit = Fruits(name='西瓜',
               introduction='这是西瓜的介绍',
               price='2')
fruit1 = Fruits(name='香蕉',
               introduction='这是香蕉的介绍',
               price='1')
db.session.add(fruit)
db.session.add(fruit1)

db.session.commit()