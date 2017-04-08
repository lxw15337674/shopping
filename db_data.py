from app import db
from app.models import User

# user= User('123','123'
# )
# db.session.add(user)
# db.session.commit()

admin = User.query.filter_by(name='123').first()
print(admin.name)