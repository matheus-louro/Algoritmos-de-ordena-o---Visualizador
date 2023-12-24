import random
import matplotlib.pyplot as plt
import time
import argparse
from matplotlib.animation import FuncAnimation

def parse_args():
    '''
    Função para obter os argumentos de linha de comando que informam o número de elementos na lista e o algoritmo de ordenação.
    Os algoritmos de ordenação são escolhidos a partir das seguintes letras:
    s - Selection Sort
    i - Insertion Sort
    b - Bubble Sort
    m - Merge Sort
    q - Quick Sort
    '''
    parser = argparse.ArgumentParser(description="Sorting Algorithm Visualizer")
    parser.add_argument("num_elements", type=int, help="Number of elements in the array")
    parser.add_argument("sorting_algorithm", choices=["s", "i", "b", "m", "q"], help="Sorting algorithm")

    return parser.parse_args()

def main():
    args = parse_args()
    n = args.num_elements
    method = args.sorting_algorithm

    # Cria a lista com n elementos e embaralha a lista
    lst = [x + 1 for x in range(n)]
    random.seed(time.time())
    random.shuffle(lst)

    # Chama a função escolhida para criar o generator que será passado para função FuncAnimation
    match method:
        case 's':
            title = 'Selection Sort'
            generator = selection_sort(lst)
        case 'i':
            title = 'Insertion Sort'
            generator = insertion_sort(lst)
        case 'b':
            title = 'Bubble sort'
            generator = bubble_sort(lst)
        case 'm':
            title = "Merge sort"
            generator = merge_sort(lst, 0, n-1)
        case 'q':
            title = 'Quick sort'
            generator = quick_sort(lst, 0, n-1)

    # Inicializa uma figure e axis
    fig, ax = plt.subplots()
    ax.set_title(title)

    # Inicializa um gráfico de barras. A função matplotlib.pyplot.bar() retorna uma lista de objetos, onde cada objeto é uma
    # barra (retângulo) no gráfico.
    bar_rects = ax.bar(range(len(lst)), lst, align="edge", color='green')
    
    # Define os limites dos eixos. A altura do eixo y foi definida desse modo para que as barras não sobreponham o espaço 
    # reservado para o texto no gráfico
    ax.set_xlim(0, n)
    ax.set_ylim(0, 1.07 * n)
    
    # Coloca os textos no canto superior-esquerdo no gráfico
    # Steps é o número de operações que o algoritmo de ordenação realiza (cada "yield" é tratado como 1 operação)
    # time_text é o tempo de execução do algoritmo
    steps = ax.text(0.02, 0.95, "", transform=ax.transAxes)
    time_text = ax.text(0.2, 0.95, "", transform=ax.transAxes)

    # Começa a cronometrar o tempo de execução do algoritmo
    start_time = time.time()

    # Define a função update_fig() que será usada pela matplotlib.animation.FuncAnimation para atualizar a animação do gráfico.
    iteration = [0]
    def update_fig(lst, rects, iteration):
        for rect, val in zip(rects, lst):
            rect.set_height(val)
        iteration[0] += 1
        steps.set_text("steps: {}".format(iteration[0]))
        time_text.set_text("runtime: {:.2f} s".format(time.time() - start_time))

    anim = FuncAnimation(fig, func=update_fig,
        fargs=(bar_rects, iteration), frames=generator, interval=1,
        repeat=False, cache_frame_data=False)
    
    plt.show()


# Implementação dos algoritmos de ordenação utilizando o "yield" para criar um generator que atualizará a lista no gráfico
def selection_sort(lst):
    for i in range(len(lst) - 1):
        min_index = i
        for j in range(i + 1, len(lst)):
            if lst[j] < lst[min_index]:
                min_index = j
        lst[i], lst[min_index] = lst[min_index], lst[i]
        yield lst

def bubble_sort(lst):
    for i in range(len(lst) - 1):
        for j in range(i + 1,len(lst)):
            if lst[j] < lst[i]:
                lst[j], lst[i] = lst[i], lst[j]
            yield lst

def insertion_sort(lst):
    for i in range(1, len(lst)):
        temp = lst[i]
        j = i - 1
        while j >= 0 and temp < lst[j]:
            lst[j + 1] = lst[j]
            j -= 1
        lst[j + 1] = temp
        yield lst


def merge_sort(lst, start, end):
    if end <= start:
        return

    mid = (end + start)//2
    yield from merge_sort(lst, start, mid)
    yield from merge_sort(lst, mid + 1, end)
    yield from merge(lst, start, mid, end)
    yield lst

def merge(lst, start, mid, end):
    ''''Função auxiliar do merge sort'''
    merged = []
    leftIdx = start
    rightIdx = mid + 1
    changed = False

    while leftIdx <= mid and rightIdx <= end:
        if lst[leftIdx] < lst[rightIdx]:
            merged.append(lst[leftIdx])
            leftIdx += 1
        else:
            merged.append(lst[rightIdx])
            rightIdx += 1
        changed = True

    while leftIdx <= mid:
        merged.append(lst[leftIdx])
        leftIdx += 1
        changed = True

    while rightIdx <= end:
        merged.append(lst[rightIdx])
        rightIdx += 1
        changed = True

    if changed:
        lst[start:end + 1] = merged
        yield lst

def quick_sort(lst, start, end):
    if start >= end:
        return
    
    pivotIdx = (start + end) // 2
    lst[pivotIdx], lst[end] = lst[end], lst[pivotIdx]
    pivot = lst[end]

    pivotIdx = start

    for i in range(start, end):
        if lst[i] < pivot:
            lst[i], lst[pivotIdx] = lst[pivotIdx], lst[i]
            pivotIdx += 1
            yield lst

    lst[end], lst[pivotIdx] = lst[pivotIdx], lst[end]
    yield lst

    yield from quick_sort(lst, start, pivotIdx - 1)
    yield from quick_sort(lst, pivotIdx + 1, end)


if __name__ == '__main__':
    main()