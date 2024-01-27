from flask import Flask, render_template, request
import requests
from datetime import datetime

app = Flask(__name__)

def get_facebook_info(user_id):
    fields = 'id,is_verified,cover,created_time,work,hometown,username,link,name,locale,location,about,website,birthday,gender,relationship_status,significant_other,quotes,first_name,subscribers.limit(0)'
    access_token = 'EAAD6V7os0gcBO3AjmZCI4ZAHEhrdNEgJEWT1f6TNa46215Fwk3vJQkyzDFUwNWrClDZB2r6nF4Pa1HzXRQSlmECuA6BQsf7uZBocKwvDMZASoY0PmXAhYPuoIWeZBrdVJHv2FOSr6WEnZC2VxizDSHuCDtPgxHUZAf9fki67ZABbxid4S6XfN0vjK1v6bmAZDZD'  # Thay YOUR_FACEBOOK_ACCESS_TOKEN bằng token của bạn

    response = requests.get(f"https://graph.facebook.com/{user_id}?fields={fields}&access_token={access_token}")
    data = response.json()
    created_time = data.get('created_time', '')
    
    if created_time:
        created_datetime = datetime.strptime(created_time, '%Y-%m-%dT%H:%M:%S%z')
        created_date = created_datetime.strftime('%d/%m/%Y')
        user_info = {
            'created_date': created_date,
            'name': data.get('name', ''),
        }
        return user_info
    else:
        return {'created_date': "There is no information with this facebook uid", 'name': ''}

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_id = request.form['uid']
        user_info = get_facebook_info(user_id)
        return render_template('result.html', user_id=user_id, user_info=user_info)
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
