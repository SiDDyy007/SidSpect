from io import StringIO
import pandas as pd
import requests

def get_metabolites_from_wikipathways(wp_id):
    url = f"https://www.wikipathways.org/wikipathways-assets/pathways/{wp_id}/{wp_id}-datanodes.tsv"
    response = requests.get(url)
    
    if response.status_code == 200:
        # Use StringIO to read the TSV content as a file
        tsv_content = StringIO(response.content.decode('utf-8'))
        df = pd.read_csv(tsv_content, sep='\t')

        # Filter rows where 'Type' column is 'Metabolite'
        metabolites = df[df['Type'] == 'Metabolite']
        metabolites = metabolites[pd.notna(metabolites['InChI'])]
        return metabolites
    else:
        raise Exception(f"Error: Unable to download file (Status code: {response.status_code})")


