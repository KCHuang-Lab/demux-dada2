install.packages("conflicted", repos='https://cloud.r-project.org') #repos='http://cran.us.r-project.org'
install.packages("tidyverse", repos='https://cloud.r-project.org')
if (!require("BiocManager", quietly = TRUE))
  install.packages("BiocManager", repos='https://cloud.r-project.org')
BiocManager::install("dada2", version="3.16",ask=FALSE)
BiocManager::install("phyloseq",version="3.16",ask=FALSE)
install.packages("cowplot", repos='https://cloud.r-project.org')
install.packages("foreach", repos='https://cloud.r-project.org')

