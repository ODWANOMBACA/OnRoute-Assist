from myapp import db

class AssistanceRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    location = db.Column(db.String(255))
    assistance_type = db.Column(db.String(64))
    status = db.Column(db.String(64))
    # Add more fields as needed
