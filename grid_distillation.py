import os

import numpy as np
import matplotlib.pyplot as plt


from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from sklearn.model_selection import train_test_split


class ImageClusterSampler:
    def __init__(self, X, y, n_clusters=2):
        self.X = X
        self.y = y
        self.n_clusters = n_clusters
        self.cluster_labels = None
        self.X_pca = None
        self.kmeans = KMeans(n_clusters=self.n_clusters, random_state=42)
        self.pca = PCA(n_components=2, random_state=42)
    
    def cluster_images(self):
        self.kmeans.fit(self.X.reshape(self.X.shape[0], -1))
        self.cluster_labels = self.kmeans.labels_
        self.X_pca = self.pca.fit_transform(self.X.reshape(self.X.shape[0], -1))

    def plot_clusters(self):
        plt.figure(figsize=(10, 6))
        for i in range(self.n_clusters):
            cluster_data = self.X_pca[self.cluster_labels == i]
            plt.scatter(cluster_data[:, 0], cluster_data[:, 1], label=f'Cluster {i}')
        plt.title('Clustering of Cats and Dogs')
        plt.xlabel('PCA Component 1')
        plt.ylabel('PCA Component 2')
        plt.legend()
        plt.show()

    def select_diverse_samples(self, cluster_indices, n_samples):


        if len(cluster_indices) <= n_samples:
            return cluster_indices
        
        selected_indices = []
        grid_size = int(np.ceil(np.sqrt(n_samples)))
        x_min, x_max = np.min(self.X_pca[:, 0]), np.max(self.X_pca[:, 0])
        y_min, y_max = np.min(self.X_pca[:, 1]), np.max(self.X_pca[:, 1])
        
        x_grid = np.linspace(x_min, x_max, grid_size + 1)
        y_grid = np.linspace(y_min, y_max, grid_size + 1)
        
        # plot also all the grids for each iteration on the same graph
        for i in range(grid_size):
            for j in range(grid_size):
                x_start, x_end = x_grid[i], x_grid[i + 1]
                y_start, y_end = y_grid[j], y_grid[j + 1]


                
                grid_indices = [
                    idx for idx in cluster_indices 
                    if x_start <= self.X_pca[idx, 0] < x_end and y_start <= self.X_pca[idx, 1] < y_end
                ]
                
                if grid_indices:
                    selected_indices.append(np.random.choice(grid_indices))

                
        
        while len(selected_indices) < n_samples:
            selected_indices.append(np.random.choice(cluster_indices))
        
        return selected_indices[:n_samples]

    def get_selected_samples(self, n_samples):
        selected_samples = []
        for label in range(2):
            label_indices = np.where(self.y == label)[0]
            label_cluster_labels = self.cluster_labels[label_indices]
            unique_clusters = np.unique(label_cluster_labels)
            
            for cluster_id in unique_clusters:
                cluster_indices = label_indices[label_cluster_labels == cluster_id]
                selected_indices = self.select_diverse_samples(cluster_indices, n_samples)
                selected_samples.extend(selected_indices)
        return selected_samples
    
    def plot_selected_samples_on_clusters(self, selected_samples):
        plt.figure(figsize=(10, 6))
        for i in range(self.n_clusters):
            cluster_data = self.X_pca[self.cluster_labels == i]
            plt.scatter(cluster_data[:, 0], cluster_data[:, 1], label=f'Cluster {i}', alpha=0.5)
        
        selected_data = self.X_pca[selected_samples]
        plt.scatter(selected_data[:, 0], selected_data[:, 1], color='red', label='Selected Samples', edgecolor='k')
        
        plt.title('Clustering of Cats and Dogs with Selected Samples')
        plt.xlabel('PCA Component 1')
        plt.ylabel('PCA Component 2')
        plt.legend()
        plt.show()


