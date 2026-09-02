import smtplib
import pandas as pd
from email.message import EmailMessage

# Load your Excel file with messages
df = pd.read_excel("C:\\Users\\sachi\\OneDrive\\Desktop\\code\\python\\referralTemplate\\sendingBulkEmail\\personalized_cold_emails.xlsx")

# Email credentials
YOUR_EMAIL = "sachin.sddn@gmail.com"
YOUR_PASSWORD = "gpmw npwc oofs fvqr"

# Setup SMTP
server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
server.login(YOUR_EMAIL, YOUR_PASSWORD)

# Send emails
for i, row in df.iterrows():
    msg = EmailMessage()
    msg['Subject'] = f"Application for Software Engineer Role at {row['Company']}"
    msg['From'] = YOUR_EMAIL
    msg['To'] = row['Email']
    msg.set_content(row['Message'])

    server.send_message(msg)
    print(f"Sent to {row['Contact Name']} at {row['Email']}")

server.quit()