from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                            QLabel, QPushButton, QSpinBox, QComboBox,
                            QTableWidget, QTableWidgetItem, QInputDialog,
                            QMessageBox, QGroupBox, QLineEdit, QScrollArea,
                            QDoubleSpinBox, QDialog, QFormLayout, QWizard,
                            QWizardPage)
from PyQt6.QtCore import QTimer, Qt, pyqtSignal
from PyQt6.QtGui import QFont
from tournament_manager import TournamentManager
from tournament_types import TournamentType, BlindLevel, Player, PayoutStructure
from decimal import Decimal
from typing import List, Dict, Optional

class TournamentSetupWizard(QWizard):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Tournament Setup")
        self.setup_pages()
        
    def setup_pages(self):
        # Tournament Type Page
        type_page = QWizardPage()
        type_page.setTitle("Tournament Type")
        type_layout = QVBoxLayout()
        
        self.type_combo = QComboBox()
        self.type_combo.addItems([t.value for t in TournamentType])
        
        type_layout.addWidget(QLabel("Select tournament type:"))
        type_layout.addWidget(self.type_combo)
        type_page.setLayout(type_layout)
        
        # Buy-in Page
        buyin_page = QWizardPage()
        buyin_page.setTitle("Buy-in Information")
        buyin_layout = QFormLayout()
        
        self.buyin_spin = QDoubleSpinBox()
        self.buyin_spin.setRange(0, 1000000)
        self.buyin_spin.setValue(100)
        self.buyin_spin.setPrefix("$")
        
        self.bounty_spin = QDoubleSpinBox()
        self.bounty_spin.setRange(0, 1000000)
        self.bounty_spin.setValue(50)
        self.bounty_spin.setPrefix("$")
        
        buyin_layout.addRow("Buy-in amount:", self.buyin_spin)
        buyin_layout.addRow("Bounty amount:", self.bounty_spin)
        buyin_page.setLayout(buyin_layout)
        
        # Add pages
        self.addPage(type_page)
        self.addPage(buyin_page)
        
    def get_tournament_settings(self) -> Optional[Dict]:
        if self.result() == QWizard.DialogCode.Accepted:
            return {
                'tournament_type': TournamentType(self.type_combo.currentText()),
                'buy_in': Decimal(str(self.buyin_spin.value())),
                'bounty_amount': (Decimal(str(self.bounty_spin.value())) 
                                if self.type_combo.currentText() == TournamentType.PKO.value 
                                else None)
            }
        return None

class DisplayWindow(QMainWindow):
    def __init__(self, tournament_manager: TournamentManager):
        super().__init__()
        self.tournament_manager = tournament_manager
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_display)
        self.timer.start(1000)  # Update every second
        self.setup_ui()
        
    def setup_ui(self):
        self.setWindowTitle("Tournament Display")
        self.setMinimumSize(800, 600)
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout()
        
        # Use large, bold font for displays
        large_font = QFont()
        large_font.setPointSize(48)
        large_font.setBold(True)
        
        medium_font = QFont()
        medium_font.setPointSize(36)
        medium_font.setBold(True)
        
        # Level and blind info
        level_group = QGroupBox()
        level_layout = QVBoxLayout()
        
        self.level_label = QLabel("Level: 1")
        self.level_label.setFont(medium_font)
        self.level_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.blind_label = QLabel("25/50")
        self.blind_label.setFont(large_font)
        self.blind_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.ante_label = QLabel("Ante: 0")
        self.ante_label.setFont(medium_font)
        self.ante_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        level_layout.addWidget(self.level_label)
        level_layout.addWidget(self.blind_label)
        level_layout.addWidget(self.ante_label)
        level_group.setLayout(level_layout)
        
        # Timer display
        self.time_label = QLabel("20:00")
        self.time_label.setFont(large_font)
        self.time_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Status (hand for hand, etc.)
        self.status_label = QLabel()
        self.status_label.setFont(medium_font)
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Players remaining
        self.players_label = QLabel()
        self.players_label.setFont(medium_font)
        self.players_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        layout.addWidget(level_group)
        layout.addWidget(self.time_label)
        layout.addWidget(self.status_label)
        layout.addWidget(self.players_label)
        
        central_widget.setLayout(layout)
        self.update_display()
        
    def update_display(self):
        # Update level info
        level = self.tournament_manager.get_current_level_info()
        self.level_label.setText(f"Level: {self.tournament_manager.current_level + 1}")
        self.blind_label.setText(f"{level.small_blind:,}/{level.big_blind:,}")
        self.ante_label.setText(f"Ante: {level.ante:,}" if level.ante > 0 else "")
        
        # Update status
        if self.tournament_manager.hand_for_hand:
            self.status_label.setText("HAND FOR HAND")
            self.status_label.setStyleSheet("QLabel { color: red; }")
        else:
            self.status_label.setText("")
            self.status_label.setStyleSheet("")
            
        # Update players remaining
        remaining = self.tournament_manager.get_remaining_players()
        self.players_label.setText(f"Players Remaining: {remaining}")

# ... rest of the file remains unchanged ... 