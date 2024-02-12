# eth_bot


Get Rich with Ethereum

  This Python script aims to automate Ethereum trading by applying technical analysis strategies to real-time market data. It leverages the Bybit API for fetching current Ethereum prices and executes trades based 
 on predefined indicators such as RSI (Relative Strength Index) and Stochastic Oscillator values. The script is designed to run continuously, making decisions to buy or sell Ethereum based on the calculated     
 probability of price increase and various market conditions.

Features:
  Real-Time Data Fetching: Utilizes the Bybit API to monitor Ethereum's price in real-time.
  Technical Analysis: Implements RSI and Stochastic Oscillator calculations to make trading decisions.
  Automated Trading: Automatically places buy or sell orders based on specific market indicators.
  SQLite Database Integration: Optionally stores transaction data for further analysis.
  Dynamic Configuration: Uses environment variables for API keys, trading thresholds, and other configurations.
  
Prerequisites:

  Before running this script, you'll need:

    Python 3.x installed on your machine.
    An account on Bybit with API keys generated.
    The following Python libraries: pybit, ccxt, requests, numpy, and sqlite3. Installation commands are included in the script.

Setup:

  Clone the Repository: Clone this repository to your local machine.
  Install Dependencies: Ensure all required Python libraries are installed. The script attempts to install missing packages automatically.
  Configure API Keys: Store your Bybit API key and secret in environment variables or a .env file for security.
  Database Setup (Optional): If you wish to store transactions, ensure SQLite is set up on your machine.
  
Usage:
  
  To run the script, simply execute:

    python get_rich_with_ethereum.py

  Ensure you monitor the script's activity and remain compliant with your trading platform's terms of service.

Disclaimer:

  This script is provided for educational purposes only. Trading cryptocurrencies involves significant risk, and you should only trade with funds you can afford to lose. The author bears no responsibility for any financial losses incurred.

Author
Fran Carrasco

Contact
Email: francelta@gmail.com
GitHub: https://github.com/francelta
License
This project is private and the rights belong to the author.


