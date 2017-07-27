clean_textlibrary(RTextTools)
library(tm)
library(SparseM)
library(SnowballC)
library(topicmodels)


clean_data <- function(str_data)
{
  str_data = gsub("[^\x20-\x7e]"," ", str_data)
  str_data = gsub("(@|http)[^[:blank:]]*|[[:punct:]]|[[:digit:]]"," ", str_data)
  str_data = gsub("\\s+", " ", str_data)
  str_data = tolower(str_data)
  return(str_data)
}

library(openxlsx)
df <- read.xlsx(PATH_TO_FILE)
text <- df$Content
clean_text<-clean_data(text)
print(length(clean_text))

extended_stopwords<-c(TYPE YOUR STOP WORDS HERE)
myStopwords = c(stopwords(kind="en"), extended_stopwords)
for (i in 1:length(clean_text)) { clean_text[i] = gsub(',','',toString(wordStem(scan_tokenizer(removeWords(clean_text[i],words=myStopwords)))), ignore.case = TRUE )}
print(length(clean_text))

corp<-Corpus(VectorSource(mmr_clean_text))
dtm<-DocumentTermMatrix(corp)
dtm<-removeSparseTerms(dtm,0.995)
dtm = dtm[rowSums(as.matrix(dtm))>0,]
lda.model = LDA(dtm, k=3, method='Gibbs', control=list(seed=2015, burnin=500, iter=2500));
topic_matrix = terms(lda.model, 20)


gammaDF<-as.data.frame(lda.model@gamma)

colnames(gammaDF) <- c("Topic 1", "Topic 2", "Topic 3")

n = nrow(gammaDF)
print(n)
res<-colSums(gammaDF)/n

print(res)

topic_matrix<-rbind(topic_matrix, 21)
topic_matrix[21,]<-res

# write.csv(topic_matrix, file = PATH_TO_DEST_FILE)
