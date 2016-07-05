library(ade4)
library(cluster)
library(fpc)

quintiles <- read.csv('Results/quintiles.csv', header = TRUE, sep = ";")
mat_quintiles <- as.matrix(quintiles)

dudi1 <- dudi.pca(mat_quintiles, scan = FALSE, nf = 3) # a normed PCA
data <- dudi1$tab

## Sommes cumulées des contributions
kip <- 100 * dudi1$eig/sum(dudi1$eig)
cumsum(kip)

## Choix des composantes pour les cercles de correlations
#l <- list(dudi1$c1[2], dudi1$c1[3])
l <- dudi1$c1

## Cercles de correlations
#s.corcircle(l, lab = 2:30)

##kmeans
cl <- kmeans(data, 4)
plotcluster(data, cl$cluster, pch = 16)

##centres
cl$centers

##taille de chaque cluster
cl$size
