from datetime import datetime

from passlib.apps import custom_app_context as pwd_context

from app import auth, db


class User(db.Model):
    """This class implements User model. It act as a proxy to interact with users table in database
        
        :param username: Unique alphanumeric username
        :type username: str
        :param password: Plain password
        :type password: str
        
    """
    __tablename__ = 'users'

    #: Unique id given to user at the timem of account creation
    id = db.Column(db.Integer, primary_key=True)
    #: Unique alphanumeric username
    username = db.Column(db.String(32), index=True, unique=True)
    #: Hashed passwomrd
    password = db.Column(db.String(128))
    #: Datetime when user created account
    registered_on = db.Column(db.DateTime,
                              nullable=False,
                              default=datetime.utcnow)

    def __init__(self, username: str, password: str):
        self.username = username
        self.password = self.hash_password(password)
        self.registered_on = datetime.utcnow()

    def hash_password(self, password):
        """Generates hash of plain password before storing into database

        :param password: Plain password
        :type password: str
        :return: Hashed password
        :rtype: str
        """
        return pwd_context.hash(password)

    @staticmethod
    @auth.verify_password
    def verify_password(username, password):
        """Verfies whether password given by user is valid

        :param username: Unique alphanumeric username
        :type username: str
        :param password: Plain password
        :type password: str
        :return: Whether the password is valid for given user
        :rtype: bool
        """
        user = User.query.filter_by(username=username).first()
        if not user or not pwd_context.verify(password, user.password):
            return False
        return True
