import os, functools, requests, json

from flask import Flask, session, render_template, request, url_for, redirect, jsonify
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


# if user is already logged in, send capitalized username to index.html if not, open login.html
@app.route("/")
@app.route("/index")
def main():
    if session.get('user_id'):
        user_id = session.get('user_id')

        user = db.execute("SELECT * FROM users WHERE id = :user_id", {"user_id" :user_id}).fetchone()
        username = user.username

        return render_template("index.html", username=username.capitalize())
    else:
        return render_template("login.html")


# opening login page, check whether user is already logged in or not.
@app.route("/login")
def login():

    if session.get('user_id'):
        return render_template("error.html", message="You are already logged in.")

    else:
        return render_template("login.html")


@app.route('/signin', methods=['POST'])
def signin():

        username = request.form.get("username")
        password = request.form.get("password")
        user = db.execute("SELECT * FROM users WHERE username= :username AND password = :password",
                    {"username": username, "password": password}).fetchone()

        if user is None:
            return render_template("error.html", message="Invalid Username or Password.")

        else :
            session.clear()
            session['user_id'] = user['id']
            return render_template("index.html", username=username.capitalize())


@app.route("/register_form")
def register_form():

    if session.get('user_id'):
        return render_template("error.html", message="Before subscribe, please log out first.")

    return render_template('register_form.html')


@app.route('/register', methods=['POST'])
def register() :

    username = request.form.get("username")
    password = request.form.get("password")

    db.execute("INSERT INTO users (username, password) VALUES (:username, :password)",
            {"username": username, "password": password})

    db.commit()
    return render_template("registered.html", username=username.capitalize())


@app.route('/weather', methods=['GET', 'POST'])
def weather():

   if request.method == 'GET':
        if session.get('user_id'):
            return render_template("weather.html")

        else:
            return render_template("error.html", message="Please log in first.")


@app.route('/search', methods=['POST'])
def search():

    keyword = request.form.get("keyword").upper()
    lenkeyword = len(keyword)
    zips = db.execute("SELECT * FROM zips WHERE substring(zipcode,position(:keyword in zipcode), :lenkeyword) = :keyword OR substring(city,position(:keyword in city), :lenkeyword) = :keyword", {"keyword": keyword, "lenkeyword": lenkeyword}).fetchall()

    # zips = db.execute("SELECT * FROM zips WHERE (city LIKE: '%' + 'keyword' + '%') OR (zipcode LIKE: '%' + 'keyword' + '%') ", {"keyword": keyword}).fetchall()
    lenzips = len(zips)
    if zips == None:
        return render_template("error.html", message="Invaid ZIP Code.")

    else:
        return render_template("result.html", zips=zips, weather=weather, lenzips=lenzips)


@app.route('/search/<zipcode>', methods=['GET', 'POST'])
def location(zipcode):

    zips = db.execute("SELECT * FROM zips WHERE zipcode = :zipcode", {"zipcode": zipcode}).fetchone()
    zip_id = zips.id
    print(zip_id, "why")
    zip_lat = str(zips.lat)
    zip_long = str(zips.long)

    weather = requests.get("https://api.darksky.net/forecast/5d5612e56b037284a0f8cbdce183d180/" + zip_lat + "," + zip_long).json()

    # print(json.dumps(weather["currently"], indent = 2))

    w_time = weather["currently"]["time"]
    w_summary = weather["currently"]["summary"]
    w_temp = weather["currently"]["temperature"]
    w_dewpoint = weather["currently"]["dewPoint"]
    w_humid = int(weather["currently"]["humidity"]*100)

    user_id = session.get('user_id')
    user = db.execute("SELECT * FROM users WHERE id = :user_id", {"user_id" :user_id}).fetchone()

    comment = request.form.get('comment')

    if request.method == 'POST':
        db.execute("INSERT INTO comments(comment, users_id, zips_id) VALUES(:comment, :user_id, :zip_id)",
                        {"comment" :comment, "user_id" :user_id, "zip_id" :zip_id})
        db.commit()

    comments = db.execute("SELECT * FROM comments WHERE zips_id = :zip_id", {"zip_id": zip_id}).fetchall()

    return render_template("location.html",
                zips=zips, weather=weather, w_time=w_time, w_summary=w_summary,
                w_temp=w_temp, w_dewpoint=w_dewpoint, w_humid=w_humid, comments=comments)


@app.route('/search/<zipcode>/check_in', methods=['GET'])
def check_in(zipcode):

    user_id = session.get('user_id')

    if request.method == 'GET':
        checkin_check = db.execute("SELECT * FROM check_in_list WHERE checker_id = :user_id AND check_zipcode = :zipcode",
                                {"user_id": user_id, "zipcode": zipcode}).rowcount == 0

        if checkin_check == True:
            db.execute("INSERT INTO check_in_list (checker_id, check_zipcode) VALUES (:user_id, :zipcode)", {"user_id": user_id, "zipcode": zipcode})

            db.execute("UPDATE zips SET check_in = check_in + '1' WHERE zipcode = :zipcode", {"zipcode": zipcode})
            db.commit()

            return render_template("check_in.html", message="Checked in successfully!")

        else:
            return render_template("check_in_error.html", message="You have already checked in here before.")


@app.route('/api/<zipcode>', methods=['GET'])
def api(zipcode):

    zipcode = db.execute("SELECT * FROM zips WHERE zipcode = :zipcode", {"zipcode": zipcode}).fetchone()

    if zipcode == None:
        return jsonify({"error": "invalid zipcode"}), 404

    else:
        return jsonify({
            "zip": zipcode.zipcode,
            "place_name": zipcode.city,
            "state": zipcode.state,
            "latitude": zipcode.lat,
            "longitude": zipcode.long,
            "population": zipcode.population,
            "check_ins" : zipcode.check_in,
        })


@app.route('/logout')
def logout():

    if session.get('user_id'):
        session.clear()
        return main()

    else:
	    return render_template("error.html", message="You are not logged in yet.")


if __name__ == "__main__":
    main()