library(FactoMineR) # PCA
library(ggplot2) # drawing


res.pca1 = prcomp(USArrests, scale. = TRUE)
res.pca2 = PCA(USArrests, graph=TRUE)
plot.PCA(res.pca2, axes=c(1, 2), choix="ind", habillage="ind")


# create data frame with scores
scores = as.data.frame(res.pca1$x)

# plot of observations
pdf("prcomp_res.pdf")

ggplot(data=scores, aes(x=PC1, y=PC2, label=rownames(scores))) +
geom_hline(yintercept=0, colour="gray65") +
geom_vline(xintercept=0, colour="gray65") +
geom_text(colour="tomato", alpha=0.8, size=4) +
ggtitle("PCA plot of USA States - Crime Rates")

dev.off()