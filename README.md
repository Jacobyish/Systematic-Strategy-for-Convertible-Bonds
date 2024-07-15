# Systematic Multi-Factor Strategy for Convertible Bonds

This repository contains code and resources for developing a systematic multi-factor strategy for trading convertible bonds. The strategy involves several steps including data collection, factor engineering, factor analysis, and backtesting. The goal is to create a robust, data-driven approach to identifying profitable trading opportunities in the convertible bond market.

## Repository Structure

- **Data Collection**
  - `get_code.py`: Script for retrieving and handling bond codes.
  - `get_data.py`: Script for downloading and preprocessing bond market data.

- **Factor Engineering**
  - `factor_cal.py`: Script for creating and calculating factors based on extensive research to suit the needs of the strategy.

- **Factor Analysis**
  - `factor_analysis.py`: Script for analyzing the performance of various factors. Key metrics include:
    - Information Coefficient (IC)
    - Information Ratio (IR)
    - Quantile performance of the factors

- **Backtesting**
  - `backtest_3facs.py`: Script for backtesting the strategy results. Focuses on evaluating:
    - Holding periods
    - Annual return
    - Sharpe ratio
    - Annual volatility
    - Win rate
    - Maximum drawdown

## Getting Started

### Prerequisites

Ensure you have the following installed:

- Python 3.8 or later
- Necessary Python libraries (listed in `requirements.txt`)

### Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/convertible-bonds-strategy.git
    ```
2. Navigate to the project directory:
    ```sh
    cd convertible-bonds-strategy
    ```
3. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

### Usage

1. **Data Collection**: Run the data collection scripts to gather and preprocess market data.
    ```sh
    python get_code.py
    python get_data.py
    ```

2. **Factor Engineering**: Create and calculate factors tailored to the strategy.
    ```sh
    python factor_cal.py
    ```

3. **Factor Analysis**: Analyze the factors to determine their performance and suitability.
    ```sh
    python factor_analysis.py
    ```

4. **Backtesting**: Backtest the strategy to evaluate its performance using historical data.
    ```sh
    python backtest_3facs.py
    ```

## Results

The backtesting script will generate performance metrics including annual return, Sharpe ratio, annual volatility, win rate, and maximum drawdown. These metrics are crucial for assessing the viability and robustness of the trading strategy.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue if you have suggestions for improvements or find any bugs.


## Acknowledgments

- Special thanks to the quantitative research team at Dongxing Securities for their support and insights during the development of this strategy.

---

Feel free to modify this README as necessary to better fit the specifics of your project.
