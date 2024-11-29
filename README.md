# Masonite - Module Machine

Added features to Masonite framework:

- Scheduler High Rate
  - Parallel jobs execution
  - Load / discharge Jobs from database
  - Dynamic code loading ( at runtime, no watchdog or --reload flag )
  - DB failure proof ( no need restart if DB is offline )

## Load migrations and seeds

### Dev mode

Create from .env-example a .env file for setup application db etc..

`python craft migrate`

`python craft seed:run Jobs`

### Test mode

`export DB_CONFIG_PATH='tests/database_config.py'`

`python craft migrate -c postgres_test`

`python craft seed:run Jobs`

`unset DB_CONFIG_PATH`

export necessary because the config option not work correctly, for example:

`python craft seed:run Jobs --config tests/database_config.py`


For running tests:

`python -m pytest`

## Run

Is necessary use only one worker for the correct use of scheduler high rate. For example if you use 
gunicorn:

`gunicorn -w 1 wsgi:application --bind localhost:8080`

for show the port to external:

`gunicorn -w 1 wsgi:application --bind 0.0.0.0:8080`


The execution of the application with craft create a double instance of application,
it is because the watch-dog used in package Werkzeug don't close the first instance but
create another for watching the files changes, thereafter is not raccomanded.

### Use job's arguments

The `args` column is a json and is fillable in this way:

`{'name': 'Job_A', 'class_name': 'Job_1', 'interval': 0.1, 'run': False, 'args': '{"key": "value"}'}`

For getting a dictionary (dict type) is easy to retrive with `job_model.args` in the start method of Job.

The column `start_second` in the Jobs table, indicate the exact second for the starts of the job. Is useful when 
you must planning an exact schedule's table.
