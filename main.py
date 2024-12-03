import sys
from decimal import Decimal
from PyQt6.QtWidgets import QApplication
from tournament_types import TournamentType, BlindLevel, PayoutStructure
from tournament_manager import TournamentManager
from main_window import AdminWindow, DisplayWindow

def create_default_blind_structure():
    return [
        BlindLevel(25, 50, 0, 20),
        BlindLevel(50, 100, 0, 20),
        BlindLevel(75, 150, 0, 20),
        BlindLevel(100, 200, 25, 20),
        BlindLevel(150, 300, 25, 20),
        BlindLevel(200, 400, 50, 20),
        BlindLevel(300, 600, 75, 20),
        BlindLevel(400, 800, 100, 20),
        BlindLevel(500, 1000, 100, 20),
        BlindLevel(600, 1200, 200, 20),
        BlindLevel(800, 1600, 200, 20),
        BlindLevel(1000, 2000, 300, 20),
        BlindLevel(1500, 3000, 400, 20),
        BlindLevel(2000, 4000, 500, 20),
        BlindLevel(3000, 6000, 1000, 20),
        BlindLevel(4000, 8000, 1000, 20),
        BlindLevel(5000, 10000, 1000, 20),
        BlindLevel(6000, 12000, 2000, 20),
        BlindLevel(8000, 16000, 2000, 20),
        BlindLevel(10000, 20000, 3000, 20),
    ]

def create_default_payout_structures():
    return [
        PayoutStructure(
            positions={
                1: Decimal('0.65'),
                2: Decimal('0.35')
            },
            min_players=2
        ),
        PayoutStructure(
            positions={
                1: Decimal('0.50'),
                2: Decimal('0.30'),
                3: Decimal('0.20')
            },
            min_players=7
        ),
        PayoutStructure(
            positions={
                1: Decimal('0.40'),
                2: Decimal('0.25'),
                3: Decimal('0.15'),
                4: Decimal('0.12'),
                5: Decimal('0.08')
            },
            min_players=15
        ),
        PayoutStructure(
            positions={
                1: Decimal('0.35'),
                2: Decimal('0.20'),
                3: Decimal('0.15'),
                4: Decimal('0.10'),
                5: Decimal('0.08'),
                6: Decimal('0.07'),
                7: Decimal('0.05')
            },
            min_players=30
        )
    ]

def main():
    app = QApplication(sys.argv)
    
    # Create tournament manager with default settings
    manager = TournamentManager(
        tournament_type=TournamentType.PKO,  # Change to REGULAR for non-bounty tournaments
        buy_in=Decimal('100'),
        blind_structure=create_default_blind_structure(),
        payout_structures=create_default_payout_structures(),
        bounty_amount=Decimal('50')  # Set to None for regular tournaments
    )
    
    # Create windows
    admin_window = AdminWindow(manager)
    display_window = DisplayWindow(manager)
    
    # Show windows
    admin_window.show()
    display_window.show()
    
    sys.exit(app.exec())

if __name__ == '__main__':
    main() 