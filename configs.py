import os 

HUBSPOT_API_KEY_DEFAULT = "demo"
HUBSPOT_API_KEY = os.environ.get('HUBSPOT_API_KEY', HUBSPOT_API_KEY_DEFAULT)
HUBSPOT_RECENTLY_UPDATED_CONTACTS_URL = f"https://api.hubapi.com/contacts/v1/lists/recently_updated/contacts/recent"
RECENT_UPDATED_CONTACT_COUNT_PER_PAGE = os.environ.get('RECENT_UPDATED_CONTACT_COUNT_PER_PAGE', 100)

OUTPUT_PROPERTIES_FILE = os.environ.get('OUTPUT_PROPERTIES_FILE', 'results/properties.csv')
OUTPUT_FORM_SUBMISSIONS_FILE = os.environ.get('OUTPUT_FORM_SUBMISSIONS_FILE', 'results/form_submissions.csv')
OUTPUT_OTHER_FIELDS_FILE = os.environ.get('OUTPUT_OTHER_FIELDS_FILE', 'results/other_fields.csv')

DEBUG = os.environ.get('DEBUG', False)    
LOG_FILE = os.environ.get('LOG_FILE', 'logs/hubspot_etl.log')

DEFAULT_FORMAT_FILE = "[%(asctime)s][%(threadName)-32s][%(thread)-32s][%(name)-15s][%(levelname)-6s]  %(message)s " \
        "(%(filename)s:%(lineno)d) "
DEFAULT_FORMAT = "[%(threadName)-15s][%(thread)-32s][$BOLD%(name)-32s$RESET][%(levelname)-6s]  %(message)s " \
        "($BOLD%(filename)s$RESET:%(lineno)d) "

LOG_FORMAT = os.environ.get('LOG_FORMAT', DEFAULT_FORMAT)
LOG_FORMAT_FILE = os.environ.get('LOG_FORMAT_FILE', DEFAULT_FORMAT_FILE)