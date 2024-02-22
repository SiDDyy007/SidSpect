**SidSpec: A Pathway-Informed Tool for Optimizing Metabolomics Experimental Design**

__Overview__

SidSpec bridges the gap between pathway analysis and experiment planning in metabolomics research. Using a WikiPathways identifier as input, SidSpec leverages the GNPS/ReDU repositories to provide insights into successful analytical methods for the metabolites within that pathway. This data-driven guidance supports researchers in selecting the best extraction techniques, chromatography choices, and ionization polarities for their metabolomics experiments.

__Features__

* Seamless integration of WikiPathways pathway data
* InChIKey-based metabolite matching with GNPS/ReDU records
* Statistical summaries of method distribution for pathway compounds
* Interactive visualizations of analytical method usage patterns (histograms, pie charts)
* User-friendly Streamlit web interface

__Setup__

Clone Repository: Clone this repository to your local machine.

__Install Dependencies:__

`pip install -r requirements.txt`

__Download Datasets__

* Download the required GNPS/ReDU dataset from [link to dataset]
* Download any necessary WikiPathways data from [link to WikiPathways]
* Place the downloaded datasets in the root directory of the project.

__Running the Application__

Launch Streamlit: From the project's root directory, execute the following command in your terminal:

`streamlit run app_homepage.py`

__Using SidSpec:__
- The SidSpec interface will launch in your web browser.
- Input a WikiPathways identifier (e.g., WP1234) in the designated field.
- Explore the metabolite summary and visualizations to gain insights into optimal analytical methods.


We welcome contributions, bug reports, and suggestions for improvement. Please feel free to open an issue or submit a pull request.