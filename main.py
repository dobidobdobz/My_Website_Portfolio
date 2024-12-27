from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
from flask import Flask, render_template, request, jsonify
import smtplib
import os

# Environment variables to be kept confidential
MAIL = os.environ.get("MAIL")
PASS = os.environ.get("PASS")
T0_MAIL = os.environ.get("T0_MAIL")
HOST = os.environ.get("HOST")

# starting flask server
app = Flask(__name__)

class TicTacToe:

    def __init__(self):
        self.board = [' ']*9
        self.current_player = "X"
        self.winning_combinations = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]

    def make_move(self, position):
        if self.board[position] == ' ':
            self.board[position] = self.current_player
            self.current_player = "O" if self.current_player == "X" else "X"
            return True
        return False

    def check_winner(self):
        for combo in self.winning_combinations:
            if self.board[combo[0]] == self.board[combo[1]] == self.board[combo[2]] != ' ':
                return self.board[combo[0]]
        if ' ' not in self.board:
            return "Tie"
        return None

    def get_winning_combination(self):
        for combo in self.winning_combinations:
            if self.board[combo[0]] == self.board[combo[1]] == self.board[combo[2]] != ' ':
                return combo
        return None

    def reset_board(self):
        self.board = [' ']*9

game = TicTacToe()

# Initialize the constant
is_tic_tac_toe = False

# Creates an instance of the scheduler
scheduler = BackgroundScheduler()

# server url & renders specific html template according conditional GET OR POST request.
@app.route("/", methods=["GET", "POST"])
def home():
    global is_tic_tac_toe

    # using request.headers to get the "User-agent" clients Operating system, browser, and what device is being used
    user_device = request.headers.get('User-agent')

    # Is set to false until detected otherwise in if statements
    is_mobile_device = False
    is_iphone = False

    # If conditional searches if CLient connecting to website is Mobile or Iphone
    if "Mobile" in user_device or "iPhone" in user_device:
        if "iPhone" in user_device:
            is_iphone = True
            is_mobile_device = True
        else:    
            is_mobile_device = True

        if request.method == "POST":
            # data input from CONTACT FORM, id=email in HTML form & from id=name in HTML form etc.
            name_on_form = request.form.get("name")
            email_on_form = request.form.get("email")
            message_on_form = request.form.get("message")
            try:
                # executes sending email with data
                connection = smtplib.SMTP(host=HOST, port=587)
                connection.starttls()
                connection.login(user=MAIL, password=PASS)
                connection.sendmail(
                    to_addrs=T0_MAIL,
                    from_addr=MAIL,
                    msg=f"From:CONTACT WEB-PORTFOLIO \nSubject: CONTACT ALERT! {name_on_form}! FROM WEBSITE PORTFOLIO! \n\n "
                    f"Client name: {name_on_form}\n"
                    f"Client email: {email_on_form}\n"
                    f"Message from client: {message_on_form}"
                )
                connection.quit()
                mail_sent_successfully = f"Thank you, {name_on_form}, your message has been sent!"
                return render_template("index.html", mail_sent_successfully=mail_sent_successfully, is_mobile_device=is_mobile_device, is_iphone=is_iphone)
            except:
                mail_sent_error = f"Error! your message has been not sent!"
                return render_template("index.html", mail_sent_error=mail_sent_error, is_mobile_device=is_mobile_device, is_iphone=is_iphone)

        return render_template("index.html", is_mobile_device=is_mobile_device, is_iphone=is_iphone, board=game.board, is_tic_tac_toe=is_tic_tac_toe)
    
    # Desktop version handling (not mobile or iPhone)
    else:
        if request.method == "POST":
            name_on_form = request.form.get("name")
            email_on_form = request.form.get("email")
            message_on_form = request.form.get("message")
            try:
                connection = smtplib.SMTP(host=HOST, port=587)
                connection.starttls()
                connection.login(user=MAIL, password=PASS)
                connection.sendmail(
                    to_addrs=T0_MAIL,
                    from_addr=MAIL,
                    msg=f"From:CONTACT WEB-PORTFOLIO \nSubject: CONTACT ALERT! {name_on_form}! FROM WEBSITE PORTFOLIO! \n\n "
                    f"Client name: {name_on_form}\n"
                    f"Client email: {email_on_form}\n"
                    f"Message from client: {message_on_form}"
                )
                connection.quit()
                mail_sent_successfully = f"Thank you, {name_on_form}, your message has been sent!"
                return render_template("index.html", mail_sent_successfully=mail_sent_successfully, is_mobile_device=is_mobile_device)
            except:
                mail_sent_error = f"Error! your message has been not sent!"
                return render_template("index.html", mail_sent_error=mail_sent_error, is_mobile_device=is_mobile_device)

        return render_template("index.html", is_mobile_device=is_mobile_device, board=game.board, is_tic_tac_toe=is_tic_tac_toe)

def reset_tic_tac_toe():
    global is_tic_tac_toe
    is_tic_tac_toe = False  # Reset the constant to False
    print(f"Game state reset at {datetime.now()}")

@app.route('/toggle_tic_tac_toe', methods=['POST'])
def toggle_tic_tac_toe():
    global is_tic_tac_toe  # Access the global variable
    is_tic_tac_toe = True   # Change the constant to True

    # Schedule the reset task to run after 90 seconds
    scheduler.add_job(reset_tic_tac_toe, 'date', run_date=datetime.now() + timedelta(seconds=90))

    print(f"Job scheduled to reset at: {datetime.now() + timedelta(seconds=90)}")
    
    return jsonify({'status': 'success', 'is_tic_tac_toe': is_tic_tac_toe})

# runs flask server in debug mode applying changes as they are made.
if __name__ == '__main__':
    scheduler.start()  # Start the scheduler
    app.run(debug=True)
