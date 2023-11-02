#!/bin/bash

# if any of the commands in your code fails for any reason, the entire script fails
set -o errexit
# exits if any of your variables is not set
set -o nounset

#celery -A django_celery_example worker -l INFO
celery -A config worker --loglevel=info --concurrency 1 -E