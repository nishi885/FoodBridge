# 📊 Data Collection Guide

Best practices for collecting real demand data to improve model accuracy.

---

## 📋 Data Collection Template

Use this template to collect real data from your NGOs.

### Column Definitions

| Column | Type | Values | Example |
|--------|------|--------|---------|
| `date` | Date | YYYY-MM-DD | 2024-04-15 |
| `location` | Text | North/South/East/West Area | North Area |
| `day_of_week` | Text | Monday-Sunday | Friday |
| `temperature` | Number | 5-35°C | 15 |
| `weather_condition` | Text | Sunny/Rainy/Cloudy | Sunny |
| `is_event` | Number | 0 or 1 | 1 |
| `holiday` | Number | 0 or 1 | 0 |
| `actual_meals_distributed` | Number | Count | 95 |
| `notes` | Text | Optional | Festival event |

---

## 📝 Daily Data Collection Process

### For Each NGO Location:

1. **Record Location**: Which area (North/South/East/West)
2. **Get Weather**: Temperature and condition
3. **Mark Events**: Any special events/festivals happening?
4. **Mark Holidays**: Is it a holiday?
5. **Count Meals**: How many meals were actually distributed?

### Simple Google Form Template

Create a Google Form with these fields:

```
📍 Location *
   ☐ North Area
   ☐ South Area
   ☐ East Area
   ☐ West Area

📅 Date * [YYYY-MM-DD]

🌡️ Temperature (°C) *
   [Number input, range 5-35]

🌦️ Weather Condition *
   ☐ Sunny
   ☐ Rainy
   ☐ Cloudy

🎉 Event/Festival? *
   ☐ Yes
   ☐ No

📅 Holiday? *
   ☐ Yes
   ☐ No

🍽️ Meals Distributed Today * [Number input]

📝 Notes (Optional)
   [Text area]
```

---

## 📱 Mobile Data Collection

Use mobile app or SMS:

### Via WhatsApp/SMS
```
Send daily: Location, Temperature, Weather, Event(Y/N), Holiday(Y/N), Meals Distributed

Example:
North Area, 15°C, Sunny, Y, N, 95
```

### Via Mobile App
- Create simple mobile form
- Auto-fill location from GPS
- Get weather from location
- Manual input for event/holiday/meals

---

## 💾 CSV Format for Bulk Import

When you have collected data, format as CSV:

```csv
date,location,day_of_week,temperature,weather_condition,is_event,holiday,actual_meals_distributed
2024-04-01,North Area,Monday,12,Cloudy,0,0,82
2024-04-02,North Area,Tuesday,14,Sunny,0,0,88
2024-04-03,North Area,Wednesday,11,Rainy,0,0,75
2024-04-04,North Area,Thursday,15,Sunny,0,0,92
2024-04-05,North Area,Friday,13,Cloudy,1,0,105
2024-04-06,North Area,Saturday,18,Sunny,1,0,145
2024-04-07,North Area,Sunday,19,Sunny,0,0,135
```

---

## 🔄 How to Retrain with New Data

### Step 1: Append Data
Add new records to `data/training_data.csv`:

```
Rename the target column from:
  meals_needed  → actual_meals_distributed
  
Keep the same columns.
```

### Step 2: Update Feature Engineering
If adding new features, modify `train_model.py`:

```python
# Add custom features
df['month'] = pd.to_datetime(df['date']).dt.month
df['week_of_year'] = pd.to_datetime(df['date']).dt.isocalendar().week
df['is_summer'] = df['month'].isin([6, 7, 8]).astype(int)
```

### Step 3: Retrain
```bash
python src/train_model.py
```

### Step 4: Monitor Improvement
Check if new R² score is better!

---

## 📊 Collection Metrics

### Target Collection Rate

- **Minimum**: 10 records per location per month
- **Better**: 20-30 records per location per month
- **Excellent**: 50+ records per location per month

### Sample Size for Good Model

- 100-200 total records: Basic model
- 500+ records: Good accuracy
- 1000+ records: Excellent predictions

### Time to Good Predictions

- Week 1: Collect initial 40 records
- Month 1: Collect ~50 records total
- Month 3: Collect ~150 records, retrain monthly
- Month 6: Collect ~300 records, weekly updates

---

## 🎯 What Not to Include

❌ **Don't collect**:
- Personal information (NGO names, beneficiary details)
- Sensitive data (staff information)
- Duplicate data (same day/location twice)
- Invalid data (missing fields, out-of-range values)

✅ **Do validate**:
- Temperature is between 5-35°C
- Location is one of: North, South, East, West Area
- Day matches the date
- Meals count is reasonable (>0)

---

