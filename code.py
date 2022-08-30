import random as rd
import re
import math
import string
import matplotlib.pyplot as plt
from pandas import DataFrame
def cleandata(url):
    f = open(url, "r", encoding="utf8")
    tweets = list(f)
    list_of_tweets = []
    for i in range(len(tweets)):
        tweets[i] = tweets[i].strip('\n')
        tweets[i] = tweets[i][50:]
        tweets[i] = " ".join(filter(lambda x: x[0] != '@', tweets[i].split()))
        tweets[i] = re.sub(r"http\S+", "", tweets[i])
        tweets[i] = re.sub(r"www\S+", "", tweets[i])
        tweets[i] = tweets[i].strip()
        tweet_len = len(tweets[i])
        if tweet_len > 0:
            if tweets[i][len(tweets[i]) - 1] == ':':
                tweets[i] = tweets[i][:len(tweets[i]) - 1]
        tweets[i] = tweets[i].replace('#', '')
        tweets[i] = tweets[i].lower()
        tweets[i] = tweets[i].translate(str.maketrans('', '', string.punctuation))
        tweets[i] = " ".join(tweets[i].split())
        list_of_tweets.append(tweets[i].split(' '))
    f.close()
    return list_of_tweets
def kmeans(tweets, k=4, max_iterations=50):
    centroids = []
    count = 0
    hash_map = dict()
    while count < k:
        random_tweet_idx = rd.randint(0, len(tweets) - 1)
        if random_tweet_idx not in hash_map:
            count += 1
            hash_map[random_tweet_idx] = True
            centroids.append(tweets[random_tweet_idx])
    iter_count = 0
    prev_centroids = []
    while (is_converged(prev_centroids, centroids)) == False and (iter_count < max_iterations):
        print(" iteration " + str(iter_count))
        clusters = assign_cluster(tweets, centroids)
        prev_centroids = centroids
        centroids = update_centroids(clusters)
        iter_count = iter_count + 1
        if (iter_count == max_iterations):
            print("max iterations , Kmeans not similar ")
        else:
            print("similar")

    sse = SSE(clusters)

    return clusters, sse
def is_converged(prev_centroid, new_centroids):
    if len(prev_centroid) != len(new_centroids):
        return False
    for c in range(len(new_centroids)):
        if " ".join(new_centroids[c]) != " ".join(prev_centroid[c]):
            return False
    return True
def assign_cluster(tweets, centroids):
    clusters = dict()
    for t in range(len(tweets)):
        min_dis = math.inf
        cluster_idx = -1;
        for c in range(len(centroids)):
            dis = Jaccard(centroids[c], tweets[t])
            if centroids[c] == tweets[t]:
                cluster_idx = c
                min_dis = 0
                break
            if dis < min_dis:
                cluster_idx = c
                min_dis = dis
        if min_dis == 1:
            cluster_idx = rd.randint(0, len(centroids) - 1)
        clusters.setdefault(cluster_idx, []).append([tweets[t]])
        last_tweet_idx = len(clusters.setdefault(cluster_idx, [])) - 1
        clusters.setdefault(cluster_idx, [])[last_tweet_idx].append(min_dis)
    return clusters
def update_centroids(clusters):
    centroids = []
    for c in range(len(clusters)):
        min_dis_sum = math.inf
        centroid_idx = -1
        min_dis_dp = []
        for t1 in range(len(clusters[c])):
            min_dis_dp.append([])
            dis_sum = 0
            for t2 in range(len(clusters[c])):
                if t1 != t2:
                    if t2 < t1:
                        dis = min_dis_dp[t2][t1]
                    else:
                        dis = Jaccard(clusters[c][t1][0], clusters[c][t2][0])
                    min_dis_dp[t1].append(dis)
                    dis_sum += dis
                else:
                    min_dis_dp[t1].append(0)
            if dis_sum < min_dis_sum:
                min_dis_sum = dis_sum
                centroid_idx = t1
        centroids.append(clusters[c][centroid_idx][0])
    return centroids
def Jaccard(tweet1, tweet2):
    intersection = set(tweet1).intersection(tweet2)
    union = set().union(tweet1, tweet2)
    return 1 - (len(intersection) / len(union))
def SSE(clusters):
    SSE = 0
    for c in range(len(clusters)):
        for t in range(len(clusters[c])):
            SSE = SSE + (clusters[c][t][1] * clusters[c][t][1])
    return SSE
if _name_ == '_main_':
    data_url = 'cnnhealth.txt'
    tweets = cleandata(data_url)
    experiments = 5
    k = 3
    for e in range(experiments):
        print("Kmeans for experiment  " + str((e + 1)) + " for k = " + str(k))
        clusters, sse = kmeans(tweets, k)
        for c in range(len(clusters)):
            print(str(c+1) + ": ", str(len(clusters[c])) + " tweets")
        print("SSE : " + str(sse))
        print('\n')
        k = k + 1