Challenge:

Merge synthetic sales data with economic indicators (gas prices, CPI) from the FRED API.
Automate data fetching, merging, and integrity checks, including anomaly detection and alerts.

###################################################################################

Project Description
- Generates fake sales data for 50 products over a year.
- Retrieves gas prices and CPI from FRED.
- Merges data weekly.
- Identifies missing values and spikes.
- Logs alerts.

###################################################################################

Assumptions

- Every week starts on a Sunday.
- We spot spikes using some basic stats.
- Files are saved right here on our computers.

###################################################################################

Steps to Run :

1. Make sure the listed modules are installed in your system 
    pandas
    numpy
    requests

    How to install : 

    Open Terminal and type "pip install pandas numpy requests"

2. Go to Fred api and create your account. 
   Once done, create an API key from there and use it in api_call.py at the below line.

   API_KEY = "YOUR_APIKEY_HERE" (line 7)

   In my case the api key was : ef9a748ee6c2d209d2099fb50e9f07f1

3. Run the refresh script to refresh the data (refresh.py) using below command 

   python Scripts/refresh.py
   python3 Scripts/refresh.py (in my case as i have Python 3.9.6 installed)

4. Output sample files will be stored in the '/data' folder.

