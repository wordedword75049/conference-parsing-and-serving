from typing import Tuple, Dict, Union
from flask import Flask, request, render_template, send_file, abort
import os
import logging
import logging.config
from settings import LOGGING_CONFIG

app = Flask(__name__)
filesave_path = os.getenv("REGISTRY_STORAGE", '/server/persistent-data')

logging.config.dictConfig(LOGGING_CONFIG)
app_logger = logging.getLogger('app.endpoints')

def status_response(message: str, status: int) -> Tuple[Dict[str, Union[str, int]], int]:
    return {'response': message, 'status': status}, status


@app.route('/')
def hello():
    try:
        files = os.listdir(filesave_path)
        return render_template('listing.html', files=files)
    except Exception:
        message = 'Something went wrong while serving url: ' + request.full_path[:-1]
        app_logger.error(message)
        return status_response(message, 500)


@app.route('/healthcheck')
def healthcheck():
    print('hello')
    app_logger.info('Hello from healthcheck, everything looks ok')
    return 'Hello very World!'


@app.route('/<path:subpath>')
def list_conferences(subpath):
    try:
        abs_path = os.path.join(filesave_path, subpath)

        # Return 404 if path doesn't exist
        if not os.path.exists(abs_path):
            return abort(404)

        # Check if path is a file and serve
        if os.path.isfile(abs_path):
            return send_file(abs_path)

        # Show directory contents
        files = os.listdir(abs_path)
        return render_template('listing.html', files=files, prefix='')
    except Exception:
        message = 'Something went wrong while serving url: ' + request.full_path[:-1]
        app_logger.exception(message)
        return status_response(message, 500)


@app.route('/upload', methods=['POST'])
def upload():
    try:
        filetype = request.args.get('type')
        conference = request.args.get('conference')
        year = request.args.get('year')
        absolute_path = filesave_path + '/' + conference + '/' + year + '/' if filetype != 'registry' else filesave_path + '/registry/'
        if filetype == 'image':
            absolute_path += 'images/'
        if not os.path.exists(absolute_path):
            os.makedirs(absolute_path)
        file = request.files['file']
        filename_for_save = file.filename.split('/')[-1] if filetype != 'registry' else conference + '_' + year + '.csv'
        if not os.path.exists(absolute_path + filename_for_save):
            file.save(absolute_path + filename_for_save)
        message = "File " + filename_for_save + " saved succesfully"
        app_logger.info(message)
        return status_response(message, 200)
    except Exception:
        message = "Error encountered while saving file " + filename_for_save
        app_logger.exception(message)
        return status_response(message, 500)



def check_path(path):
    if not os.path.exists(path):
        os.makedirs(path)


def save_file(path, filename, file):
    files_unique = True
    try:
        if not os.path.exists(path + filename):
            file.save(path + filename)
            message = "File " + filename + " saved succesfully"
            app_logger.info(message)
        else:
            message = "File " + filename + " already exists. Happily doing nothing"
            app_logger.info(message)
            files_unique = False
        return files_unique
    except Exception:
        message = f"Error encountered while saving file {filename}"
        app_logger.exception(message)


if __name__ == '__main__':
    app.run()
