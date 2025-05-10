import tkinter as tk
from tkinter import messagebox
import heapq

# Graph Class for Campus Navigation
class CampusGraph:
    def __init__(self):
        self.graph = {}

    def add_location(self, location):
        if location not in self.graph:
            self.graph[location] = {}

    def add_route(self, loc1, loc2, distance):
        if loc1 in self.graph and loc2 in self.graph:
            self.graph[loc1][loc2] = distance
            self.graph[loc2][loc1] = distance
        else:
            print("Location not found in graph")

    def find_shortest_path(self, start, end):
        if start not in self.graph or end not in self.graph:
            return None, "Location not found"
        
        queue = [(0, start)]  # (distance, location)
        distances = {loc: float('inf') for loc in self.graph}
        distances[start] = 0
        previous_nodes = {loc: None for loc in self.graph}
        
        while queue:
            current_distance, current_location = heapq.heappop(queue)
            
            if current_location == end:
                path = []
                while current_location is not None:
                    path.append(current_location)
                    current_location = previous_nodes[current_location]
                return distances[end], list(reversed(path))
            
            for neighbor, weight in self.graph[current_location].items():
                distance = current_distance + weight
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    previous_nodes[neighbor] = current_location
                    heapq.heappush(queue, (distance, neighbor))
        
        return None, "Path not found"

# GUI Application
class CampusNavigationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Campus Navigation System")
        self.graph = CampusGraph()

        tk.Label(root, text="Add Locations").grid(row=0, column=0)
        self.location_entry = tk.Entry(root)
        self.location_entry.grid(row=0, column=1)
        tk.Button(root, text="Add", command=self.add_location).grid(row=0, column=2)

        tk.Label(root, text="Add Routes").grid(row=1, column=0)
        self.route_start = tk.Entry(root)
        self.route_start.grid(row=1, column=1)
        self.route_end = tk.Entry(root)
        self.route_end.grid(row=1, column=2)
        self.route_distance = tk.Entry(root)
        self.route_distance.grid(row=1, column=3)
        tk.Button(root, text="Add", command=self.add_route).grid(row=1, column=4)

        tk.Label(root, text="Find Path").grid(row=2, column=0)
        self.path_start = tk.Entry(root)
        self.path_start.grid(row=2, column=1)
        self.path_end = tk.Entry(root)
        self.path_end.grid(row=2, column=2)
        tk.Button(root, text="Find", command=self.find_path).grid(row=2, column=3)

    def add_location(self):
        loc = self.location_entry.get()
        if loc:
            self.graph.add_location(loc)
            messagebox.showinfo("Success", f"Location {loc} added successfully")
        else:
            messagebox.showerror("Error", "Enter a location")

    def add_route(self):
        loc1 = self.route_start.get()
        loc2 = self.route_end.get()
        try:
            distance = float(self.route_distance.get())
            self.graph.add_route(loc1, loc2, distance)
            messagebox.showinfo("Success", f"Route {loc1} <-> {loc2} added")
        except ValueError:
            messagebox.showerror("Error", "Enter a valid distance")

    def find_path(self):
        start = self.path_start.get()
        end = self.path_end.get()
        distance, path = self.graph.find_shortest_path(start, end)
        if path:
            messagebox.showinfo("Shortest Path", f"Path: {' -> '.join(path)}\nDistance: {distance} units")
        else:
            messagebox.showerror("Error", "Path not found")

if __name__ == "__main__":
    root = tk.Tk()
    app = CampusNavigationApp(root)
    root.mainloop()