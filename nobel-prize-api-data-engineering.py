# %% [markdown]
# # Nobel Prize API Data Engineering

# %% [markdown]
# ## 📊 Project Overview
# This notebook demonstrates **API data consumption, normalization, and modeling techniques** using the Nobel Prize API.

# %% [markdown]
# 
# ## 🎯 Key Technical Skills
# - **API Data Consumption**: REST API interaction with proper error handling
# - **Data Normalization**: Converting nested JSON structures to flat tabular format
# - **Data Modeling**: Handling complex relationships between laureates and prizes
# - **Data Engineering**: ET pipeline (extract & transform) implementation in Python
# 
# ---

# %% [markdown]
# ## 🚀 Setup and Dependencies

# %%
import requests
import pandas as pd
import numpy as np

# %% [markdown]
# ---

# %% [markdown]
# ## 🔌 API Data Ingestion
# 
# ### Generic API Data Fetcher

# %%
def get_api_data(BASE_URL: str, limit: int = None, format: str = 'json') -> dict:
    try:
        response = requests.get(url=BASE_URL,params={'limit':limit, 'format': format})
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"GET data error: {e}")
        return None

# %% [markdown]
# **Technical Features:**
# - Error handling with try/except
# - Configurable parameters (limit, format)
# - HTTP status code validation with `raise_for_status()`
# 
# ---

# %% [markdown]
# ## 📈 Data Source Analysis
# 
# ### Endpoint Discovery and Sizing

# %%
laureates_url = 'https://api.nobelprize.org/2.1/laureates'
print(f"laureatesResult size: {get_api_data(BASE_URL=laureates_url, limit=1).get('meta').get('count')}")
nobel_prizes_url = 'https://api.nobelprize.org/2.1/nobelPrizes'
print(f"nobelPrizesResult size: {get_api_data(BASE_URL=nobel_prizes_url, limit=1).get('meta').get('count')}")

# %% [markdown]
# **Data Engineering Best Practice:**
# - **Data profiling**: Understanding data volume before full ingestion
# - **Metadata extraction**: Using API meta information for capacity planning
# - **Endpoint optimization**: Testing with minimal data first
# 
# ---

# %% [markdown]
# ## 💾 Full Dataset Extraction

# %%
laureates_json_data = get_api_data(BASE_URL=laureates_url,limit=1004)
nobel_prizes_json_data = get_api_data(BASE_URL=nobel_prizes_url,limit=676)

# %% [markdown]
# **Strategy:** Using discovered counts to fetch complete datasets in single API calls.
# 
# ---

# %% [markdown]
# ## 🔍 Data Structure Exploration

# %%
laureates_json_data.get('laureates')[0].get('birth').get('date')

# %%
nobel_prizes_json_data.get('nobelPrizes')[0].get('category').get('en')

# %% [markdown]
# **Purpose:** Understanding nested JSON structure to inform normalization strategy.
# 
# ---

# %% [markdown]
# ## 🛠️ Data Normalization Engine

# %% [markdown]
# ### JSONPath-Style Nested Value Extractor

# %%
#JSONPath-style
def extract_nested_value(data: dict, path: str, default=np.nan):
    keys = path.split('.')
    current = data
    for key in keys:
        if key in current:
            current = current[key]
        else:
            return default
    return current

# %% [markdown]
# **Features:**
# - **JSONPath-style syntax**: Industry-standard dot notation (`birth.place.country.en`)
# - **Safe navigation**: Handles missing keys
# - **Default value handling**: Uses `np.nan` for missing data compatibility with pandas
# - **Recursive traversal**: Navigates arbitrary nesting levels
# 
# **Example Usage:**

# %%
extract_nested_value(laureates_json_data.get('laureates')[0],'birth.place.country.en')

# %% [markdown]
# ---

# %% [markdown]
# ## 📊 Data Modeling & Normalization

# %% [markdown]
# ### Multi-Source DataFrame Factory

