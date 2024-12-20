from flask import Flask, render_template, request
import smtplib
import os
import darkdetect
import getostheme


# Environment variables to be kept confidential
MAIL = os.environ.get("MAIL")
PASS = os.environ.get("PASS")
T0_MAIL = os.environ.get("T0_MAIL")
HOST = os.environ.get("HOST")
# PORT = os.environ.get("PORT")

# starting flask server
app = Flask(__name__)


# server url & renders specific html template according conditional GET OR POST request.
@app.route("/", methods=["GET", "POST"])
def home():

    user_device = request.headers.get('User-agent')
    print(user_device)
    print(type(user_device))

    is_mobile_safari = False
    is_mobile_chrome = False
    is_mobile_device = False
    is_iphone = False

    if "Mobile" in user_device or "iPhone" in user_device:
        print("found mobile or iPhone in list")
        if "iPhone" in user_device:
            
            is_iphone = True
            is_mobile_device = True
            
            print(f"device is mobile:{is_mobile_device}")
            print(f"device is iphone:{is_iphone}")
            
            if "Chrome" in user_device: 
                is_mobile_chrome = True
                print(f'chrome broswer: {is_mobile_chrome}')
                return render_template("index.html", is_mobile_device=is_mobile_device, is_iphone=is_iphone, is_mobile_chrome=is_mobile_chrome)
            else:
                return render_template("index.html", is_mobile_device=is_mobile_device, is_iphone=is_iphone)
        else:    
            is_mobile_device = True
            print(f"is not a iphone most likely a andriod: {is_mobile_device}")
            return render_template("index.html", is_mobile_device=is_mobile_device)
    else:
        # condition to execute post request
        if request.method == "POST":
            # data input from CONTACT FORM, id=email in HTML form & from id=name in HTML form etc.
            name_on_form = request.form.get("name")
            email_on_form = request.form.get("email")
            message_on_form = request.form.get("message")
            # error handling to display feedback to client if MSG / email sent was successful or not from CONTACT FORM!
            try:
                # executes sending email with data
                connection = smtplib.SMTP(host=HOST, port=int(PORT))
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
        else:
            print(is_mobile_device)
            print(type(is_mobile_device))
            return render_template("index.html", is_mobile_device=is_mobile_device)


# runs flask server in debug mode applying changes as they are made.
if __name__ == '__main__':
    app.run(debug=True)
