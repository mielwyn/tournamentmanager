from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                            QLabel, QPushButton, QSpinBox, QComboBox,
                            QTableWidget, QTableWidgetItem, QInputDialog,
                            QMessageBox, QGroupBox, QLineEdit, QScrollArea,
                            QDoubleSpinBox, QDialog, QFormLayout)
from PyQt6.QtCore import QTimer, Qt, pyqtSignal
from tournament_manager import TournamentManager
from tournament_types import TournamentType, BlindLevel, Player, PayoutStructure, MultiwayAllInResult
from decimal import Decimal
from typing import List, Dict

class BlindStructureDialog(QDialog):
    def __init__(self, blind_structure: List[BlindLevel], parent=None):
        super().__init__(parent)
        self.blind_structure = blind_structure.copy()
        self.setup_ui()
        
    def setup_ui(self):
        self.setWindowTitle("Edit Blind Structure")
        layout = QVBoxLayout()
        
        # Blind structure table
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Small Blind", "Big Blind", "Ante", "Duration (min)"])
        
        # Add existing levels
        self.update_table()
        
        # Add/Remove buttons
        btn_layout = QHBoxLayout()
        add_btn = QPushButton("Add Level")
        add_btn.clicked.connect(self.add_level)
        remove_btn = QPushButton("Remove Level")
        remove_btn.clicked.connect(self.remove_level)
        
        btn_layout.addWidget(add_btn)
        btn_layout.addWidget(remove_btn)
        
        layout.addWidget(self.table)
        layout.addLayout(btn_layout)
        
        # OK/Cancel buttons
        buttons = QHBoxLayout()
        ok_btn = QPushButton("OK")
        ok_btn.clicked.connect(self.accept)
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        
        buttons.addWidget(ok_btn)
        buttons.addWidget(cancel_btn)
        layout.addLayout(buttons)
        
        self.setLayout(layout)
        
    def update_table(self):
        self.table.setRowCount(len(self.blind_structure))
        for i, level in enumerate(self.blind_structure):
            self.table.setItem(i, 0, QTableWidgetItem(str(level.small_blind)))
            self.table.setItem(i, 1, QTableWidgetItem(str(level.big_blind)))
            self.table.setItem(i, 2, QTableWidgetItem(str(level.ante)))
            self.table.setItem(i, 3, QTableWidgetItem(str(level.duration_minutes)))
            
    def add_level(self):
        last_level = self.blind_structure[-1] if self.blind_structure else BlindLevel(100, 200, 0, 20)
        new_level = BlindLevel(
            last_level.small_blind * 2,
            last_level.big_blind * 2,
            last_level.ante * 2 if last_level.ante > 0 else 0,
            last_level.duration_minutes
        )
        self.blind_structure.append(new_level)
        self.update_table()
        
    def remove_level(self):
        if len(self.blind_structure) > 1:
            self.blind_structure.pop()
            self.update_table()
            
    def get_blind_structure(self) -> List[BlindLevel]:
        return self.blind_structure

