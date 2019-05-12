import time
from datetime import datetime
from pprint import pprint
from airflow import DAG
from airflow.models import Variable
from airflow.operators.python_operator import PythonOperator

default_args = {
    'depends_on_past': False,
    'start_date': datetime(2019, 1, 1),
    'email': ['orr@twiggle.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 0
}

dag = DAG('sleep_variable', default_args=default_args, catchup=False, schedule_interval=None)

print_context_task = PythonOperator(
    task_id='print_context',
    provide_context=True,
    python_callable=lambda ds, **context: pprint(context),
    dag=dag)

sleep_timeout = float(Variable.get('sleep_timeout', default_var=5))

sleep_task = PythonOperator(
    task_id='sleep_task',
    python_callable=lambda: time.sleep(sleep_timeout),
    dag=dag)

print_context_task >> sleep_task
