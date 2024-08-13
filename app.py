import time
from flask import Flask, Response, json, render_template, request

app = Flask(__name__)



messages = [{'name' : 'Aditya', 'msg' : 'Hi Students 🙋‍♂️'}]

@app.route('/watch-broadcast')
def watch_broadcast():
    return render_template('watch_broadcast.html')


@app.route('/send-broadcast')
def send_broadcast():
    return render_template('send_broadcast.html')

# sse will connect to this endpoint
@app.route('/stream')
def stream():
    preMsg = None
    def response():
        while True:
            nonlocal preMsg
            currMsg = messages[-1]
            if (currMsg != preMsg):
                preMsg = currMsg
                data = json.dumps(currMsg)
                yield f"data: {data}\nevent: message\n\n"
            time.sleep(0.5)
    return Response(response(), mimetype="text/event-stream")


@app.route('/message/<name>/<msg>')
def message(name, msg):
    messages.append({'name' : name, 'msg' : msg})
    print(messages)
    return {'message' : 'message created'}, 200

if (__name__ == "__main__"):
    app.run(debug=True)