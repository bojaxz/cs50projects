import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""

    # select current information on stocks for current user
    rows = db.execute("""
        SELECT symbol, SUM(shares) as Total_Shares
        FROM transactions
        WHERE user_id=:user_id
        Group BY symbol
        HAVING Total_Shares > 0;
    """, user_id=session["user_id"])

    # prepare list for stocks
    my_stocks = []
    total_cash = 0

    # for loop to build my_stocks list as shares are added
    for row in rows:
        stock = lookup(row["symbol"])
        my_stocks.append({
            "symbol": stock["symbol"],
            "name": stock["name"],
            "shares": row["Total_Shares"],
            "price": usd(stock["price"]),
            "total": usd(stock["price"] * row["Total_Shares"])
        })
        total_cash += stock["price"] * row["Total_Shares"]

    # select statement for current cash for current user
    rows = db.execute("SELECT cash FROM users WHERE id=:user_id", user_id=session["user_id"])
    cash = rows[0]["cash"]
    total_cash += cash

    return render_template("index.html", my_stocks=my_stocks, cash=usd(cash), total_cash=usd(total_cash))


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    # if request is post, lookup stock name, multiply number of shares by total cost
    if request.method == "POST":
        if not request.form.get("symbol"):
            return apology("Please enter Symbol", 403)

        rows = db.execute("SELECT cash FROM users WHERE id=:id", id=session["user_id"])
        cash = rows[0]["cash"]
        symbol = request.form.get("symbol").upper()
        stock = lookup(symbol)

        # return error is symbol name of stock is not valid
        if stock is None:
            return apology("Please enter a valid Symbol name", 404)

        # get number of shares from buy.html
        shares = int(request.form.get("shares"))

        # do math on total cash spent on buy
        spent = shares * stock["price"]

        # return error if current cash is less than spent amount
        if cash < spent:
            return apology("Sorry, you do not enough cash to make this purchase", 403)

        # update database to include new stock purchase
        db.execute("INSERT INTO transactions (user_id, symbol, shares, price) VALUES (:user_id, :symbol, :shares, :price)",
        user_id=session["user_id"], symbol=stock["symbol"], shares=shares, price=stock["price"])

        # update the total amount of cash for the user by subtracting spent amount from total cash
        updated_cash = cash - spent

        # update user's cash amount with updated_cash in previous line
        db.execute("UPDATE users SET cash=:updated_cash where id=:id", updated_cash=updated_cash, id=session["user_id"])

        # flash message that share was bought and return to buy.html
        flash("Share bought!")
        return redirect("/buy")

    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    # select statement to build my_stocks list for logged in user
    rows = db.execute("""
        SELECT symbol, shares, price, transaction_time
        FROM transactions
        WHERE user_id=:user_id
        ORDER BY 1 DESC;
    """, user_id=session["user_id"])

    # list for my_stocks to display transaction history
    my_stocks = []

    for row in rows:
        stock = lookup(row["symbol"])

        # add to list for "Buy" transactions
        if row["shares"] > 0:
            my_stocks.append({
                "symbol": row["symbol"],
                "name": stock["name"],
                "shares": row["shares"],
                "price": usd(row["price"]),
                "time": row["transaction_time"],
                "action": "buy"
            })
        # add to list for "Sell" transactions
        if row["shares"] < 0:
            my_stocks.append({
                "symbol": row["symbol"],
                "name": stock["name"],
                "shares": row["shares"],
                "price": usd(row["price"]),
                "time": row["transaction_time"],
                "action": "sell"
            })

    return render_template("history.html", my_stocks=my_stocks)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():

    # if statement for post requests
    if request.method == "POST":

        # return error is symbol name is missing
        if not request.form.get("symbol"):
            return apology("Please enter Symbol", 403)

        # grab symbol name from quote.html form
        symbol = request.form.get("symbol").upper()
        # run lookup function for symbol name
        stock = lookup(symbol)

        # return error if symbol name is not valid
        if stock == None:
            return apology("Invaild Symbol Name", 403)

        # return quoted.html to display quoted stock information
        return render_template("quoted.html", stock=stock)

    # get request will display quote.html
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():

    # get request displays register.html
    if request.method == "GET":
        return render_template("register.html")

    # post request condition. Allows user to register for a new account
    else:

        # gets username from register.html form, username.
        username = request.form.get("username")
        if not username:
            return apology("must provide a username", 403)

        # checks if entered username is already in the database. If so, return error that username is not unique.
        usernames = db.execute("SELECT username FROM users")
        if username in usernames:
            return apology("username must be unique", 403)

        # gets password from register.html form, password.
        password = request.form.get("password")
        if not password:
            return apology("you must provide an password", 403)

        # gets confirmation from register.html form, confirmation. Also checks to ensure that password and confirmation match
        confirmation = request.form.get("confirmation")
        if confirmation != password:
            return apology("password does not match", 403)

        # adds username and password to users table in finance.db and hashes password
        db.execute("INSERT INTO users (username, hash) VALUES (:username, :hash)", username=username, hash=generate_password_hash(password))
        return redirect("/")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    # post request condition. If symbol is not entered, return error
    if request.method == "POST":
        if not request.form.get("symbol"):
            return apology("Please enter Symbol", 403)

        # select statement to get current user's available cash
        rows = db.execute("SELECT cash FROM users WHERE id=:id", id=session["user_id"])
        cash = rows[0]["cash"]

        # get symbol entered on form from sell.html, symbol
        symbol = request.form.get("symbol").upper()

        # run lookup function on symbol name
        stock = lookup(symbol)

        # return error if symbol name is not valid
        if stock is None:
            return apology("Please enter a valid symbol name", 404)

        # get number of shares to sell from sell.html form, shares
        shares = int(request.form.get("shares"))

        # select statement to check user's total number of shares for the specified symbol name and user_id
        rows1 = db.execute("""
            SELECT SUM(shares) as Total_Shares
            FROM transactions
            WHERE user_id=:user_id AND symbol=:symbol;
        """, user_id=session["user_id"], symbol=symbol)

        # create variable for number of current shares using previous select statement
        current_shares = int(rows1[0]["Total_Shares"])

        # if the number of shares enter to sell is higher than the number of shares the user owns, return an error
        if shares > current_shares:
            return apology("Sorry, you do not own enough shares to complete this sale", 403)

        # get the number of updated shares by subtracting the number of sold shares by the number of total current shares
        updated_shares = current_shares - shares

        # get the profit of sold shares
        profit = shares * stock["price"]

        # variable for users updated cash
        updated_cash = cash + profit

        # insert statement to include the sale of shares.
        # In order for this transaction to display in the history page, we enter this transation in its own line and then run a SUM(shares) with same symbol name
        db.execute("INSERT INTO transactions (user_id, symbol, shares, price) VALUES (:user_id, :symbol, :shares, :price)",
        user_id=session["user_id"], symbol=stock["symbol"], shares=0-shares, price=stock["price"])

        # update the users cash to reflect the sale
        db.execute("UPDATE users SET cash=:updated_cash WHERE id=:id", updated_cash=updated_cash, id=session["user_id"])

        # flash a message that the sale was successful
        flash("Share sold!")

        # redirect user back to sell.html
        return redirect("/sell")

    # get request condition will display sell.html
    else:
        return render_template("sell.html")