class GridImageClusterSampler(ImageClusterSampler):
    def plot_clusters_with_grids(self, n_samples):
        plt.figure(figsize=(10, 6))
        for i in range(self.n_clusters):
            cluster_data = self.X_pca[self.cluster_labels == i]
            plt.scatter(cluster_data[:, 0], cluster_data[:, 1], label=f'Cluster {i}', alpha=0.5)
        
        grid_size = int(np.ceil(np.sqrt(n_samples)))
        x_min, x_max = np.min(self.X_pca[:, 0]), np.max(self.X_pca[:, 0])
        y_min, y_max = np.min(self.X_pca[:, 1]), np.max(self.X_pca[:, 1])
        
        x_grid = np.linspace(x_min, x_max, grid_size + 1)
        y_grid = np.linspace(y_min, y_max, grid_size + 1)
        
        for x in x_grid:
            plt.axvline(x=x, color='k', linestyle='--', alpha=0.5)
        for y in y_grid:
            plt.axhline(y=y, color='k', linestyle='--', alpha=0.5)
        
        plt.title('Clustering of Cats and Dogs with Grids')
        plt.xlabel('PCA Component 1')
        plt.ylabel('PCA Component 2')
        plt.legend()
        plt.show()
    
    def get_grid_sampled_indices(self, cluster_indices, n_samples):
        if len(cluster_indices) <= n_samples:
            return cluster_indices
        
        grid_size = int(np.ceil(np.sqrt(n_samples)))
        x_min, x_max = np.min(self.X_pca[:, 0]), np.max(self.X_pca[:, 0])
        y_min, y_max = np.min(self.X_pca[:, 1]), np.max(self.X_pca[:, 1])
        
        x_grid = np.linspace(x_min, x_max, grid_size + 1)
        y_grid = np.linspace(y_min, y_max, grid_size + 1)
        
        sampled_indices = []
        for i in range(grid_size):
            for j in range(grid_size):
                x_start, x_end = x_grid[i], x_grid[i + 1]
                y_start, y_end = y_grid[j], y_grid[j + 1]
                
                grid_indices = [
                    idx for idx in cluster_indices 
                    if x_start <= self.X_pca[idx, 0] < x_end and y_start <= self.X_pca[idx, 1] < y_end
                ]
                
                if grid_indices:
                    sampled_indices.append(np.random.choice(grid_indices))

        while len(sampled_indices) < n_samples:
            sampled_indices.append(np.random.choice(cluster_indices))
        
        return sampled_indices[:n_samples]

    def get_selected_samples(self, n_samples):
        selected_samples = []
        for label in range(2):
            label_indices = np.where(self.y == label)[0]
            label_cluster_labels = self.cluster_labels[label_indices]
            unique_clusters = np.unique(label_cluster_labels)
            
            for cluster_id in unique_clusters:
                cluster_indices = label_indices[label_cluster_labels == cluster_id]
                selected_indices = self.get_grid_sampled_indices(cluster_indices, n_samples)
                selected_samples.extend(selected_indices)
        return selected_samples

