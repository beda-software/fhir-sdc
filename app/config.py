import pytz
import os

app_superadmin_email = os.environ.get(
    'APP_SUPERADMIN_EMAIL', 'admin@health-samurai.io')
app_superadmin_password = os.environ.get('APP_SUPERADMIN_PASSWORD',
                                         os.environ.get('AIDBOX_ADMIN_PASSWORD'))

secret_key = os.environ.get('SECRET_KEY', '').encode()
local_tz = pytz.timezone(os.environ.get('LOCAL_TZ', 'US/Central'))

from_email = os.environ.get('FROM_EMAIL', 'donotreply@example.com')

frontend_url = os.environ.get('FRONTEND_URL', 'http://localhost:3000')
backend_public_url = os.environ.get('BACKEND_PUBLIC_URL', 'http://localhost:8080')

gc_bucket = os.environ.get('BUCKET', '')
gc_account_file = os.environ.get('BUCKET_ACCOUNT_PATH', '') or \
                  os.environ.get('GOOGLE_APPLICATION_CREDENTIALS', '')


google_oauth_app_id = os.environ.get('GOOGLE_OAUTH_APP_ID')
google_oauth_app_secret = os.environ.get('GOOGLE_OAUTH_APP_SECRET')

root_dir = os.path.dirname(os.path.abspath(__name__))
