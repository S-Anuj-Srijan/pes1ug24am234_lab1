# Skyscraper Stack Repair Lab

This project is a precision timing and balance tower stacking game using **Pygame**. It introduces students to 1D bounding-box intersection math, dynamic geometry slicing, vertical camera offset scrolling, and escalating difficulty curves within an object-oriented codebase.
---

## What's Provided

A working Skyscraper Stack game with:

- A foundation block positioned at the base of the arena
- Horizontally oscillating active blocks that bounce between screen boundaries at escalating speeds
- Precision placement triggered via `Space` key or left mouse click
- Automatic dynamic width trimming based on overlap alignment against the previous tier
- Downward camera scrolling when the stack exceeds the vertical threshold
- A Game Over collapse screen displaying total tower height with instant restart functionality

The original lab included **one deliberate bug**, which is now fixed. The **three optional features** below remain unimplemented.

### **Use an LLM (e.g. ChatGPT or Claude) as your debugging and pair-programming partner for this lab.**
---

## Getting Started

### Setup

1. Make sure you have Python 3.10+ installed.
2. Install dependencies:

```bash
pip install pygame
```

3. Run the game:

```bash
python main.py
```

**Controls:** Press Space or Left-Click to drop the active block. Press Space, R, or Left-Click to restart after Game Over. Close the window to quit.

### How to Play

1. Run `python main.py` from the project folder.
2. Watch the active block move horizontally above the tower.
3. Press **Space** or **left-click** when it lines up with the top block.
4. A successful placement adds one point to the displayed height. Overhangs are trimmed, with an existing minimum block width of 10 pixels, so precise timing helps keep the tower wide.
5. Blocks move faster as the tower grows. The stack shifts downward when its top reaches the upper part of the screen.
6. A complete miss, including edges that only touch with zero overlap, ends the game. Press **Space**, **R**, or **left-click** to try again.

## Completed Fixes and Verification

### Inverted overlap condition

Inspected `main.py`, `game/game_engine.py`, and `game/block.py` and traced the placement logic to `GameEngine.drop_block()` in `game/game_engine.py`.

The code calculates the horizontal intersection of the active block and the tower's top block:

```python
left = max(act.x, top_block.x)
right = min(act.x + act.width, top_block.x + top_block.width)
overlap = right - left
```

The original success condition was backwards:

```python
is_successful_drop = overlap <= 0
```

This treated misses as successful placements and ended the game when blocks actually overlapped. It was changed to:

```python
is_successful_drop = overlap > 0
```

Positive overlap now places a block and increases the score; zero or negative overlap triggers game over.

### Space key restart

The game-over screen advertised Space or R to restart, but the keyboard handler only accepted R. Updated `GameEngine.handle_event()` to accept both keys:

```python
event.key in (pygame.K_SPACE, pygame.K_r)
```

The existing left-click restart remains available. Both code fixes were made in `game/game_engine.py`; `main.py` and `game/block.py` were unchanged.

### Verification Results

Ran a headless Python check against the actual game engine using Pygame's dummy video driver. All six checks passed:

- Fully aligned drop: increases the score and continues play.
- Partial overlap of 30 pixels: creates a 30-pixel block and continues play.
- Edges touching with zero overlap: triggers game over without increasing the score.
- Complete miss: triggers game over.
- Space after game over: resets the score and resumes play.
- R after game over: resets the score and resumes play.

These were direct logic checks; no gameplay video was recorded and no permanent test file was added.


## Tasks to Complete

Each task must be completed using an iterative process involving LLM suggestions and your critical code review.

### Task 1: Fix the inverted overlap placement bug (completed)

Originally, landing a block on the tower caused game over, while dropping it into empty air allowed play to continue. The drop condition is now corrected, as documented above.

### Task 2: Implement "Perfect Placement" bonus & width restoration

Currently, any placement slightly off-center permanently shaves down the block's width. Introduce a precision reward: if a dropped block aligns almost flush with the top of the tower, snap it into place without trimming, show a "PERFECT!" prompt with bonus score, and slightly restore lost width if multiple perfect drops are landed in a row
 
### Task 3: Implement falling off-cut debris animation

Sliced off-cut sections of blocks disappear instantly from the arena without visual feedback. Add animated debris that creates a falling, rotating remnant of the trimmed overhang whenever a block is cut, giving weight and impact to imperfect placements.

### Task 4: Implement Atmospheric Background Shifting

The sky remains a static color throughout the entire climb regardless of tower height. Transition the background through dynamic atmospheric color gradients as the skyscraper stacks higher

---

## Expected Behavior

- Dropping a block while aligned over the stack trims the edges, places the block, and increases the tower height score.
- Dropping a block outside the stack triggers the TOWER COLLAPSED! game over screen.
- As the stack grows taller, it shifts downward in steps so the top of the tower remains visible.
- Pressing Space, R, or Left-Click on the collapse screen resets the tower and restores base dimensions.

## Folder Structure

```
word_scramble/
├── game/
│   ├── game_engine.py
│   └── text_box.py
├── main.py
└── README.md
```

## Submission Checklist

Submission is only the following three things:

- [] A 10-second video of gameplay **before** your changes, showing the bug/broken behavior
- [] A 10-second video of gameplay **after** your changes, showing the bug fixed and the new features working
- [] The Chat/LLM used page link, with the complete chat history
