from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/api/hello', methods=['GET'])
def hello():
    visitor_name = request.args.get('visitor_name', 'Guest')
    ip = request.remote_addr
    location = get_location(ip)
    temperature = get_temperature(location)
    greeting = f"Hello, {visitor_name}!, The temperature is {temperature} degrees Celsius in {location}."
    response = {
        "client_ip": ip,
        "location": location,
        "greeting": greeting
    }
    return jsonify(response)

def get_location(ip):
    response = requests.get(f"http://ip-api.com/json/{ip}")
    data = response.json()
    location = data.get('city')
    return location

def get_temperature(location):
    api_key = '133b79edd1fa5214bfdcb3de31bbd027'
    response = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric")
    data = response.json()
    temperature = data.get('main', {}).get('temp')
    return temperature

if __name__ == '__main__':
    app.run(host='0.0.0.0')