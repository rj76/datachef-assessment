Datachef assessment
====================

Setup
------
- create & activate virtualenv
- run `pip install -r requirements.txt`
- change database settings in `settings.py`
- run `./manage.py migrate`


Import datasets
----------------
- run `./manage.py run_batch`


Tests
------
- run `pytest apps`