class ParallelogramImageClusterSampler:
    def __init__(self, X, y, n_clusters=2):
        self.X = X
        self.y = y
        self.n_clusters = n_clusters
        self.cluster_labels = None
        self.X_pca = None
        self.kmeans = KMeans(n_clusters=self.n_clusters, random_state=42)
        self.pca = PCA(n_components=2, random_state=42)
    
    def cluster_images(self):
        self.kmeans.fit(self.X.reshape(self.X.shape[0], -1))
        self.cluster_labels = self.kmeans.labels_
        self.X_pca = self.pca.fit_transform(self.X.reshape(self.X.shape[0], -1))

    def plot_clusters_with_parallelograms(self, angle=30, grid_size=10):
        plt.figure(figsize=(10, 6))
        for i in range(self.n_clusters):
            cluster_data = self.X_pca[self.cluster_labels == i]
            plt.scatter(cluster_data[:, 0], cluster_data[:, 1], label=f'Cluster {i}', alpha=0.5)
        
        x_min, x_max = np.min(self.X_pca[:, 0]), np.max(self.X_pca[:, 0])
        y_min, y_max = np.min(self.X_pca[:, 1]), np.max(self.X_pca[:, 1])
        
        x_length = (x_max - x_min) / grid_size
        dx = x_length * np.cos(np.radians(angle))
        dy = x_length * np.sin(np.radians(angle))
        y_length = dy

        for i in range(grid_size):
            for j in range(grid_size):
                x_start = x_min + i * x_length
                y_start = y_min + j * y_length

                parallelogram = [
                    (x_start, y_start),
                    (x_start + x_length, y_start),
                    (x_start + x_length + dx, y_start + dy),
                    (x_start + dx, y_start + dy)
                ]
                
                parallelogram_x, parallelogram_y = zip(*parallelogram)
                plt.plot(parallelogram_x + (parallelogram_x[0],), parallelogram_y + (parallelogram_y[0],), 'k--', alpha=0.5)
        
        plt.title('Clustering with Parallelogram Grids')
        plt.xlabel('PCA Component 1')
        plt.ylabel('PCA Component 2')
        plt.legend()
        plt.show()
    
    def get_parallelogram_sampled_indices(self, cluster_indices, n_samples, angle=30, grid_size=10):
        if len(cluster_indices) <= n_samples:
            return cluster_indices
        
        x_min, x_max = np.min(self.X_pca[:, 0]), np.max(self.X_pca[:, 0])
        y_min, y_max = np.min(self.X_pca[:, 1]), np.max(self.X_pca[:, 1])
        
        x_length = (x_max - x_min) / grid_size
        dx = x_length * np.cos(np.radians(angle))
        dy = x_length * np.sin(np.radians(angle))
        y_length = dy
        
        sampled_indices = []
        
        for i in range(grid_size):
            for j in range(grid_size):
                x_start = x_min + i * x_length
                y_start = y_min + j * y_length

                parallelogram_indices = [
                    idx for idx in cluster_indices 
                    if (self.X_pca[idx, 0] >= x_start and self.X_pca[idx, 0] < x_start + x_length + dx and
                        self.X_pca[idx, 1] >= y_start and self.X_pca[idx, 1] < y_start + y_length and
                        (self.X_pca[idx, 1] - y_start) < dy / dx * (self.X_pca[idx, 0] - x_start + x_length))
                ]
                
                if parallelogram_indices:
                    sampled_indices.append(np.random.choice(parallelogram_indices))

        while len(sampled_indices) < n_samples:
            sampled_indices.append(np.random.choice(cluster_indices))
        
        return sampled_indices[:n_samples]

    def get_selected_samples(self, n_samples):
        selected_samples = []
        for label in range(2):
            label_indices = np.where(self.y == label)[0]
            label_cluster_labels = self.cluster_labels[label_indices]
            unique_clusters = np.unique(label_cluster_labels)
            
            for cluster_id in unique_clusters:
                cluster_indices = label_indices[label_cluster_labels == cluster_id]
                selected_indices = self.get_parallelogram_sampled_indices(cluster_indices, n_samples)
                selected_samples.extend(selected_indices)
        return selected_samples

    def plot_selected_samples_on_clusters(self, selected_samples):
        plt.figure(figsize=(10, 6))
        for i in range(self.n_clusters):
            cluster_data = self.X_pca[self.cluster_labels == i]
            plt.scatter(cluster_data[:, 0], cluster_data[:, 1], label=f'Cluster {i}', alpha=0.5)
        
        selected_data = self.X_pca[selected_samples]
        plt.scatter(selected_data[:, 0], selected_data[:, 1], color='red', label='Selected Samples', edgecolor='k')
        
        plt.title('Clustering with Selected Samples')
        plt.xlabel('PCA Component 1')
        plt.ylabel('PCA Component 2')
        plt.legend()
        plt.show()


