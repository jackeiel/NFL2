
# Lecture 5 - demo
# J. Rhee


# set working directory
setwd("")

# libraries
# install.packages() if needed
library(neuralnet) #has nn function/model
library(caret)
library(forecast)
library(ISLR)


### Neural Networks - Classification

df <- data.frame("Fat" = c(0.2,0.1,0.2,0.2,0.4,0.3),
                 "Salt" = c(0.9,0.1,0.4,0.5,0.5,0.8),
                 "Acceptance" =c("like","dislike","dislike","dislike","like","like"))
df

df$Like <- df$Acceptance=="like"
df$Dislike <- df$Acceptance=="dislike"
df

nn <- neuralnet(Like + Dislike ~ Salt + Fat, data = df, linear.output = F, hidden = c(3))
# the paramenter: hidden
# c(3) means single layer with 3 neurons
# c(1,4,2) means that the 1st hidden layer has one node,
#                     the 2nd hidden layer has four nodes,
#                     the 3rd hidden layer has two nodes.

# display weights
nn$weights

# display predictions
prediction(nn)

# plot network
plot(nn, rep="best")

# prediction on training
predict <- compute(nn, df[,1:2])
predict$net.result

predicted.class <- apply(predict$net.result,1,which.max) - 1
predicted.class

confusionMatrix(as.factor(ifelse(predicted.class=="1", "dislike", "like")), df$Acceptance)


### Neural Networks - Prediction

housing.df <- read.csv("BostonHousing.csv")
dim(housing.df)
head(housing.df)

var_selected <- c("MEDV", "CRIM", "CHAS", "RM")

housing.df <- housing.df[ , var_selected ]
dim(housing.df)
head(housing.df)


# partition
trainPercent <- round(nrow(housing.df) * 0.60)
totalRecords <- 1:nrow(housing.df)
idx          <- sample(totalRecords, trainPercent)
train.df <- housing.df[idx, ]
test.df  <- housing.df[-idx, ]

dim(train.df)
dim(test.df)

## linear regression (HW 3 Problem 1)
lr.model <- lm(MEDV ~ ., data = train.df)
summary(lr.model)

# prediction on training set
pred.train <- predict(lr.model, train.df[,-1])
residuals.train <- train.df$MEDV - pred.train
accuracy(pred.train, train.df$MEDV)

# prediction on test set
pred.test <- predict(lr.model, test.df[,-1])
residuals.test <- test.df$MEDV - pred.test
accuracy(pred.test, test.df$MEDV)


## neural networks

# normalize
norm.values <- preProcess(train.df, method="range")
train.norm.df <- predict(norm.values, train.df)
test.norm.df <- predict(norm.values, test.df)

range(train.norm.df$MEDV)
range(train.df$MEDV)
a <- range(train.df$MEDV)[1]; a
b <- range(train.df$MEDV)[2]; b

# run nn
nn <- neuralnet(MEDV ~ .,
                data = train.norm.df, 
                hidden = c(2,3))  # first hidden layer with 2 nodes
                                  # second hidden layer with 3 nodes

plot(nn)
nn$weights

# prediction on training set
train.prediction <- compute(nn, train.norm.df[,-1])
train.prediction$net.result
train.norm.df$MEDV
# nomalize back the output to the original scale
train.prediction$net.result * (b-a) + a
train.df$MEDV
accuracy(as.numeric(train.prediction$net.result) * (b-a) + a, train.df$MEDV)

# prediction on test set
test.prediction <- compute(nn, test.norm.df[,-1])
test.prediction$net.result
test.norm.df$MEDV
# nomalize back the output to the original scale
test.prediction$net.result * (b-a) + a
test.df$MEDV
accuracy(as.numeric(test.prediction$net.result) * (b-a) + a, test.df$MEDV)

## Compare the results of LR and NN !!!


### Hierarchical Clustering

utilities.df <- read.csv("Utilities.csv")
head(utilities.df)

# set row names to the utilities column
row.names(utilities.df) <- utilities.df[,1]

# remove the utility column
utilities.df <- utilities.df[,-1]
head(utilities.df)


