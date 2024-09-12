import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))

load_dotenv()
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI=os.environ.get('DATABASE_URI') or 'sqlite:///' + os.path.join(basedir,'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    FLASK_DEBUG = True
    FLASK_ENV = 'development'

    # Admin config
    # Fluid layout True or False
    FLASK_ADMIN_FLUID_LAYOUT = True
    # Set the theme name
    FLASK_ADMIN_SWATCH = 'flatly'

    # Stripe config
    STRIPE_PUBLIC_KEY = os.getenv("STRIPE_PUBLIC_KEY")
    STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")
