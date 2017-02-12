rm(list=ls())
# mmr<-read.csv('../mmr_media_stage2.csv', header = TRUE, sep = ',', stringsAsFactors = FALSE)
mmr<-read.csv('../extract/res_stage2_split.csv', header = TRUE, sep = ',', stringsAsFactors = FALSE)

mmr_text<-mmr$Contents

library(RTextTools)
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

mmr_clean_text<-clean_data(mmr_text)
print(length(mmr_clean_text))

extended_stopwords<-c('gm', 'gmo' ,'mosquito','mosquitoes',
                      'genetically', 'modified',
                      'engineered' ,
                      'altered',
                      'transgenic',
                      'aedes', 'aegypti', 'ox',
                      'will', 'can','said','photo', 'thing', 'update','image', 'link', 'things', 'people','like','well','come','com','ten', 'million','tens', 'millions','done','cnn', 'minute', 'minutes','mins', 'ago', 'updated')
myStopwords = c(stopwords(kind="en"), extended_stopwords)
# doc = vector(mode = 'character', length = 309)
for (i in 1:length(mmr_clean_text)) { mmr_clean_text[i] = gsub(',','',toString(wordStem(scan_tokenizer(removeWords(mmr_clean_text[i],words=myStopwords)))), ignore.case = TRUE )}
print(length(mmr_clean_text))

corp<-Corpus(VectorSource(mmr_clean_text))
dtm<-DocumentTermMatrix(corp)
dtm<-removeSparseTerms(dtm,0.995)
dtm = dtm[rowSums(as.matrix(dtm))>0,]
lda.model = LDA(dtm, k=5, method='Gibbs', control=list(seed=2015, burnin=500, iter=2500));
topic_matrix = terms(lda.model, 20)
write.csv(topic_matrix, file = "topic_matrix_5_20_method3.csv")
