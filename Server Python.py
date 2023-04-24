from flask import Flask, render_template, request
import csv

app = Flask(__name__)
messages = []


@app.route('/')
def wifi_tool():
    return render_template('wifi_tool.html')

@app.route('/run_test', methods=['POST'])
def run_test():
    test_name = request.form['test_name']


    if test_name == 'button1':

        # Read the SSIDs from the csv file
        with open('/home/cameronmuihread/mysite/templates/ssid.csv', 'r') as f:
            reader = csv.reader(f)
            ssids = [row[0].strip() for row in reader]

        match = False #Setting it as a default value

        # Get the SSID from the message
        ssid = next((message.split('You are connected to: ')[1] for message in messages if 'You are connected to:' in message), None)
        # Check if there is a match between connected SSID and SSIDs in CSV file
        if ssid in ssids:
            match = "True"

        # Define data dictionary with match variable included
        data = {
            'ssid': [message for message in messages if 'You are connected to:' in message],
            'security': [message for message in messages if 'Security protocol for' in message],
            'ip': [message for message in messages if 'IP Address:' in message],
            'match': match
        }

        return render_template('button1.html', data=data)

    elif test_name == 'button2':
        data = {
            'list': [message for message in messages if '[' in message],
            'port': [message for message in messages if 'Port' in message]
                }
        return render_template('button2.html', data=data)


    elif test_name == 'button3':
        data = {
            'ssid': [message for message in messages if 'SSID' in message],
            'signal': [message for message in messages if 'Signal' in message],
            'security': [message for message in messages if 'Security:' in message]
                }
        return render_template('button3.html', data=data)


    elif test_name == 'button4':
        data = {
            'vpn': [message for message in messages if 'VPN:' in message],
                }
        return render_template('button4.html', data=data)


    elif test_name == 'button5':
        return render_template('button5.html')


    elif test_name == 'Client Data':
        return render_template('index.html', messages=messages)
    else:
        return 'Invalid test name'


@app.route('/send_message', methods=['POST'])
def send_message():
    message = request.json.get('message')
    print(f'Received message: {message}')
    messages.append(message)
    return f'Message received: {message}'

if __name__ == '__main__':
    app.run(debug=True)