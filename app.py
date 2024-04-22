from flask import Flask, render_template, request


app = Flask(__name__)


@app.route('/Welcome_to_LinguaCompare')
def hello():
    user_name1 = "dfghjkl"
    return render_template('LinguaCompare_main.html', name=user_name1)


@app.route('/main_page', methods=['POST', 'GET'])
def main_page():
    if request.method == 'GET':
        return render_template('Welcome_to_LinguaCompare.html')
    elif request.method == 'POST':
        # responce равен вводу пользователя
        responce = request.form['text']
        return "Форма отправлена"


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1', debug=True)


# if __name__ == '__main__':
# *app.run(debug=True)D:/Milena/PycharmProjects/pythonProject_LINGUA_COMPARE
