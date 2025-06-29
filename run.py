from app import create_app
from app.extensions import db  # ✅ from extensions
from app.models import User


app = create_app()

with app.app_context():
    db.create_all()
    # 🚨 Reset sessions on every restart
    users = User.query.all()
    for u in users:
        u.is_active_session = False
    db.session.commit()

if __name__ == '__main__':
    app.run(debug=True)