# Data Matching Application

A Streamlit-based web application for matching two CSV files after removing duplicates.

## Features
- Upload two CSV files
- Remove duplicates from both datasets
- Match datasets based on user-selected columns
- Support for different join types (inner, left, right, outer)
- Download matched results as Excel file

## Installation
1. Clone the repository:
```bash
git clone <repository-url>
cd <repository-folder>
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running Locally
```bash
streamlit run app.py
```

## Deployment to Streamlit Cloud
1. Push your code to a GitHub repository
2. Sign in to Streamlit Cloud (share.streamlit.io)
3. Create a new app and link it to your GitHub repository
4. Specify `app.py` as the main file
5. Deploy the app

## Requirements
See `requirements.txt` for the list of required Python packages.

## Usage Notes
- Both CSV files must have at least one common column for matching
- Ensure the selected columns for matching have compatible data types
- The application supports standard CSV formats

## License
MIT License