import argparse
from os.path import exists

from FactorGraphGeneration import *

if __name__ == "__main__":
    # argparse preliminaries
    parser = argparse.ArgumentParser(description='Run the PepGM algorithm from command line')
    parser.add_argument('--targetTaxa', type=str, nargs=1,
                        help='Path to text file with taxids. Format requirements: one taxid per line.')
    parser.add_argument('--PSM_Report', type=str, required=True,
                        help='Path to PSM report (PeptideShaker output).')
    parser.add_argument('--PeptideMapPath', type=str, required=True,
                        help='Path to mapped taxon peptide pairs (json file).')
    parser.add_argument('--out', type=str, required=True,
                        help='Output directory')
    parser.add_argument('--sourceDB', type=str, nargs='?', const='', default="all[FILT]",
                        help='Name of the DB queried through Entrez.')
    parser.add_argument('--APIkey', type=str, const="", help='your NCBI API key if you have one', nargs="?")
    parser.add_argument('--APImail', help='e-mail connected to your NCBI API key', const="", nargs="?")
    args = parser.parse_args()

    # e-mail for fetching viral protein sequences from entrez
    if args.APIkey and args.APImail:
        Entrez.email = args.APImail
        Entrez.api_key = args.APIkey

    Entrez.tool = 'PepGM'

    # init networkx graph object
    Taxongraph = TaxonGraph()
    Taxongraph.GetAllLeafTaxaFromTaxids(args.targetTaxa[0])
    # only fetch TaxonData if the PeptideMap File doesn't exist yet:
    if not exists(args.PeptideMapPath):
        print(exists(args.PeptideMapPath))
        Taxongraph.FetchTaxonData(args.PeptideMapPath, args.sourceDB)
    Taxongraph.CreateTaxonPeptidegraphFromPSMresults(args.PSM_Report, args.PeptideMapPath, 0.001)
    # Taxongraph.CreateExample()
    Factorgraph = FactorGraph()
    Factorgraph.ConstructFromTaxonGraph(Taxongraph)
    CTFactorgraph = GenerateCTFactorGraphs(Factorgraph)
    CTFactorgraph.SaveToGraphML(args.out)
