rm(list=ls())
library(openxlsx)
tweets <- read.xlsx(YOUR_PATH_TO_FILE)
content<-tweets$Tweet


library(RTextTools)
library(tm)
library(SparseM)
library(SnowballC)
# library(topicmodels)

combine_tweet <- function(str_data, n) #by timeline
{
docs = c()
start_idx = 1
while (start_idx<=length(str_data))
{

  if (start_idx + n-1 >= length(str_data))
  {
  docs = c(docs, paste(str_data[start_idx:length(str_data)], collapse = " "))
  }

  docs = c(docs, paste(str_data[start_idx:(start_idx+n-1)], collapse = " "))
  start_idx = start_idx + n

}
print(start_idx)
return(docs)
}




clean_data <- function(str_data)
{
  str_data = gsub("[^\x20-\x7e]"," ", str_data)
  str_data = gsub("(@|http)[^[:blank:]]*|[[:punct:]]|[[:digit:]]"," ", str_data)
  str_data = gsub("\\s+", " ", str_data)
  str_data = tolower(str_data)
  return(str_data)
}




#####################  MAIN   #######################

combined_text<-combine_tweet(content,4)
tail(combined_text)
tail(content)
combined_text <- combined_text[1:8906]


clean_text<-clean_data(combined_text)
print(length(clean_text))
myStopwords = c(stopwords(kind="en"))
# doc = vector(mode = 'character', length = 309)
for (i in 1:length(clean_text)) { clean_text[i] = gsub(',','',toString(wordStem(scan_tokenizer(removeWords(clean_text[i],words=myStopwords)))), ignore.case = TRUE )}
print(length(clean_text))



write.xlsx(clean_text, "pre/trump.xlsx", row.names = F)


#######################################################
