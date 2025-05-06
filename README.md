# 📊 Data Visualization Final Project

## Project Overview
The US Accidents Dashboard is an interactive data visualization application built to analyze and uncover insights from over 2.25 million accident records across the United States. Leveraging the power of **Dash, Plotly, and Pandas**, this project transforms raw accident datasets into meaningful visual narratives for public safety analysis and informed decision-making.

The application enables users to identify accident-prone areas, analyze contributing weather and infrastructure factors, and visualize the trends from 2016 to 2023.

## Motivation & Problem Statement
While statistical methods exist for examining accident data, they often fall short of being intuitive for public use. This project addresses that gap by utilizing data visualization to:

- Assess the impact of infrastructure on severity

- Offer an accessible dashboard to different user groups

Despite existing safety efforts, traffic accidents remain prevalent due to poor weather, road conditions, and human error. Traditional accident datasets often bury useful insights. **This project transforms these datasets into rich, interactive visual formats to guide data-driven road safety initiatives.**


## Project Structure
```
DATA_VISUALIZATION_PROJECT/
│
├── assets/                        # Static files like images, icons, fonts
│
├── Vizs/                          # Visualization scripts                         
│   ├── area_viz.py                # Makes this a package (optional, but useful)
│   ├── bar_viz.py
│   ├── choroplethmap_viz.py
│   ├── donut_viz.py
│   ├── dotplot_viz.py
│   ├── line_viz.py
│
├── data/                          # Data files (move CSVs here)
│   └── US_Accidents_March23.csv
│
├── .gitignore                     # Git ignored files (see below)
├── Dashboard_final.py            # Main app / dashboard entry point
├── requirements.txt              # Python dependencies
├── README.md                     # Project overview and instructions
├── Scrolling_application.py      # Possibly merge into Dashboard_final.py?
├── scrollytell_section.py        # Can also be grouped logically in /Vizs or merged
│
└── venv/                          # Virtual environment (ignored via .gitignore)


```


## Dataset Info
- **Source:** US Accidents (2016–2023) - Kaggle

- **Size:** ~3GB (Not uploaded to GitHub due to file size limitations)

- **Download Note:**     Please download the [dataset](https://www.kaggle.com/datasets/sobhanmoosavi/us-accidents) manually from Kaggle and place it in the project directory as US_Accidents_March23.csv.

### Key Visual Insights

| Insight | Description | Visualization Types | Example Image |
|--------|-------------|---------------------|---------------|
| **1. Where & when do severe accidents occur?** | Analyze spatial & temporal patterns to understand risk zones across states and times | Choropleth map | ![Severe Accidents Map](assets/Bhavitha_viz.png) |
| **2. How does weather impact severity?** | Discover how weather like rain, fog, or snow influences accident severity | Stacked Bar Charts | ![Weather vs Severity](assets/Sreemayeeviz.png) |
| **3. When are roads most dangerous?** | Identify accident trends by hour and weekday | Line Plot| ![Hourly and Weekly Trends](assets/Manogna2_viz.png) |
| **4. Are traffic signals reducing severity?** | Examine if features like traffic lights and stop signs lower severity | Dot Plot | ![Traffic Features Impact](assets/Divya_viz.jpg) |
| **5. How is accident severity trending?** | Track longitudinal trends in accident severity from 2016 to 2023 | Area Chart | ![Severity Trends Over Time](assets/Manognaviz.jpg) |


## Features
-  Interactive graphs and charts
-  Custom color palettes
-  Real-time data updates
-  Scrollable dashboard application

## Technologies Used
- Python 3.10+
- Matplotlib
- Plotly
- Seaborn
- Dash

## How to Run
1. Clone the repository:
   ```bash
   git clone https://github.com/Manognarayasam/Data_Visualization_Final_Project
   ```
2. Download Dataset from Kaggle: 
  Download the `US_Accidents_March23.csv` dataset from [here](https://www.kaggle.com/datasets/sobhanmoosavi/us-accidents) and place it in the project root.

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the dashboard:
   ```bash
   streamlit run Dashboard_final.py
   ```
5. View the Dashboard
    ```
    http://localhost:xxxx/
    ```

## Interactive Website
![Streamlit Interactive Website](assets/Dashboard.png)


## License
This project is licensed under the MIT License.
