import tkinter as tk
import tkinter.messagebox

HUMAN = "X"
AI = "O"

def check_win(board, player):
    win_conditions = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],
        [0, 3, 6], [1, 4, 7], [2, 5, 8],
        [0, 4, 8], [2, 4, 6]
    ]

    for condition in win_conditions:
        if all(board[i] == player for i in condition):
            return True
    return False

def check_tie(board):
    return " " not in board

def minimax(board, depth, maximizing):
    if check_win(board, AI):
        return 1
    if check_win(board, HUMAN):
        return -1
    if check_tie(board):
        return 0

    if maximizing:
        max_eval = float("-inf")
        for i in range(9):
            if board[i] == " ":
                board[i] = AI
                eval = minimax(board, depth + 1, False)
                board[i] = " "
                max_eval = max(max_eval, eval)
        return max_eval
    else:
        min_eval = float("inf")
        for i in range(9):
            if board[i] == " ":
                board[i] = HUMAN
                eval = minimax(board, depth + 1, True)
                board[i] = " "
                min_eval = min(min_eval, eval)
        return min_eval

def best_move(board):
    best_eval = float("-inf")
    best_move = -1
    for i in range(9):
        if board[i] == " ":
            board[i] = AI
            eval = minimax(board, 0, False)
            board[i] = " "
            if eval > best_eval:
                best_eval = eval
                best_move = i
    return best_move

def human_move(button, index):
    if board[index] == " ":
        board[index] = HUMAN
        button.config(text=HUMAN, state=tk.DISABLED)
        if check_win(board, HUMAN):
            tkinter.messagebox.showinfo("Tic-Tac-Toe", "You win!")
            update_scoreboard("human")
            restart_game()
        elif check_tie(board):
            tkinter.messagebox.showinfo("Tic-Tac-Toe", "It's a tie!")
            update_scoreboard("tie")
            restart_game()
        else:
            ai_index = best_move(board)
            board[ai_index] = AI
            buttons[ai_index].config(text=AI, state=tk.DISABLED)
            if check_win(board, AI):
                tkinter.messagebox.showinfo("Tic-Tac-Toe", "AI wins!")
                update_scoreboard("ai")
                restart_game()
            elif check_tie(board):
                tkinter.messagebox.showinfo("Tic-Tac-Toe", "It's a tie!")
                update_scoreboard("tie")
                restart_game()

def restart_game():
    global board
    for i in range(9):
        board[i] = " "
        buttons[i].config(text=" ", state=tk.NORMAL)

def update_scoreboard(result):
    if result == "human":
        scoreboard["Human"] += 1
    elif result == "ai":
        scoreboard["AI"] += 1
    else:
        scoreboard["Tie"] += 1
    score_label.config(text=f"Human: {scoreboard['Human']} | AI: {scoreboard['AI']} | Tie: {scoreboard['Tie']}")

root = tk.Tk()
root.title("Tic-Tac-Toe")

board = [" " for _ in range(9)]
buttons = [None] * 9

for i in range(9):
    buttons[i] = tk.Button(root, text=" ", font=('normal', 20), width=6, height=2,
                           command=lambda i=i: human_move(buttons[i], i))
    buttons[i].grid(row=i // 3, column=i % 3)

restart_button = tk.Button(root, text="Restart", font=('normal', 12), width=15, height=1, command=restart_game)
restart_button.grid(row=3, columnspan=3)

scoreboard = {"Human": 0, "AI": 0, "Tie": 0}
score_label = tk.Label(root, text=f"Human: {scoreboard['Human']} | AI: {scoreboard['AI']} | Tie: {scoreboard['Tie']}")
score_label.grid(row=4, columnspan=3)

root.mainloop()