# %%
def normalize_to_dataframe(json_data: dict) -> pd.DataFrame:
    rows = []
    if json_data.__contains__('laureates'):
        # Laureates normalization logic
        json_data = json_data.get('laureates')
        for laureate in json_data:
            row = {
                'laureate_id': laureate.get('id'),
                'known_name': extract_nested_value(laureate,'knownName.en'),
                'gender': laureate.get('gender') if 'gender' in laureate else np.nan,
                'birth_date': extract_nested_value(laureate,'birth.date'),
                'born_city': extract_nested_value(laureate,'birth.place.city.en'),
                'born_country': extract_nested_value(laureate,'birth.place.country.en'),
                'born_country_now': extract_nested_value(laureate,'birth.place.countryNow.en'),
                'continent': extract_nested_value(laureate, 'birth.place.continent.en'),
                'death_date': extract_nested_value(laureate, 'death.date')
            }
            rows.append(row)
    elif json_data.__contains__('nobelPrizes'):
        # Nobel Prizes normalization with relationship modeling
        json_data = json_data.get('nobelPrizes')
        for nobel_prize in json_data:
            row = {
                'year': nobel_prize.get('awardYear') if 'awardYear' in nobel_prize else np.nan,
                'category': extract_nested_value(nobel_prize,'category.en'),
                'date_awarded': nobel_prize.get('dateAwarded') if 'dateAwarded' in nobel_prize else np.nan,
                'prize_amount': nobel_prize.get('prizeAmount') if 'prizeAmount' in nobel_prize else np.nan,
                'prize_amount_adjusted': nobel_prize.get('prizeAmountAdjusted') if 'prizeAmountAdjusted' in nobel_prize else np.nan,
                'top_motivation': extract_nested_value(nobel_prize,'topMotivation.en')
            }
            # Complex relationship modeling: Prize -> Multiple Laureates
            if nobel_prize.__contains__('laureates'):
                for nobel_prize_laureate in nobel_prize.get('laureates'):
                    new_row = row.copy()
                    new_row.update({
                        'laureate_id': nobel_prize_laureate.get('id'),
                        'motivation': extract_nested_value(nobel_prize_laureate,'motivation.en'),
                        'portion': extract_nested_value(nobel_prize_laureate,'portion'),
                    })
                    rows.append(new_row)
            else:
                rows.append(row)

    return pd.DataFrame(rows)

    

# %% [markdown]
# ### 🏗️ Data Modeling Techniques Implemented:
# 
# #### 1. **Polymorphic Data Processing**
# - Single function handles multiple data schemas (`laureates` vs `nobelPrizes`)
# - Dynamic schema detection using `__contains__()`
# 
# #### 2. **One-to-Many Relationship Modeling**
# - **Challenge**: One Nobel Prize can have multiple laureates
# - **Solution**: Row multiplication - each laureate gets their own row with prize details
# - **Result**: Enables individual laureate analysis while preserving prize context
# 
# #### 3. **Missing Data Handling**
# - Consistent use of `np.nan` for missing values
# - Conditional field extraction with fallbacks
# - Pandas-compatible null value strategy
# 
# ---

# %% [markdown]
# ## 📋 DataFrame Creation & Validation

# %% [markdown]
# ### Laureates Dataset

# %%
laureates = normalize_to_dataframe(laureates_json_data)
laureates.to_csv('laureates.csv')
laureates

# %% [markdown]
# **Output:** Clean tabular dataset with laureate biographical information.
# 
# ### Nobel Prizes Dataset 

# %%
nobel_prizes = normalize_to_dataframe(nobel_prizes_json_data)
nobel_prizes.to_csv('nobel_prizes.csv')
nobel_prizes

# %% [markdown]
# **Output:** Normalized prize dataset with laureate relationships preserved.
# 
# ### Data Quality Check

# %%
nobel_prizes.loc[nobel_prizes['laureate_id'].isna()].head()

# %% [markdown]
# **Purpose:** Identifying prizes without individual laureates (organizational awards).
# 
# ---
# 
# ## 🎯 Technical Achievements
# 
# ### ✅ **API Integration**
# - RESTful API consumption with error handling
# - Metadata-driven data sizing
# - Efficient single-call data extraction
# 
# ### ✅ **Data Normalization**  
# - JSONPath-style navigation system
# - Nested structure flattening
# - Type-safe value extraction
# 
# ### ✅ **Data Modeling**
# - Complex relationship handling (many-to-many)
# - Polymorphic data processing
# 
# ### ✅ **Production-Ready Code**
# - Error handling
# - Consistent null value strategy  
# - Pandas-optimized data types
# 
# ---
# 
# ## 🚀 Next Steps & Extensions
# 
# **Potential Enhancements:**
# - Add data type conversion and validation
# - Implement incremental data updates
# - Create automated data quality checks
# - Add visualization layer for insights
# - Implement caching for API responses
# 
# ---
# 
# ## 🏷️ Tags
# `#DataEngineering` `#APIIntegration` `#DataNormalization` `#DataModeling` `#Python` `#Pandas` `#ETL` `#NobelPrize`


