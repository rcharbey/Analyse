library(ade4)
library(cluster)
library(fpc)
quintiles <- read.csv('quintiles.csv', header = TRUE, sep = ";")
mat_quintiles <- as.matrix(quintiles)
dudi1 <- dudi.pca(mat_quintiles, scan = FALSE) # a normed PCA
data <- dudi1$tab

par(mfrow = c(2,2))
# s.corcircle(dudi1$co, lab = colnames(mat_quintiles))
cl <- kmeans(data, 7)
plotcluster(data, cl$cluster)
