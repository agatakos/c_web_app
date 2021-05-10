
# Running the image


 1. Download and install Docker. 

 2. Create an account and login on your machine. You should see a small Docker logo in your tray bar. 

 3. Clone the repository

        git clone https://github.com/agatakos/c_web_app.git
 
 4. Change directory

        cd c_web_app

 5. Source the env variables and install requirements

        source .env

        pip install -r requirements.txt

 6. Compose docker image
    
        docker-compose build

 7. Run the image, if you haven't renamed it this should work 

        docker run -p 5000:5000 c_web_app_web
 
 8. Go to this address in your browser or paste it in Postman (or see below for sample curl calls)
      
        http://0.0.0.0:5000/

# API Endpoints


 ## 1. Policy count

 Returns count of policies for each user.

 URL

        /policy_count/user_id

  Method:

        GET

 URL Params

 Optional:

        user_id=[string]

 Success Response:

 Code: 200
 Content: `{UserId: user0000123, PolicyCount: 2}`

 Error Response:

 Code: 404 NOT FOUND

 Sample Call:

        curl -v http://0.0.0.0:5000/new_user_count/


 ## 2. Days active

 Returns count of days for each user where user status is Active.

 URL

        /days_active/user_id

 Method:

        GET

 URL Params

 Optional:

        user_id=[string]

 Success Response:

 Code: 200
 Content: `{User: user000123, DaysActive: 7}`

 Error Response:

 Code: 404 NOT FOUND

 Sample Call:

        curl -v http://0.0.0.0:5000/days_active/user000123


 ## 3. New user count by date

 Returns count of new users for each day.

 URL

        /new_user_count/date

 Method:

        GET

 URL Params

 Optional:

        date=[string]

 Success Response:

 Code: 200

 Content: ```{
             NewUserCount: 7,
             Date: 2020-04-16,
            Status: new,
            }```

 Error Response:

 Code: 404 NOT FOUND

 Sample Call:

        curl -v http://0.0.0.0:5000/new_user_count/2020-04-16


 ## 4. Lapsed users count by month

 Returns count of lapsed users for each month.

 URL

        /lapsed_users_count/year_month

 Method:

        GET

 URL Params

 Optional:

        year_month=[string]

 Success Response:

 Code: 200

 Content: ```{
            LapsedUserCount: 3,
            Month: 2020-04,
            Status: lapsed,
            }```

Error Response:

Code: 404 NOT FOUND

Sample Call:

        curl -v http://0.0.0.0:5000/lapsed_users_count/2020-04

    
 ## 5. New user premiums

 Returns sum of premiums per underwiter where user is in new status and reason for transaction is policy sale.

 URL

        /new_user_premiums/underwriter

 Method:

        GET

 URL Params

 Required:

        underwriter=[string]

 Success Response:

 Code: 200

 Content: ```{
                Underwriter: red,
                PremiumTotals: 75,
            }```

 Error Response:

 Code: 404 NOT FOUND

 Sample Call:

        curl -v http://0.0.0.0:5000/new_user_premiums/red

       