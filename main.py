import ExtractFileInfo as EFI
import io
import AnalyzeAndMatch as AAM
import CreateDictToAnalyze as CDA
import CreateSinonimos as CRS
import AnalyzeHistorical_Match as AHM
import os

if os.path.exists('Dados/Results.txt'):
    os.remove('Dados/Results.txt')
if os.path.exists('Dados/TM1Dict.txt'):
    os.remove('Dados/TM1Dict.txt')
if os.path.exists('Dados/SAPDict.txt'):
    os.remove('Dados/SAPDict.txt')
if os.path.exists('Dados/Sinonimos.json'):
    os.remove('Dados/Sinonimos.json')
if os.path.exists('Dados/AssociacaoTM1_X_SAP.json'):
    os.remove('Dados/AssociacaoTM1_X_SAP.json')
if os.path.exists('Dados/Statistics.txt'):
    os.remove('Dados/Statistics.txt')

#Analizar arquivos consuntivos de relacao TM1 x SAP para relacionar o que ja foi revisado pela area.
arToAnalyzeSAPValues, arAnalyzedRelations = AHM.ImportHistoricalFile('Dados/CONSUNTIVO_TM1_X_SAP_JAN_FEV_2018.txt','Mar')
arNewRelations, arValuesWithoutMatch = AHM.SearchForDefinedRelationship(arToAnalyzeSAPValues,arAnalyzedRelations)

#Load TM1 and SAP Info from File exported from TM1 Planning. It is recomended to always update the CSV file
#before starts a new check.
arTM1Info = EFI.ExtractTM1Info()
arSAPInfo = EFI.ExtractSAPInfo(arValuesWithoutMatch)

#Create a new Dict JSON file with Info loaded in SourceDict_CommonInfo csv file and in the TM1 info (suppliers name)
CRS.CreateSynonyms(arTM1Info)
arTM1_TotalWords_x_UNIQUE_PEP = CDA.SepareteTM1Dict(arTM1Info)
arSAP_TotalWords_x_UNIQUE_PEP = CDA.SepareteSAPDict(arSAPInfo)
#
with io.open('Dados/TM1Dict.txt', 'wb') as TM1Dict:
     for eachTM1_PEP in arTM1_TotalWords_x_UNIQUE_PEP:
         sWord = ''
         for eachWord in eachTM1_PEP.arWORDS:
             if eachWord.strip() <> '-':
                 if sWord == '':
                     sWord = '[ {} '.format(eachWord.encode('utf8'))
                 else:
                     sWord = sWord + ', {}'.format(eachWord.encode('utf8'))
         sWord = sWord + ']'
         sUNIQUE_PEP =  eachTM1_PEP.sUNIQUE_TM1PEP.encode('utf8').replace('"','') + ' # '.encode('utf8') + sWord + '\n'
         TM1Dict.write(sUNIQUE_PEP)

     sUNIQUE_PEP = ''
     sWord = ''
     TM1Dict.close()
with io.open('Dados/SAPDict.txt', 'wb') as SAPDict:
     for eachSAP_PEP in arSAP_TotalWords_x_UNIQUE_PEP:
         sWord = ''
         for eachWord in eachSAP_PEP.arWORDS:
             if eachWord.strip() <> '-':
                 if sWord == '':
                     sWord = '[ {} '.format(eachWord.encode('utf8'))
                 else:
                     sWord = sWord + ', {}'.format(eachWord.encode('utf8'))
         sWord = sWord + ']'
         sUNIQUE_PEP = eachSAP_PEP.sUNIQUE_SAP_PEP.encode('utf8').replace('"','') + ' # '.encode('utf8') + sWord + '\n'
         SAPDict.write(sUNIQUE_PEP)

     sUNIQUE_PEP = ''
     sWord = ''
     SAPDict.close()

AAM.RunStatistics(arToAnalyzeSAPValues,arAnalyzedRelations,arNewRelations,arValuesWithoutMatch)
#Execute validation to find the best fit for each SAP x TM1 tupple. Only the ones that are not already related by a historical and manual analysis.
AAM.getSAPItem(arSAPInfo,arTM1Info)


with io.open('Dados/Results.txt', 'a', encoding="utf-8") as ResultFile:
    sLine = ''
    for eachNewRelationLine in arNewRelations:
        sLine = eachNewRelationLine.sTM1Line + ' |***| ' + eachNewRelationLine.sSAPLine + ' |***| ' + 'RELACAO HISTORICA EXISTENTE' + ' |***| ' + 'N/A\n'
        print sLine
        ResultFile.write(sLine)
        sLine = ''
    ResultFile.close()

with io.open('Dados/Results.txt', 'r', encoding="utf-8") as ResultFile:
    sLines = ResultFile.readlines()
    ResultFile.close()

with io.open('Dados/AssociacaoTM1_X_SAP.txt', 'w', encoding="utf-8") as FileToImport:
    for eachline in sLines:
        arValuesToSave = eachline.split('|***|')
        if arValuesToSave[0].strip() == 'NAO ENCONTROU MATCH':
            sTM1ValueToSave = ''
        else:
            sTM1ValueToSave = arValuesToSave[0].strip()
        sLineToSave = arValuesToSave[1] + ',' + sTM1ValueToSave + '\n'
        FileToImport.write(sLineToSave)
    FileToImport.close()
