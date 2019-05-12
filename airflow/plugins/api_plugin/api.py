import os
import airflow
from airflow import configuration
from airflow.api.common.experimental import trigger_dag
from airflow.models import Variable
from flask import Blueprint, request, jsonify
from flask_admin import BaseView, expose

# Using UTF-8 Encoding so that response messages don't have any characters in them that can't be handled
os.environ['PYTHONIOENCODING'] = 'utf-8'
endpoint = '/api'

apis = [
    {
        "path": "version",
        "description": "Displays Airflow version",
        "parameters": []
    },
    {
        "path": "trigger-dag",
        "description": "Trigger the sleep_triggered DAG run with custom sleep timeout",
        "parameters": [
            {"name": "timeout"}
        ]
    },
    {
        "path": "get-timeout",
        "description": "Get the custom sleep timeout for the sleep_variable DAG",
        "parameters": []
    },
    {
        "path": "set-timeout",
        "description": "Set the custom sleep timeout for the sleep_variable DAG",
        "parameters": [
            {"name": "timeout"}
        ]
    }
]


class Api(BaseView):
    @expose('/')
    def index(self):
        return self.render('index.html',
                           airflow_webserver_base_url=configuration.get('webserver', 'BASE_URL'),
                           rest_api_endpoint=endpoint,
                           apis=apis)

    @expose('/version', methods=['GET'])
    def version(self):
        return self._create_response(200, True, airflow.__version__)

    @expose('/trigger-dag', methods=['GET'])
    def trigger_dag(self):
        sleep_timeout = request.args.get('timeout', None)
        if not self.is_number(sleep_timeout):
            return self._create_response(400, False, 'sleep_timeout parameter is not a number')
        try:
            trigger = trigger_dag.trigger_dag('sleep_triggered', conf={'sleep_timeout': sleep_timeout})
        except Exception as e:
            return self._create_response(400, False, str(e))
        return self._create_response(200, True, 'dag triggered with response: {}'.format(trigger))

    @expose('/get-timeout', methods=['GET'])
    def get_sleep_timeout(self):
        sleep_timeout = Variable.get('sleep_timeout', default_var=5)
        return self._create_response(200, True, 'sleep timeout is {} seconds'.format(sleep_timeout))

    @expose('/set-timeout', methods=['GET'])
    def set_sleep_timeout(self):
        sleep_timeout = request.args.get('timeout', None)
        if not self.is_number(sleep_timeout):
            return self._create_response(200, True, 'sleep_timeout parameter is not a number')
        Variable.set('sleep_timeout', sleep_timeout)
        return self._create_response(200, True, 'sleep timeout set to {} seconds'.format(sleep_timeout))

    @staticmethod
    def _create_response(status_code: int, success: bool, message: str):
        return jsonify({
            'result': 'success' if success else 'error',
            'message': message
        }), status_code

    @staticmethod
    def is_number(s):
        try:
            float(s)
            return True
        except ValueError:
            return False


api_view = Api(category='Admin', name='Api', url=endpoint)
api_bp = Blueprint(
    'api_bp',
    __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='/static/'
)
