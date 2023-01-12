import json
import os

from flask import Flask, render_template
import logging


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True, static_folder='static')
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'feeder.sqlite'),
    )

    @app.route('/')
    def index():
        
        # for flightradar24
        pathToFile = 'feeder/fr24feed.ini'
        with open(pathToFile, 'r') as f:
            lines = f.readlines()
        sharing_key = lines[1].split('=')[1][1:][:-2]

        # for flightaware
        pathToFile = 'feeder/piaware.conf'
        with open(pathToFile, 'r') as f:
            lines = f.readlines()
        feeder_id = lines[-1].split()[1]

        #for opensky
        pathToFile = 'feeder/05-serial.conf'
        with open(pathToFile, 'r') as f:
            lines = f.readlines()
        serial = lines[-1].split(' = ')[1]

        logging.basicConfig(filename='record.log', level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
        # app.logger.info(config.sections())
        
        pathToFile = 'feeder/10-debconf.conf'
        with open(pathToFile, 'r') as f:
            lines = f.readlines()
        
        app.logger.info(lines)
        username = lines[9].split('=')[1]
        
        # for ads-b exhchange
        pathToFile = 'feeder/adsbexchange'
        with open(pathToFile, 'r') as f:
            lines = f.readlines()
        
        app.logger.info(lines)

        user = lines[5].split('=')[1][1:][:-2]

        pathToFile = 'feeder/adsbx-uuid'
        with open(pathToFile, 'r') as f:
            uuid = f.readline()

        #for planefinder

        pathToFile = 'feeder/pfclient-config.json'

        with open(pathToFile, 'r') as f:
            data = json.load(f)
        app.logger.info(data)

        share_code = data.get('sharecode', 'no data')

        return render_template('index.html', 
            sharing_key=sharing_key, 
            feeder_id=feeder_id, 
            serial=serial, 
            username=username,
            user = user,
            uuid = uuid,
            share_code=share_code)



    @app.route('/flightradar-configuration')
    def flightradar_configuration():
        return render_template('/pages/flightradar24/configuration.html')



    @app.route('/flightaware-configuration')
    def flightaware_configuration():
        return render_template('/pages/flightaware/configuration.html')
    
    @app.route('/opensky-configuration')
    def opensky_configuration():
        return render_template('/pages/opensky/configuration.html')
    
    @app.route('/ads-b-configuration')
    def adsb_configuration():
        return render_template('/pages/adsb/configuration.html')
    return app