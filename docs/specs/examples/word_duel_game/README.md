# Example: Word Duel - Educational Game

> A fun word game created in 30 minutes using specifications

## The Story

**Marcus's Goal**: "My 10-year-old loves Wordle but it's only once a day. I want to make a word game we can play together that helps him learn new vocabulary."

**Traditional Approach**: Learning game frameworks, UI libraries, word databases...

**AGET Approach**: 30 minutes to a playable game

## Step 1: Game Design in Plain English (8 minutes)

Marcus creates `FUNCTIONAL_REQUIREMENTS.md`:

```markdown
# Word Duel - Functional Requirements

## Core Gameplay

### FR-001: Two-Player Word Battle
**User Story**: As players, we want to compete in real-time word challenges
**Acceptance Criteria**:
- Two players take turns
- 30 seconds per turn
- Points based on word length
- First to 100 points wins

### FR-002: Vocabulary Learning
**User Story**: As a parent, I want the game to teach new words
**Acceptance Criteria**:
- Show word definitions after each round
- Track words learned
- Difficulty levels (easy/medium/hard)
- Age-appropriate word lists

### FR-003: Fun Challenges
**User Story**: As players, we want variety to keep it interesting
**Acceptance Criteria**:
- Different game modes:
  - Speed round (most words in 60 seconds)
  - Theme round (animals, food, etc.)
  - Letter challenge (words starting with X)
- Power-ups:
  - Hint (shows first letter)
  - Skip (get new challenge)
  - Double points

### FR-004: Progress Tracking
**User Story**: As a learner, I want to see improvement
**Acceptance Criteria**:
- Show statistics after each game
- Track vocabulary growth
- Achievement badges
- Leaderboard for family
```

## Step 2: Game Rules (5 minutes)

Marcus creates `BUSINESS_RULES.md`:

```markdown
# Word Duel - Game Rules

### BR-001: Fair Play
**Rule**: Words must be real English words from dictionary
**Implementation**: Check against word list API or local dictionary

### BR-002: Age Appropriate
**Rule**: Word difficulty matches player age
**Settings**:
- Age 8-10: Common 3-5 letter words
- Age 11-13: Include 6-7 letter words
- Age 14+: All words including advanced

### BR-003: Educational Focus
**Rule**: Learning happens through play, not forced
**How**: Show definitions naturally after play

### BR-004: Quick Rounds
**Rule**: Games last 5-10 minutes maximum
**Why**: Maintain attention and allow multiple rounds

### BR-005: Positive Reinforcement
**Rule**: Celebrate effort, not just winning
**Examples**: "Great try!", "New word learned!", "Fastest time!"
```

## Step 3: Simple Data Structure (5 minutes)

```markdown
# Word Duel - Data Specifications

## Game State
```python
game = {
    'players': ['Player1', 'Player2'],
    'scores': [0, 0],
    'current_turn': 0,
    'round': 1,
    'mode': 'classic',
    'words_played': [],
    'time_remaining': 30
}
```

## Word Entry
```python
word = {
    'text': 'RAINBOW',
    'player': 'Marcus',
    'points': 7,  # Length-based
    'definition': 'An arc of colors in the sky',
    'difficulty': 'easy',
    'timestamp': '2025-09-25T10:30:00'
}
```

## Player Profile
```python
player = {
    'name': 'Marcus Jr',
    'age': 10,
    'total_words': 234,
    'vocabulary_size': 89,
    'favorite_mode': 'speed',
    'achievements': ['Word Wizard', 'Speed Demon']
}
```
```

## Step 4: AI Creates the Game (12 minutes)

Marcus tells AI:

> "Build this word game using Python with a simple text interface. Make it colorful and fun!"

The AI generates:

