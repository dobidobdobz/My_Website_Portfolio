from flask import Flask, render_template, request, , jsonify
import smtplib
import os

# Environment variables to be kept confidential
MAIL = os.environ.get("MAIL")
PASS = os.environ.get("PASS")
T0_MAIL = os.environ.get("T0_MAIL")
HOST = os.environ.get("HOST")
# PORT = os.environ.get("PORT")

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

is_tic_tac_toe = False


# server url & renders specific html template according conditional GET OR POST request.
@app.route("/", methods=["GET", "POST"])
def home():

    # using request.headers to get the "User-agent" clients Operating system, broswer, and what device is being used 
    user_device = request.headers.get('User-agent')

    # Is set to false until detected otherwise in if statements
    is_mobile_device = False
    is_iphone = False

    # If conditional searches if CLient connecting to website is Mobile or Iphone
    if "Mobile" in user_device or "iPhone" in user_device:

        # if conditional that confirms if its android or iphone
        if "iPhone" in user_device:

            #sets to True if detected
            is_iphone = True
            is_mobile_device = True

            # if condition to execute post request  
            if request.method == "POST":
                
                # data input from CONTACT FORM, id=email in HTML form & from id=name in HTML form etc.
                name_on_form = request.form.get("name")
                email_on_form = request.form.get("email")
                message_on_form = request.form.get("message")
                
                # error handling to display feedback to client if MSG / email sent was successful or not from CONTACT FORM!
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
                    # renders feedback if successful in html
                    mail_sent_successfully = f"Thank you, {name_on_form}, your message has been sent!"
                    return render_template("index.html", mail_sent_successfully=mail_sent_successfully, is_mobile_device=is_mobile_device, is_iphone=is_iphone)
               
                except:
                    # renders feedback if error occurs in html
                    mail_sent_error = f"Error! your message has been not sent!"
                    # passes it into the frontend! client side HTML and renders home() / index html 
                    return render_template("index.html", mail_sent_error=mail_sent_error, is_mobile_device=is_mobile_device, is_iphone=is_iphone)
            
            
            # passes it into the frontend! client side HTML and renders home() / index html 
            return render_template("index.html", is_mobile_device=is_mobile_device, is_iphone=is_iphone)

        # If not iphone and it is_mobile_device = True, passed into frontend HTML!
        else:    
            
            is_mobile_device = True

            # condition to execute post request
            if request.method == "POST":
                # data input from CONTACT FORM, id=email in HTML form & from id=name in HTML form etc.
                name_on_form = request.form.get("name")
                email_on_form = request.form.get("email")
                message_on_form = request.form.get("message")
                
                # error handling to display feedback to client if MSG / email sent was successful or not from CONTACT FORM!
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
                    # renders feedback if successful in html
                    mail_sent_successfully = f"Thank you, {name_on_form}, your message has been sent!"
                    return render_template("index.html", mail_sent_successfully=mail_sent_successfully, is_mobile_device=is_mobile_device)
                    
                except:
                    # renders feedback if error occurs in html
                    mail_sent_error = f"Error! your message has been not sent!"
                    # passes it into the frontend! client side HTML and renders home() / index html 
                    return render_template("index.html", is_mobile_device=is_mobile_device, mail_sent_error=mail_sent_error)
                    
            else: 
                return render_template("index.html", is_mobile_device=is_mobile_device)
            
    # if not mobile or iphone else: its desktop!        
    else:
        # if condition to execute post request  
        if request.method == "POST":
            # data input from CONTACT FORM, id=email in HTML form & from id=name in HTML form etc.
            name_on_form = request.form.get("name")
            email_on_form = request.form.get("email")
            message_on_form = request.form.get("message")
            # error handling to display feedback to client if MSG / email sent was successful or not from CONTACT FORM!
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
                # renders feedback if successful in html
                mail_sent_successfully = f"Thank you, {name_on_form}, your message has been sent!"
                return render_template("index.html", mail_sent_successfully=mail_sent_successfully, is_mobile_device=is_mobile_device)
            except:
                # renders feedback if error occurs in html
                mail_sent_error = f"Error! your message has been not sent!"
                return render_template("index.html", mail_sent_error=mail_sent_error, is_mobile_device=is_mobile_device)
        # renders html file with is_mobile = False         
        else:
            return render_template("index.html", is_mobile_device=is_mobile_device, board=game.board, is_tic_tac_toe=is_tic_tac_toe)


@app.route("/", methods=["GET", "POST"])
def home_tic_tac_toe():
    return render_template("index.html", board=game.board)


@app.route("/make_move", methods=["POST"])
def make_move():
    data = request.get_json()
    position = data["position"]
    if game.make_move(position):
        winner = game.check_winner()
        winning_combination = game.get_winning_combination()
        return jsonify({ "status": "success", "winner": winner, "board": game.board, "winning_combination": winning_combination})
    else:
        return jsonify({'status': "error", "message": "invalid move"})


@app.route("/restart", methods=["POST"])
def clear():
    game.reset_board()
    return jsonify({ "status": "success" })


@app.route('/toggle_tic_tac_toe', methods=['POST'])
def toggle_tic_tac_toe():
    global is_tic_tac_toe  # Access the global variable
    is_tic_tac_toe = True   # Change the constant to True
    return jsonify({'status': 'success', 'is_tic_tac_toe': is_tic_tac_toe})


# runs flask server in debug mode applying changes as they are made.
if __name__ == '__main__':
    app.run(debug=True)