class TriangularImageClusterSampler:
    def __init__(self, X, y, n_clusters=2):
        self.X = X
        self.y = y
        self.n_clusters = n_clusters
        self.cluster_labels = None
        self.X_pca = None
        self.kmeans = KMeans(n_clusters=self.n_clusters, random_state=42)
        self.pca = PCA(n_components=2, random_state=42)
    
    def cluster_images(self):
        self.kmeans.fit(self.X.reshape(self.X.shape[0], -1))
        self.cluster_labels = self.kmeans.labels_
        self.X_pca = self.pca.fit_transform(self.X.reshape(self.X.shape[0], -1))

    def plot_clusters_with_triangles(self, grid_size=10):
        plt.figure(figsize=(10, 6))
        for i in range(self.n_clusters):
            cluster_data = self.X_pca[self.cluster_labels == i]
            plt.scatter(cluster_data[:, 0], cluster_data[:, 1], label=f'Cluster {i}', alpha=0.5)
        
        x_min, x_max = np.min(self.X_pca[:, 0]), np.max(self.X_pca[:, 0])
        y_min, y_max = np.min(self.X_pca[:, 1]), np.max(self.X_pca[:, 1])
        
        side_length = (x_max - x_min) / grid_size
        height = np.sqrt(3) / 2 * side_length
        
        for i in range(-1, grid_size + 1):
            for j in range(-1, grid_size + 1):
                x_start = x_min + i * side_length
                y_start = y_min + j * height

                if (i + j) % 2 == 0:
                    triangle = [
                        (x_start, y_start),
                        (x_start + side_length / 2, y_start + height),
                        (x_start - side_length / 2, y_start + height)
                    ]
                else:
                    triangle = [
                        (x_start, y_start),
                        (x_start + side_length, y_start),
                        (x_start + side_length / 2, y_start + height)
                    ]

                triangle_x, triangle_y = zip(*triangle)
                plt.plot(triangle_x + (triangle_x[0],), triangle_y + (triangle_y[0],), 'k--', alpha=0.5)
        
        plt.title('Clustering with Triangular Grids')
        plt.xlabel('PCA Component 1')
        plt.ylabel('PCA Component 2')
        plt.legend()
        plt.show()
    
    def get_triangle_sampled_indices(self, cluster_indices, n_samples, grid_size=10):
        if len(cluster_indices) <= n_samples:
            return cluster_indices
        
        x_min, x_max = np.min(self.X_pca[:, 0]), np.max(self.X_pca[:, 0])
        y_min, y_max = np.min(self.X_pca[:, 1]), np.max(self.X_pca[:, 1])
        
        side_length = (x_max - x_min) / grid_size
        height = np.sqrt(3) / 2 * side_length
        
        sampled_indices = []
        
        for i in range(-1, grid_size + 1):
            for j in range(-1, grid_size + 1):
                x_start = x_min + i * side_length
                y_start = y_min + j * height

                if (i + j) % 2 == 0:
                    triangle_indices = [
                        idx for idx in cluster_indices 
                        if self.point_in_triangle(self.X_pca[idx], 
                                                  (x_start, y_start), 
                                                  (x_start + side_length / 2, y_start + height), 
                                                  (x_start - side_length / 2, y_start + height))
                    ]
                else:
                    triangle_indices = [
                        idx for idx in cluster_indices 
                        if self.point_in_triangle(self.X_pca[idx], 
                                                  (x_start, y_start), 
                                                  (x_start + side_length, y_start), 
                                                  (x_start + side_length / 2, y_start + height))
                    ]

                if triangle_indices:
                    sampled_indices.append(np.random.choice(triangle_indices))

        while len(sampled_indices) < n_samples:
            sampled_indices.append(np.random.choice(cluster_indices))
        
        return sampled_indices[:n_samples]
    
    def point_in_triangle(self, point, v1, v2, v3):
        def sign(p1, p2, p3):
            return (p1[0] - p3[0]) * (p2[1] - p3[1]) - (p2[0] - p3[0]) * (p1[1] - p3[1])
        
        b1 = sign(point, v1, v2) < 0.0
        b2 = sign(point, v2, v3) < 0.0
        b3 = sign(point, v3, v1) < 0.0
        
        return ((b1 == b2) & (b2 == b3))

    def get_selected_samples(self, n_samples):
        selected_samples = []
        for label in range(2):
            label_indices = np.where(self.y == label)[0]
            label_cluster_labels = self.cluster_labels[label_indices]
            unique_clusters = np.unique(label_cluster_labels)
            
            for cluster_id in unique_clusters:
                cluster_indices = label_indices[label_cluster_labels == cluster_id]
                selected_indices = self.get_triangle_sampled_indices(cluster_indices, n_samples)
                selected_samples.extend(selected_indices)
        return selected_samples

    def plot_selected_samples_on_clusters(self, selected_samples):
        plt.figure(figsize=(10, 6))
        for i in range(self.n_clusters):
            cluster_data = self.X_pca[self.cluster_labels == i]
            plt.scatter(cluster_data[:, 0], cluster_data[:, 1], label=f'Cluster {i}', alpha=0.5)
        
        selected_data = self.X_pca[selected_samples]
        plt.scatter(selected_data[:, 0], selected_data[:, 1], color='red', label='Selected Samples', edgecolor='k')
        
        plt.title('Clustering with Selected Samples')
        plt.xlabel('PCA Component 1')
        plt.ylabel('PCA Component 2')
        plt.legend()
        plt.show()

