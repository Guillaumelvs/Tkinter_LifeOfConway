import numpy as np
import tkinter as tk

#Create the tkinter interface

my_window = tk.Tk()
my_window.title("Life of Conway")
my_window['bg'] = "#191E1A"




dim_canvas = tk.Canvas(my_window, width=200, height=80, bg='black') 
dim_canvas.grid()
dim_canvas.place(relx=1, rely=0.5, anchor='e')



dim_canvas.create_text(5, 17, anchor='w', text="Nombre de cases en hauteur :", fill="white")
dim_canvas.create_text(5, 43, anchor='w', text="Nombre de cases en largueur :", fill="white")
dim_canvas.create_text(5, 67, anchor='w', text="Taille des cases :", fill="white")


#Make the choice of height interactive :

dim_height = tk.StringVar()
dim_height.set("30")
height_entry = tk.Entry(dim_canvas, textvariable=dim_height, width=5, bg="#B2C3B9")
height_entry.grid()
height_entry.place(relx=1, rely=0.2, anchor='e')


#Make the choice of width interactive :

dim_widht = tk.StringVar()
dim_widht.set("30")
widht_entry = tk.Entry(dim_canvas, textvariable=dim_widht, width=5, bg="#B2C3B9")
widht_entry.grid()
widht_entry.place(relx=1, rely=0.5, anchor='e')


#Make the dimension of sqaures interactive :

dim_lenght = tk.StringVar()
dim_lenght.set("15")
lenght_entry = tk.Entry(dim_canvas, textvariable=dim_lenght, width=5, bg="#B2C3B9")
lenght_entry.grid()
lenght_entry.place(relx=1, rely=0.8, anchor='e')




shape_conway = [int(dim_height.get()), int(dim_widht.get())]
dim_square = int(dim_lenght.get())


#Creating the life of Conway algorithm :

def alive_cell(i, j, conway_life) :
    
    return ("green" if conway_life[i,j] < 2 else "black")



def alive_neighbor(i, j, conway_life, shape_conway) :
    
    alive_nei_number = 0
    
    if alive_cell(i, j, conway_life) == "green" :
        alive_nei_number = -1
        
    for row in range(max(i-1, 0), min(i+2, shape_conway[0])) :
        for col in range(max(j-1, 0), min(j+2, shape_conway[1])) :
            if alive_cell(row, col, conway_life) == "green" :
                alive_nei_number = alive_nei_number + 1  
                
    return alive_nei_number    
                
       
            
def new_state(conway_life, list_frames, shape_conway) :
    
    new_conway_life = np.zeros(shape_conway)
    
    for row in range(shape_conway[0]) :
        for col in range(shape_conway[1]) :
            nb_alive_neigh = alive_neighbor(row, col, conway_life, shape_conway)
            cell_state = alive_cell(row, col, conway_life)
            old_value = conway_life[row, col]
            new_value = (cell_state == "black" and nb_alive_neigh != 3)*old_value + (cell_state == "green")*((nb_alive_neigh > 3)*2 + (nb_alive_neigh < 2)*3 + (nb_alive_neigh == 2 or nb_alive_neigh == 3))
            new_conway_life[row, col] = new_value
            color = alive_cell(row, col, new_conway_life)
            list_frames[row*shape_conway[1] + col].configure(bg=color)
            
    return(new_conway_life)     



def conway_in_action(shape_conway, dim_square, conway_life, list_frames) :
    
    stop_conway = False
    number_of_game = 1
    
    while stop_conway == False :
        conway_life = new_state(conway_life, list_frames, shape_conway)
        msg_to_display = "State number " + str(number_of_game)
        user_wish = tk.messagebox.askquestion(msg_to_display, "A new state ?")
        number_of_game += 1
        
        if user_wish == "no" : 
            stop_conway = True
    
    

def play():
    
    shape_conway = [int(dim_height.get()), int(dim_widht.get())]
    dim_square = int(dim_lenght.get())
    main_canvas = tk.Canvas(my_window, width=shape_conway[1]*dim_square, height=shape_conway[0]*dim_square, bg='black') 
    main_canvas.grid()
    main_canvas.place(relx=0.5,rely=0.5, anchor='center')
    conway_life = np.random.randint(4, size=(shape_conway[0], shape_conway[1]))
    list_frames = []
    
    for row in range(shape_conway[0]) :
        for col in range(shape_conway[1]) :
            color = alive_cell(row, col, conway_life)
            actual_frames = tk.Frame(main_canvas, width=dim_square, height=dim_square, bg=color)
            actual_frames.grid(row=row, column=col)
            list_frames.append(actual_frames)
            
    conway_in_action(shape_conway, dim_square, conway_life, list_frames)
    
    for c in list_frames :
        c.grid_forget()
        
    main_canvas.place_forget()
    main_canvas.grid_forget()


#Customize our window

menubar = tk.Menu(my_window)



my_menu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="Conway Life action", menu=my_menu)
my_menu.add_command(label="New Conway", command=play)
my_menu.add_command(label="Close Conway life", command=my_window.destroy)


   
my_window.config(menu=menubar)
my_window.attributes('-fullscreen', 1)




my_window.mainloop()