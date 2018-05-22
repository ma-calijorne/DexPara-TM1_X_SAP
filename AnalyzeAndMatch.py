#encoding = utf8
import json
import io

#Pegar 1 item SAP e achar seu correspondente no tm1---------------------------------------------------------------------

def getSAPItem(arSAPItems,arTM1Items):

    iContItemSAP = 1
    for eachSAPItem in arSAPItems:
        arEachSAPItem = eachSAPItem.Descricao.split('-')
        if len(arEachSAPItem) > 0:
            sCodPEP_SAP = arEachSAPItem[0].strip().split('.')[0].strip().upper().replace('"','')
            # if sCodPEP_SAP == 'PB1322':
            # IF APENAS PARA DEBUGAR DETERMINADAS PEPs
            #     print 'teste'
            Search_for_TM1_Item(sCodPEP_SAP,arTM1Items,eachSAPItem)
        print 'ID: {} : Item SAP Lido: {}'.format(iContItemSAP,arEachSAPItem)
        iContItemSAP = iContItemSAP + 1

def Search_for_TM1_Item(sCodPEP_SAP,arTM1Items,eachSAPItem):

    arTM1SubSetItems = []
    for eachTM1Item in arTM1Items:
        sCodPEP_TM1 = eachTM1Item.PEP.split('.')[0].strip().upper()
        # if sCodPEP_TM1 == 'PB1322':
        # IF APENAS PARA DEBUGAR DETERMINADAS PEPs
        #     print 'teste'
        if sCodPEP_SAP.strip().upper() == sCodPEP_TM1.strip().upper():
            arTM1SubSetItems.append(eachTM1Item)
            #itens com mesma PEP
    matchDescription(sCodPEP_SAP,eachSAPItem,arTM1SubSetItems)

def matchDescription(sCodPEP_SAP,eachSAPItem,arTM1Items):

    class ResulSet:
        sItemTM1 = ''
        sItemSAP = ''
        arResultMatch = []
        iTamanhoResultMatch = 0


    arResultSETMAP = []
    sSAPNormilizedDescription = ''
    for eachTM1Item in arTM1Items:
        arResultSet = []
        arTM1Words = ImproveTM1ListInformation(eachTM1Item)
        sSAPNormilizedDescription = normalizeSAPItem(eachSAPItem.Descricao)
        arSAPWords = sSAPNormilizedDescription.split(' ')
        arTM1Words, arSAPWords = normilizeWordVectors(sCodPEP_SAP,arSAPWords,arTM1Words)
        arCompare = set(arTM1Words) & set(arSAPWords)
        for eachChar in arCompare:
            if eachChar <> '-':
                arResultSet.append(eachChar)
        if len(arResultSet) > 0:
            objResultSet = ResulSet()
            objResultSet.sItemTM1 = eachTM1Item.Descricao.upper()
            objResultSet.sItemSAP = eachSAPItem.Descricao
            objResultSet.arResultMatch = arResultSet
            objResultSet.iTamanhoResultMatch = len(arResultSet)
            arResultSETMAP.append(objResultSet)
        else:
            objResultSet = ResulSet()
            objResultSet.sItemTM1 = 'NAO ENCONTROU MATCH'
            objResultSet.sItemSAP = eachSAPItem.Descricao
            objResultSet.arResultMatch = arResultSet
            objResultSet.iTamanhoResultMatch = len(arResultSet)
            arResultSETMAP.append(objResultSet)

    objBestFited = CheckBestFit(arResultSETMAP)
    if len(arResultSETMAP) > 0:
        SaveFile(objBestFited.sItemTM1, objBestFited.sItemSAP, objBestFited.arResultMatch)
    else:
        arNUll = []
        SaveFile('NAO EXISTE TM1', eachSAPItem.Descricao, arNUll)

def normalizeSAPItem(sSAPDescription):

    sSAPDescFinal = ''
    bPrimeiroPonto = True
    bPrimeiroTraco = True
    for eachChar in sSAPDescription:
        if eachChar == '.':
            if bPrimeiroPonto:
                sSAPDescFinal = sSAPDescFinal + eachChar
            else:
                sSAPDescFinal = sSAPDescFinal + ' '
            bPrimeiroPonto = False
        else:
            if eachChar == '-':
                if bPrimeiroTraco:
                    sSAPDescFinal = sSAPDescFinal + eachChar
                else:
                    sSAPDescFinal = sSAPDescFinal + ' '
                bPrimeiroTraco = False
            else:
                sSAPDescFinal = sSAPDescFinal + eachChar

    sSAPDescFinal = sSAPDescFinal.replace('__',' ').replace('_',' ').replace('(','').replace(')','')
    return sSAPDescFinal

