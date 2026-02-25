#!/bin/bash
python -m celery -A tasks.celery_conf:celery_app worker --loglevel=INFO