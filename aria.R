# Script to generate nutrient analysis tables in SMC database

# Generates two nutrient datasets comparing TN and TP results: one where ND results replaced with 0, another where ND results replaced with 1/2MDL
# 'analysis_chem_nutrients_0'
# 'analysis_chem_nutrients_1/2MDL'

# Written by Annie Holt
# last updated: 9/23/2021

#### Nutrient SMC Data Import ####

# Load dependencies.Connect to SMC database using login (in-house use only).


# required packages
library(DBI)
library(dplyr)
library(RPostgreSQL)
library(CSCI)
library(readxl)

# Create connection to the database
print('Connecting to the database')

print('Created database connection')


bugs <- read_excel('test_taxonomy.xlsx', sheet = 2) 

# You need to create the sampleid column
# You need to make SampleID column. sampleid is in this format stationcode_MMDDYYYY_CollectionMethodCode_Replicate 
# (example: 105PS0129_08112010_BMI_RWB_1)
# bugs <- bugs %>% mutate(sampleid='')

bugs <- bugs %>%
  select(c('stationcode','fieldsampleid','finalid','baresult','lifestagecode','distinctcode')) %>%
  rename(
    `StationCode` = stationcode,
    `SampleID` = sampleid,
    `FinalID` = finalid,
    `BAResult` = baresult,
    `LifeStageCode` = lifestagecode,
    `Distinct` = distinct
  )

gis <- dbGetQuery(con, 'SELECT * FROM vw_csci_gispredictors') %>% filter(StationCode %in% bugs$stationcode)

bugs <- bugs %>% mutate(BAResult = as.numeric(BAResult)) # this can be altered in the view definition
bugs <- cleanData(bugs)

metadata <- BMIMetrics::loadMetaData()

namecheck <- paste(bugs$FinalID, bugs$LifeStageCode) %in% paste(metadata$FinalID, metadata$LifeStageCode)
missing <- which(!namecheck)
if(length(missing)>0){
  casenamecheck <- paste(toupper(bugs$FinalID[missing]), bugs$LifeStageCode[missing]) %in% paste(toupper(metadata$FinalID), metadata$LifeStageCode)
  bugs$FinalID[missing][casenamecheck] <- 
    as.character(metadata$FinalID[match(toupper(bugs$FinalID[missing][casenamecheck]), toupper(metadata$FinalID))])
  if(length(namecheck) != (sum(namecheck) + sum(casenamecheck)))
    warning(c("The following FinalID/LifeStageCode combinations did not match with the internal database:",
              paste(unique(paste(bugs$FinalID[!namecheck], bugs$LifeStageCode[!namecheck])), collapse=", ")))
}
notfound <- bugs %>% filter(!namecheck)
bugs <- bugs %>% filter(namecheck)


result <- CSCI(bugs, gis )




