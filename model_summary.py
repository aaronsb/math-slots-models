#!/usr/bin/env python3
import json
import sys
from typing import Dict, Any
from pathlib import Path

# ANSI Color codes
CYAN = "\033[96m"      # Headers
GREEN = "\033[92m"     # Game info
YELLOW = "\033[93m"    # Description
MAGENTA = "\033[95m"   # Important numbers
RESET = "\033[0m"      # Reset color
BOLD = "\033[1m"       # Bold text

def load_model_config(file_path: str) -> Dict[str, Any]:
    """Load and parse the JSON model configuration file."""
    with open(file_path, 'r') as f:
        return json.load(f)

def analyze_rtp(rtp_config: list) -> dict:
    """Analyze RTP configuration and return key statistics."""
    if not rtp_config:
        return {}
    
    min_rtp = min(float(x['min_ret']) for x in rtp_config)
    max_rtp = max(float(x['max_ret']) for x in rtp_config)
    total_weight = sum(x['weight'] for x in rtp_config)
    weighted_avg = sum(float(x['min_ret']) * x['weight'] for x in rtp_config) / total_weight
    
    return {
        'min_rtp': min_rtp,
        'max_rtp': max_rtp,
        'weighted_avg_rtp': round(weighted_avg, 2),
        'configurations': len(rtp_config)
    }

def analyze_bets(bets_config: list) -> dict:
    """Analyze betting configurations and return key statistics."""
    if not bets_config:
        return {}
    
    unique_lines = set(bet['lines'] for bet in bets_config)
    unique_denoms = set(bet['denom'] for bet in bets_config)
    unique_bpl = set(bet['bpl'] for bet in bets_config)
    
    min_bet = min(bet['lines'] * bet['bpl'] * bet['denom'] for bet in bets_config)
    max_bet = max(bet['lines'] * bet['bpl'] * bet['denom'] for bet in bets_config)
    
    return {
        'total_configurations': len(bets_config),
        'available_lines': sorted(list(unique_lines)),
        'denominations': sorted(list(unique_denoms)),
        'bet_per_line_options': sorted(list(unique_bpl)),
        'min_total_bet': min_bet,
        'max_total_bet': max_bet
    }

def summarize_model(config: Dict[str, Any]) -> str:
    """Generate a formatted summary of the model configuration."""
    summary = []
    
    # Basic Game Information
    summary.append(f"{CYAN}{BOLD}=== Game Information ==={RESET}")
    summary.append(f"Game Name: {GREEN}{config.get('game_name', 'N/A')}{RESET}")
    summary.append(f"Game Code: {GREEN}{config.get('game_code', 'N/A')}{RESET}")
    
    # Description
    if 'description' in config:
        summary.append(f"\n{CYAN}{BOLD}=== Description ==={RESET}")
        summary.append(f"{YELLOW}{config['description']}{RESET}")
    
    # Math Settings
    math_type = config.get('math_setting', {}).get('type', {})
    summary.append(f"\n{CYAN}{BOLD}=== Math Configuration ==={RESET}")
    summary.append(f"Model Type: {math_type.get('model_type', 'N/A')}")
    summary.append(f"Game Type: {math_type.get('name', 'N/A')} (v{math_type.get('version', 'N/A')})")
    if math_type.get('cycle_size'):
        summary.append(f"Cycle Size: {MAGENTA}{math_type['cycle_size']}{RESET}")
    
    # RTP Analysis
    rtp_stats = analyze_rtp(config.get('rtp', []))
    if rtp_stats:
        summary.append(f"\n{CYAN}{BOLD}=== RTP Analysis ==={RESET}")
        summary.append(f"RTP Range: {MAGENTA}{rtp_stats['min_rtp']}%{RESET} - {MAGENTA}{rtp_stats['max_rtp']}%{RESET}")
        summary.append(f"Weighted Average RTP: {MAGENTA}{rtp_stats['weighted_avg_rtp']}%{RESET}")
        summary.append(f"Number of RTP Configurations: {MAGENTA}{rtp_stats['configurations']}{RESET}")
    
    # Betting Analysis
    bet_stats = analyze_bets(config.get('bets', []))
    if bet_stats:
        summary.append(f"\n{CYAN}{BOLD}=== Betting Configuration ==={RESET}")
        summary.append(f"Total Bet Configurations: {MAGENTA}{bet_stats['total_configurations']}{RESET}")
        summary.append(f"Available Lines: {MAGENTA}{', '.join(map(str, bet_stats['available_lines']))}{RESET}")
        summary.append(f"Denominations: {MAGENTA}{', '.join(map(str, bet_stats['denominations']))}{RESET}")
        summary.append(f"Bet Per Line Options: {MAGENTA}{', '.join(map(str, bet_stats['bet_per_line_options']))}{RESET}")
        summary.append(f"Total Bet Range: {MAGENTA}{bet_stats['min_total_bet']}{RESET} - {MAGENTA}{bet_stats['max_total_bet']}{RESET} credits")
    
    return "\n".join(summary)

def main():
    if len(sys.argv) != 2:
        print("Usage: python model_summary.py <path_to_json_config>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    if not Path(file_path).exists():
        print(f"Error: File '{file_path}' not found.")
        sys.exit(1)
    
    try:
        config = load_model_config(file_path)
        summary = summarize_model(config)
        print(summary)
    except json.JSONDecodeError:
        print(f"Error: '{file_path}' is not a valid JSON file.")
        sys.exit(1)
    except Exception as e:
        print(f"Error processing file: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
