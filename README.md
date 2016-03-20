# Project Four

Project Four is a Django application that uses the Open Secrets, VoteSmart, and the NPR News APIs. 

## Description 
This application is a group project built as part of the software development capstone course at Minneapolis Community and Technical College. Our goals for the project were to explore consuming APIs using the Django framework.

## Features
- Users can explore the contributions made to United States Congressional legislators via OpenSecrets, alongside position rankings from VoteSmart and recent news articles about the candidate from NPR.
- Users can save legislator profiles to their own user profile for later viewing

## Instructions
 - Install the required Python packages in your virtualenv by running `pip install -r requirements.txt`
 - You will need to add your own OpenSecrets, VoteSmart and NPR API keys as environment variables. Keys can be acquired at the urls below:
  - <http://www.opensecrets.org/resources/create/apis.php>
  - <http://votesmart.org/share/api>
  - <http://www.npr.org/api/index>
 - From the open_secrets directory run python manage.py runserver and visit <127.0.0.1:8000> in your browser to use the app.
