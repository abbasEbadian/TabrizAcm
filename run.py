from pcpc import app
from pcpc import db
from pcpc import bcrypt
from pcpc.models import User
import sys
if __name__ == "__main__":
    if sys.argv[-1] == "recreate_database":
        db.drop_all()
        db.create_all()
        admin = User(name="ادمین", identifier="admin", user_type="admin", password=bcrypt.generate_password_hash("admin"))
        db.session.add_all([admin])
        db.session.commit()
    app.run(debug=True, use_reloader=True)
