import numpy as np
import pandas as pd


def list_to_csv_line(a_list, csv_sep):  # Concatenates items of a list by using csv separator
    line = ''
    for item in a_list:
        line += str(item) + csv_sep
    return line[:-len(csv_sep)]  # Remove last separator character


class KMeans:
    def __init__(self, iteration_num: int, num_of_class: int):
        self.num_of_class = num_of_class
        self.header = []
        self.dataset = []
        self.num_of_instances = len(self.dataset)
        self.cluster_labels = []
        self.iteration_num = iteration_num
        self.initial_centroids = []
        self.last_centroids = []

    def load_dataset(self, dataset_name, delimiter, has_header):
        if has_header:
            header_idx = 0
        else:
            header_idx = None

        df = pd.read_csv(dataset_name, sep=delimiter, header=header_idx)
        self.header = df.columns.tolist()
        self.dataset = df.values

    @staticmethod
    def __comp_euclidean_score(data_point):
        score = 0.0
        for data_point_dim in data_point:
            score += data_point_dim * data_point_dim
        return score

    @staticmethod
    def compute_euclidean_dist(point, centroid):
        return np.sqrt(np.sum((point - centroid) ** 2))

    @staticmethod
    def compute_new_centroids(cluster_label, centroids):
        return np.array(cluster_label + centroids) / 2

    def print_results(self):
        print('-' * 80)
        print('Result of k-Means Clustering:')
        for i in range(self.num_of_instances):
            for instance_item in self.dataset[i]:
                print('%d,' % instance_item, end='')  # Dataset
            print('%d' % self.cluster_labels[i])  # Label
        print('-' * 80)
        num_of_1s = self.cluster_labels.count(1)
        num_of_0s = self.cluster_labels.count(0)
        print('Num of 1s:%d' % num_of_1s)
        print('Num of 0s:%d' % num_of_0s)
        print('Percentage of 1s: %.3f%%' % (100 * num_of_1s / (num_of_0s + num_of_1s)))

    def __find_min_max(self, compute_min: bool):
        # Initialize with first point.
        extreme_point = self.dataset[0]
        extreme_point_score = self.__comp_euclidean_score(self.dataset[0])

        for i in range(self.dataset.__len__()):
            if compute_min == (extreme_point_score > self.__comp_euclidean_score(self.dataset[i])):
                extreme_point_score = self.__comp_euclidean_score(self.dataset[i])
                extreme_point = self.dataset[i]

        print('Min Point: ', end='') if compute_min else print('Max Point: ', end='')
        for item in extreme_point:
            print('\t%.2f' % item, end='')
        print(' -> Score: %.4f' % extreme_point_score)

        return extreme_point  # Min or Max

    def create_two_initial_centroids(self):
        initial_centroids = [] * self.num_of_class
        min_point = self.__find_min_max(compute_min=True)
        max_point = self.__find_min_max(compute_min=False)

        initial_centroids.append(min_point)
        initial_centroids.append(max_point)
        self.initial_centroids = initial_centroids

    def iterate_k_means(self):
        new_centroids = self.initial_centroids
        for i in range(self.iteration_num):
            for j in range(len(self.dataset)):
                distance = {}
                for k in range(self.num_of_class):
                    distance[k] = self.compute_euclidean_dist(self.dataset[j], new_centroids[k])
                label = min(distance, key=distance.get)
                new_centroids[label] = self.compute_new_centroids(self.dataset[j], new_centroids[label])

                if i == (self.iteration_num - 1):
                    self.cluster_labels.append(label)

        self.last_centroids = new_centroids

    def write_dataset(self, output_file, delimiter):
        output_csv = open(output_file, 'w')

        self.header.append('class_success')
        new_header = list_to_csv_line(self.header, delimiter)
        output_csv.write(new_header + '\n')

        for i in range(self.dataset.__len__()):
            dataset_item_list = self.dataset[i].tolist()
            dataset_item_list.append(self.cluster_labels[i])
            output_csv.write(list_to_csv_line(dataset_item_list, delimiter) + '\n')
        output_csv.close()