try:
    
    from flask import Flask
    import RPi.GPIO as GPIO
    import time

    GPIO.setmode(GPIO.BOARD);
    GPIO.setup(7,GPIO.OUT);
    GPIO.output(7,True);
    


    app = Flask(__name__)

    isOpen = False

    @app.route('/open')
    def opendoor():
        isOpen = True
        writeStatus(isOpen)
        #Toggle Twice Because of Stop State
        toggleSwitch();
        toggleSwitch();
        
        return 'Garage is Open'

    @app.route('/close')
    def close():
        isOpen = False
        writeStatus(isOpen)
        #Toggle Twice Because of Stop State
        toggleSwitch();
        toggleSwitch();
        
        return 'Garage is Closed'

    @app.route('/toggle')
    def toggle():
        isOpen = readStatus()
        writeStatus(not isOpen) #Toggle to the Opposite Status
        toggleSwitch();    
        return 'Garage has been Toggled'

    @app.route('/status')
    def status():
        status = "closed"
        isOpen = readStatus()
        if(isOpen):
            status = "open"
        return 'Garage is ' + status

    def toggleSwitch():
        print("Handling Sequence")
        GPIO.output(7,False);
        time.sleep(3)
        GPIO.output(7,True);
        


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
        return str_to_bool(data)

    def str_to_bool(s):
        if s == 'True':
            return True;
        elif s == 'False':
            return False;
        else:
            raise ValueErrorflask  

    if __name__ == '__main__':
        app.run(debug=True,port=5000, host='0.0.0.0')
        
finally:
    print("Handling Cleanup")
    GPIO.cleanup();