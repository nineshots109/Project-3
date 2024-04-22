## Running the Application

To run the application locally, follow these steps:

1. Clone the repository to your local machine:
gh repo clone nineshots109/Project-3

$ cd Project-3

Initialize a virtual environment:

If on Windows:


2. Initialize a virtual environment:
- Windows:
  ```
  $ python3 -m venv venv
  $ venv\Scripts\activate.bat
  ```
- Unix/MacOS:
  ```
  $ python3 -m venv venv
  $ source venv/bin/activate
  ```
  

In order for Flask to run, there must be a SECRET_KEY variable declared. Generating one is simple with Python 3:

$ python3 -c "import secrets; print('SECRET_KEY=' + secrets.token_hex(16))" > config.env


3. Install the requirements:
$ pip install -r requirements.txt


4. Install these necessary dependencies:

Type "sudo apt-get update" then install sass and redis-server

For Sass:

  $ gem install sass

5. For Redis:
  - Mac: $ brew install redis
  - Linux: $ sudo apt-get install redis-server
  

5. Creating database:
$ python manage.py recreate_db

If there is an error with python manage.py recreate_db, just try it again - it should work. If not, move on to next step!

6. Run the app:
$ source venv/bin/activate
$ honcho start -e config.env -f Local


7. Open your web browser and navigate to [http://localhost:5000](http://localhost:5000) to view the application.

Enjoy the food recipes with Spoonacular API
