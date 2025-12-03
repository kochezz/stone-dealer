# ⛏️ Zambia Mining Site Assessment Planner

A comprehensive Streamlit web application for planning and assessing mining site viability across Zambia, with Chingola as the base of operations.

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)

## 🌟 Features

### 🗺️ Interactive Multi-Property Mapping
- View all filtered properties simultaneously on an interactive map
- Chingola base location always visible (green marker)
- Property locations color-coded (red markers)
- Hover tooltips with property details
- Route visualization for selected properties

### 🔍 Advanced Filtering System
- **Province Filter** - 10 Zambian provinces
- **District Filter** - 62 districts (dynamic based on province selection)
- **Commodity Filter** - 32 mineral types
- **Status Filter** - Operational status (Active/Inactive/Unknown)
- **Distance Slider** - Filter by distance from base (0-6000 km)

### 📊 Analytics Dashboard
Four interactive visualizations:
1. **Commodity Distribution** - Bar chart of top commodities
2. **Property Status** - Donut chart showing operational status
3. **Province Distribution** - Geographic distribution of properties
4. **Distance Analysis** - Histogram of distances from base

### 📋 Comprehensive Data Table
- Sortable and filterable data display
- Single-row selection for detailed view
- Organized property information cards
- Expandable sections for full details
- Mini-map with route visualization

## 📁 Dataset

- **239 mining properties** across Zambia
- **10 provinces** represented
- **32 commodity types** tracked
- **18 data attributes** per property

### Data Quality
✅ Coordinates rounded to 4 decimal places (~11m precision)
✅ Standardized town and city names
✅ Proper sentence case formatting
✅ Province and district classifications
✅ Distance and travel time calculations

## 🚀 Quick Start

### Prerequisites
```bash
Python 3.8+
```

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/your-username/zambia-mining-planner.git
cd zambia-mining-planner
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Run the application**
```bash
streamlit run app.py
```

4. **Open in browser**
```
http://localhost:8501
```

## 🌐 Live Demo

**Deployed App:** [Your Streamlit App URL]

## 📊 Usage Examples

### Example 1: Find Copper Properties in Copperbelt
1. Select "Copperbelt Province" in Province filter
2. Select "Copper" in Commodity filter
3. View results on map (should show ~30 properties)

### Example 2: Properties Within 200km
1. Adjust Distance slider to 200km
2. Map automatically updates to show nearby properties
3. Check Analytics tab for distribution insights

### Example 3: Detailed Property Analysis
1. Go to Data Table tab
2. Click on any property row
3. View comprehensive details including geology, reserves, and location
4. See mini-map with direct route from base

## 📈 Screenshots

### Map View
*(Multi-property visualization with base and properties)*

### Analytics Dashboard
*(Charts showing commodity, status, province distributions)*

### Data Table
*(Searchable table with detailed property view)*

## 🛠️ Technology Stack

- **Frontend:** Streamlit
- **Data Processing:** Pandas, NumPy
- **Visualizations:** Plotly Express, Plotly Graph Objects
- **Maps:** Plotly Mapbox
- **Styling:** Custom CSS

## 📦 Project Structure

```
zambia-mining-planner/
│
├── app.py                              # Main Streamlit application
├── zambia_mining_app_data_final.csv    # Cleaned dataset
├── requirements.txt                     # Python dependencies
│
├── docs/                                # Documentation
│   ├── APP_USER_GUIDE.md               # Comprehensive user guide
│   ├── QUICK_DEPLOYMENT_GUIDE.md       # Quick deployment steps
│   └── COMPLETE_FINAL_REPORT.md        # Data cleaning report
│
└── README.md                            # This file
```

## 🎯 Key Metrics

- **Total Properties:** 239
- **Provinces Covered:** 10
- **Districts:** 62
- **Commodities Tracked:** 32
- **Base Location:** Chingola, Copperbelt Province

## 🗺️ Province Distribution

| Province | Properties |
|----------|-----------|
| Central Province | 48 |
| North-Western Province | 44 |
| Northern Province | 41 |
| Copperbelt Province | 30 |
| Eastern Province | 18 |
| Muchinga Province | 15 |
| Southern Province | 15 |
| Lusaka Province | 14 |
| Western Province | 8 |
| Luapula Province | 6 |

