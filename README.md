# SmartXI

SmartXI is a Streamlit web application that recommends football teams based on your budget, formation, and playing style. It can also predict the market value of individual players using trained machine learning models.

---

## Project Structure

- `app.py` - Main Streamlit app.
- `trainTeam.py` - Script to train the team recommendation model.
- `trainMarket.py` - Script to train the player market value prediction model.
- `data.csv` - Dataset with player information.
- Model pickle files (`market_value_model.pkl`, `label_encoders.pkl`, etc.) generated after training.

---

## Setup Instructions

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

### Installation

1. Clone or download the project files to your local machine.
2. Navigate to the project directory in your terminal or command prompt.
3. (Optional but recommended) Create and activate a virtual environment:

   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # macOS/Linux
   source venv/bin/activate
   ```

4. Install required Python packages:

   ```bash
   pip install streamlit pandas plotly scikit-learn numpy
   ```

5. Ensure `data.csv` is present in the project folder.
6. Run training scripts to generate the necessary model files:

   ```bash
   python trainMarket.py
   python trainTeam.py
   ```

---

## Running the Application

Start the Streamlit app by running:

```bash
streamlit run app.py
```

This will launch the app in your default web browser, usually at `http://localhost:8501`.

---

## How to Use

### Options

- **Recommend a Team:**  
  Enter your budget, select a formation (4-3-3, 4-4-2, or 3-4-3), and choose a playing style (Attacking, Balanced, Defensive). Click "Generate Team" to see a recommended lineup and a visual formation on the field.

- **Predict Player Market Value:**  
  Select a player from the dropdown list and click "Predict" to see an estimated market value and a radar chart showing key player stats.

---

## Notes & Troubleshooting

- Ensure `data.csv` is complete and correctly formatted.
- If you encounter errors about missing model files, re-run the training scripts.
- Plotly visualizations require a functional browser.
- Use a virtual environment to avoid dependency conflicts.

---

## Contact

Feel free to reach out if you have questions or need assistance.

---

Enjoy building your SmartXI football team! ⚽