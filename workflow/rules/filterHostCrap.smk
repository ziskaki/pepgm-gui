rule AddHostandCrap:
    input:
        DatabaseDirectory + 'crap.fasta',
        DatabaseDirectory + HostName + '.fasta'

    output: DatabaseDirectory + HostName + '+crap.fasta'

    shell: 'cat {input} > {output}'

rule RemoveDuplicatesHostandCrap:
    input: DatabaseDirectory + HostName + '+crap.fasta'
    output: DatabaseDirectory + HostName + '+crap_UNI.fasta'
    conda: 'envs/graphenv.yml'
    shell: 'seqkit rmdup -s {input} > {output}'

rule AddDecoysHostandCrap:
    input: DatabaseDirectory + HostName + '+crap_UNI.fasta'
    output: DatabaseDirectory + HostName + '+crap_UNI_concatenated_target_decoy.fasta'
    shell: 'java -cp ' + SearchGUI + 'eu.isas.searchgui.cmd.FastaCLI -in {input} -decoy'

rule SearchSpectraHostandCrap:
    input:
        SamplePath,
        DatabaseDirectory + HostName + '+crap_UNI_concatenated_target_decoy.fasta',
        ParametersFile
    params:
        samplename=SampleName,
        hostname=HostName,
    output: ResultsDir + SampleName + '/SpectraFilter/' + HostName + '_searchgui_out.zip'
    shell: 'java -cp ' + SearchGUI + ' eu.isas.searchgui.cmd.SearchCLI -spectrum_files {input[0]} -fasta_file {input[1]} -output_folder ' + ResultsDir + '{params.samplename}/SpectraFilter -id_params {input[2]} -output_default_name {params.hostname}_searchgui_out -psm_fdr 1 -peptide_fdr 1 -protein_fdr 1 ' + searchengines + ' 1'

rule RunPeptideShakerHostandCrap:
    input:
        ResultsDir + SampleName + '/SpectraFilter/' + HostName + '_searchgui_out.zip',
        SamplePath,
        DatabaseDirectory + HostName + '+crap_UNI_concatenated_target_decoy.fasta',
    params:
        samplename=SampleName,
        hostname=HostName
    output: ResultsDir + SampleName + '/SpectraFilter/' + HostName + '.psdb'
    shell: 'java -cp ' + PeptideShaker + ' eu.isas.peptideshaker.cmd.PeptideShakerCLI -reference {params.hostname} -fasta_file {input[2]} -identification_files {input[0]} -spectrum_files {input[1]} -out {output}'

rule SimplePeptideListHostandCrap:
    input: ResultsDir + SampleName + '/SpectraFilter/' + HostName + '.psdb'
    output: ResultsDir + SampleName + '/SpectraFilter/' + HostName + '_Default_PSM_Report.txt'
    params:
        samplename=SampleName,
        hostname=HostName

    shell: 'java -cp ' + PeptideShaker + ' eu.isas.peptideshaker.cmd.ReportCLI -in {input} -out_reports ' + ResultsDir + '{params.samplename}/SpectraFilter -reports 3'

rule FilterSpectra:
    input:
        ResultsDir + SampleName + '/SpectraFilter/' + HostName + '_Default_PSM_Report.txt',
        SamplePath
    output: ResultsDir + SampleName + '/SpectraFilter/Filtered_' + HostName + '.mgf'
    conda: 'envs/graphenv.yml'
    shell: "python3 workflow/scripts/filterHostSpectra.py --SpectrumFile {input[1]} --PSMReport {input[0]} --out {output}"
