from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Часть алгоритма

def count_trees(n, ar):
    d = np.asarray([[sum([ar[k][i] for k in range(n)]) if i==j else 0 for j in range(n) ] for i in range(n)])
    b = d - ar
    s = 0
    for i in range(n):
        s += round(np.linalg.det(minor(b, i, i)))
    return s

def minor(arr,i,j):
    # ith row, jth column removed
    return arr[np.array(list(range(i))+list(range(i+1,arr.shape[0])))[:,np.newaxis],
               np.array(list(range(j))+list(range(j+1,arr.shape[1])))]

def parse_graph(graph_edges_list):
    nodes = []
    income = {}
    outcome = {}

    for i,j in graph_edges_list:
        outcome [i]  = outcome.get(i, []) + [j]
        income [j] = income.get(j, []) + [i]
        if not i in nodes :
            nodes += [i]
        if not j in nodes :
            nodes += [j]

    return (nodes, income, outcome)

def is_tree(graph_edges_list, root):
    nodes, income, outcome = parse_graph(graph_edges_list)
    if sum( [ len(j) for j in outcome.values() ] )!=len(nodes) - 1 :
        return False

    def visit_outcome(r, visited):
        if r in visited:
            return False
        visited += [r]
        if r in outcome:
            for j in outcome[r]:
                if not visit_outcome(j, visited):
                    return False
        return True

    visited = []
    if not visit_outcome(root, visited):
        return False
    return sorted(visited)==sorted(nodes)

def clusters_join(clusters, a, b ):
    clustter_a = [ i for i in clusters if a in i ][0]
    clustter_b = [ i for i in clusters if b in i ][0]
    if clustter_a != clustter_b :
        return [ i for i in clusters if (a not in i) and (b not in i) ] + [ clustter_a + clustter_b ]
    else:
        return [i for i in clusters]

def clusters_check(clusters, a, b ):
    for i in clusters :
        if a in i :
            return not (b in i)
    return False

def seek_subtree(graph_edges_list):
    nodes, income, outcome = parse_graph(graph_edges_list)
    result = []

    possible_roots = [ i for i in nodes if not i in income ]
    if len(possible_roots) > 1 :
        return [] # no solutions.
    if len(possible_roots) ==0 :
        possible_roots = [i for i in nodes]

    for root in possible_roots:
        non_root_nodex = [ i for i in nodes if i!=root ]
        non_root_nodex = sorted( non_root_nodex, key = lambda i : len(income[i]) )

        clusters = nodes.copy()

        def visit_left_node( left_nodes, clusters, edges ):
            if len(left_nodes) == 0 :
                if is_tree(edges, root):
                    return [ edges ]
            else:
                b = left_nodes[0]
                result = []
                for a in income[b]:
                    if clusters_check(clusters, a, b):
                        result += visit_left_node( left_nodes[1:], clusters_join(clusters, a,b),  edges+[a+b],  )
                return result

        result  = visit_left_node( non_root_nodex, nodes, []  )

    return result
                
# Часть фронтэнда

def get_mat(event, n, text_var):
    matrix = []
    for i in range(n):
        matrix.append([])
        for j in range(n):
            try:    
                matrix[i].append(int(text_var[i][j].get()))
            except ValueError:
                messagebox.showwarning("Предупреждение", "Ввёденные данные некоректны")
                return
            except IndexError:
                messagebox.showwarning("Предупреждение", "Ввёденные данные некоректны")
                return
    ar = np.asarray(matrix)
    print_DiGraph(n, ar)

def print_DiGraph(n, ar):
    graph = nx.from_numpy_array(ar, create_using=nx.DiGraph)
    graph = nx.relabel_nodes(graph, {k:chr(k+65) for k in graph.nodes})
    ct = int(count_trees(n, ar))
    labl3 = Label(root, text="Количество прадеревьев: "+str(ct),bg="gray")
    labl3.pack()
    plt.figure("Граф G")
    nx.draw(graph, with_labels=True)
    if ct != 0:
        i=1
        for pratree in seek_subtree([''.join(i) for i in graph.edges]):
            gr = nx.DiGraph()
            gr.add_edges_from([tuple(list(i)) for i in pratree])
            plt.figure("Прадерево №"+str(i))
            nx.draw(gr, with_labels=True)
            i += 1
    else:
        messagebox.showwarning("Предупреждение", "Нет прадеревьев") 
    plt.show()
 
def show_fr2(event, n):
    ent.pack_forget()
    labl.pack_forget()
    button.pack_forget()
    labl2 = Label(root, text="Введите матрицу смежности", bg="gray", font=("Helvetica", fontsize))
    labl2.pack()
    table = Frame(root)
    table.configure(bg='gray')
    text_var = []
    entries = []
    for i in range(n):
        # append an empty list to your two arrays
        # so you can append to those later
        text_var.append([])
        entries.append([])
        for j in range(n):
            # append your StringVar and Entry
            text_var[i].append(StringVar())
            entries[i].append(Entry(table, textvariable=text_var[i][j],width=1))
            entries[i][j].grid(column=j, row=i, padx=5, pady=5)
    table.pack()
    button2 = ttk.Button(root,text="SUBMIT", style='New.TButton')
    button2.pack()
    button2.bind('<Button-1>', lambda e, f = n, ar=text_var: get_mat(e, f, ar))
    
root = Tk()
# Base size
normal_width = 1920
normal_height = 1080
# Get screen size
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.configure(bg='gray')
root.geometry("%dx%d" % (screen_width/1.5, screen_height/1.5))
root.state("zoomed")
root.title("Task 8")
root.iconbitmap("icon.ico")
root.minsize(width=222, height=222)
# Get percentage of screen size from Base size
percentage_width = screen_width / (normal_width / 100)
percentage_height = screen_height / (normal_height / 100)

# Make a scaling factor, this is bases on average percentage from
# width and height.
scale_factor = ((percentage_width + percentage_height) / 2) / 100

# Set the fontsize based on scale_factor,
# if the fontsize is less than minimum_size
# it is set to the minimum size
fontsize = int(14 * scale_factor)
minimum_size = 8
if fontsize < minimum_size:
    fontsize = minimum_size

# Create a style and configure for ttk.Button widget
default_style = ttk.Style()
default_style.configure('New.TButton', font=("Helvetica", fontsize))

labl = Label(root, text="Введите количество вершин", bg="gray", font=("Helvetica", fontsize))
labl.pack()
ent = Entry(root, width=5, justify="right")
ent.pack()
button = ttk.Button(root, text="SUBMIT", style='New.TButton')
try:
    button.bind('<Button-1>', lambda e: show_fr2(e, int(ent.get())))
except ValueError:
    messagebox.showwarning("Предупреждение", "Ввёденные данные некоректны")
button.pack()

root.mainloop()
 