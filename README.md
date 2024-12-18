
# Quiz Application

To clone and set up the Django project, follow these steps:

### 1. Clone the Repository
Clone the project from GitHub:
```bash
git clone https://github.com/Morkmork23/Quiz_app.git
```
### 2. Navigate to the Project Directory
Change into the project folder:
```bash
cd Quiz_app
```

### 3. Create a Virtual Environment:
```bash
python -m venv env
```
#### Set Up the Virtual Environment
If the project uses a virtual environment, create and activate it.
```bash
env\Scripts\activate
```

### 4. Install Django
Reinstall Django inside the virtual environment:

- If you're using 'Python3':
```bash
  python -m pip install django
```

### 5. Run Migrations
After installing Django, apply the migrations:
```bash
python manage.py migrate
```


### 6. Start the Development Server
Once the migrations complete successfully, start the server:
```bash
python manage.py runserver
```