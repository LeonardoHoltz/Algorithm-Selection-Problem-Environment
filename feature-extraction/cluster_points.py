from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

clusters_range = range(2, 21, 2) # Search for clusters in range [2, 20], giving a step of 2

def number_clusters(X):
    best_n, best_silhouette = 1, -1.0
    for n_cluster in clusters_range:
        clusterer = KMeans(n_clusters=n_cluster, random_state=10)
        cluster_labels = clusterer.fit_predict(X)
        silhouette_avg = silhouette_score(X, cluster_labels)
        # print("Para cluster = ", n_cluster, " Valor= ", silhouette_avg)

        if (silhouette_avg > best_silhouette):
            best_silhouette = silhouette_avg
            best_n = n_cluster
    
    return best_n, len(X)/best_n
