from airflow.plugins_manager import AirflowPlugin
from api_plugin.api import api_bp, api_view


class ApiPlugin(AirflowPlugin):
    name = "api_plugin"
    operators = []
    flask_blueprints = [api_bp]
    hooks = []
    executors = []
    admin_views = [api_view]
    menu_links = []

