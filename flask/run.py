from app import app

if __name__ == "__main__":
    #isso faz com que o app rode no IP local da máquina 
    app.run(host='0.0.0.0')