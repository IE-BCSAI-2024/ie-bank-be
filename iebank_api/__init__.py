from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from dotenv import load_dotenv
import os
# Import the `configure_azure_monitor()` function from the
# `azure.monitor.opentelemetry` package.
from azure.monitor.opentelemetry import configure_azure_monitor

# Import the tracing api from the `opentelemetry` package.
from opentelemetry import trace

# Configure OpenTelemetry to use Azure Monitor with the 
# APPLICATIONINSIGHTS_CONNECTION_STRING environment variable.
configure_azure_monitor(
    connection_string="InstrumentationKey=f8c8089f-b240-4e9c-bd28-02a41c17907b;IngestionEndpoint=https://northeurope-2.in.applicationinsights.azure.com/;LiveEndpoint=https://northeurope.livediagnostics.monitor.azure.com/;ApplicationId=dcb1a741-784c-42e4-a33d-9468dc7c046c",
)

app = Flask(__name__)

load_dotenv()

# Select environment based on the ENV environment variable
if os.getenv('ENV') == 'local':
    print("Running in local mode")
    app.config.from_object('config.LocalConfig')
elif os.getenv('ENV') == 'dev':
    print("Running in development mode")
    app.config.from_object('config.DevelopmentConfig')
elif os.getenv('ENV') == 'ghci':
    print("Running in github mode")
    app.config.from_object('config.GithubCIConfig')
else:
    print("Running in production mode")
    app.config.from_object('config.ProductionConfig')

db = SQLAlchemy(app)

from iebank_api.models import Account

with app.app_context():
    db.create_all()
CORS(app)

from iebank_api import routes
