# lqxshane

rm(list = ls())
library(jiebaR) # chinese word segmentation
library(SnowballC)
library(tm)


# First load dataframes containing your target text


Sys.setlocale("LC_ALL","zh_CN.utf-8") # set sys language, need to reset at the end
rm(content, res, res_by_col, seg)
content <- df$Contents
content <- gsub("\n"," ", content)

## SKIP THIS IF YOU'RE NOT DEALING WITH CHINESE
seg <- worker(stop_word = "../../code/stop_words.txt", bylines = TRUE) # provide your own stop words here
res <- segment(content, seg)
res_by_col <- sapply(res, function(x){ paste(x, collapse = " ")})


myCorpus<-Corpus(VectorSource(res_by_col))
myCorpus<-tm_map(myCorpus, stripWhitespace)
# myCorpus<-tm_map(myCorpus, removePunctuation)
myCorpus<-tm_map(myCorpus, removeNumbers)
myCorpus[[209]]$content


#######################################
# load exact match dictionary

library(openxlsx)
myKeyword_exact <- read.xlsx("exact_dict.xlsx")



options(mc.cores=1) # must be 1 core or it fails
exact_df <- function(corpus, keywordExact) {
  checker_df <- data.frame()
  for (i in 1:ncol(keywordExact)){
    if (i %% 10000 == 0){print(i)}
    myDTM <- DocumentTermMatrix(corpus, control=list(wordLengths=c(1,Inf), dictionary = keywordExact[,i]))
    myTM <- as.matrix(myDTM)
    checker <- rowSums(myTM)
    # checker <- checker >0 # logical
    if (nrow(checker_df)==0) {
      checker_df <- data.frame(checker)
    } else {
      checker_df <- cbind(checker_df, checker)
    }
  }
  colnames(checker_df) <- colnames(myKeyword_exact)
  return(checker_df)
}

#################################################
exact_labels <- exact_df(myCorpus, myKeyword_exact)
output <- cbind(content, exact_labels)

# Out put subtopics in batch
for (i in 2:ncol(output)) {
  str <- colnames(output)[i]
  # sub <- head(output[output[,i] > 0,], 50)
  sub <- output[output[, i] > 0,]
  keep <- c("content", str)
  sub <- sub[keep]
  sub <- sub[order(- sub[, i]), ]
  filename <- paste("res/res_exact_", str, ".xlsx", sep = "")
  write.xlsx(sub, file = filename)
}

##################################

Sys.setenv(LANG = "en_US.UTF-8")
Sys.getlocale()
