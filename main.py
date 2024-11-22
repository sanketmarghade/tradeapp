from flask import Flask, render_template, request
from tradingview_ta import TA_Handler, Interval

# Define interval options
INTERVAL_OPTIONS = {
    "1 Minute": Interval.INTERVAL_1_MINUTE,
    "5 Minutes": Interval.INTERVAL_5_MINUTES,
    "15 Minutes": Interval.INTERVAL_15_MINUTES,
    "30 Minutes": Interval.INTERVAL_30_MINUTES,
    "1 Hour": Interval.INTERVAL_1_HOUR,
    "2 Hours": Interval.INTERVAL_2_HOURS,
    "4 Hours": Interval.INTERVAL_4_HOURS,
    "1 Day": Interval.INTERVAL_1_DAY,
    "1 Week": Interval.INTERVAL_1_WEEK,
    "1 Month": Interval.INTERVAL_1_MONTH
}

# Create Flask app
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    analysis_result = None
    error_message = None

    if request.method == 'POST':
        symbol_input = request.form['symbol'].strip().upper()
        selected_interval_name = request.form['interval']

        if not symbol_input:
            error_message = "Error: Trading symbol cannot be empty."
        else:
            selected_interval = INTERVAL_OPTIONS.get(selected_interval_name)

            # Check if the selected interval is valid
            if not selected_interval:
                error_message = "Error: Invalid interval selected."
            else:
                try:
                    # Set up the TA handler
                    handler = TA_Handler(
                        symbol=symbol_input,
                        screener="india",
                        exchange="NSE",
                        interval=selected_interval
                    )

                    analysis = handler.get_analysis()
                    analysis_result = {
                        "summary": analysis.summary,
                        "indicators": analysis.indicators
                    }
                except Exception as e:
                    error_message = f"An error occurred: {str(e)}"

    return render_template('index.html', 
                           analysis_result=analysis_result,
                           error_message=error_message,
                           intervals=INTERVAL_OPTIONS.keys())

if __name__ == '__main__':
    app.run(debug=False,port=5000)
