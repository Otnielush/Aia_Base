from application import init_app

app = init_app()

if __name__ == '__main__':
    app.run(host ='192.168.1.15', port="5555")


