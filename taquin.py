from tkinter import *
from random import randrange
from classes import *
from time import sleep

res = None

def clic(event):
    global i_empty, j_empty, bravo,done
    if bravo:
        return
    i=event.y//100
    j=event.x//100
    nro=board[i][j]
    rect, txt=items[nro]
    if j+1 ==j_empty and i==i_empty:
        cnv.move(rect, 100, 0)
        cnv.move(txt, 100, 0)
    elif j-1 ==j_empty and i==i_empty:
        cnv.move(rect, -100, 0)
        cnv.move(txt, -100, 0)
    elif i+1 ==i_empty and j==j_empty:
        cnv.move(rect, 0, 100)
        cnv.move(txt, 0, 100)
    elif i-1 ==i_empty and j==j_empty:
        cnv.move(rect, 0, -100)
        cnv.move(txt, 0, -100)
    else:
        return
    board[i][j],board[i_empty][j_empty]=(
        board[i_empty][j_empty],board[i][j])
    i_empty=i
    j_empty=j
    if board==win or done == steps:
        lbl.configure(text="Bravo !")
        bravo=True
    if res != None and not bravo:
        lbl.config(text = nextMov())
        done = done+1

def voisins(n, i, j):
    return [(a,b) for (a, b) in
            [(i, j+1),(i, j-1), (i-1, j), (i+1,j)]
            if a in range(n) and b in range(n)]

def echange(board, empty):
    i, j=empty
    V=voisins(3, i, j)
    ii, jj=V[randrange(len(V))]
    board[ii][jj], board[i][j]=board[i][j],board[ii][jj]
    return ii, jj

def normal(board, empty):
    i_empty, j_empty = empty
    for i in range(i_empty, 3):
        (board[i][j_empty], board[i_empty][j_empty])= (
            board[i_empty][j_empty], board[i][j_empty])
        i_empty=i
    for j in range(j_empty, 3):
        board[i_empty][j], board[i_empty][j_empty]= (
            board[i_empty][j_empty],board[i_empty][j])
        j_empty=j

def melanger(N):
    board=[[3*lin+1+col for col in range(3)]
        for lin in range(3)]

    empty=(2,2)

    for i in range(N):
        empty=echange(board, empty)
    return board

def init(N=100):
    global i_empty, j_empty, items, board, bravo,res
    cnv.delete("all")
    items=[None]

    board=melanger(N)
    for i in range(3):
        for j in range(3):
            if board[i][j]==9:
                i_empty, j_empty=i, j

    empty=i_empty, j_empty
    normal(board, empty)
    i_empty, j_empty=2,2
    print(board)
    items=[None for i in range(10)]

    for i in range(3):
        for j in range(3):
            x, y=100*j, 100*i
            A, B, C=(x, y), (x+100, y+100), (x+50, y+50)
            rect = cnv.create_rectangle(A, B, fill="#bb57b0")
            nro=board[i][j]
            txt = cnv.create_text(C, text=board[i][j], fill="black",
                            font=FONT)
            items[nro]=(rect, txt)
    rect, txt=items[9]        
    cnv.delete(rect)
    cnv.delete(txt)
    lbl.configure(text="")
    bravo=False    
        

#items=[None for i in range(10)]
"""board=[[6, 7, 4 ],
       [5, 8, 2],
       [1, 3, 9]]
"""

def resolutionA():
    global board,res,steps,done
    done = 0
    steps = 0
    puzzle = Taquin(board)
    movements = []
    print(puzzle)
    move_seq = iter(Search(puzzle).bfs())
    for from_state, to_state in pairs(move_seq):
        steps= steps+1
        print()
        movements.append(Taquin.direction(from_state, to_state))
        print(Taquin.direction(from_state, to_state))
        print(to_state)
    print("solved in ",steps," steps")
    print(movements)
    res = movements
    steps = len(movements)
    lbl.config(text = res[0])


steps = 0
done = 0
def nextMov():
    global res,steps,done
    global res,master,board

    return res[min(done+1,steps-1)]









FONT=('Ubuntu', 27, 'bold')
master=Tk()
cnv=Canvas(master, width=300, height=300, bg='gray70')
cnv.pack(side='left')
master.title('Taquin')
menuBar = Menu(master)
menuQuitter = Menu(menuBar)
menuMelanger = Menu(menuBar)
menuResolution = Menu(menuBar)
menuBar.add_cascade(label = " Résolution ", menu=menuResolution)
menuResolution.add_command(label=" Recherche en largeur ")
menuResolution.add_command(label=" Recherche par A* ",command = resolutionA)

master.config(menu=menuBar)


btn=Button(text="Mélanger", command=init)
btn.pack()
btn=Button(text="résoudre", command = resolutionA)

btn.pack()

btn=Button(text="simuler", command=nextMov)
btn.pack()

btn=Button(text="Quitter", command=master.destroy)
btn.pack()

lbl=Label(text="      ", font=('Ubuntu', 25, 'bold'), 
          justify=CENTER, width=7)
lbl.pack(side="left")



cnv.bind("<Button-1>", clic)
init()

win=[[1, 2, 3],
     [4, 5, 6],
     [7, 8, 9]]

master.mainloop()