class BrickImageClusterSampler(ImageClusterSampler):
    def plot_clusters_with_bricks(self, n_samples):
        plt.figure(figsize=(10, 6))
        for i in range(self.n_clusters):
            cluster_data = self.X_pca[self.cluster_labels == i]
            plt.scatter(cluster_data[:, 0], cluster_data[:, 1], label=f'Cluster {i}', alpha=0.5)
        
        grid_size = int(np.ceil(np.sqrt(n_samples)))
        x_min, x_max = np.min(self.X_pca[:, 0]), np.max(self.X_pca[:, 0])
        y_min, y_max = np.min(self.X_pca[:, 1]), np.max(self.X_pca[:, 1])
        
        x_grid = np.linspace(x_min, x_max, grid_size + 1)
        y_grid = np.linspace(y_min, y_max, grid_size + 1)
        
        # Define the parallelogram shape by skewing the grid
        skew_factor = (x_max - x_min) / (grid_size * 2)  # Adjust skew factor as needed
        
        for i in range(grid_size):
            for j in range(grid_size):
                x_start, x_end = x_grid[i] + j * skew_factor, x_grid[i + 1] + j * skew_factor
                y_start, y_end = y_grid[j], y_grid[j + 1]
                
                plt.plot([x_start, x_end], [y_start, y_start], 'k--', alpha=0.5)
                plt.plot([x_start, x_end], [y_end, y_end], 'k--', alpha=0.5)
                plt.plot([x_start, x_start], [y_start, y_end], 'k--', alpha=0.5)
                plt.plot([x_end, x_end], [y_start, y_end], 'k--', alpha=0.5)
        
        plt.title('Clustering of Cats and Dogs with Brick Grids')
        plt.xlabel('PCA Component 1')
        plt.ylabel('PCA Component 2')
        plt.legend()
        plt.show()
    
    def get_brick_sampled_indices(self, cluster_indices, n_samples):
        if len(cluster_indices) <= n_samples:
            return cluster_indices
        
        grid_size = int(np.ceil(np.sqrt(n_samples)))
        x_min, x_max = np.min(self.X_pca[:, 0]), np.max(self.X_pca[:, 0])
        y_min, y_max = np.min(self.X_pca[:, 1]), np.max(self.X_pca[:, 1])
        
        x_grid = np.linspace(x_min, x_max, grid_size + 1)
        y_grid = np.linspace(y_min, y_max, grid_size + 1)
        
        sampled_indices = []
        skew_factor = (x_max - x_min) / (grid_size * 2)  # Adjust skew factor as needed
        
        for i in range(grid_size):
            for j in range(grid_size):
                x_start, x_end = x_grid[i] + j * skew_factor, x_grid[i + 1] + j * skew_factor
                y_start, y_end = y_grid[j], y_grid[j + 1]
                
                grid_indices = [
                    idx for idx in cluster_indices 
                    if x_start <= self.X_pca[idx, 0] < x_end and y_start <= self.X_pca[idx, 1] < y_end
                ]
                
                if grid_indices:
                    sampled_indices.append(np.random.choice(grid_indices))

        while len(sampled_indices) < n_samples:
            sampled_indices.append(np.random.choice(cluster_indices))
        
        return sampled_indices[:n_samples]

    def get_selected_samples(self, n_samples):
        selected_samples = []
        for label in range(2):
            label_indices = np.where(self.y == label)[0]
            label_cluster_labels = self.cluster_labels[label_indices]
            unique_clusters = np.unique(label_cluster_labels)
            
            for cluster_id in unique_clusters:
                cluster_indices = label_indices[label_cluster_labels == cluster_id]
                selected_indices = self.get_parallelogram_sampled_indices(cluster_indices, n_samples)
                selected_samples.extend(selected_indices)
        return selected_samples
    
