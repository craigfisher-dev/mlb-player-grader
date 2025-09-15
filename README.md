# mlb-player-grader

Player evaluation tool that grades MLB hitters based on current season performance. Input any player name and get their batting average, OBP, OPS, and an overall grade (S+ to F) using a data-driven grading system.

**Live App:** https://mlb-player-grader.onrender.com/

![Ohtani S+ grade example](https://github.com/user-attachments/assets/d612452d-5695-45b8-bfd8-7aa92a64534d)
<sub>*Example: Ohtani earning S+ grade (137/145 points) with elite stats across all categories*</sub>

## Features:
- Player search with real-time MLB data
- Grading using BA (Max 30pts), OBP (Max 30pts), OPS (Max 80pts) + bonus (Max 5pts) = 145 total
- Player photos (headshot + action shots)
- Bonus points for well-rounded hitters
- Handles all current MLB players

**Built with:** Python, Streamlit, MLB StatsAPI, Render

## Grading System
- **S+:** 120+ points (Elite hitter)
- **S:** 110-119 points (Excellent)
- **A:** 95-109 points (Above average)
- **B:** 80-94 points (Good)
- **C:** 60-79 points (League average)
- **D:** 45-59 points (Poor)
- **F:** <45 points (Very poor)
