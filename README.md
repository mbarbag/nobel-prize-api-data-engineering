# Nobel prize API data extraction & transformation
> **Project that extracts Nobel Prize data from APIs, normalizes nested JSONs into dataframes, and explores many-to-many relationships between prizes and laureates.**


## Key Technical Skills

- **API Data Extraction** - Data ingestion with error handling
- **Data Normalization** - JSONPath-style navigation for nested structures  
- **Data Modeling** - Many-to-many relationship handling between prizes and laureates

## Data Source

This project use the **official Nobel Prize API v2.1** provided by [NobelPrize.org](https://www.nobelprize.org/about/developer-zone-2/).

## Usage
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/nobel-prize-api-data-engineering.git
   cd nobel-prize-api-data-engineering
   ```

2. Open the Jupyter notebook:
   ```bash
   jupyter notebook nobel-prize-api-data-engineering.ipynb
   ```

3. Run all cells to execute the complete data processing workflow

## Future Enhancements

- Save processed data to a cloud data-lake
- Add data type conversion and validation
- Implement incremental data updates
