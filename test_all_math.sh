#!/bin/bash

# ANSI color codes
CYAN='\033[96m'
GREEN='\033[92m'
YELLOW='\033[93m'
BOLD='\033[1m'
RESET='\033[0m'

# Default slidemode to false
SLIDEMODE=false

# Parse command line arguments
while [[ "$#" -gt 0 ]]; do
    case $1 in
        --slidemode) SLIDEMODE=true ;;
        *) echo "Unknown parameter: $1"; exit 1 ;;
    esac
    shift
done

# Function to wait for enter key if slidemode is enabled
wait_for_enter() {
    if [ "$SLIDEMODE" = true ]; then
        echo -e "\n${YELLOW}Press ENTER to continue...${RESET}"
        read
        clear
    fi
}

# Print header
echo -e "${CYAN}${BOLD}=== Testing All Math Models ===${RESET}"
echo -e "${CYAN}Started at: $(date)${RESET}"
echo

# Find all JSON files in the current directory
for model in *.json; do
    # Skip if no json files found
    [[ -e "$model" ]] || continue
    
    # Clear screen in slidemode
    if [ "$SLIDEMODE" = true ]; then
        clear
    fi
    
    echo -e "${CYAN}${BOLD}=== Testing model: ${GREEN}$model${RESET} ===${RESET}"
    echo -e "${YELLOW}Started at: $(date)${RESET}"
    echo -e "${CYAN}----------------------------------------${RESET}"
    # python game_client.py --model "$model" --rounds 50 --show-rtp-dist - optionally show rtp distribution
    python game_client.py --model "$model" --rounds 5000
    echo -e "${CYAN}----------------------------------------${RESET}"
    echo
    
    # Wait for enter in slidemode
    wait_for_enter
done

echo -e "${CYAN}${BOLD}All math models tested!${RESET}"
echo -e "${CYAN}Completed at: $(date)${RESET}"