class PayoutStructureDialog(QDialog):
    def __init__(self, payout_structures: List[PayoutStructure], parent=None):
        super().__init__(parent)
        self.payout_structures = payout_structures.copy()
        self.setup_ui()
        
    def setup_ui(self):
        self.setWindowTitle("Edit Payout Structures")
        layout = QVBoxLayout()
        
        # Structure selector
        self.structure_combo = QComboBox()
        self.update_structure_combo()
        self.structure_combo.currentIndexChanged.connect(self.load_structure)
        
        # Payout table
        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Position", "Percentage"])
        
        # Minimum players
        min_players_layout = QHBoxLayout()
        min_players_layout.addWidget(QLabel("Minimum Players:"))
        self.min_players_spin = QSpinBox()
        self.min_players_spin.setRange(2, 1000)
        min_players_layout.addWidget(self.min_players_spin)
        
        # Buttons
        btn_layout = QHBoxLayout()
        add_structure_btn = QPushButton("Add Structure")
        add_structure_btn.clicked.connect(self.add_structure)
        remove_structure_btn = QPushButton("Remove Structure")
        remove_structure_btn.clicked.connect(self.remove_structure)
        add_position_btn = QPushButton("Add Position")
        add_position_btn.clicked.connect(self.add_position)
        
        btn_layout.addWidget(add_structure_btn)
        btn_layout.addWidget(remove_structure_btn)
        btn_layout.addWidget(add_position_btn)
        
        layout.addWidget(self.structure_combo)
        layout.addLayout(min_players_layout)
        layout.addWidget(self.table)
        layout.addLayout(btn_layout)
        
        # OK/Cancel
        buttons = QHBoxLayout()
        ok_btn = QPushButton("OK")
        ok_btn.clicked.connect(self.accept)
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        
        buttons.addWidget(ok_btn)
        buttons.addWidget(cancel_btn)
        layout.addLayout(buttons)
        
        self.setLayout(layout)
        if self.payout_structures:
            self.load_structure(0)
            
    def update_structure_combo(self):
        self.structure_combo.clear()
        for structure in self.payout_structures:
            self.structure_combo.addItem(f"{structure.min_players}+ players")
            
    def load_structure(self, index):
        if index < 0 or not self.payout_structures:
            return
            
        structure = self.payout_structures[index]
        self.min_players_spin.setValue(structure.min_players)
        
        self.table.setRowCount(len(structure.positions))
        for i, (pos, percentage) in enumerate(structure.positions.items()):
            self.table.setItem(i, 0, QTableWidgetItem(str(pos)))
            self.table.setItem(i, 1, QTableWidgetItem(str(float(percentage * 100))))
            
    def add_structure(self):
        new_structure = PayoutStructure({1: Decimal('1.0')}, 2)
        self.payout_structures.append(new_structure)
        self.update_structure_combo()
        self.structure_combo.setCurrentIndex(len(self.payout_structures) - 1)
        
    def remove_structure(self):
        if len(self.payout_structures) > 1:
            index = self.structure_combo.currentIndex()
            self.payout_structures.pop(index)
            self.update_structure_combo()
            self.structure_combo.setCurrentIndex(0)
            
    def add_position(self):
        index = self.structure_combo.currentIndex()
        structure = self.payout_structures[index]
        next_pos = max(structure.positions.keys()) + 1
        structure.positions[next_pos] = Decimal('0.05')  # 5% default
        self.load_structure(index)
        
    def get_payout_structures(self) -> List[PayoutStructure]:
        return self.payout_structures

