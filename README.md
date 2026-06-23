# BMW-STOCK-DATA-ANALYSIS
End-to-end data science project on BMW historical stock price data (OHLCV, 1996–present): data cleaning, exploratory data analysis, predictive modelling, and an interactive dashboard.

## Project Structure

```
BMW Stock Data Analysis/
├── Data/
│   ├── Raw/
│   │   └── BMW_Data.csv              # Original raw dataset
│   └── Clean/
│       └── Final_BMW_dataset.csv     # Cleaned dataset (output of EDA notebook)
├── Notebooks/
│   ├── Data_Cleaning_and_EDA.ipynb   # Data cleaning + exploratory data analysis
│   ├── Modeling.ipynb                # Regression & classification models
│   └── Dashboard.py                  # Streamlit interactive dashboard
├── README.md
└── requirements.txt
```

## Workflow

1. **Data Cleaning & EDA** (`Notebooks/Data_Cleaning_and_EDA.ipynb`)
   Loads `Data/Raw/BMW_Data.csv`. Parses and sorts dates, checks for missing values/duplicates, validates OHLC logical consistency, flags zero-volume days, computes daily returns/volatility, plots moving averages and correlations. Outputs the cleaned dataset to `Data/Clean/Final_BMW_dataset.csv`.

2. **Modelling** (`Notebooks/Modeling.ipynb`)
   Loads `Data/Clean/Final_BMW_dataset.csv`. Engineers lag and rolling features, then builds:
   - **Regression** — predicts next-day Close price
   - **Classification** — predicts next-day direction (Up/Down)
   Uses a time-based train/test split (no shuffling) to avoid lookahead bias.

3. **Dashboard** (`Notebooks/Dashboard.py`)
   Loads `Data/Clean/Final_BMW_dataset.csv`. Interactive Streamlit app for exploring price trends, returns, volatility, and correlations, styled with a custom cute/techy color palette.

## Tools & Libraries Used

| Tool / Library | Purpose |
|---|---|
| **Python 3** | Core programming language |
| **Jupyter Notebook** (`nbformat`, `nbconvert`) | Notebook creation and execution for EDA & modelling |
| **pandas** | Data loading, cleaning, manipulation, feature engineering |
| **NumPy** | Numerical operations (returns, rolling stats, array handling) |
| **Matplotlib** | Static plotting in the EDA/modelling notebooks |
| **Seaborn** | Statistical visualizations (distributions, heatmaps, boxplots) |
| **scikit-learn** | Machine learning models — Linear/Logistic Regression, Random Forest, Gradient Boosting — plus scaling and evaluation metrics |
| **Streamlit** | Interactive web dashboard framework |
| **Plotly** (`plotly.graph_objects`, `plotly.express`) | Interactive charts in the dashboard (line, candlestick, histogram, heatmap, scatter) |

## How to Run

### Setup
From the project root:
```bash
pip install -r requirements.txt
```

### Notebooks
Open `Notebooks/Data_Cleaning_and_EDA.ipynb` or `Notebooks/Modeling.ipynb` in Jupyter and run all cells. Each notebook reads/writes CSVs using relative paths into `Data/Raw/` and `Data/Clean/`, so always launch Jupyter from the project root (or adjust the paths at the top of the notebook if you launch from elsewhere).

### Dashboard
From the project root:
```bash
streamlit run Notebooks/Dashboard.py
```
Then open the local URL Streamlit prints (default `http://localhost:8501`).

## Notes
- The official BMW roundel logo is not used anywhere in this project since it's trademarked brand IP — the dashboard instead uses an original stylized "BMW" badge and watermark in the requested color palette.
- This project is for educational/coursework purposes. The predictive models are not intended as financial or trading advice.

## Author
Developed by **Cynthia Mueni**
Github Profile:https://github.com/thea09-cpu
