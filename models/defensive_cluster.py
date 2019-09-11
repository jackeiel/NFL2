import pandas as pd

'''
the goal here is to do the following:
1.) cluster teams into three categories based off of their defensive stats
2.) find average points allowed in each cluster
3.) cluster with highest average points allowed gets a score of 1
    cluster with middle points allowed gets score of 0
    cluster with fewest points allowed gets score of -1
    (this should create a type of indicator variable based on defensive stats, which penalizes an offensive prediction
    when going against a top flight defense)
4.) assign teams as keys to a dictionary with their value for the week as -1, 0, 1. 
5.) call the dictionary to assign the value in the offensive linear model
'''