## 📈 Data Quality Checks

```python
# Run these checks before retraining:

import pandas as pd

df = pd.read_csv('data/training_data.csv')

# Check for missing values
print("Missing values:")
print(df.isnull().sum())

# Check data types
print("\nData types:")
print(df.dtypes)

# Check value ranges
print("\nTemperature range:", df['temperature'].min(), "-", df['temperature'].max())
print("Meals range:", df['meals_needed'].min(), "-", df['meals_needed'].max())

# Check unique values
print("\nUnique locations:", df['location'].unique())
print("Unique weather:", df['weather_condition'].unique())
print("Unique days:", df['day_of_week'].unique())

# Check duplicates
print("\nDuplicate rows:", df.duplicated().sum())

# Check date range
print("\nDate range:", df['date'].min(), "to", df['date'].max())
```

---

## 🔍 Data Collection Checklist

- [ ] Form created (Google Form / Mobile App / SMS)
- [ ] Instructions given to NGO staff
- [ ] Daily collection started
- [ ] Weekly data review
- [ ] Monthly data quality check
- [ ] Monthly model retraining
- [ ] Performance tracking

---

## 📊 Visualization Dashboard Ideas

Once you have enough data, create dashboard showing:

```
1. Demand by Location
   - North Area: Avg 95 meals/day
   - South Area: Avg 120 meals/day
   - East Area: Avg 75 meals/day
   - West Area: Avg 110 meals/day

2. Demand by Day of Week
   - Weekday: Avg 85 meals
   - Weekend: Avg 135 meals
   - +59% on weekends!

3. Demand by Weather
   - Sunny: Avg 110 meals
   - Rainy: Avg 95 meals
   - Cloudy: Avg 100 meals

4. Impact of Events
   - Without event: Avg 90 meals
   - With event: Avg 125 meals
   - +39% on event days!

5. Model Accuracy Over Time
   - Week 1-2: 70% accuracy
   - Week 3-4: 78% accuracy
   - Month 2: 85% accuracy
   - Month 3: 88% accuracy
```

---

## 🎓 Advanced: Add More Features

After collecting 500+ records, consider adding:

### 1. Trend Features
```python
# Meals distributed last 7 days
df['avg_meals_last_7days'] = df['meals_needed'].rolling(7).mean()

# Trend (increasing/decreasing)
df['is_increasing_trend'] = df['meals_needed'].diff() > 0
```

### 2. Seasonal Features
```python
# Quarter of year
df['quarter'] = pd.to_datetime(df['date']).dt.quarter

# Is summer/winter
df['is_summer'] = df['month'].isin([6, 7, 8]).astype(int)
df['is_winter'] = df['month'].isin([12, 1, 2]).astype(int)
```

### 3. Location-specific Features
```python
# Average demand for this location
df['location_avg'] = df.groupby('location')['meals_needed'].transform('mean')

# Day-location combination
df['location_day_avg'] = df.groupby(['location', 'day_of_week'])['meals_needed'].transform('mean')
```

### 4. Integration with External Data
```python
# Public event calendar
# School holidays
# Festival dates
# Weather patterns
# Economic indicators
```

---

## 💡 Pro Tips

### Tip 1: Start Small
Don't overwhelm staff. Start with 5-10 records manually.
Gradually increase to daily automated collection.

### Tip 2: Use Defaults
Make location/date auto-filled if possible.
Only ask for: temperature, weather, event, holiday, meals.

### Tip 3: Regular Reviews
- Weekly: Check data quality
- Bi-weekly: Review trends
- Monthly: Retrain model

### Tip 4: Feedback Loop
- Share predictions with NGOs
- Get feedback on accuracy
- Adjust model if needed

### Tip 5: Incentivize
Reward accurate data collection:
- Accuracy bonus
- Recognition
- Better resource allocation based on predictions

---

## 📝 Sample Data Log Sheet

Use this to manually track before entering into system:

```
Date: ___________
Location: □ North □ South □ East □ West Area

Weather Information:
- Temperature: ______°C
- Condition: □ Sunny □ Rainy □ Cloudy

Special Information:
- Event/Festival: □ Yes □ No
- Holiday: □ Yes □ No

Distribution:
- Meals Distributed: ________ units
- Notes: ________________________

Collected by: ________________
Verified by: __________________
```

---

## 🚀 Getting Started

1. **Choose collection method**: Form / App / Manual
2. **Create instructions**: Train staff
3. **Start collecting**: Daily data
4. **Review weekly**: Check quality
5. **Retrain monthly**: Improve model
6. **Track accuracy**: Monitor improvements

---

**Remember**: Good data = Better predictions = Better food distribution! 📊✨
