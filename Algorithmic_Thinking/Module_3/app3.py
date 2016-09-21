# coding=utf-8
"""Application 3"""

import alg_cluster
import alg_clusters_matplotlib
import alg_project3_viz
import project3
import random
import time
import matplotlib.pyplot as plt
import urllib2


DIRECTORY = "http://commondatastorage.googleapis.com/codeskulptor-assets/"
DATA_3108_URL = DIRECTORY + "data_clustering/unifiedCancerData_3108.csv"
DATA_896_URL = DIRECTORY + "data_clustering/unifiedCancerData_896.csv"
DATA_290_URL = DIRECTORY + "data_clustering/unifiedCancerData_290.csv"
DATA_111_URL = DIRECTORY + "data_clustering/unifiedCancerData_111.csv"

def get_random_clusters(num_clusters):
    """
    creates a list of clusters where
    each cluster in this list corresponds
    to one randomly generated point in
    the square with corners (±1,±1).
    """
    cluster_list = []

    for cluster in range(num_clusters):
        cluster_list.append(alg_cluster.Cluster(set(), random.uniform(-1, 1), random.uniform(-1, 1), 0, 0))

    return cluster_list


def question1():
    clusters = range(2, 201)

    slow_closest_time = []
    fast_closest_time = []

    for num_clusters in clusters:
        cluster_list = get_random_clusters(num_clusters)

        ###slow_closet_pair_efficiency###
        start_time_slow = time.time()

        project3.slow_closest_pair(cluster_list)

        total_time_slow = time.time() - start_time_slow

        slow_closest_time.append(total_time_slow)

        ###fast_closest_pair efficiency###

        start_time_fast = time.time()

        project3.fast_closest_pair(cluster_list)

        total_time_fast = time.time() - start_time_fast

        fast_closest_time.append(total_time_fast)

    plt.plot(clusters, slow_closest_time, '-b', label='slow_closest_pair')
    plt.plot(clusters, fast_closest_time, '-r', label='fast_closest_pair')

    plt.legend(loc='upper right')
    plt.title('Efficiency')
    plt.xlabel('Number of clusters')
    plt.ylabel('Running time')

    plt.show()

def compute_distortion(cluster_list, data_table):

    error_list = []
    for cluster in cluster_list:
        error_list.append(cluster.cluster_error(data_table))
    return sum(error_list)

def question7():

    data_table = alg_project3_viz.load_data_table(DATA_111_URL)

    singleton_list = []
    for line in data_table:
        singleton_list.append(alg_cluster.Cluster(set([line[0]]), line[1], line[2], line[3], line[4]))

    clusters_hierarchical = project3.hierarchical_clustering(singleton_list, 9)
    clusters_kmeans = project3.kmeans_clustering(singleton_list, 9, 5)

    distortion_hierarchical = compute_distortion(clusters_hierarchical, data_table)
    distortion_kmeans = compute_distortion(clusters_kmeans, data_table)

    print "distortion hierarchical: ", distortion_hierarchical
    print "distortion k-means: ", distortion_kmeans

def compute_data_table(data_table):

    data_table_list = []
    for line in data_table:
        data_table_list.append(alg_cluster.Cluster(set([line[0]]), line[1], line[2], line[3], line[4]))
    return data_table_list

def question10():

    data_table_111 = alg_project3_viz.load_data_table(DATA_111_URL)
    data_table_290 = alg_project3_viz.load_data_table(DATA_290_URL)
    data_table_896 = alg_project3_viz.load_data_table(DATA_896_URL)

    data_table_list_111 = compute_data_table(data_table_111)
    data_table_list_290 = compute_data_table(data_table_290)
    data_table_list_896 = compute_data_table(data_table_896)

    clusters = range(6,21)

    distortion_h_111_y = []
    distortion_h_290_y = []
    distortion_h_896_y = []

    distortion_k_111_y = []
    distortion_k_290_y = []
    distortion_k_896_y = []


    for idx in clusters:
        ###y points for hierarchicall data_111
        h_111 = project3.hierarchical_clustering(data_table_list_111, idx)
        distortion_h_111 = compute_distortion(h_111, data_table_111)
        distortion_h_111_y.append(distortion_h_111)

        ###y points for k-means data_111
        k_111 = project3.kmeans_clustering(data_table_list_111, idx, 5)
        distortion_k_111 = compute_distortion(k_111, data_table_111)
        distortion_k_111_y.append(distortion_k_111)

        ###y points for hier data_290
        h_290 = project3.hierarchical_clustering(data_table_list_290, idx)
        distortion_h_290 = compute_distortion(h_290, data_table_290)
        distortion_h_290_y.append(distortion_h_290)

        ###y points for k-means data 290
        k_290 = project3.kmeans_clustering(data_table_list_290, idx, 5)
        distortion_k_290 = compute_distortion(k_290, data_table_290)
        distortion_k_290_y.append(distortion_k_290)

        ###y points for hier data_896
        h_896 = project3.hierarchical_clustering(data_table_list_896, idx)
        distortion_h_896 = compute_distortion(h_896, data_table_896)
        distortion_h_896_y.append(distortion_h_896)

        ###y points for k-means data 896
        k_896 = project3.kmeans_clustering(data_table_list_896, idx, 5)
        distortion_k_896 = compute_distortion(k_896, data_table_896)
        distortion_k_896_y.append(distortion_k_896)



    plt.plot(clusters, distortion_h_111_y, '-b', label = 'hierarchical' )
    plt.plot(clusters, distortion_k_111_y, '-r', label = 'k-means')
    plt.title('Distortion for 111 points')
    plt.legend(loc = 'upper right')
    plt.xlabel('Number of clusters')
    plt.ylabel('Distortion')
    plt.show()

    plt.plot(clusters, distortion_h_290_y, '-b', label='hierarchical')
    plt.plot(clusters, distortion_k_290_y, '-r', label='k-means')
    plt.title('Distortion for 290 points')
    plt.legend(loc='upper right')
    plt.xlabel('Number of clusters')
    plt.ylabel('Distortion')
    plt.show()

    plt.plot(clusters, distortion_h_896_y, '-b', label='hierarchical')
    plt.plot(clusters, distortion_k_896_y, '-r', label='k-means')
    plt.title('Distortion for 896 points')
    plt.legend(loc='upper right')
    plt.xlabel('Number of clusters')
    plt.ylabel('Distortion')
    plt.show()





