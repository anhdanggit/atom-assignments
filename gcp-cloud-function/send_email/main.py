def send_email(request):
    """Responds to any HTTP request.
    Args:
        request (flask.Request): HTTP request object.
    Returns:
        The response text or any set of values that can be turned into a
        Response object using
        `make_response <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>`.
    """
    import os
    import json
    import email, smtplib, ssl
    from email import encoders
    from email.mime.base import MIMEBase
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    import datetime as dt # to work with date, time
    import sys

    request_json = request.get_json() #--> get the request json
    if request_json and 'subject' in request_json:
        print('subject ==> {}'.format(request_json['subject']))
    if request_json and 'receiver_email' in request_json:
        print('receiver_email ==> {}'.format(request_json['receiver_email']))
    
    
    ## 1A - Take input from request json
    receiver_email = request_json['receiver_email']
    subject = request_json['subject']
    
    ## 1B - Get ENV set in Cloud
    #sender_email = os.getenv('SENDER_EMAIL') ## PLEASE MEMBER TO SET THE ENV VARIABLES IN YOUR CLOUD FUNC
    sender_email = os.environ.get('SENDER_EMAIL')
    password = os.environ.get('PWD_EMAIL')
    print('=== Step 1: Get Input') 
    
    ## 2 - Email Set
    email = MIMEMultipart()
    email["From"] = sender_email
    email["To"] = receiver_email 
    email["Subject"] = subject


    ## 3 - Email Contents
    # We use html, you can convert word to html: https://wordtohtml.net/
    html1 = """
    <html>
    <h1><strong>Hello World</strong></h1>
    <body>
    <p>Hi!<br>
       How are you?<br>
       Here is the <a href="https://docs.python.org/3.4/library/email-examples.html">link</a> you wanted.
    </p>
    </body>
    </html>
    """
    html2 = """
    <html>
    Email sent at <b>{}</b><br>
    </html>
    """.format(dt.datetime.now().isoformat())

    text3 = '--- End ----'

    # Combine parts
    part1 = MIMEText(html1, 'html')
    part2 = MIMEText(html2, 'html')
    part3 = MIMEText(text3, 'plain')

    email.attach(part1)
    email.attach(part2)
    email.attach(part3)
    print('=== Step 2: Prep Contents')

    ## 4 - Create SMTP session for sending the mail
    try:
        session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
        session.starttls() #enable security
        print('=== Step 3: Enable Security')
        session.login(sender_email, password) #login with mail_id and password
        print('=== Step 4: Login Success!')
        text = email.as_string()
        session.sendmail(sender_email, receiver_email, text)
        session.quit()
        print('DONE! Mail Sent from {} to {}'.format(sender_email, receiver_email))
        message = 'DONE! Mail Sent from {} to {}'.format(sender_email, receiver_email)
        status = 'OK'
    except:
        print('=== ERROR: {}'.format(sys.exc_info()[0]))
        message = 'ERROR: {}'.format(sys.exc_info()[0])
        status = 'FAIL'

    
    out = {'status': status, 'message': message}
    headers= {
        'Access-Control-Allow-Origin': '*',
        'Content-Type':'application/json'
        }
    return (json.dumps(out), 200, headers)