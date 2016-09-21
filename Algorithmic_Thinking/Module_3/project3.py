"""
Week2/ Project3
"""
import math
import alg_cluster


def slow_closest_pair(cluster_list):
    """
    Takes a list of Cluster objects and returns a
    closest pair where the pair is represented by
    the tuple (dist, idx1, idx2) with idx1 < idx2
    where dist is the distance between the
    closest pair cluster_list[idx1] and cluster_list[idx2].
    This function should implement the brute-force closest
    pair method described in SlowClosestPair from Homework 3.
    """
    distance = float('+inf')
    idx1 = -1
    idx2 = -1

    for dummy_idx1 in range(len(cluster_list)):
        for dummy_idx2 in range(dummy_idx1 + 1, len(cluster_list)):

            distance_between_clusters = cluster_list[dummy_idx1].distance(cluster_list[dummy_idx2])

            if distance_between_clusters < distance:
                distance = distance_between_clusters
                idx1 = dummy_idx1
                idx2 = dummy_idx2

    return distance, min(idx1, idx2), max(idx1, idx2)


def fast_closest_pair(cluster_list):
    """
    Takes a list of Cluster objects and returns a
    closest pair where the pair is represented by
    the tuple (dist, idx1, idx2) with idx1 < idx2
    where dist is the distance between the
    closest pair cluster_list[idx1] and cluster_list[idx2].
    This function should implement the divide-and-conquer
    closest pair method described FastClosestPair from Homework 3.
    :rtype: object
    :param cluster_list:
    :return:(dist, idx1, idx2)
    """

    nodes = len(cluster_list)

    if nodes <= 3:
        return slow_closest_pair(cluster_list)

    middle_point = nodes / 2

    cluster_list.sort(key=lambda cluster: cluster.horiz_center())

    cluster_list_left = cluster_list[:middle_point]
    cluster_list_right = cluster_list[middle_point:]

    distance_left = fast_closest_pair(cluster_list_left)
    distance_right = fast_closest_pair(cluster_list_right)

    distance = min((distance_left[0], distance_left[1], distance_left[2]),
                   (distance_right[0], distance_right[1] + middle_point, distance_right[2] + middle_point))

    mid = (cluster_list[middle_point - 1].horiz_center() + cluster_list[middle_point].horiz_center()) / 2.0

    return min(distance, closest_pair_strip(cluster_list, mid, distance[0]))


def closest_pair_strip(cluster_list, horiz_center, half_width):
    """
    Takes a list of Cluster objects and two floats
    horiz_center and half_width. horiz_center specifies
    the horizontal position of the center line for a vertical strip.
    half_width specifies the maximal distance of any point in the strip
    from the center line. This function should implement the helper
    function described in ClosestPairStrip from Homework 3 and return
    a tuple corresponding to the closest pair of clusters that lie
    in the specified strip. (Again the return pair of indices should
    be in ascending order.)

    :param cluster_list:
    :param horiz_center:
    :param half_width:
    :return:
    """
    cluster_s = []

    for dummy_idx in range(len(cluster_list)):
        if abs(cluster_list[dummy_idx].horiz_center() - horiz_center) < half_width:
            cluster_s.append(dummy_idx)

    cluster_s.sort(key=lambda cluster_s: cluster_list[cluster_s].vert_center())

    distance = float('+inf')
    idx1 = -1
    idx2 = -1

    for dummy_u in range(len(cluster_s) - 1):
        for dummy_v in range(dummy_u + 1, min(dummy_u + 3, len(cluster_s) - 1) + 1):

            temp_distance = cluster_list[cluster_s[dummy_u]].distance(cluster_list[cluster_s[dummy_v]])

            if temp_distance < distance:
                distance = temp_distance
                idx1 = cluster_s[dummy_u]
                idx2 = cluster_s[dummy_v]

    return distance, min(idx1, idx2), max(idx1, idx2)


def hierarchical_clustering(cluster_list, num_clusters):
    """
    Takes a list of Cluster objects and applies
    hierarchical clustering as described in the pseudo-code
    HierarchicalClustering from Homework 3 to this list of clusters.
    This clustering process should proceed until
    num_clusters clusters remain. The function then returns this list of clusters.
    :param cluster_list:
    :param num_clusters:
    :return: clusters
    """

    clusters = [dummy_cluster.copy() for dummy_cluster in cluster_list]

    while len(clusters) > num_clusters:
        closest_points = fast_closest_pair(clusters)

        idx1 = closest_points[1]
        idx2 = closest_points[2]

        clusters[idx1].merge_clusters(clusters[idx2])

        del clusters[idx2]

    return clusters


def nearest_cluster(point, cluster_list):
    """Helper function"""
    distance = float('inf')

    for idx_i in range(len(cluster_list)):

        if point.distance(cluster_list[idx_i]) < distance:
            distance = point.distance(cluster_list[idx_i])
            nearest = idx_i

    return nearest


def kmeans_clustering(cluster_list, num_clusters, num_iterations):
    """
    Takes a list of Cluster objects and applies k-means clustering
    as described in the pseudo-code KMeansClustering from Homework 3
    to this list of clusters. This function should compute an initial list
    of clusters (line 2 in the pseudo-code) with the property that each
    cluster consists of a single county chosen from the set of the num_cluster
     counties with the largest populations. The function should then compute
     num_iterations of k-means clustering and return this resulting list of clusters.
    :param cluster_list:
    :param num_clusters:
    :param num_iterations:
    :return:
    """

    cluster = [dummy_cluster.copy() for dummy_cluster in cluster_list]
    cluster.sort(key=lambda cluster_list: cluster_list.total_population(), reverse=True)

    # position initial clusters at the location of clusters with largest populations
    center = [dummy_cluster for dummy_cluster in cluster[:num_clusters]]

    for dummy_iter in range(num_iterations):

        cluster_k = [alg_cluster.Cluster(set(), 0, 0, 0, 0) for _ in range(num_clusters)]

        for dummy_idx in range(len(cluster_list)):

            cluster_sel = nearest_cluster(cluster_list[dummy_idx], center)

            cluster_k[cluster_sel].merge_clusters(cluster_list[dummy_idx])

        for dummy_center in range(num_clusters):
            center[dummy_center] = cluster_k[dummy_center].copy()

    return center
