from flask import Flask, render_template, request, send_file
from datetime import datetime
import csv
import names
import random
import string
import io

app = Flask(__name__, template_folder='/app')

@app.route('/', methods=['GET', 'POST'])
def index():
    download_link = None
    template_var = {}
    if request.method == 'POST':
        if 'nino_dropdown' in request.form:
            value = request.form['nino_dropdown']
            if value == '5k':
                count = 5000
            elif value == '10k':
                count = 10000
            elif value == '20k':
                count = 20000
            elif value == '50k':
                count = 50000
            else:
                count = 0
            if count > 0:
                filename = generate_ninos(count)
                download_link = '/download/{}'.format(filename)
                template_var = {"download_link": download_link, "filename": filename}
        elif 'email_dropdown' in request.form:
            value = request.form['email_dropdown']
            if value == '5k':
                count = 5000
            elif value == '10k':
                count = 10000
            elif value == '20k':
                count = 20000
            elif value == '50k':
                count = 50000
            else:
                count = 0
            if count > 0:
                filename = generate_emails(count)
                download_link = '/download/{}'.format(filename)
                template_var = {"download_link": download_link, "filename": filename}

        elif 'applicant_dropdown' in request.form:
            value = request.form['applicant_dropdown']
            if value == '500':
                count = 500
            elif value == '5k':
                count = 5000
            elif value == '10k':
                count = 10000
            elif value == '20k':
                count = 20000
            elif value == '50k':
                count = 50000
            else:
                count = 0
            if count > 0:
                filename = generate_applicants(count)
                download_link = '/download/{}'.format(filename)
                template_var = {"download_link": download_link, "filename": filename}
    return render_template('index.html', **template_var)

@app.route('/download/<filename>')
def download(filename):
    return send_file(filename, as_attachment=True)

def generate_ninos(count):
    letters1 = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N', 'P', 'R', 'S', 'T', 'W']
    letters2 = ['A', 'B', 'C', 'D']
    generated = set()
    while len(generated) < count:
        s = ''.join([random.choice(letters1) for _ in range(2)])
        s += str(random.randint(100000, 999999))
        s += random.choice(letters2)
        if s not in generated:
            generated.add(s)
    strings = list(generated)
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['Generated NINO Strings'])
    for s in strings:
        writer.writerow([s])
    # Save the CSV file with a unique name and return its filename
    now = datetime.now()
    date_str = now.strftime('%y%m%d%H%M%S')
    filename = 'NINO_' + str(count) + '_' + date_str + '.csv'
    with open('/app/'+ filename, 'w', newline='') as f:
        f.write(output.getvalue())
    return filename

def generate_emails(count):
    domains = ['gmail.com', 'testtest.com', 'testemail.com', 'nftemail.com']
    emails = set()
    while len(emails) < count:
        username = ''.join(random.choice(string.ascii_lowercase) for _ in range(10))
        domain = random.choice(domains)
        email = f'{username}@{domain}'
        emails.add(email)
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['Generated Emails'])
    for email in emails:
        writer.writerow([email])
    # Save the CSV file with a unique name and return its filename
    now = datetime.now()
    date_str = now.strftime('%y%m%d%H%M%S')
    filename = 'Emails_' + str(count) + '_' + date_str + '.csv'
    with open('/app/'+ filename, 'w', newline='') as f:
        f.write(output.getvalue())
    return filename

def generate_applicants(count):
    num_of_records = count
    now = datetime.now()
    date_str = now.strftime('%y%m%d%H%M%S')
    filename = 'Random_Applicant_'+str(num_of_records)+'_'+date_str+'.csv'
    with open('/app/'+ filename, mode ='w', newline='') as file:
        writer = csv.writer(file)

        writer.writerow(['First Name', 'Last Name', 'Day', 'Month', 'Year', 'DOB'])

        for i in range(num_of_records):
            first_name = names.get_first_name()
            last_name = names.get_last_name()
            day = random.randint(1, 28)
            month = random.randint(1, 12)
            year = random.randint(1950, 2000)

            writer.writerow([first_name, last_name, day, month, year, str(day)+'.'+str(month)+'.'+str(year)])
    return filename

if __name__ == '__main__':
    app.run(host='0.0.0.0', port = 5000)