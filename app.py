from flask import Flask

app = Flask(__name__)

isOpen = False

@app.route('/open')
def opendoor():
    isOpen = True
    writeStatus(isOpen)
    return 'Garage is Open'

@app.route('/close')
def close():
    isOpen = False
    writeStatus(isOpen)
    return 'Garage is Closed'


@app.route('/status')
def status():
    
    return readStatus()
    
    status = "closed"

    if(isOpen):
        status = "open"
    
    return 'Garage is ' + str(isOpen)

def writeStatus(isOpen):
    with open("state.txt", "r+") as f:
        f.seek(0)
        f.write(str(isOpen))
        f.truncate()
        f.close()


def readStatus():
    data="failed"
    with open("state.txt", "r+") as f:
        data = f.read()
        f.close()
   

    return data



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')