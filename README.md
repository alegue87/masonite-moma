# Masonite - Module Machine

Added features to Masonite framework:

- Scheduler High Rate
  - Parallel jobs execution
  - Load / discharge Job from database

## Load migrations and seeds

### Dev mode

`python craft migrate`

`python craft seed:run Jobs`

### Test mode

`python craft migrate -c postgres_test`

`python craft seed:run Jobs -c postgres_test`

For running tests:

`python -m pytest`

## Run

Is necessary use only one worker for the correct use of scheduler high rate. For example if you use 
gunicorn:

`gunicorn -w 1 wsgi:application --bind localhost:8080`

The execution of the application with craft create a double instance of application,
it is because the watch-dog used in package Werkzeug don't close the first instance but
create another for watching the files changes.

## 