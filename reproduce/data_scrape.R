#  =============================================================================
#  TCGA-Assembler version 2
#
#  Copyright (C) <2017>  <Yitan Zhu>
#  This file is part of TCGA-Assembler.
#
#  TCGA-Assembler is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  TCGA-Assembler is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with TCGA-Assembler.  If not, see <http://www.gnu.org/licenses/>.
#  =============================================================================


#' =============================================================================
#' Quick Start Examples of TCGA-Assembler Version 2
#' =============================================================================

#' Load functions
source("Module_A.R")
source("Module_B.R")

#' set data saving path
sPath1 <- "./QuickStartExample/ESCA/Part1_DownloadedData"
sPath2 <- "./QuickStartExample/ESCA/Part2_BasicDataProcessingResult"
sPath3 <- "./QuickStartExample/ESCA/Part3_AdvancedDataProcessingResult"

#' choose a cancer type
sCancer <- "ESCA"

#' choose some patients
# vPatientID <- c("TCGA-A7-A13F", "TCGA-AO-A12B")
vPatientID = NULL

#' =============================================================================
#' Part 1: Downloading Data of 7 different platforms using Module A functions
#' =============================================================================
#' Download somatic mutation data
path_somaticMutation <-
	DownloadSomaticMutationData(cancerType = sCancer,
															assayPlatform = "somaticMutation_DNAseq",
															inputPatientIDs = vPatientID,
															saveFolderName = sPath1)

#' Download copy number alternation data
# path_copyNumber <-
# 	DownloadCNAData(cancerType = sCancer,
# 									assayPlatform = "cna_cnv.hg19",
# 									inputPatientIDs = vPatientID,
# 									saveFolderName = sPath1)
#' Download DNA methylation 450 data
path_methylation_450 <-
	DownloadMethylationData(cancerType = sCancer,
													assayPlatform = "methylation_450",
													inputPatientIDs = vPatientID,
													saveFolderName = sPath1)

#' Download miRNA	expression data
path_miRNAExp <-
	DownloadmiRNASeqData(cancerType = sCancer,
											 assayPlatform = "mir_HiSeq.hg19.mirbase20",
											 inputPatientIDs = vPatientID,
											 saveFolderName = sPath1)

#' Download gene expression data
path_geneExp <-
	DownloadRNASeqData(cancerType = sCancer,
										 assayPlatform = "gene.normalized_RNAseq",
										 inputPatientIDs = vPatientID,
										 saveFolderName = sPath1)


#' Process somatic mutation data
list_somaticMutation <-
	ProcessSomaticMutationData(inputFilePath = path_somaticMutation[1],
														 outputFileName = paste(sCancer,
																										"somaticMutation",
																										sep = "__"),
														 outputFileFolder = sPath2)

#' Process copy number alternation data
#' calculate an average copy number for each gene in each sample
# list_copyNumber <-
# 	ProcessCNAData(inputFilePath = path_copyNumber[1],
# 								 outputFileName = paste(sCancer,
# 																				"copyNumber",
# 																				sep = "__"),
# 								 refGenomeFile = "./SupportingFiles/Hg19GenePosition.txt",
# 								 outputFileFolder = sPath2)

#' Process DNA methylation 450 data
list_methylation_450 <-
	ProcessMethylation450Data(inputFilePath = path_methylation_450[1],
														outputFileName = paste(sCancer,
																									 "methylation_450",
																									 sep = "__"),

														outputFileFolder = sPath2)

#' Process miRNA expression data
list_miRNAExp <-
	ProcessmiRNASeqData(inputFilePath = path_miRNAExp[1],
											outputFileName = paste(sCancer,
																						 "miRNAExp",
																						 sep = "__"),
											outputFileFolder = sPath2)

#' Process gene expression data
list_geneExp <-
	ProcessRNASeqData(inputFilePath = path_geneExp[1],
										outputFileName = paste(sCancer,
																					 "geneExp",
																					 sep = "__"),
										dataType = "geneExp",
										outputFileFolder = sPath2)

list_methylation_450_TSS <-
	CalculateSingleValueMethylationData(input = list_methylation_450,
																			regionOption = c("TSS200", "TSS1500"),
																			DHSOption = "Both",
																			outputFileName = paste(sCancer,
																														 "methylation_450",
																														 sep = "__"),
																			outputFileFolder = sPath3)

# l_methylation     <- list(Des  = list_methylation_450_TSS$Des,
# 													Data = list_methylation_450_TSS$Data,
# 													dataType = "methylation")
                                                                         
# l_miRNAExp        <- list(Des  = list_miRNAExp$Des,
# 													Data = list_miRNAExp$Data,
# 													dataType = "miRNAExp")
# inputDataList      <- vector("list", 2)
# inputDataList[[1]] <- l_methylation
# inputDataList[[2]] <- l_miRNAExp
# print("step 3")
# list_CombinedData <- CombineMultiPlatformData(inputDataList = inputDataList)

# #' 4th step: Write the combined multiplatform data to a tab-delimited txt file
# print("step 4")
# write.table(cbind(list_CombinedData$Des, list_CombinedData$Data),
# 						file = paste(sPath3,
# 												 "CombinedMultiPlatformData.txt",
# 												 sep = "/"),
# 						quote = FALSE,
# 						sep = "\t",
# 						na = "",
# 						col.names = TRUE,
# 						row.names = FALSE)
