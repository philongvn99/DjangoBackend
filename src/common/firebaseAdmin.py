# pylint: disable=C0103
from _United import settings
import firebase_admin
from firebase_admin import credentials


cred = credentials.Certificate(settings.FIREBASE_CONFIG_FILE)

djangoFirebaseAdmin = firebase_admin.initialize_app(cred)
