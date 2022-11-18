# QUICK START

## Step 1: Environment Settings
```commandline
pip install -r requirements.txt
```
## Step 2: SQL Migrate
### Edit settings.py
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',  
        'NAME': 'comp9900',  # your database name
        'USER': 'root',  # your mysql user name
        'PASSWORD': 'root1234',  # your mysql password
        'HOST': '',  # 
        'PORT': '3306',  # 
    }
}
```
### Model Migrate
```commandline
python3 manage.py migrate
```

## Step 3: Run server
```commandline
python3 manage.py runserver
```
```
daphne -b 127.0.0.1 -p 5000 comp9900.asgi:application
```