class MultiwayAllInDialog(QDialog):
    def __init__(self, tournament_manager: TournamentManager, parent=None):
        super().__init__(parent)
        self.tournament_manager = tournament_manager
        self.setup_ui()
        
    def setup_ui(self):
        self.setWindowTitle("Process Multiway All-in")
        layout = QVBoxLayout()
        
        # Player selection
        self.player_table = QTableWidget()
        self.player_table.setColumnCount(3)
        self.player_table.setHorizontalHeaderLabels(["Player", "Selected", "Position"])
        self.update_player_table()
        
        # Buttons
        btn_layout = QHBoxLayout()
        process_btn = QPushButton("Process")
        process_btn.clicked.connect(self.process_allin)
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        
        btn_layout.addWidget(process_btn)
        btn_layout.addWidget(cancel_btn)
        
        layout.addWidget(self.player_table)
        layout.addLayout(btn_layout)
        self.setLayout(layout)
        
    def update_player_table(self):
        active_players = [p for p in self.tournament_manager.players.values() if not p.eliminated]
        self.player_table.setRowCount(len(active_players))
        
        for i, player in enumerate(active_players):
            # Player name
            self.player_table.setItem(i, 0, QTableWidgetItem(player.name))
            
            # Checkbox for selection
            checkbox = QTableWidgetItem()
            checkbox.setFlags(Qt.ItemFlag.ItemIsUserCheckable | Qt.ItemFlag.ItemIsEnabled)
            checkbox.setCheckState(Qt.CheckState.Unchecked)
            self.player_table.setItem(i, 1, checkbox)
            
            # Position spinbox
            position_spin = QSpinBox()
            position_spin.setRange(1, len(active_players))
            self.player_table.setCellWidget(i, 2, position_spin)
            
    def process_allin(self):
        selected_players = []
        positions = {}
        
        for i in range(self.player_table.rowCount()):
            if self.player_table.item(i, 1).checkState() == Qt.CheckState.Checked:
                player_name = self.player_table.item(i, 0).text()
                position = self.player_table.cellWidget(i, 2).value()
                
                # Find player by name
                player = next(p for p in self.tournament_manager.players.values() 
                            if p.name == player_name)
                selected_players.append(player)
                positions[player.id] = position
                
        if len(selected_players) < 2:
            QMessageBox.warning(self, "Error", "Select at least 2 players")
            return
            
        if len(set(positions.values())) != len(positions):
            QMessageBox.warning(self, "Error", "Each player must have a unique position")
            return
            
        result = MultiwayAllInResult(
            players=selected_players,
            finishing_positions=positions
        )
        
        bounty_prizes = self.tournament_manager.process_multiway_allin(result)
        
        # Show results
        if bounty_prizes:
            msg = "Bounty prizes won:\n"
            for player_id, prize in bounty_prizes.items():
                player = self.tournament_manager.players[player_id]
                msg += f"{player.name}: {prize}\n"
            QMessageBox.information(self, "Results", msg)
            
        self.accept()