# compute Euclidean distance
# (to compute other distance measures, change the value in method = )
d <- dist(utilities.df, method = "euclidean")
d
# However, we can't use this for clustering (distance-based algorithm)
# because it hasn't been standardized.


# normalize input variables
utilities.df.norm <- sapply(utilities.df, scale)
head(utilities.df.norm)

# add row names: utilities
row.names(utilities.df.norm) <- row.names(utilities.df) 
head(utilities.df.norm)

# compute normalized distance based on Sales (column 6) and Fuel Cost (column 8)
d.norm <- dist(utilities.df.norm[,c(6,8)], method = "euclidean")
d.norm
# we can use this standardized data.
plot(utilities.df.norm[,6],utilities.df.norm[,8])
# clusterin!  
hc1 <- hclust(d.norm, method = "single")
plot(hc1, hang = -1)
rect.hclust(hc1, k = 6)
cutree(hc1, k = 6)

hc2 <- hclust(d.norm, method = "complete")
plot(hc2, hang = -1)
rect.hclust(hc2, k = 6)
cutree(hc2, k = 6)

hc3 <- hclust(d.norm, method = "average")
plot(hc3, hang = -1)
rect.hclust(hc3, k = 6)
cutree(hc3, k = 6)

hc4 <- hclust(d.norm, method = "centroid")
plot(hc4, hang = -1)
rect.hclust(hc4, k = 6)
cutree(hc4, k = 6)

hc5 <- hclust(d.norm, method = "ward.D")
plot(hc5, hang = -1)
rect.hclust(hc5, k = 6)
cutree(hc5, k = 6)


### K-Means Clustering

x=matrix(rnorm(50*2), ncol=2)
x[1:25,1]=x[1:25,1]+3
x[1:25,2]=x[1:25,2]-4
x
plot(x)

x <- scale(x)
plot(x)

km.out <- kmeans(x,2,nstart=20)
km.out$cluster
plot(x, col=(km.out$cluster+1), main="K-Means Clustering Results with K=2", xlab="", ylab="", pch=20, cex=2)

km.out <- kmeans(x,3,nstart=20)
km.out
plot(x, col=(km.out$cluster+1), main="K-Means Clustering Results with K=3", xlab="", ylab="", pch=20, cex=2)

km.out <- kmeans(x,4,nstart=20)
km.out
plot(x, col=(km.out$cluster+1), main="K-Means Clustering Results with K=3", xlab="", ylab="", pch=20, cex=2)


## comparison between k-means and hier clustering

km.out <- kmeans(x, 3, nstart=20)
plot(x, col=(km.out$cluster+1), main="K-Means Clustering Results with K=3", xlab="", ylab="", pch=20, cex=2)

dist.x <- dist(x, method = "euclidean")
hc <- hclust(dist.x, method = "average")
plot(hc, hang = -1)
rect.hclust(hc, k = 3)

km.out$cluster
cutree(hc, k = 3)

table(km.out$cluster,cutree(hc1, k = 3))


### Extra Data: The NCI60 data

nci.labs=NCI60$labs
nci.data=NCI60$data
dim(nci.data)
nci.labs[1:4]
table(nci.labs)

sd.data=scale(nci.data)
data.dist=dist(sd.data)

# Hier Clustering

plot(hclust(data.dist), labels=nci.labs, main="Complete Linkage", xlab="", sub="",ylab="")
plot(hclust(data.dist, method="average"), labels=nci.labs, main="Average Linkage", xlab="", sub="",ylab="")
plot(hclust(data.dist, method="single"), labels=nci.labs,  main="Single Linkage", xlab="", sub="",ylab="")

hc.out=hclust(dist(sd.data))
hc.clusters=cutree(hc.out,4)
table(hc.clusters,nci.labs)
plot(hc.out, labels=nci.labs)
abline(h=139, col="red")
hc.out

# k-means with k=4
km.out=kmeans(sd.data, 4, nstart=20)
km.clusters=km.out$cluster

# comparisons
table(km.clusters,hc.clusters)


### End

