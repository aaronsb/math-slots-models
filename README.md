# Math Model Simulator/Tester

A comprehensive system for testing and validating slot game math models. This tool provides capabilities for simulating game sessions, analyzing Return-to-Player (RTP) distributions, and visualizing results.

## Features

- **Math Engine**: Core simulation engine for game logic with support for FINITE and TRUE_RANDOM math models
- **Game Client**: Interface for running simulations with configurable parameters
- **Model Summary**: Analysis tools for math model configurations
- **Visualization**: Visual representations of simulation results including balance progression and RTP performance

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/mathtest.git
cd mathtest
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Running Single Model Tests

```bash
python game_client.py --model game_config.json --rounds 5000 --show-rtp-dist
```

### Batch Testing All Models

```bash
./test_all_math.sh
```

### Command Line Options

- `--model`: Specify the math model configuration file
- `--rounds`: Number of spins to simulate (default: 100)
- `--show-rtp-dist`: Display RTP distribution table

## Configuration

Math models are defined using JSON configuration files. Example structure:

```json
{
    "game_name": "Game Title",
    "game_code": "GAME_CODE",
    "math_setting": {
        "type": {
            "model_type": "FINITE|TRUE_RANDOM",
            "name": "LINES",
            "version": 1,
            "cycle_size": 1000
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

## Project Structure

- `mathengine.py`: Core simulation engine
- `game_client.py`: Simulation interface
- `model_summary.py`: Configuration analysis tools
- `visualization.py`: Results visualization
- `test_all_math.sh`: Batch testing script
- `docs/`: Detailed documentation
- Various JSON files: Different slot game configurations

## Best Practices

1. Run sufficient rounds (5000+ recommended) for statistical significance
2. Test across different bet configurations
3. Verify RTP convergence over time
4. Monitor balance progression and win frequency

## Documentation

For detailed system documentation, please refer to [docs/math-model-system.md](docs/math-model-system.md).

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.
