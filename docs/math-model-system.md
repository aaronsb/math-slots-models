# Math Model Simulator/Tester System Documentation

## Overview

The Math Model Simulator/Tester is a comprehensive system for testing and validating slot game math models. It provides tools for simulating game sessions, analyzing Return-to-Player (RTP) distributions, and visualizing results.

## System Architecture

The system consists of several key components:

### 1. Math Engine (mathengine.py)
- Core simulation engine that handles game logic
- Supports two types of math models:
  - FINITE: Uses a predetermined cycle of RTP values
  - TRUE_RANDOM: Randomly selects RTP values based on weights
- Manages bet configurations, denominations, and payline settings
- Handles spin mechanics and RTP calculations

### 2. Game Client (game_client.py)
- Provides the interface for running simulations
- Manages game sessions with configurable parameters:
  - Number of rounds
  - Starting balance
  - Bet configurations
- Tracks and displays real-time statistics:
  - Current balance
  - Total wagered amount
  - Actual RTP
  - Win/loss data

### 3. Model Summary (model_summary.py)
- Analyzes math model configurations
- Generates detailed reports including:
  - RTP ranges and weighted averages
  - Available betting configurations
  - Line and denomination settings
  - Statistical distributions

### 4. Visualization (visualization.py)
- Creates visual representations of simulation results
- Generates scatter plots showing:
  - Balance progression over time
  - Trend analysis
  - RTP performance
- Supports terminal-based graphics output (Kitty/Sixel)

## Configuration Files

The system uses JSON configuration files to define math models:

```json
{
    "game_name": "Game Title",
    "game_code": "GAME_CODE",
    "math_setting": {
        "type": {
            "model_type": "FINITE|TRUE_RANDOM",
            "name": "LINES",
            "version": 1,
            "cycle_size": 1000  // For FINITE models
        }
    },
    "rtp": [
        {
            "id": "RTP_1",
            "min_ret": "92.5",
            "max_ret": "95.0",
            "weight": 1
        }
    ],
    "bets": [
        {
            "id": "BET_1",
            "lines": 20,
            "bpl": 1,
            "denom": 1
        }
    ]
}
```

## Usage

### Running Tests

1. Single Model Test:
```bash
python game_client.py --model game_config.json --rounds 5000 --show-rtp-dist
```

2. Batch Testing:
```bash
./test_all_math.sh [--slidemode]
```

### Command Line Options

- `--model`: Specify the math model configuration file
- `--rounds`: Number of spins to simulate (default: 100)
- `--show-rtp-dist`: Display RTP distribution table
- `--slidemode`: (for test_all_math.sh) Interactive mode with pauses between models

## Analysis Features

1. RTP Analysis
- Expected vs. actual RTP comparison
- RTP distribution across spins
- Weighted average calculations

2. Betting Analysis
- Total bet configurations
- Available lines and denominations
- Min/max bet ranges

3. Visualization
- Balance progression charts
- Trend analysis
- Win/loss distribution

## Output Examples

### Console Output
```
=== Game Title Demo (FINITE) ===
Starting Balance: $1000
Bet Configuration: 20 lines $1 per line denomination 1
Expected RTP Range: 92.50% - 95.00%

Round 10 - Current Balance: $980
...
=== Final Statistics ===
Final Balance: $950
Total Spins: 100
Total Wagered: $2000
Total Won: $1950
Actual RTP: 93.75%
```

### Visual Output
- Generates PNG files with balance progression charts
- Displays charts directly in terminal (if supported)
- Shows trend lines and reference points

## Best Practices

1. Testing Strategy
- Run sufficient rounds (5000+ recommended) for statistical significance
- Test across different bet configurations
- Verify RTP convergence over time

2. Configuration Management
- Maintain separate configs for different game types
- Document RTP settings and weights
- Version control math model changes

3. Results Analysis
- Compare actual vs. expected RTP
- Monitor balance progression
- Analyze win frequency and distribution

## Troubleshooting

Common issues and solutions:

1. Insufficient Balance
- Increase starting balance
- Reduce bet amounts
- Check denomination settings

2. RTP Divergence
- Verify weight distributions
- Increase sample size
- Check cycle size (FINITE models)

3. Visualization Issues
- Ensure matplotlib is installed
- Check terminal graphics support
- Verify write permissions for output files
