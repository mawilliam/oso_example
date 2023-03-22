# oso_example
Minimal reproducible example of an Oso error.

# Steps to reproduce
1. Create a virtual environment using Python 3.8 and activate it
2. Install the requirements: `python -m pip install -r requirements.txt`
3. Install the dev requirements: `python -m pip install -r requirements.txt`
4. Migrate the app: `python manage.py makemigrations` and `python manage.py migrate`
5. Run the tests: `pytest`
