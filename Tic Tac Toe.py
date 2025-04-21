import streamlit as st
import random
import pickle

class TicTacToe:
    def __init__(self):
        self.reset()

    def reset(self):
        self.board = [' '] * 9
        self.winner = None
        return self.get_state()

    def get_state(self):
        return ''.join(self.board)

    def available_moves(self):
        return [i for i, spot in enumerate(self.board) if spot == ' ']

    def make_move(self, square, letter):
        if self.board[square] == ' ':
            self.board[square] = letter
            if self.check_winner(square, letter):
                self.winner = letter
            return True
        return False

    def check_winner(self, square, letter):
        row_ind = square // 3
        col_ind = square % 3
        row = self.board[row_ind * 3:(row_ind + 1) * 3]
        col = [self.board[col_ind + i * 3] for i in range(3)]
        diag1 = [self.board[i] for i in [0, 4, 8]]
        diag2 = [self.board[i] for i in [2, 4, 6]]
        return any(all(s == letter for s in line) for line in [row, col, diag1, diag2])

class QLearningAgent:
    def __init__(self, alpha=0.1, gamma=0.9, epsilon=0.1):
        self.q_table = {}
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon

    def get_q(self, state, action):
        return self.q_table.get((state, action), 0.0)

    def choose_action(self, state, actions):
        q_vals = [self.get_q(state, a) for a in actions]
        max_q = max(q_vals)
        return random.choice([a for a, q in zip(actions, q_vals) if q == max_q])

    def load(self, filename='q_table.pkl'):
        with open(filename, 'rb') as f:
            self.q_table = pickle.load(f)

# Streamlit layout
st.set_page_config(page_title="Tic Tac Toe: Play Against AI", layout="centered")
st.title("🤖 Tic Tac Toe: Play Against Q-Learning Agent")

# Initialize session state if it's not already set
if 'env' not in st.session_state:
    st.session_state.env = TicTacToe()
    st.session_state.agent = QLearningAgent()
    st.session_state.agent.load('q_table.pkl')
    st.session_state.board = st.session_state.env.board
    st.session_state.state = st.session_state.env.get_state()
    st.session_state.game_over = False
    st.session_state.message = "Your move!"

# Function to display the game board
def print_board(board):
    return [board[i:i + 3] for i in range(0, 9, 3)]

# Handle the player's move (O) and agent's move (X)
def handle_move(i):
    # Player's move (O)
    if st.session_state.board[i] == ' ' and not st.session_state.game_over:
        st.session_state.env.make_move(i, 'O')
        st.session_state.board = st.session_state.env.board
        if st.session_state.env.winner == 'O':
            st.session_state.game_over = True
            st.session_state.message = "You win!"
        elif len(st.session_state.env.available_moves()) == 0:
            st.session_state.game_over = True
            st.session_state.message = "It's a draw!"
        else:
            # Agent's move (X)
            state = st.session_state.env.get_state()
            actions = st.session_state.env.available_moves()
            action = st.session_state.agent.choose_action(state, actions)
            st.session_state.env.make_move(action, 'X')
            st.session_state.board = st.session_state.env.board
            if st.session_state.env.winner == 'X':
                st.session_state.game_over = True
                st.session_state.message = "Agent wins!"
            elif len(st.session_state.env.available_moves()) == 0:
                st.session_state.game_over = True
                st.session_state.message = "It's a draw!"
            
            # Update the board after agent's move to show the current state
            st.session_state.state = st.session_state.env.get_state()

# Display the board with clickable cells (without disabling buttons)
cols = st.columns(3)
for i in range(9):
    with cols[i % 3]:
        button_text = st.session_state.board[i] if st.session_state.board[i] != ' ' else " "
        if st.button(button_text, key=f"btn_{i}"):
            handle_move(i)

# Display the game message (Win/Draw)
st.markdown(f"### {st.session_state.message}")

# Reset game button logic
if st.button("🔄 Reset Game"):
    st.session_state.env = TicTacToe()
    st.session_state.board = st.session_state.env.board
    st.session_state.state = st.session_state.env.get_state()
    st.session_state.game_over = False
    st.session_state.message = "Your move!"

# Divider
st.markdown("---")
st.caption("Built with Q-Learning | Streamlit")