@app.route("/add_cash", methods=["GET", "POST"])
@login_required
def add_cash():
    """Add cash to account"""

    # get request will display the add_cash.html page which displays the user's total cash currently available.
    # along with a form to request more cash if they run out.
    if request.method == "GET":

        # select to get users current cash
        rows = db.execute("SELECT cash FROM users WHERE id=:id", id=session["user_id"])
        cash = rows[0]["cash"]

        # returns the add_cash.html page using the cash variable in USD to display their current cash
        return render_template("add_cash.html", cash=usd(cash))

    # post request condition
    else:

        # if user does not enter a cash amount greater than 0, return an error that cash amount greater than 0 needs to be added
        if not request.form.get("cash_amount"):
            return apology("Please enter positive amount of cash", 403)

        # get the amount of cash a user would like to add from cash_amount field in form on add_cash.html
        added_cash = int(request.form.get("cash_amount"))
        rows = db.execute("SELECT cash FROM users WHERE id=:id", id=session["user_id"])
        cash = rows[0]["cash"]

        # once an amount is entered, update the user's total cash by adding the cash_amount ent
        updated_cash = added_cash + cash

        db.execute("UPDATE users SET cash=:updated_cash WHERE id=:id", updated_cash=updated_cash, id=session["user_id"])

        flash("Cash Added!")
        return redirect("/")



def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
