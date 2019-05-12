from airflow.plugins_manager import AirflowPlugin
from twiggle_api_plugin.twiggle_api import twiggle_api_bp, twiggle_api_view


class TwiggleApiPlugin(AirflowPlugin):
    name = "twiggle_api_plugin"
    operators = []
    flask_blueprints = [twiggle_api_bp]
    hooks = []
    executors = []
    admin_views = [twiggle_api_view]
    menu_links = []
