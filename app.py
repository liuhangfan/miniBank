from flask import Flask, request, make_response, redirect, render_template, abort

from account_service import get_balance, do_transfer
from user_service import logged_in, get_user_with_credentials, g
from flask_wtf.csrf import CSRFProtect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yoursupersecrettokenhere'

# using the Flask-WTF library which includes CSRF protection by default
csrf = CSRFProtect(app)

# To prevent brute force attacks, especially on login and API endpoints, implementing rate limiting
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://",
)

@app.route("/", methods=['GET'])
def home():
    # Redirect users to login page if not logged in, otherwise forward to dashboard
    if not logged_in():
        return render_template("login.html")
    return redirect('/dashboard')


@app.route("/login", methods=["POST"])
@limiter.limit("5 per minute") # Specific limit for login attempts to mitigate password guessing attacks
def login():
    email = request.form.get("email")
    password = request.form.get("password")
    user = get_user_with_credentials(email, password)
    if not user:
        # Generic error message to prevent user enumeration (not distinguishing between wrong email or password)
        return render_template("login.html", error="Invalid credentials")
    response = make_response(redirect("/dashboard"))
    response.set_cookie("auth_token", user["token"])
    return response, 303


@app.route("/dashboard", methods=['GET'])
def dashboard():
    # Ensures that only logged-in users can see the dashboard, otherwise redirects to login
    if not logged_in():
        return render_template("login.html")
    return render_template("dashboard.html", email=g.user)


@app.route("/details", methods=['GET'])
def details():
    if not logged_in():
        return render_template("login.html")
    account_number = request.args['account']
    balance = get_balance(account_number, g.user)
    if balance is None:
        return render_template("dashboard.html", error="Invalid account number")
    return render_template(
        "details.html",
        user=g.user,
        account_number=account_number,
        balance=balance)


@app.route("/transfer", methods=["GET"])
def transferGet():
    if not logged_in():
        return render_template("login.html")
    return render_template("transfer.html")


@app.route("/transfer", methods=["POST"])
def transfer():
    if not logged_in():
        return render_template("login.html")
    source = request.form.get("from")
    target = request.form.get("to")
    try:
        amount = int(request.form.get("amount"))
    except (TypeError, ValueError):
        abort(400, "Invalid amount provided")

    if amount < 0:
        abort(400, "NO STEALING")
    if amount > 1000:
        abort(400, "WOAH THERE TAKE IT EASY")

    available_balance = get_balance(source, g.user)
    if available_balance is None:
        abort(404, "Account not found")
    if amount > available_balance:
        abort(400, "You don't have that much")

    if do_transfer(source, target, amount):
        pass  # TODO GIVE FEEDBACK
    else:
        abort(400, "Something bad happened")

    response = make_response(redirect("/dashboard"))
    return response, 303


@app.route("/logout", methods=['GET'])
def logout():
    response = make_response(redirect("/dashboard"))
    response.delete_cookie('auth_token')
    return response, 303

@app.errorhandler(429)
def ratelimit_handler(e):
    return "You have hit the rate limit", 429