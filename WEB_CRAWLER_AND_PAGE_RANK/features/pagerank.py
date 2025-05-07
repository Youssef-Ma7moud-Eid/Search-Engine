import numpy as np
import os
import json

class PageRank:
    def __init__(self):
        self.damping_factor = 0.85
        self.maxerr = 0.0001
        self.datasetsPath = 'C:/Users/LAPTOP/OneDrive/Desktop/page_rank/datasets'
        self.neighbours = []
        self.visited_urls = []

    def load_neighbours_urls(self):
        self.neighbours = []

        with open(f'{self.datasetsPath}\\neighbours.txt', 'r') as f:
            lines = f.readlines()

        for line in lines:

            elements = line.strip().split(':')

            values = [int(elem) for elem in elements[1].split(',') if elem.strip()]

            self.neighbours.append(values)

    def load_visited_urls(self):
        try:
            with open(f'{self.datasetsPath}\\test.txt', 'r') as f:
                lines = f.readlines()
                return [line.strip() for line in lines]
        except FileNotFoundError:
            print(f"File '{self.datasetsPath}' not found.")

    def create_adjacency_matrix(self):
        self.visited_urls = self.load_visited_urls()
        self.load_neighbours_urls()
        adjacency_matrix = np.zeros((len(self.visited_urls), len(self.visited_urls)))  # Initialize a matrix of zeros
        index = 0
        for neighbour in self.neighbours:
            for j in neighbour:
                adjacency_matrix[index][j] = 1
            index += 1

        return  adjacency_matrix

    def page_rank(self):
        adjacency_matrix = self.create_adjacency_matrix()

        arr = np.array(adjacency_matrix, dtype=float)
        s = []
        for i in range(0, len(adjacency_matrix)):
            s.append(np.sum(adjacency_matrix[i, :]))
        print('sum of rows: ', s)

        M = arr
        for j in range(0, len(adjacency_matrix)):
            if s[j] != 0:   # invalid value encountered in divide
                M[:, j] = M[:, j] / s[j]

        r_new = (1.0 + np.zeros([len(M), 1])) / len(M)

        c = (1.0 - self.damping_factor) * r_new

        r_prev = r_new

        while True:
            r_new = self.damping_factor * np.matmul(M, r_prev) + c
            diff = np.sum(abs(r_new - r_prev))  # 0.00001
            if diff < self.maxerr:  # 0.0000000001    <   #  0.00000001
                break

            r_prev = r_new

        rank_page = [item for sublist in r_prev for item in sublist]
        # Construct the ranked pages dictionary
        ranked_pages ={url: score for url, score in self.visited_urls},{ rank_page}

        self.write_map_in_file(ranked_pages)
        return ranked_pages

    def write_map_in_file(self, my_map):
        try:
            with open(f'{self.datasetsPath}\\page_rank.json', 'w') as file:
                json.dump(my_map, file, indent=4)  # Write the map to the file
            print("Write successful!")
        except Exception as e:
            print(f"Error writing to file: {e}")
