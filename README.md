# Nobel Prize API Data Engineering

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Pandas](https://img.shields.io/badge/Pandas-Latest-green.svg)](https://pandas.pydata.org/)
[![API](https://img.shields.io/badge/API-Nobel%20Prize%202.1-gold.svg)](https://app.swaggerhub.com/apis/NobelMedia/NobelMasterData/2.1)
[![License](https://img.shields.io/badge/License-MIT-orange.svg)](LICENSE)

> **Data engineering project demonstrating API consumption, data normalization, and relationship modeling using the Nobel Prize API.**

## 🎯 Project Overview

This repository demonstrates **data engineering skills** through data extraction and transformation implementation for Nobel Prize data. The project transforms nested JSON data from the public Nobel Prize API into clean, analysis-ready pandas DataFrames using normalization and modeling techniques.

### 🏆 Key Technical Skills

- **🔌 API Data Extraction** - Data ingestion with error handling
- **📊 Data Normalization** - JSONPath-style navigation for nested structures  
- **🏗️ Data Modeling** - Many-to-many relationship handling between prizes and laureates
- **⚡ Data Transformation** - Type-safe operations with null handling
- **🔄 Extract & Transform Pipeline** - Complete data extraction and transformation

---
## 📡 Data Source

This project utilizes the **official Nobel Prize API v2.1** provided by [NobelPrize.org](https://www.nobelprize.org/about/developer-zone-2/).

### API Information:
- **Provider**: NobelPrize.org  
- **Version**: 2.1
- **Documentation**: [SwaggerHub API Docs](https://app.swaggerhub.com/apis/NobelMedia/NobelMasterData/2.1#/info)
- **License**: Open data, free to use
- **Update Frequency**: Real-time updates including new laureate announcements

> **Note**: NobelPrize.org offers open data to developers in two ways: as API and as Linked Data. The data is free to use and contains information about Nobel Prizes and Nobel Laureates. Data is updated as information on www.nobelprize.org is updated, including at the time of announcements of new Laureates.

### Endpoints Used:
- `https://api.nobelprize.org/2.1/laureates` - Individual laureate information
- `https://api.nobelprize.org/2.1/nobelPrizes` - Prize details with laureate relationships

---
### Usage
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

---

## 🏗️ Architecture & Implementation

### Core Components

#### 1. **API Data Extraction**
```python
def get_api_data(BASE_URL: str, limit: int = None, format: str = 'json') -> dict
```
- HTTP client with error handling
- Configurable pagination support
- Metadata extraction for capacity planning

#### 2. **Data Normalization**
```python  
def extract_nested_value(data: dict, path: str, default=np.nan)
```
- **JSONPath-style navigation**: Dot notation (`birth.place.country.en`)
- **Safe traversal**: Handles missing nested keys
- **Type-safe operations**: Consistent null value handling

#### 3. **Data Modeling**
```python
def normalize_to_dataframe(json_data: dict) -> pd.DataFrame
```
- **Polymorphic processing**: Single function handles multiple data schemas
- **Relationship preservation**: One-to-many modeling (prizes → laureates)
- **Denormalization strategy**: Optimized for analytical queries

---
## 🚀 Future Enhancements

- [ ] **Data Persistence**: Save processed data to databases or files
- [ ] **Incremental Updates**: Delta processing for new laureates
- [ ] **Data Validation Layer**: Automated quality checks and alerts
- [ ] **Performance Optimization**: Parallel processing for datasets
- [ ] **Data Visualization**: Interactive dashboards and insights
- [ ] **Scheduling**: Automated data refresh workflows
---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🔗 Links

- **API Documentation**: [Nobel Prize API v2.1](https://app.swaggerhub.com/apis/NobelMedia/NobelMasterData/2.1)
- **Data Source**: [NobelPrize.org Developer Zone](https://www.nobelprize.org/about/developer-zone-2/)
- **Jupyter Notebook**: [nobel-prize-api-data-engineering.ipynb](nobel-prize-api-data-engineering.ipynb)

---

## 🏷️ Tags

`#DataEngineering` `#API` `#DataNormalization` `#DataModeling` `#Python` `#Pandas` `#NobelPrize` `#DataScience` `#ExtractTransform`

---

<div align="center">

**⭐ If this project helped you, please give it a star! ⭐**

</div>