class AdminWindow(QMainWindow):
    player_eliminated = pyqtSignal(int, int)  # eliminated_id, eliminator_id
    
    def __init__(self, tournament_manager: TournamentManager):
        super().__init__()
        self.tournament_manager = tournament_manager
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_clock)
        self.remaining_seconds = 0
        self.setup_ui()
        
    def setup_ui(self):
        self.setWindowTitle("Tournament Admin")
        self.setMinimumSize(1200, 800)
        
        # Create main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout()
        main_widget.setLayout(main_layout)
        
        # Left panel for tournament controls
        left_panel = QWidget()
        left_layout = QVBoxLayout()
        left_panel.setLayout(left_layout)
        
        # Tournament Info Group
        info_group = QGroupBox("Tournament Info")
        info_layout = QVBoxLayout()
        
        self.level_label = QLabel("Level: 1")
        self.blind_label = QLabel("Blinds: -/-")
        self.time_label = QLabel("Time Remaining: --:--")
        self.players_left_label = QLabel("Players Remaining: 0")
        
        info_layout.addWidget(self.level_label)
        info_layout.addWidget(self.blind_label)
        info_layout.addWidget(self.time_label)
        info_layout.addWidget(self.players_left_label)
        info_group.setLayout(info_layout)
        
        # Timer Controls
        timer_group = QGroupBox("Timer Controls")
        timer_layout = QHBoxLayout()
        
        self.start_pause_button = QPushButton("Start")
        self.start_pause_button.clicked.connect(self.toggle_timer)
        self.next_level_button = QPushButton("Next Level")
        self.next_level_button.clicked.connect(self.next_level)
        self.prev_level_button = QPushButton("Previous Level")
        self.prev_level_button.clicked.connect(self.prev_level)
        
        timer_layout.addWidget(self.prev_level_button)
        timer_layout.addWidget(self.start_pause_button)
        timer_layout.addWidget(self.next_level_button)
        timer_group.setLayout(timer_layout)
        
        # Structure Controls
        structure_group = QGroupBox("Tournament Structure")
        structure_layout = QVBoxLayout()
        
        edit_blinds_btn = QPushButton("Edit Blind Structure")
        edit_blinds_btn.clicked.connect(self.edit_blind_structure)
        edit_payouts_btn = QPushButton("Edit Payout Structure")
        edit_payouts_btn.clicked.connect(self.edit_payout_structure)
        
        structure_layout.addWidget(edit_blinds_btn)
        structure_layout.addWidget(edit_payouts_btn)
        structure_group.setLayout(structure_layout)
        
        # Hand for Hand Controls
        hfh_group = QGroupBox("Hand for Hand")
        hfh_layout = QHBoxLayout()
        
        self.hfh_button = QPushButton("Enable Hand for Hand")
        self.hfh_button.setCheckable(True)
        self.hfh_button.clicked.connect(self.toggle_hand_for_hand)
        
        hfh_layout.addWidget(self.hfh_button)
        hfh_group.setLayout(hfh_layout)
        
        # Add groups to left panel
        left_layout.addWidget(info_group)
        left_layout.addWidget(timer_group)
        left_layout.addWidget(structure_group)
        left_layout.addWidget(hfh_group)
        left_layout.addStretch()
        
        # Right panel for player management
        right_panel = QWidget()
        right_layout = QVBoxLayout()
        right_panel.setLayout(right_layout)
        
        # Player Management
        player_group = QGroupBox("Player Management")
        player_layout = QVBoxLayout()
        
        # Player controls
        player_controls = QHBoxLayout()
        self.add_player_button = QPushButton("Add Player")
        self.add_player_button.clicked.connect(self.add_player)
        self.eliminate_player_button = QPushButton("Process Elimination")
        self.eliminate_player_button.clicked.connect(self.process_elimination)
        self.multiway_allin_button = QPushButton("Multiway All-in")
        self.multiway_allin_button.clicked.connect(self.process_multiway_allin)
        
        player_controls.addWidget(self.add_player_button)
        player_controls.addWidget(self.eliminate_player_button)
        player_controls.addWidget(self.multiway_allin_button)
        
        # Player table
        self.player_table = QTableWidget()
        self.player_table.setColumnCount(4)
        self.player_table.setHorizontalHeaderLabels(["ID", "Name", "Bounty", "Status"])
        
        player_layout.addLayout(player_controls)
        player_layout.addWidget(self.player_table)
        player_group.setLayout(player_layout)
        
        right_layout.addWidget(player_group)
        
        # Add panels to main layout
        main_layout.addWidget(left_panel, 1)
        main_layout.addWidget(right_panel, 2)
        
    def toggle_timer(self):
        if self.timer.isActive():
            self.timer.stop()
            self.start_pause_button.setText("Start")
        else:
            if self.remaining_seconds <= 0:
                current_level = self.tournament_manager.blind_structure[self.tournament_manager.current_level]
                self.remaining_seconds = current_level.duration_minutes * 60
            self.timer.start(1000)
            self.start_pause_button.setText("Pause")
            
    def update_clock(self):
        if self.remaining_seconds > 0:
            self.remaining_seconds -= 1
            minutes = self.remaining_seconds // 60
            seconds = self.remaining_seconds % 60
            self.time_label.setText(f"Time Remaining: {minutes:02d}:{seconds:02d}")
        else:
            self.timer.stop()
            self.start_pause_button.setText("Start")
            QMessageBox.information(self, "Level Complete", "Current level has ended!")
            
    def next_level(self):
        if self.tournament_manager.current_level < len(self.tournament_manager.blind_structure) - 1:
            self.tournament_manager.current_level += 1
            self.update_level_display()
            
    def prev_level(self):
        if self.tournament_manager.current_level > 0:
            self.tournament_manager.current_level -= 1
            self.update_level_display()
            
    def update_level_display(self):
        level = self.tournament_manager.blind_structure[self.tournament_manager.current_level]
        self.level_label.setText(f"Level: {self.tournament_manager.current_level + 1}")
        self.blind_label.setText(f"Blinds: {level.small_blind}/{level.big_blind}" + 
                               (f" Ante: {level.ante}" if level.ante > 0 else ""))
        self.remaining_seconds = level.duration_minutes * 60
        self.update_clock()
        
    def toggle_hand_for_hand(self):
        self.tournament_manager.hand_for_hand = self.hfh_button.isChecked()
        self.hfh_button.setText("Disable Hand for Hand" if self.tournament_manager.hand_for_hand 
                              else "Enable Hand for Hand")
        
    def edit_blind_structure(self):
        dialog = BlindStructureDialog(self.tournament_manager.blind_structure, self)
        if dialog.exec():
            self.tournament_manager.blind_structure = dialog.get_blind_structure()
            self.update_level_display()
            
    def edit_payout_structure(self):
        dialog = PayoutStructureDialog(self.tournament_manager.payout_structures, self)
        if dialog.exec():
            self.tournament_manager.payout_structures = dialog.get_payout_structures()
            
    def add_player(self):
        name, ok = QInputDialog.getText(self, "Add Player", "Enter player name:")
        if ok and name:
            self.tournament_manager.add_player(name)
            self.update_player_table()
            
    def process_elimination(self):
        eliminated_id, ok1 = QInputDialog.getInt(self, "Process Elimination", 
                                               "Enter eliminated player ID:", 1, 1)
        if not ok1:
            return
            
        if self.tournament_manager.tournament_type == TournamentType.PKO:
            eliminator_id, ok2 = QInputDialog.getInt(self, "Process Elimination",
                                                   "Enter eliminator player ID:", 1, 1)
            if not ok2:
                return
                
            bounty_won = self.tournament_manager.process_knockout(eliminator_id, eliminated_id)
            QMessageBox.information(self, "Knockout Processed", 
                                  f"Player {eliminator_id} won {bounty_won} bounty")
        else:
            self.tournament_manager.players[eliminated_id].eliminated = True
            
        self.update_player_table()
        self.player_eliminated.emit(eliminated_id, eliminator_id if self.tournament_manager.tournament_type == TournamentType.PKO else 0)
        
        # Show payout if in the money
        prize = self.tournament_manager.calculate_prize(self.tournament_manager.get_remaining_players() + 1)
        if prize:
            QMessageBox.information(self, "Payout", 
                                  f"Player {eliminated_id} wins {prize}")
        
    def process_multiway_allin(self):
        dialog = MultiwayAllInDialog(self.tournament_manager, self)
        if dialog.exec():
            self.update_player_table()
        
    def update_player_table(self):
        self.player_table.setRowCount(len(self.tournament_manager.players))
        active_players = 0
        
        for idx, (player_id, player) in enumerate(self.tournament_manager.players.items()):
            if not player.eliminated:
                active_players += 1
                
            self.player_table.setItem(idx, 0, QTableWidgetItem(str(player.id)))
            self.player_table.setItem(idx, 1, QTableWidgetItem(player.name))
            self.player_table.setItem(idx, 2, QTableWidgetItem(str(player.bounty) if player.bounty else "-"))
            self.player_table.setItem(idx, 3, QTableWidgetItem("Active" if not player.eliminated else "Eliminated"))
            
        self.players_left_label.setText(f"Players Remaining: {active_players}")

class DisplayWindow(QMainWindow):
    def __init__(self, tournament_manager: TournamentManager):
        super().__init__()
        self.tournament_manager = tournament_manager
        self.timer = QTimer()
        self.setup_ui()
        
    def setup_ui(self):
        self.setWindowTitle("Tournament Display")
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout()
        
        self.blind_label = QLabel()
        self.time_label = QLabel()
        self.status_label = QLabel()
        
        # Set large font for visibility
        font = self.blind_label.font()
        font.setPointSize(48)
        self.blind_label.setFont(font)
        self.time_label.setFont(font)
        self.status_label.setFont(font)
        
        # Center align text
        self.blind_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.time_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        layout.addWidget(self.blind_label)
        layout.addWidget(self.time_label)
        layout.addWidget(self.status_label)
        
        central_widget.setLayout(layout) 