## ⚒️ Top Commodities

| Commodity | Count |
|-----------|-------|
| Copper | 92 |
| Diamond | 34 |
| Gold | 30 |
| Iron | 26 |
| Zinc | 18 |

## 🔧 Configuration

### Change Base Location
Edit in `app.py`:
```python
CHINGOLA_COORDS = (-12.5333, 27.8500)  # Your coordinates
CHINGOLA_NAME = "Your Base Name"
```

### Modify Colors
Edit map colors in `create_multi_property_map()`:
```python
color_discrete_map={'Base': '#00C853', 'Property': '#FF5722'}
```

## 📝 Data Schema

### Core Columns
- `Property_Name` - Name of mining property
- `Latitude` / `Longitude` - Geographic coordinates (4 decimal precision)
- `Province` - Zambian province (10 options)
- `Clean_District` - Standardized district name
- `Primary_Commodity` - Main mineral resource
- `Status` - Operational status
- `Distance_From_Chingola_km` - Distance from base
- `Travel_Time_From_Chingola_Hours` - Estimated travel time

### Additional Columns
- Commodity_2, Commodity_3 - Secondary minerals
- Reserves - Reserve information
- Geology_Classification - Geological type
- Geology_Description - Detailed geology
- District/Town - Location description

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### Development Setup
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Data sourced from Zambian geological surveys and mining registries
- Built with [Streamlit](https://streamlit.io/)
- Maps powered by [Plotly](https://plotly.com/)
- Data cleaning and standardization performed December 2024

## 📞 Contact

**Project Owner:** [Your Name]
**Email:** [Your Email]
**Project Link:** [GitHub Repository URL]

## 🔄 Version History

### v2.0.0 (Current) - Enhanced Version
- ✨ Multi-property map view
- ✨ 5 advanced filters (Province, District, Commodity, Status, Distance)
- ✨ Analytics dashboard with 4 charts
- ✨ Three-tab interface (Map, Analytics, Data Table)
- ✨ Detailed property views with mini-maps
- ✨ Modern UI/UX design
- ✨ Clean, standardized dataset (239 properties)

### v1.0.0 - Original Version
- Basic single-property map
- 2 basic filters
- Simple table view

## 🚀 Deployment

### Streamlit Cloud (Recommended)
1. Push code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect repository
4. Deploy!

### Heroku
```bash
heroku create your-app-name
git push heroku main
```

### Docker
```bash
docker build -t zambia-mining-planner .
docker run -p 8501:8501 zambia-mining-planner
```

## 📚 Documentation

- **User Guide:** See `docs/APP_USER_GUIDE.md` for comprehensive usage instructions
- **Deployment Guide:** See `docs/QUICK_DEPLOYMENT_GUIDE.md` for step-by-step deployment
- **Data Report:** See `docs/COMPLETE_FINAL_REPORT.md` for data cleaning details

## 🎯 Roadmap

### Planned Features
- [ ] Export functionality (CSV, PDF reports)
- [ ] Route optimization for multiple properties
- [ ] Comparison mode for side-by-side analysis
- [ ] Historical tracking of property status
- [ ] Offline mode with cached data
- [ ] Mobile app version

## ⚠️ Known Issues

- 28 properties have questionable coordinates (see coordinate_issues_report.txt)
- Mobile view is limited (best viewed in landscape)
- Large filter combinations may cause slight performance lag

## 💡 Tips & Best Practices

1. **Start with Province filter** - Narrow down geographically first
2. **Use Distance slider** - Reduce map markers for better performance
3. **Check Analytics first** - Get overview before diving into details
4. **Export filtered data** - Use Data Table for detailed analysis
5. **Bookmark properties** - Keep track of sites of interest

---

## 📊 Stats

![GitHub repo size](https://img.shields.io/github/repo-size/your-username/zambia-mining-planner)
![GitHub stars](https://img.shields.io/github/stars/your-username/zambia-mining-planner)
![GitHub forks](https://img.shields.io/github/forks/your-username/zambia-mining-planner)

---

**Built with ❤️ for Zambian mining operations**

**Last Updated:** December 2024
