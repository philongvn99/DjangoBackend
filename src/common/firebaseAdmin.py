# pylint: disable=C0103
import firebase_admin as fa
from _United import settings

cred = fa.credentials.Certificate(settings.FIREBASE_CONFIG_FILE)

djangoFirebaseAdmin = fa.initialize_app(cred)
