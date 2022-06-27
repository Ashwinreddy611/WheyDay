# Github Deployment 
* The initial set up of the project was done using the code institute template. This was done by finding the code institute on GitHub and clicking the green button on their gitpod full template repository. 
* Once in Gitpod Files were staged using the git add . command in the terminal, then git commit -m to commit the files with an accompanying message and then git push to push to my repository and keep the repository updated. 

# Heroku Deployment
* First of all an app was created in Heroku called WheyDay where the region chosen was the one closest to me and in this instance that is Europe.
* Next a postgres database was needed so I went to my gitpod workspace for the project and installed the dj_database_url and psycopg2 dependencies using the command pip3 install. Then I added these to the requirements.txt file by using the command pip3 freeze > requirements.txt. Then in gitpood I imported the dj_database_url to the settings.py file.

* `DATABASES = {
    'default': dj_database_url.parse('DATABASE_URL')
}`  Was then used in order to set up the postgres database. All the models are then migrated into the new database using python3 manage.pr migrate. A new superuser was then created using python3 manage.py createsuperuser. This was then committed without the environment variables.

* The above was then wrapped in an if statement where the postgres database is used otherwise the gitpod database is used. As following: 
* `if "DATABASE_URL" in os.environ:
        DATABASES = {
            "default": dj_database_url.parse(os.environ.get('DATABASE_URL'))
        }
  else:
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': BASE_DIR / 'db.sqlite3',
            }
        }`

* Gunicorn was then installed to tell heroku this app is a web app and a procfile was created. Within the procfile `web: gunicorn <appname>.wsgi:application` was added.

* Heroku is now ready to be connected via the gitpod terminal and this is started off by using the command heroku login -i and the loggin in. then the command `heroku config:set DISABLE_COLLECTSTATIC=1 --app <appname>` Was then used to disable the collection of static files until aws is set up.

* Now heroku is needed to be an allowed host using this code: `ALLOWED_HOSTS = ["<heroku appname>.herokuapp.com", "localhost"]` This allows the app to be run on heroku and locally in gitpod.

* These changes were pushed to github and then pushing to heroku was set up using `heroku git:remote -a <heroku appname>`.

* Again this gets pushed to github using git push heroku master.

* Now on the deploy section of the heroku app i went to the deploy section and selected deployment via github. And searched for my app repo. I then connected and enabled automatic deploys. 

* I then set up an account on AWS and created a bucket on s3 in order to hold my static files. I clicked the create button name and selected the nearest region and then uncheck block public access. Now click create button.

* In the bucket properties i turned on static hosting. In the index and error inputs i put index.html and error.html respectively.

* In the permissions section, this code was pasted in: 

`
[
    
      {
          "AllowedHeaders": [
              "Authorization"
          ],
          "AllowedMethods": [
              "GET"
          ],
          "AllowedOrigins": [
              "*"
          ],
          "ExposedHeaders": [


          ]
      }
  ]
 `
* And then the policy was generated. As a part of the policy i selected s3 bucket policy. And then select all principals. I selected action to get object, pasted in the arn from my bucket policy page and clicked add statement. I then clicked generate policy and pasted that into the bucket policy and added /* on the resource key and clicked save. 

* I then went to the access control list section and set list object for everyone.

* Now on the aws site i searched for IAM and created a group. I then created a group policy by clicking the create policy button select the JSON tab and then import managed policies then search s3 and select on Amazons3fullaccess and import. In the resource section i pasted in the arn previously used. I clicked through the review policy, filled in the name and description and clicked generate policy. 

* Back into the group, click on permission and attach the policy then find the policy just created and attached it.

* Now it was time to create the user and users was selected from the sidebar and add user was selected. A username was created and programmatic access was selected and then next was clicked. I then selected the group and the user as well and clicked through the then end to create user. The csv file was downloaded and it contains user keys for the app. 

* The bucket is now ready to connect to django. And initially boto3 and django-storages is installed in gitpod. This was then added to the requirements file. An environment variable called USE_AWS is created and the following settings are needed: 

`if "USE_AWS" in os.environ:
      AWS_STORAGE_BUCKET_NAME = "<bucket name>"
      AWS_S3_REGION_NAME = "<bucket region>"
      AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID") # taken from downloaded csv file
      AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
 
      AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
 
      STATICFILES_STORAGE = "custom_storages.StaticStorage"
      STATICFILES_LOCATION = "static"
      DEFAULT_FILE_STORAGE = "custom_storages.MediaStorage"
      MEDIAFILES_LOCATION = "media"
 
      STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{STATICFILES_LOCATION}/'
      MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{MEDIAFILES_LOCATION}/'`

* Back in heroku i clicked on settings tab and then clicked reveal config vars and then set up the environmental variables as required.

* In gitpod i created custom_storaged.py and imported s3boto3storage. I set uo classes to tell django when the files should be stored as written below: 
`   class StaticStorage(S3Boto3Storage):
        location = settings.STATICFILES_LOCATION
  
    class MediaStorage(S3Boto3Storage):
        location = settings.MEDIAFILES_LOCATION `

* These changes were then pushed to github. 

* Media files were then added to AWS in the bucket and then clicked to upload the files.

* Next the following environment variables were set up for functionality: 
    * DJANGO_SECRET_KEY = your secret key
    * STRIPE_PUBLIC_KEY = your stripe public key
    * STRIPE_SECRET_KEY = your stripe secret key
    * STRIPE_WH_SECRET = your stripe webhook secret
    * IN_DEVELOPMENT = True

* The database models were then migrated using python3 manage.py makemigrations -dry-run. Then python3 manage.py makemigrations. Then python3 manage.py migrate -plan and finally python3 manage.py migrate.

* Another superuser is created to access the admin and so done so using aforementioned method.

* The Project is now properly deployed.












