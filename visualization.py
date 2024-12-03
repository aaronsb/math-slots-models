from dataclasses import dataclass
from typing import List
import matplotlib.pyplot as plt
import io
import os
import subprocess

@dataclass
class SpinRecord:
    """Records data for a single spin"""
    spin_number: int
    balance: int
    bet_amount: int
    win_amount: int

class GameVisualizer:
    """Visualizes game statistics"""
    def __init__(self):
        self.spins: List[SpinRecord] = []

    def record_spin(self, spin_number: int, balance: int, bet_amount: int, win_amount: int):
        """Record data for a single spin"""
        self.spins.append(SpinRecord(spin_number, balance, bet_amount, win_amount))

    def generate_scatter_plot(self, title: str):
        """Generate a scatter plot showing balance progression"""
        if not self.spins:
            return

        # Calculate RTP and bet size
        total_bet = sum(spin.bet_amount for spin in self.spins)
        total_won = sum(spin.win_amount for spin in self.spins)
        rtp = (total_won / total_bet * 100) if total_bet > 0 else 0
        bet_size = self.spins[0].bet_amount if self.spins else 0

        # Create figure and axis
        plt.figure(figsize=(10, 6))
        
        # Plot balance progression
        x = [spin.spin_number for spin in self.spins]
        y = [spin.balance for spin in self.spins]
        
        # Add starting balance reference line
        plt.axhline(y=1000, color='gray', linestyle='--', alpha=0.3, label='Starting Balance')
        
        # Plot points and trend line with different colors
        plt.scatter(x, y, color='blue', alpha=0.6, label='Balance')
        plt.plot(x, y, color='red', alpha=0.3, label='Trend')
        
        # Customize plot
        plt.title(f"{title}\nBet Size: ${bet_size} | RTP: {rtp:.2f}%")
        plt.xlabel("Spin Number")
        plt.ylabel("Balance ($)")
        plt.grid(True, alpha=0.3)
        plt.legend()
        
        # Save plot with unique filename based on game type
        filename = title.lower().replace(" ", "_") + "_progression.png"
        plt.savefig(filename, dpi=100)
        plt.close()
        
        # Try to display using terminal graphics
        try:
            term = os.environ.get('TERM', '').lower()
            if 'kitty' in term:
                print("\nDisplaying plot using kitty graphics protocol:\n")
                subprocess.run(['kitty', '+kitten', 'icat', filename], check=True)
            elif 'xterm' in term or 'vt' in term:
                print("\nDisplaying plot using sixel:\n")
                # Suppress the ImageMagick warning by redirecting stderr to DEVNULL
                subprocess.run(['magick', 'convert', filename, '-resize', '800x600', 'sixel:-'], 
                            check=True, stderr=subprocess.DEVNULL)
            else:
                print(f"Plot saved as: {filename}")
        except Exception as e:
            print(f"Terminal graphics output failed (falling back to PNG): {str(e)}")
            print(f"Plot saved as: {filename}")
