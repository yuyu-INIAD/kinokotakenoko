from flask import Flask, render_template, request
app = Flask(__name__)

import re
kinoko_count = 3
takenoko_count = 5
messages = ["kinoko is wonderful!", "takenoko is awesome!"]

@app.route('/')
def top():
    return render_template('index.html', **vars())

@app.route('/vote', methods=['POST'])
def answer():
    global kinoko_count,takenoko_count,messages
    if request.form.get("item") == "kinoko":
        kinoko_count += 1
    elif request.form.get("item") == "takenoko":
        takenoko_count += 1
    messages.append(request.form.get("message"))
    if len(messages) > 3:
        messages = messages[-3:]
    print(request.form,kinoko_count,takenoko_count)
    kinoko_percent = kinoko_count / (kinoko_count + takenoko_count) * 100
    takenoko_percent = takenoko_count / (kinoko_count + takenoko_count) * 100
    message_html = ""
    for i in range(len(messages)):
        message = messages[i]
        message = re.sub(r'&', r'&amp', message)
        message = re.sub(r'<', r'&lt', message)
        message = re.sub(r'<', r'&gt', message)
        message = re.sub(r'\*(.+)\*', r'<strong>\1</strong>', message)
        message = re.sub(r'(0[789]0)-\d+-\d+', r'\1-****_****', message)
        message_html += '<div class="alert {1}" role="alert">{0}</div>\n'.format(
            message, 'alert-warning ms-5' if i % 2 == 0 else 'alert-success me-5')
        message = re.sub(r"(htt?ps//[a-zA-z./]+.*)", r'<a href="\1">\1</a>',message)
    return render_template('vote.html', **vars())

if __name__ == '__main__':
    app.run(debug=True)
