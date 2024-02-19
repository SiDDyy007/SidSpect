import streamlit as st
import pandas as pd
import plotly.express as px
from wikipathways_processing import get_metabolites_from_wikipathways  

# Load the Redu file
@st.cache_data
def get_datasets():
    st.title("SidSpec @ Wang Bioinformatics Lab")
    st.image('sidspec_logo.png', width=100)
    t1 = pd.read_csv('Redu_Latest.tsv', sep='\t').drop_duplicates()
    t2 = pd.read_csv('Redu_all_sampleinformation.tsv', sep='\t')
    return (t1, t2)

#Get metabolites from WikiPathway
@st.cache_data
def get_metabolites(wikipath_id):
    return get_metabolites_from_wikipathways(wikipath_id)

redu_df, wang_df = get_datasets()
wp_id = st.text_input('Enter the WikiPathways ID:')

if wp_id:
    wp_df = get_metabolites(wp_id)

    # Check if 'InChI' column exists and is not empty
    if 'InChI' in wp_df.columns and not wp_df['InChI'].empty:
        # Extract InChIKeys from 'InChI' column, filter valid ones, and get unique values
        wp_inchikeys = wp_df['InChI'].astype(str).str.split(':', expand=True)[1].fillna('')

        # Filter wp_df to keep only rows with valid InChIKeys
        wp_df_filtered = wp_df[wp_inchikeys.str.match('^[A-Z]{14}-[A-Z]{10}-[A-Z]$')]

        # Now, concatenate 'Label' with filtered 'InChIKeys'
        wp_df_filtered['Label_InChIKey'] = wp_df_filtered['Label'] + ' (' + wp_df_filtered['InChI'].astype(str).str.split(':', expand=True)[1] + ')'

        # Count the number of files for each InChIKey in wp_df_filtered
        inchikey_file_counts = {label_inchikey: redu_df[redu_df['full_inchi_key'] == label_inchikey.split(' (')[-1].strip(')')]['filename'].nunique() 
                                for label_inchikey in wp_df_filtered['Label_InChIKey'].unique()}
        

        # Sort the dictionary by count in descending order
        inchikey_file_counts = sorted(inchikey_file_counts.items(), key=lambda item: item[1], reverse=True)

        # Display the count information
        st.write("Click on an InChIKey to view details:")
        for label_inchikey, count in inchikey_file_counts:
            inchikey = label_inchikey.split(' (')[-1].strip(')')
            label = label_inchikey.split(' (')[0]
            if count and st.button(f"{label} ({inchikey}): {count} files"):
                selected_inchikey = inchikey
                filtered_filenames = redu_df[redu_df['full_inchi_key'] == selected_inchikey]['filename'].drop_duplicates().unique()
                matching_wang_data = wang_df[wang_df['filename'].isin(filtered_filenames)].drop_duplicates()
                # Display the filtered data from wang_df
                st.write("Matching files:")
                st.dataframe(matching_wang_data)

                def plot_pie_chart(filtered_data, wang_df, column_name):
                    # Count occurrences of each unique value in the filtered data
                    filtered_counts = filtered_data[column_name].value_counts()

                    # Pie chart for the percentage distribution
                    fig_pie = px.pie(filtered_counts, names=filtered_counts.index, values=filtered_counts,
                                    title=f'Percentage Distribution of {column_name} in Filtered Data')
                    st.plotly_chart(fig_pie)

                    # Count occurrences of each unique value in wang_df
                    wang_counts = wang_df[column_name].value_counts()

                    # Calculate the percentage of matching rows in filtered_data compared to wang_df for each unique value
                    percentage = (filtered_counts / wang_counts.reindex(filtered_counts.index)) * 100

                    # Create a DataFrame for histogram
                    histogram_df = pd.DataFrame({
                        'Value': filtered_counts.index,
                        'Percentage': percentage
                    }).fillna(0)  # Fill NaN values with 0

                    # Histogram for comparing percentages
                    fig_histogram = px.bar(histogram_df, x='Value', y='Percentage',
                                        title=f'Percentage of Matching Rows vs Total rows for {column_name}',
                                        labels={'Percentage': 'Percentage (%)'})
                    st.plotly_chart(fig_histogram)

                # Plot histograms and display percentages for each column
                for column in ["SampleExtractionMethod", "IonizationSourceAndPolarity", "ChromatographyAndPhase"]:
                    if column in matching_wang_data.columns:
                        plot_pie_chart(matching_wang_data, wang_df, column)
                    else:
                        st.write(f"The column '{column}' is not in the DataFrame.")
