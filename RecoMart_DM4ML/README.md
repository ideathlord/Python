# RecoMart – DM4ML Assignment

## How to Run
1. Install dependencies
   pip install -r requirements.txt

2. Generate data
   python ingestion/generate_csv_data.py
   python ingestion/ingest_api_data.py

3. Validate
   python validation/validate_data.py

4. Clean
   python preprocessing/clean_and_eda.py

5. Features
   python features/build_features.py

6. Train Model
   python model/train_model.py