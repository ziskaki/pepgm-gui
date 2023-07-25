import logging
import os
import subprocess
import threading
import webbrowser
from pathlib import Path

import numpy as np
import yaml
from flask import Flask, render_template, request, send_file


def get_absolute_file_path(*path_components):
    """ Get absolute file path, given the script path."""
    script_dir = Path("__file__").resolve().parent
    print(script_dir)
    absolute_path = script_dir / Path(*path_components)
    return absolute_path.as_posix()


def get_float_range(start, end, step):
    """ Generate a list of numbers with a given range and step size."""
    return np.round(np.arange(start, end + step, step), 2).tolist()


def get_form_value(request, field_name, default_value=str()):
    """ Get form value from a text input field. """
    value = request.form.get(field_name)
    return value if value else default_value


def get_file_path_from_form(request, field_name):
    """ Get form value from a file upload field. """
    file_name = request.files[field_name].filename
    search_directory = Path("__file__").resolve().parents[1]
    matching_files = str(list(search_directory.glob('**/' + file_name))[0])

    return matching_files


app = Flask(__name__)

CONST_FILE = get_absolute_file_path(os.path.dirname(__file__), "config", "const.yaml")


def load_config():
    """Loads the configuration from the config.yaml file."""
    with open(CONST_FILE, 'r') as config_file:
        return yaml.safe_load(config_file)


config = load_config()

RESOURCES_DIR = config['resources_dir']
DATA_DIR = f"{RESOURCES_DIR}SampleData/"
DATABASE_DIR = f"{RESOURCES_DIR}Database/"
RESULTS_DIR = config['results_dir']
KEYS = config['keys']



def extract_configs_from_request():
    """
    Extracts configurations from the request object.

    Returns:
        dict: Extracted configuration values.
    """
    # Get the radio button values
    alpha_choice = get_form_value(request, "whichAlpha")
    # Assign default values or generate increments based on radio button selection
    alpha = (
        [0.01, 0.05, 0.10, 0.20, 0.40, 0.60] if alpha_choice == '1'
        else get_float_range(
            float(get_form_value(request, "alphaStart")),
            float(get_form_value(request, "alphaEnd")),
            float(get_form_value(request, "alphaStepSize"))
        )
    )

    beta_choice = get_form_value(request, "whichBeta")
    beta = (
        [0.01, 0.05, 0.10, 0.20, 0.40, 0.50, 0.70] if beta_choice == '1'
        else get_float_range(
            float(get_form_value(request, "betaStart")),
            float(get_form_value(request, "betaEnd")),
            float(get_form_value(request, "betaStepSize"))
        )
    )

    prior_choice = '1'
    prior = (
        [0.10, 0.30, 0.50] if prior_choice == '1'
        else get_float_range(
            float(get_form_value(request, "priorStart")),
            float(get_form_value(request, "priorEnd")),
            float(get_form_value(request, "priorStepSize"))
        )
    )

    configs = {key: get_form_value(request, key) for key in KEYS}
    configs["SamplePath"] = get_file_path_from_form(request, "SamplePath")
    configs["ParametersFile"] = get_file_path_from_form(request, "ParametersFile")
    configs["FilterSpectra"] = configs["FilterSpectra"] == '1'
    configs["AddHostandCrapToDB"] = not configs["FilterSpectra"]
    configs["DataDir"] = DATA_DIR
    configs["DatabaseDir"] = DATABASE_DIR
    configs["ResultsDir"] = RESULTS_DIR
    configs["ResourcesDir"] = RESOURCES_DIR
    configs["SearchGUI"] = get_file_path_from_form(request, "SearchGUI")
    configs["PeptideShaker"] = get_file_path_from_form(request, "PeptideShaker")
    configs["TaxidMapping"] = "taxidMapping/"
    configs["searchengines"] = configs["searchengines"]
    configs["TaxaInPlot"] = int(configs["nTaxa"])
    configs["Alpha"] = alpha
    configs["Beta"] = beta
    configs["prior"] = prior

    return configs


def create_and_write_yaml(configs, config_file_path):
    """
    Creates a YAML file from the given configurations and writes it to the specified file path.

    Args:
        configs (dict): Configuration values.
        config_file_path (str): File path to write the YAML file.
    """
    yaml_string = yaml.dump(configs, default_flow_style=None)
    print(yaml_string)
    with open(config_file_path, 'w') as config_file:
        config_file.write(yaml_string)


@app.route('/run_snakemake', methods=['POST'])
def run_snakemake():
    """
    Retrieve the number of cores and execute the Snakemake workflow.

    Returns:
        str: Success message.
    """
    config_file_path = get_absolute_file_path("config", "config.yaml")
    with open(config_file_path, 'r') as config_file:
        configs = yaml.safe_load(config_file)

    command = [
        f"pwd ; snakemake --use-conda --conda-frontend conda --cores {configs['nCores']}"
    ]
    subprocess.run(command, shell=True)
    return "Pipeline executed!"


@app.route('/create_file', methods=['POST'])
def create_file_route():
    """
    Create and send the configuration file as a response.

    Returns:
        flask.Response: File attachment response.
    """
    try:
        configs = extract_configs_from_request()
        config_file_path = get_absolute_file_path("config", "config.yaml")
        create_and_write_yaml(configs, config_file_path)
        return send_file(config_file_path, as_attachment=True)
    except Exception as e:
        logging.exception("Exception in /create_file route")
        return str(e), 500


@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Render the index page.

    Returns:
        flask.Response: Rendered HTML template.
    """
    return render_template('index.html')


def start_server():
    app.run()  # Start the Flask development server


def open_browser():
    webbrowser.open('http://localhost:5000')  # Open the browser with the desired URL


if __name__ == '__main__':
    # Start the Flask development server in a separate thread
    server_thread = threading.Thread(target=start_server)
    server_thread.start()

    # Open the browser
    open_browser()