### `word_duel.py` - Game Engine
```python
import random
import time
from typing import List, Dict
from colorama import init, Fore, Style

init(autoreset=True)  # For colorful terminal output

class WordDuel:
    """FR-001: Two-player word battle game"""

    def __init__(self):
        self.players = []
        self.scores = [0, 0]
        self.current_player = 0
        self.words_played = set()
        self.round = 1

        # BR-002: Age-appropriate word lists
        self.word_lists = {
            'easy': ['CAT', 'DOG', 'TREE', 'BOOK', 'JUMP'],
            'medium': ['RAINBOW', 'GARDEN', 'CASTLE', 'FRIEND'],
            'hard': ['SYMPHONY', 'ARCHITECTURE', 'PHILOSOPHY']
        }

    def start_game(self):
        """Initialize a new game"""
        print(Fore.CYAN + """
        ╔══════════════════════╗
        ║     WORD DUEL! 🗡️    ║
        ╚══════════════════════╝
        """)

        self.players.append(input("Player 1 name: "))
        self.players.append(input("Player 2 name: "))
        self.difficulty = input("Difficulty (easy/medium/hard): ")

        self.play_rounds()

    def play_rounds(self):
        """FR-003: Fun challenges with variety"""
        while max(self.scores) < 100:  # First to 100 wins
            self.show_scores()
            challenge = self.get_challenge()

            print(f"\n{Fore.YELLOW}Round {self.round}: {challenge['type']}")
            print(f"{Fore.GREEN}{challenge['description']}")

            # BR-004: Quick rounds (30 seconds)
            start_time = time.time()
            word = input(f"\n{self.players[self.current_player]}'s turn: ").upper()
            time_taken = time.time() - start_time

            if time_taken <= 30 and self.validate_word(word, challenge):
                points = len(word)
                if time_taken < 10:
                    points *= 2  # Speed bonus!
                    print(Fore.MAGENTA + "⚡ SPEED BONUS! Double points!")

                self.scores[self.current_player] += points
                print(Fore.GREEN + f"✓ Great! +{points} points")

                # FR-002: Vocabulary learning
                self.show_definition(word)
                self.words_played.add(word)
            else:
                print(Fore.RED + "✗ Invalid or too slow!")

            # BR-005: Positive reinforcement
            self.give_encouragement()

            self.current_player = 1 - self.current_player
            self.round += 1

        self.end_game()

    def get_challenge(self) -> Dict:
        """FR-003: Different game modes"""
        challenges = [
            {'type': 'Classic', 'description': 'Any valid word!'},
            {'type': 'Animal Round', 'description': 'Name an animal'},
            {'type': 'Letter Challenge', 'description': f'Start with {random.choice("ABCDEFG")}'},
            {'type': 'Speed Round', 'description': 'Type fast for double points!'},
            {'type': 'Long Word', 'description': 'Minimum 6 letters'}
        ]
        return random.choice(challenges)

    def validate_word(self, word: str, challenge: Dict) -> bool:
        """BR-001: Fair play - real words only"""
        if word in self.words_played:
            print(Fore.YELLOW + "Already used!")
            return False

        # In real version, check dictionary API
        # For demo, check if it's in our lists
        all_words = sum(self.word_lists.values(), [])
        return word in all_words or len(word) >= 3

    def show_definition(self, word: str):
        """FR-002: Educational component"""
        # In real version, fetch from dictionary API
        definitions = {
            'RAINBOW': 'An arc of colors formed in the sky',
            'CASTLE': 'A large fortified building',
            'FRIEND': 'A person you like and trust'
        }

        if word in definitions:
            print(Fore.CYAN + f"📚 {word}: {definitions[word]}")

    def give_encouragement(self):
        """BR-005: Positive reinforcement"""
        messages = [
            "Great vocabulary! 🌟",
            "You're on fire! 🔥",
            "Excellent word choice! 👏",
            "Keep it up! 💪",
            "Word wizard! 🧙‍♂️"
        ]
        print(Fore.MAGENTA + random.choice(messages))

    def show_scores(self):
        """Display current scores"""
        print(f"\n{Fore.BLUE}{'='*30}")
        print(f"{self.players[0]}: {self.scores[0]} | {self.players[1]}: {self.scores[1]}")
        print(f"{'='*30}")

    def end_game(self):
        """FR-004: Progress tracking"""
        winner_idx = 0 if self.scores[0] > self.scores[1] else 1
        winner = self.players[winner_idx]

        print(Fore.YELLOW + f"""
        ╔════════════════════════╗
        ║  🏆 {winner} WINS! 🏆  ║
        ╚════════════════════════╝
        """)

        print(Fore.CYAN + "\n📊 Game Statistics:")
        print(f"Total rounds: {self.round}")
        print(f"Words learned: {len(self.words_played)}")
        print(f"Final scores: {self.players[0]} ({self.scores[0]}) vs {self.players[1]} ({self.scores[1]})")

        # Save progress for next time
        self.save_progress()

if __name__ == "__main__":
    game = WordDuel()
    game.start_game()
```

## Step 5: Playing Together (5 minutes)

```bash
# Run the game
python word_duel.py

╔══════════════════════╗
║     WORD DUEL! 🗡️    ║
╚══════════════════════╝

Player 1 name: Marcus
Player 2 name: Marcus Jr
Difficulty (easy/medium/hard): easy

Round 1: Animal Round
Name an animal

Marcus's turn: ELEPHANT
✓ Great! +8 points
📚 ELEPHANT: A large mammal with a trunk
Word wizard! 🧙‍♂️

Marcus Jr's turn: TIGER
⚡ SPEED BONUS! Double points!
✓ Great! +10 points
You're on fire! 🔥
```

## What Makes This Special

### Educational + Fun
- Learning happens naturally through play
- Definitions shown without feeling like homework
- Competition motivates vocabulary building

### Quick to Build
- 8 minutes planning the game
- 12 minutes for AI to code it
- 10 minutes tweaking and playing

### Grows with the Kids
- Start with easy words
- Add new challenges
- Track improvement over time

### Family Bonding
- Play together in person
- Customize for each child
- Add family in-jokes and themes

---

*This example shows how AGET enables parents to create educational tools tailored to their children's needs in minutes, not months.*