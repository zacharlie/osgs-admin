from datetime import datetime

osgs_default_config = {
    "osgs_repo": "https://github.com/kartoza/osgs",
    "git_configured": "False",
    "git_init_dt": datetime.utcnow().isoformat(),
    "git_pull_dt": datetime.utcnow().isoformat(),
}

"""

# Just setting this will set the docker compose project prefix
# If you change this name you need to also change references to the
# compose project name in nginx confs and perhaps other places
COMPOSE_PROJECT_NAME=osgisstack
CONTACT_EMAIL=validemail@yourdomain.org
DOMAIN=example.org

# Timezone in TZ database name format
# See https://en.wikipedia.org/wiki/List_of_tz_database_time_zones
TIMEZONE=Etc/UTC

# POSTGREST
PGRST_SERVER_PROXY_URI=https://example.org/api
PGRST_DB_ANON_ROLE=anon
PGRST_DB_SCHEMA=api
PGRST_OPENAPI_SERVER_PROXY_URI=https://example.org/api
PGRST_SERVER_PORT=3000
# Generate using ssl e.g.
# openssl rand -base64 32
PGRST_JWT_SECRET=foobarxxxyyyzzz

# SWAGGER
API_URL=https://example.org/api/

# POSTGRES
POSTGRES_USER=docker
POSTGRES_PASSWORD=docker
# Disabled on public by default
POSTGRES_PUBLIC_PORT=5432
POSTGRES_PRIVATE_PORT=5432
# GEOSERVER
GEOSERVER_ADMIN_PASSWORD=myawesomegeoserver
GEOSERVER_ADMIN_USER=admin
INITIAL_MEMORY=2G
MAXIMUM_MEMORY=4G

# MERGIN DB SYNC
# Typically your email
MERGIN_DATABASE=mergin_database
MERGIN_USER=mergin_username
MERGIN_PASSWORD=mergin_password
# Should be username/project name
MERGIN_PROJECT_NAME=mergin_username/mergin_project
# Should be a geopackage in your mergin project
MERGIN_SYNC_FILE=mergin_project_geopackage.gpkg
DB_SCHEMA_MODIFIED=schematoreceivemergindata
DB_SCHEMA_BASE=mergin_sync_base_do_not_touch
MERGIN_URL="https://public.cloudmergin.com"

# MERGIN SERVER
MERGIN_SERVER_VERSION=2021.6.1
MERGIN_SERVER_SECRET_KEY=REPLACE_MERGIN_SERVER_SECRET_KEY
MERGIN_SERVER_SECURITY_PASSWORD_SALT=REPLACE_MERGIN_SERVER_SECURITY_PASSWORD_SALT
MERGIN_SERVER_USER_SELF_REGISTRATION=0
MERGIN_SERVER_USE_X_ACCEL=0
MERGIN_SERVER_GEODIFF_LOGGER_LEVEL=2
MERGIN_SERVER_MERGIN_TESTING=0
MERGIN_SERVER_MAX_CHUNK_SIZE=10485760  # 10 MB
MERGIN_SERVER_TEMP_EXPIRATION=7
MERGIN_SERVER_DELETED_PROJECT_EXPIRATION=7
MERGIN_SERVER_CLOSED_ACCOUNT_EXPIRATION=1
MERGIN_SERVER_DEFAULT_STORAGE_SIZE=104857600 # 100 MB
MERGIN_SERVER_MAIL_SUPPRESS_SEND=0  # set to 0 in production
MERGIN_SERVER_MAIL_SERVER=REPLACE_MERGIN_SERVER_MAIL_SERVER
MERGIN_SERVER_MAIL_DEFAULT_SENDER=REPLACE_MERGIN_SERVER_MAIL_DEFAULT_SENDER
MERGIN_SERVER_MAIL_USERNAME=REPLACE_MERGIN_SERVER_MAIL_DEFAULT_SENDER
# for email templates
MERGIN_SERVER_MERGIN_BASE_URL=REPLACE_MERGIN_SERVER_MERGIN_BASE_URL
MERGIN_SERVER_MERGIN_LOGO_URL=REPLACE_MERGIN_SERVER_MERGIN_LOGO_URL
MERGIN_SERVER_CONTACT_EMAIL=REPLACE_MERGIN_SERVER_CONTACT_EMAIL
MERGIN_SERVER_SLACK_HOOK_URL=REPLACE_MERGIN_SERVER_CONTACT_EMAIL
"""
