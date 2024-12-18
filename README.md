# Tournament Manager

A poker tournament management system supporting both regular and progressive knockout (PKO) tournaments.

## Features

- Support for regular and PKO tournaments
- Customizable blind structures
- Dynamic payout structures based on player count
- Hand-for-hand mode for bubble play
- Multiway all-in resolution
- Separate admin and display windows
- PKO bounty tracking and calculations
- Tournament clock with level management

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
```

2. Activate the virtual environment:
- Windows:
```bash
.\venv\Scripts\activate
```
- Linux/Mac:
```bash
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

```bash
python main.py
```

This will launch both the admin window and the display window.

## Usage

### Admin Window

- **Tournament Info**: Shows current level, blinds, time remaining, and player count
- **Timer Controls**: Start/pause timer, move between levels
- **Structure Management**: Edit blind and payout structures
- **Player Management**: Add players, process eliminations, handle multiway all-ins
- **Hand for Hand**: Toggle hand-for-hand mode for bubble play

### Display Window

Large format display showing:
- Current blind level
- Time remaining
- Tournament status (including hand-for-hand mode)

### PKO Tournament Features

- Automatic bounty calculations
- Support for multiway all-ins with proportional bounty distribution
- Tracking of player bounties
- Immediate bounty prizes and bounty additions

## Default Settings

- 20-minute levels
- Standard blind structure starting at 25/50
- Multiple payout structures based on field size
- For PKO tournaments: 50% of bounty claimed immediately, 50% added to winner's bounty

## Customization

All structures can be modified through the admin interface:
- Blind levels and durations
- Payout percentages and thresholds
- Buy-in and bounty amounts #   t o u r n a m e n t m a n a g e r  
 