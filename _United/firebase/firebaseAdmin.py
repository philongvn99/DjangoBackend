# pylint: disable=C0103
import firebase_admin as fa

from _United import settings

if not fa.get_app():
    cred = fa.credentials.Certificate(settings.FIREBASE_CONFIG_FILE)
    djangoFirebaseAdmin = fa.initialize_app(cred)
    print("Firebase Admin Initialized")
