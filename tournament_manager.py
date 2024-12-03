from decimal import Decimal
from typing import List, Dict, Optional
from tournament_types import *

class TournamentManager:
    def __init__(self, tournament_type: TournamentType, 
                 buy_in: Decimal,
                 blind_structure: List[BlindLevel],
                 payout_structures: List[PayoutStructure],
                 bounty_amount: Optional[Decimal] = None):
        self.tournament_type = tournament_type
        self.buy_in = buy_in
        self.blind_structure = blind_structure
        self.payout_structures = sorted(payout_structures, key=lambda x: x.min_players)
        self.bounty_amount = bounty_amount
        self.players: Dict[int, Player] = {}
        self.current_level = 0
        self.hand_for_hand = False
        self.total_prize_pool = Decimal('0')
        
    def add_player(self, name: str) -> Player:
        player_id = len(self.players) + 1
        bounty = self.bounty_amount if self.tournament_type == TournamentType.PKO else None
        player = Player(id=player_id, name=name, bounty=bounty)
        self.players[player_id] = player
        self.total_prize_pool += self.buy_in
        return player
        
    def process_knockout(self, eliminator_id: int, eliminated_id: int) -> Decimal:
        """Process a single knockout in a PKO tournament"""
        if self.tournament_type != TournamentType.PKO:
            raise ValueError("Knockout processing only available in PKO tournaments")
            
        eliminated_player = self.players[eliminated_id]
        eliminator = self.players[eliminator_id]
        
        bounty = eliminated_player.bounty
        # Half of bounty goes to eliminator immediately
        immediate_prize = (bounty / 2).quantize(Decimal('0.01'))
        # Other half gets added to eliminator's bounty
        eliminator.bounty += bounty - immediate_prize
        
        eliminated_player.eliminated = True
        return immediate_prize
        
    def process_multiway_allin(self, result: MultiwayAllInResult) -> Dict[int, Decimal]:
        """Process a multiway all-in situation, returning bounty prizes won"""
        bounty_prizes: Dict[int, Decimal] = {}
        if self.tournament_type != TournamentType.PKO:
            return bounty_prizes
            
        # Update player positions and elimination status
        for player in result.players:
            position = result.finishing_positions[player.id]
            player.position = position
            if position != 1:  # Not the winner
                player.eliminated = True
                
        # Process bounties for eliminated players
        for eliminated in result.players:
            if eliminated.position == 1:  # Skip the winner
                continue
                
            bounty = eliminated.bounty
            # Find players who finished better (lower position number)
            eliminators = [
                p for p in result.players 
                if p.position < eliminated.position
            ]
            
            if eliminators:
                # Split immediate bounty equally among eliminators
                share = (bounty / 2 / len(eliminators)).quantize(Decimal('0.01'))
                remaining = bounty / 2
                
                for eliminator in eliminators:
                    bounty_prizes[eliminator.id] = (
                        bounty_prizes.get(eliminator.id, Decimal('0')) + 
                        share
                    )
                    # Add equal share to eliminator's bounty
                    eliminator.bounty += remaining / len(eliminators)
                    
        return bounty_prizes
        
    def get_active_payout_structure(self) -> PayoutStructure:
        """Get the appropriate payout structure based on number of players"""
        num_players = len(self.players)
        for structure in reversed(self.payout_structures):
            if num_players >= structure.min_players:
                return structure
        return self.payout_structures[0]  # Fallback to smallest structure
        
    def calculate_prize(self, position: int) -> Optional[Decimal]:
        """Calculate prize money for a given position"""
        structure = self.get_active_payout_structure()
        if position not in structure.positions:
            return None
        return (self.total_prize_pool * structure.positions[position]).quantize(Decimal('0.01'))
        
    def get_remaining_players(self) -> int:
        """Get number of players still in the tournament"""
        return sum(1 for p in self.players.values() if not p.eliminated)