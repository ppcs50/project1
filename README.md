# Project 1

Web Programming with Python and JavaScript

## short decription
In this project, I made up a web application based on python, by using Flask, SQLAlchemy, and PostgreSQ.
Users can get some geographical information and weather information by searching ZIP Code or City name.

## What's going on here?

### /
#### application.py
this is the main file make able to run my application.

1. main(): When user accesses main page, it checks whether the user has logged in already or not, by checking the session. It returns main page(index.html) only session has user_id. Or it just keep returns login.html to users who not logged in yet.
2. login(): It get request of user's input of 'username' and 'password' from the login.html page, and checks if there is matching result in the 'users' table in my SQL database. Only when it successfully found out the match, session can get user_id and return index.html.
3. register_form(): It also checks the session whether user has logged in already or not, and only if user have not logged in yet it returns register_form.html.
4. register(): When user input new username and password on register_form.html, it will get them and check username in the database whether already exists or not. Only if same username is not exists in the 'users' table it insert into new user information in the table and returns registered.html.
5. weather(): When user click the weather tab or link it checks whether user has logged in or not, and returns weather.html when the session got user_id.
6. search(): When user input some keyword of city name or zip code, it looking for the matching results in the 'zips' table in my SQL database. If the length of the matching result is zero, it means there are no matching result, so it returns error.html. When there are 1 or more matching results, it returns result.html and send every matching result to the page at the same time.
7. location(zipcode): Based on the specific zip code which user selected, it reads 'zips' table again and save some strings, get weather information from Dark Sky API, and render them on the result.html. It also saves and reload user's comments from 'comments' table in the SQL. While saving user's comments, it saves user id and zipcode id together on the same row so that who and which zipcode user put comments. The table is joined with the others(zips, users).
8. check_in(zipcode): Based on the specific zip code of the location page, when user click the check in button, it checks matching row in the 'comments' table with user id and zipcode, and only if there is no result, it saves check in counts in the 'zips' table and insert user id with zipcode in the check in list table, and returns proper messages.
9. api(zipcode): When user accesses this route, it returns 'jsonified' values from the 'zips' table in my SQL database, based on the specific zip code. If there is no matching result, it returns 404 error.
10. logout(): When user click this button, if the session got user id, it will clear the session, but if it is not, it returns error message.

#### danp58c0q3efhn.sql
THE SQL file I saved from my ADMINER account.

#### env.sh
For setting up environment such as FLASK_APP or DEBUG, and link the PostgreSQL database.

#### import.py
To import zips.csv to my SQL database. I added some lines myself to solve the problem that missing zero zipcodes.

#### README.md
This file.

#### requirements.txt
#### zips,.csv

### /templates/
#### check_in.html, check_in_error.html
check_in(zipcode) will returns whether of these two pages depend on the result.

#### error.html
This is common error pages includes dynamic messages.

#### index.html
The main page, includes brief introduction and hello message to the user.

#### layout.html
It is the base part of my html structure, includes <header>, <nav>, and <footer>. They are all extended by jinja2.

#### location.html
It gets datas from location(), listing geographical information, weather information, and comments. It has comments input box too.

#### login.html
When it get username input and password input from user, it hands those forms to login(), so login() can check it's validity.

#### register_form.html
Same as the login.html, takes username and password and hands those values to register().

#### registered.html
When a user successfully registered, this page will be returned.

#### result.html
It lists every matching results from the databse with the keyword that user has input in the weather.html.

#### weather.html
In this page, user can input a keyword of zip codes or city names to find information.

### /static/css
#### style.css, style.css.map, style.scss
This is slightly modified version of my previous project, number 0.

## Any Additional Information
It was really tough! But so much accomplishment too. I liked it!
