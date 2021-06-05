Datachef assessment
====================

Setup
------
- create & activate virtualenv
- run `pip install -r requirements.txt`
- change database settings in `settings.py`
- run `./manage.py migrate`
- run `./manage.py runserver`
- open browser and go to http://127.0.0.1:8000/


Import datasets
----------------
- run `./manage.py run_batch`


Tests
------
- run `pytest`
