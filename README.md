# Connect Four AI 

This project is the final project for the **Artificial Intelligence course**, implementing the **Connect Four** game with two AI algorithms:  
- **Minimax with Alpha-Beta Pruning**  
- **Monte Carlo Tree Search (MCTS)**  

The game features a graphical interface using **Pygame**, an AI selection menu, smooth animations, and a scoring system to track performance.  

## 🛠 Features  
✅ Play against two different AI strategies  
✅ Animated piece drops for a smooth experience  
✅ Interactive main menu for AI selection  
✅ Real-time score tracking for both player and AI  
✅ Optimized decision-making using Minimax and MCTS  

## 📦 Installation  

### 1️⃣ Clone the Repository  
```sh
git clone https://github.com/your-username/connect-four-ai.git
cd connect-four-ai
```

### 2️⃣ Install Required Libraries  
Ensure you have Python installed, then install the following dependencies:  
```sh
pip install numpy pygame
```

### 3️⃣ Run the Game  
```sh
python connect-four-minimax.py
```

## 🎮 How to Play  
- Select an AI algorithm from the menu.  
- Click on a column to drop your piece.  
- The AI will make its move automatically.  
- The game ends when a player gets **four in a row** (vertically, horizontally, or diagonally).  

## 🤖 AI Algorithms  

### Minimax with Alpha-Beta Pruning  
- Explores possible moves up to a certain depth.  
- Evaluates board positions using a heuristic function.  
- Uses **pruning** to eliminate unnecessary calculations, improving efficiency.  

### Monte Carlo Tree Search (MCTS)  
- Simulates multiple random games to evaluate move strength.  
- Selects moves based on **exploration & exploitation** trade-offs.  
- Performs better in **longer-term strategy planning**.  

## 🏆 Which AI is Better?  
- **Minimax** is efficient for shorter decision depths and tactical play.  
- **MCTS** is better for **strategic** and **long-term planning**.  
- Try both and see which one challenges you more!  

## 🎥 GIFs
![Minimax](https://github.com/Mahdi-Rahbar/Connect-Four---AI-Project/blob/main/Gifs/Minimax.gif?raw=true) 
![MCTS](https://github.com/Mahdi-Rahbar/Connect-Four---AI-Project/blob/main/Gifs/MCTS.gif?raw=true)
