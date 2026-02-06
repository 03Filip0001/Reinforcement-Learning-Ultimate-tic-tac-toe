from src.cell import Cell, CellValues
from src.ttt import TTT

ttt = TTT()

print(ttt)

currentPlayer = CellValues.X
msg_str = "Unesi koordinate igraca {}: "
winner = CellValues.EMPTY
while winner == CellValues.EMPTY:
	msg = None
	if currentPlayer == CellValues.X:
		msg = msg_str.format(CellValues.X)
	else:
		msg = msg_str.format(CellValues.O)

	user_input = input(msg)
	i, j = map(int, user_input.split())

	ttt.setCell((i,j), currentPlayer)
	print(ttt)

	if currentPlayer == CellValues.X:
		currentPlayer = CellValues.O
	else:
		currentPlayer = CellValues.X

	winner = ttt.checkWinner()

print(ttt.printWinner())