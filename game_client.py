import json
import argparse
from collections import defaultdict
from mathengine import GameMathEngine
from visualization import GameVisualizer
from tabulate import tabulate

# ANSI color codes
class Colors:
    BLUE_BG = '\033[44m'
    WHITE = '\033[97m'
    GREEN = '\033[92m'
    RED = '\033[91m'
    ORANGE = '\033[93m'
    CYAN = '\033[96m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def load_params(filename):
    """Load math parameters from JSON file"""
    with open(filename, 'r') as f:
        return json.load(f)

def run_demo(params, rounds=100, show_rtp_dist=False):
    """Run a demo of the math engine"""
    engine = GameMathEngine(params)
    visualizer = GameVisualizer()
    
    # Track RTP distribution
    rtp_counts = defaultdict(int)
    
    # Initial setup
    balance = 1000  # Starting balance
    
    # Get the lowest available denomination from the settings
    denomination = params['denomination_settings']['values'][0]
    
    # Get first available bet config
    bet_configs = engine.get_available_bets(denomination)
    if not bet_configs:
        raise ValueError(f"No valid bets for denomination: {denomination}")
    bet_config = bet_configs[0]
    
    total_bet = bet_config.lines * bet_config.bpl * bet_config.denom
    
    print(f"\n{Colors.BLUE_BG}{Colors.WHITE}{Colors.BOLD}=== {params['game_name']} Demo ({params['math_setting']['type']['model_type']}) ==={Colors.RESET}")
    print(f"{Colors.CYAN}Starting Balance: ${Colors.BOLD}{balance}{Colors.RESET}")
    print(f"Bet Configuration: {bet_config.lines} lines ${bet_config.bpl} per line denomination {bet_config.denom}")
    
    # Calculate and display expected RTP range
    min_rtp = min(float(rtp['min_ret']) for rtp in params['rtp'])
    max_rtp = max(float(rtp['max_ret']) for rtp in params['rtp'])
    print(f"Expected RTP Range: {Colors.CYAN}{min_rtp:.2f}% - {max_rtp:.2f}%{Colors.RESET}")
    
    # Check if initial bet is too high
    if total_bet > balance:
        print(f"\n{Colors.RED}Error: Initial bet (${total_bet}) exceeds starting balance (${balance}){Colors.RESET}")
        print("Please configure lower bet amounts")
        return
    
    total_wagered = 0
    total_won = 0
    spins = 0
    
    for i in range(rounds):
        spins += 1
        
        # Check if we can afford another spin
        if balance < total_bet:
            print(f"\n{Colors.RED}Insufficient funds to continue! Balance: ${balance}{Colors.RESET}")
            break
            
        # Place bet and spin
        balance -= total_bet
        total_wagered += total_bet
        
        result = engine.spin(bet_config.lines, bet_config.bpl, bet_config.denom)
        win_amount = result.win_amount
        balance += win_amount
        total_won += win_amount
        
        # Record spin data
        visualizer.record_spin(spins, balance, total_bet, win_amount)
        
        # Track RTP for this spin
        spin_rtp = int(result.actual_return_percentage)
        rtp_counts[spin_rtp] += 1
        
        # Print progress every 10 spins with color
        if (i + 1) % 10 == 0:
            balance_color = Colors.GREEN if balance >= 1000 else Colors.ORANGE
            print(f"Round {i + 1} - Current Balance: {balance_color}${balance}{Colors.RESET}")
    
    # Print final statistics with color
    print(f"\n{Colors.BLUE_BG}{Colors.WHITE}{Colors.BOLD}=== Final Statistics ==={Colors.RESET}")
    balance_color = Colors.GREEN if balance >= 1000 else Colors.ORANGE
    print(f"Final Balance: {balance_color}${balance}{Colors.RESET}")
    print(f"Total Spins: {Colors.CYAN}{spins}{Colors.RESET}")
    print(f"Total Wagered: {Colors.ORANGE}${total_wagered}{Colors.RESET}")
    print(f"Total Won: {Colors.GREEN}${total_won}{Colors.RESET}")
    
    # Calculate RTP only if we had any wagers
    if total_wagered > 0:
        rtp = total_won/total_wagered*100
        rtp_color = Colors.GREEN if rtp >= min_rtp else Colors.ORANGE
        print(f"Expected RTP Range: {Colors.CYAN}{min_rtp:.2f}% - {max_rtp:.2f}%{Colors.RESET}")
        print(f"Actual RTP: {rtp_color}{rtp:.2f}%{Colors.RESET}\n")
    else:
        print("Actual RTP: N/A (no wagers placed)\n")
    
    # Print RTP distribution as table if requested
    if show_rtp_dist and spins > 0:
        print(f"{Colors.CYAN}RTP Distribution:{Colors.RESET}")
        table_data = []
        for rtp in sorted(rtp_counts.keys()):
            count = rtp_counts[rtp]
            percentage = (count/spins*100)
            table_data.append([f"{rtp}%", count, f"{percentage:.1f}%"])
        
        headers = ["RTP", "Count", "Percentage"]
        print(tabulate(table_data, headers=headers, tablefmt="grid"))
    
    # Generate visualization
    visualizer.generate_scatter_plot(params['game_name'])

def main():
    parser = argparse.ArgumentParser(description='Run a slot game demo')
    parser.add_argument('--model', dest='params_file', help='JSON file containing math parameters')
    parser.add_argument('--rounds', type=int, default=100, help='Number of rounds to simulate')
    parser.add_argument('--show-rtp-dist', action='store_true', help='Show RTP distribution table')
    args = parser.parse_args()
    
    params = load_params(args.params_file)
    run_demo(params, args.rounds, args.show_rtp_dist)

if __name__ == '__main__':
    main()
