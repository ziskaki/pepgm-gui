/* Creates an input element of type file and sets its accept attribute to allow only YAML files. */

function loadConfigFile() {
    const input = document.createElement('input');
    input.type = 'file';
    // Accept yaml files only
    input.accept = '.yaml, .yml';

    // When a file is selected, the function reads it and loads its content into the input fields of the form.
    input.addEventListener('change', () => {
    const file = input.files[0];
    const reader = new FileReader();
    reader.readAsText(file);

    // When the file is loaded,
    // the YAML string is parsed into a JavaScript object
    // and its values are set to the corresponding input fields.
    reader.onload = () => {
        const yamlString = reader.result;
        const inputObj = jsyaml.load(yamlString);

        // Text fields
        document.querySelector('input[name="APImail"]').value = inputObj['APImail'];
        document.querySelector('input[name="APIkey"]').value = inputObj['APIkey'];
        document.querySelector('input[name="ExperimentName"]').value = inputObj['ExperimentName'];
        document.querySelector('input[name="SampleName"]').value = inputObj['SampleName'];
        document.querySelector('input[name="HostName"]').value = inputObj['HostName'];
        document.querySelector('input[name="ReferenceDBName"]').value = inputObj['ReferenceDBName'];
        document.querySelector('input[name="ScientificHostName"]').value = inputObj['ScientificHostName'];

        // Radio button selector
        let filterOption = inputObj['FilterSpectra'];
        document.getElementById('FilterSpectra').checked = filterOption;
        document.getElementById('AddHostandCrapToDB').checked = !filterOption;

        // Search engine selector
        let searchEngine = inputObj['searchengines'];
        var selectElement = document.getElementById('searchengines');
        selectElement.value = searchEngine;


        // PSM FDR level
        let psmFDR = inputObj['psmFDR'];
        var psmFDRSlider = document.getElementById('psmFDR');
        psmFDRSlider.value = psmFDR;
        document.getElementById('psmFDR-value').textContent = psmFDR;

        // Peptide FDR level
        let peptideFDR = inputObj['peptideFDR'];
        var peptideFDRSlider = document.getElementById('peptideFDR');
        peptideFDRSlider.value = peptideFDR;
        document.getElementById('peptideFDR-value').textContent = peptideFDR;

        // Protein FDR level
        let proteinFDR = inputObj['proteinFDR'];
        var proteinFDRSlider = document.getElementById('proteinFDR');
        proteinFDRSlider.value = proteinFDR;
        document.getElementById('proteinFDR-value').textContent = proteinFDR;

        // Grid search selector
        let alphaValues = inputObj['Alpha'].map(value => parseFloat(value));
        let alphaStart = alphaValues[0];
        let alphaEnd = alphaValues[alphaValues.length - 1];
        let alphaStepSize = alphaValues[1] - alphaValues[0];
        document.querySelector('input[name="alphaStart"]').value = alphaStart;
        document.querySelector('input[name="alphaEnd"]').value = alphaEnd;
        document.querySelector('input[name="alphaStepSize"]').value = alphaStepSize;

        let betaValues = inputObj['Alpha'].map(value => parseFloat(value));
        let betaStart = betaValues[0];
        let betaEnd = betaValues[betaValues.length - 1];
        let betaStepSize = betaValues[1] - betaValues[0];
        document.querySelector('input[name="betaStart"]').value = betaStart;
        document.querySelector('input[name="betaEnd"]').value = betaEnd;
        document.querySelector('input[name="betaStepSize"]').value = betaStepSize;

        let priorValues = inputObj['prior'].map(value => parseFloat(value));
        let priorStart = priorValues[0];
        let priorEnd = priorValues[priorValues.length - 1];
        let priorStepSize = priorValues[1] - priorValues[0];
        document.querySelector('input[name="priorStart"]').value = priorStart;
        document.querySelector('input[name="priorEnd"]').value = priorEnd;
        document.querySelector('input[name="priorStepSize"]').value = priorStepSize;
        };
    });
      // Click the input element to open the file dialog for selecting a file.
      input.click();
}


function runSnakemake() {
  fetch('/run_snakemake', {method: 'POST'})
    .then(response => response.json())
    .then(data => console.log(data))
    .catch(error => console.error(error));
}


function updateValue(id, value) {
    document.getElementById(id).textContent = value;
}


function ajaxCall() {
    $(document).ready(function() {
    });
}


function checkFields() {
      var inputs = document.getElementsByTagName('input');
      for (var i = 0; i < inputs.length; i++) {
        var input = inputs[i];
        if (input.value === '' && input.name !== 'mail' && input.name !== 'key') {
          // Display a pop-up window
          alert('Please fill in all the required fields.');
          return false;
        }
      }
      return true;
}
