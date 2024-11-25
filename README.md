# Masonite - Module Machine

Added features to Masonite framework:

- Scheduler High Rate
  - Parallel jobs execution
  - Load / discharge Jobs from database
  - Dynamic code loading ( at runtime, no watchdog or --reload flag )

## Load migrations and seeds

### Dev mode

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

The execution of the application with craft create a double instance of application,
it is because the watch-dog used in package Werkzeug don't close the first instance but
create another for watching the files changes, threafter is not raccomanded.

## 