def normilizeWordVectors(sCodPEP_SAP,arSAPWords,arTM1Words):

    arNewTM1Word = []
    arNewSAPWord = []

    for eachTM1Word in arTM1Words:
        if eachTM1Word <> '-':
            if sCodPEP_SAP not in eachTM1Word:
                arNewTM1Word.append(eachTM1Word.replace(')','').replace('(','').replace('__', ' ').replace('_',' ').upper())
    for eachSAPWord in arSAPWords:
        if eachSAPWord <> '-':
            if sCodPEP_SAP not in eachSAPWord:
                arNewSAPWord.append(eachSAPWord.replace(')','').replace('(','').replace('__', ' ').replace('_',' ').upper())
    return arNewTM1Word, arNewSAPWord

def ImproveTM1ListInformation(TM1Item):

    jsonSynonyms = json.loads(io.open('Dados/Sinonimos.json',encoding='cp1252').read())
    arTM1ItemWords = []
    arTM1ItemWords = TM1Item.Descricao.split(' ')

    sTM1Item = TM1Item.Descricao.upper()
    for eachSynonym in jsonSynonyms["entity_synonyms"]:
        if eachSynonym["value"].upper() in sTM1Item.upper():
            for eachNewSynonym in eachSynonym['synonyms']:
                arTM1ItemWords.append(eachNewSynonym.upper())

    return arTM1ItemWords

def SaveFile(sTM1Item,sSAPItem,arResultMatch):

    with io.open('Dados/Results.txt', 'a', encoding="utf-8") as File:
       try:
            sResultMatch = ''
            for eachResultMatch in arResultMatch:
                if (eachResultMatch.upper().strip() == '-') or (len(eachResultMatch) <= 1) or (
                        sSAPItem.upper()  in eachResultMatch.upper().strip()):
                    print 'Condicao de Exclusao'
                else:
                    if sResultMatch == '':
                        sResultMatch = '{' + sResultMatch.upper() + ',' + eachResultMatch.upper()
                    else:
                        sResultMatch = sResultMatch.upper() + eachResultMatch.upper()

            if sResultMatch == '':
                sResultMatch = '[]'
            else:
                sResultMatch = sResultMatch.upper() + '}'
            sMatchedValues = sTM1Item.upper().replace('"','') + ' |***| ' + sSAPItem.upper().replace('"','') + ' |***| ' + sResultMatch.upper().replace('"','') + ' |***| ' + str(len(arResultMatch)) + '\n'
            File.write(sMatchedValues)
       except:
            print "Teste"
    File.close()

def CheckBestFit(arResultSet):

    bInitial = True
    iValorMax = 0
    objBestFited = ''
    try:
        for eachResult in arResultSet:
            if bInitial:
                bInitial = False
                iValorMax = eachResult.iTamanhoResultMatch
                objBestFited = eachResult
            else:
                if eachResult.iTamanhoResultMatch > iValorMax:
                    iValorMax = eachResult.iTamanhoResultMatch
                    objBestFited = eachResult
        return objBestFited
    except:
        print 'teste'

def RunStatistics(arToAnalyzeSAPValues,arAnalyzedRelations,arNewRelations,arValuesWithoutMatch):

    with io.open('Dados/Statistics.txt', 'w', encoding="utf-8") as StatisticsFile:
        iValuesToAnalyze = len(arToAnalyzeSAPValues)
        iValuesAlreadyMatched_Historie = len(arAnalyzedRelations)
        iNewRelationsMade = len(arNewRelations)
        iValuesNotMatchedEvenWithTheHistoricalData = len(arNewRelations)
        StatisticsFile.write('Quantidade de Linhas a serem Analizadas: ' + unicode(iValuesToAnalyze) + '\n')
        StatisticsFile.write('Quantidade de Linhas Historicas: ' + unicode(iValuesAlreadyMatched_Historie) + '\n')
        StatisticsFile.write('Quantidade de Matches Realizados atraves de dados historicos: ' + unicode(iNewRelationsMade) + '\n')
        StatisticsFile.write('Quantidade de Linhas a serem tratadas atraves do processo de analise de palavras: ' + unicode(iValuesNotMatchedEvenWithTheHistoricalData) + '\n')
        StatisticsFile.close()