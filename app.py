import os

from flask import Flask, request
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


app = Flask(__name__)

sg_client = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
subscribers = ['sagnewshreds@gmail.com']


@app.route('/subscribe', methods=['POST'])
def subscribe():
    from_email = request.form['from']
    subscribers.add(from_email)
    return '', 200


@app.route('/report', methods=['POST'])
def blast():
    crime = request.form['crime']

    for email in subscribers:
        send_email('narc@sagnew.com', email, 'RUNESCAPE CRIME ALERT!', crime)

    return '', 200


def send_email(from_email, to_email, subject, body):
    message = Mail(from_email,
                 to_email,
                 subject,
                 body)
    response = sg_client.send(message)
    print(response.headers)


if __name__ == '__main__':
    app.run(debug=True, port=6000)