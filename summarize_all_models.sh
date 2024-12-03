#!/bin/bash

# ANSI color codes
CYAN='\033[96m'
BOLD='\033[1m'
RESET='\033[0m'

# Print header
echo -e "${CYAN}${BOLD}=== Summarizing All Math Models ===${RESET}"
echo -e "${CYAN}Started at: $(date)${RESET}"
echo

# Find all JSON files in the current directory
for model in *.json; do
    # Skip if no json files found
    [[ -e "$model" ]] || continue
    
    echo -e "${CYAN}${BOLD}=== Summarizing model: $model ===${RESET}"
    echo -e "${CYAN}----------------------------------------${RESET}"
    python model_summary.py "$model"
    echo -e "${CYAN}----------------------------------------${RESET}"
    echo
done

echo -e "${CYAN}${BOLD}All models summarized!${RESET}"
echo -e "${CYAN}Completed at: $(date)${RESET}"
