import streamlit as st
import random
import matplotlib.pyplot as plt
import time
import numpy as np

# Sorting Algorithms

def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
                yield arr

def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
        yield arr

def selection_sort(arr):
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i+1, n):
            if arr[min_idx] > arr[j]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
        yield arr

def merge_sort(arr):
    if len(arr) > 1:
        mid = len(arr) // 2
        L = arr[:mid]
        R = arr[mid:]

        yield from merge_sort(L)
        yield from merge_sort(R)

        i = j = k = 0

        while i < len(L) and j < len(R):
            if L[i] < R[j]:
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            k += 1
            yield arr

        while i < len(L):
            arr[k] = L[i]
            i += 1
            k += 1
            yield arr

        while j < len(R):
            arr[k] = R[j]
            j += 1
            k += 1
            yield arr

def heapify(arr, n, i):
    largest = i
    l = 2 * i + 1
    r = 2 * i + 2

    if l < n and arr[l] > arr[largest]:
        largest = l

    if r < n and arr[r] > arr[largest]:
        largest = r

    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        yield arr
        yield from heapify(arr, n, largest)

def heap_sort(arr):
    n = len(arr)

    for i in range(n // 2 - 1, -1, -1):
        yield from heapify(arr, n, i)

    for i in range(n - 1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]
        yield arr
        yield from heapify(arr, i, 0)

def partition(arr, low, high):
    pivot = arr[high]
    i = low - 1
    for j in range(low, high):
        if arr[j] < pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
            yield arr
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    yield arr
    return i + 1

def quick_sort(arr, low, high):
    if low < high:
        pi = yield from partition(arr, low, high)

        yield from quick_sort(arr, low, pi - 1)
        yield from quick_sort(arr, pi + 1, high)

def quick_sort_wrapper(arr):
    yield from quick_sort(arr, 0, len(arr) - 1)

# Visualization Function

def visualize_algorithm(arr, algorithm):
    fig, ax = plt.subplots()
    ax.bar(range(len(arr)), arr, align="edge")
    ax.set_xlim(0, len(arr))
    ax.set_ylim(0, int(1.1 * max(arr)))
    text = ax.text(0.02, 0.95, "", transform=ax.transAxes)

    iterations = [0]

    st.write("Visualizing Algorithm...")
    image = st.image(fig2rgb_array(fig), use_column_width=True)

    for state in algorithm(arr):
        ax.clear()
        ax.bar(range(len(state)), state, align="edge")
        ax.set_xlim(0, len(state))
        ax.set_ylim(0, int(1.1 * max(state)))
        iterations[0] += 1
        text.set_text(f"Iterations: {iterations[0]}")
        image.image(fig2rgb_array(fig), use_column_width=True)
        time.sleep(0.1)  # Adjust the speed of animation here

def start_visualization(array_size, selected_algorithm):
    arr = random.sample(range(1, array_size + 1), array_size)
    if selected_algorithm == "Bubble Sort":
        visualize_algorithm(arr, bubble_sort)
    elif selected_algorithm == "Insertion Sort":
        visualize_algorithm(arr, insertion_sort)
    elif selected_algorithm == "Selection Sort":
        visualize_algorithm(arr, selection_sort)
    elif selected_algorithm == "Merge Sort":
        visualize_algorithm(arr, merge_sort)
    elif selected_algorithm == "Heap Sort":
        visualize_algorithm(arr, heap_sort)
    elif selected_algorithm == "Quick Sort":
        visualize_algorithm(arr, quick_sort_wrapper)

def fig2rgb_array(fig):
    fig.canvas.draw()
    buf = fig.canvas.tostring_rgb()
    ncols, nrows = fig.canvas.get_width_height()
    return np.frombuffer(buf, dtype=np.uint8).reshape(nrows, ncols, 3)

st.title("Algorithm Visualization")

# Option: Enter size and select algorithm
array_size = st.number_input("Array Size:", min_value=1, value=50)
selected_algorithm = st.selectbox("Select Algorithm:", ["Bubble Sort", "Insertion Sort", "Selection Sort", "Merge Sort", "Heap Sort", "Quick Sort"])

if st.button("Start Visualization"):
    start_visualization(array_size, selected_algorithm)
