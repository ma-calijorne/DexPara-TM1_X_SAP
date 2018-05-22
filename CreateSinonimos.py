import csv


def CreateSynonyms(arTM1Info):

    # 1 - Recuperar as informacoes do Dicionario Comum
    class CInfo:
        value = ''
        synonym = ''
    arCommonFile = []
    with open('Dados/SourceDict_CommonInfo.csv', 'rb') as csvfile:
        CommonInfo = csv.reader(csvfile, delimiter=',', quotechar='"')
        bTitle = True
        for eachRow in CommonInfo:
            if bTitle == True:
                bTitle = False
            else:
                CIObj = CInfo()
                CIObj.value = eachRow[0].replace('"','').decode("cp1252").upper()
                CIObj.synonym = eachRow[1].replace('"','').decode("cp1252").upper()
                arCommonFile.append(CIObj)

    csvfile.close()

    mountSynonymFile(arTM1Info,arCommonFile)

def mountSynonymFile (arTM1Info,arCommonFile):

    arAllSynonyms = []
    sCabecalhoJSON = '{\n' + '  "entity_synonyms": [\n'

    for eachCommonFile in arCommonFile:
        sValue = '      {\n "value": "' + eachCommonFile.value.strip().encode('cp1252') + '",'
        sSynonymsHead = '       \n"synonyms":['
        arSynonymsItems = eachCommonFile.synonym.split(';')
        iIndex = 1
        sFinalComma = ','
        for eachSynonymItem in arSynonymsItems:
            if iIndex == len(arSynonymsItems):
                    sFinalComma = ''
            sSynonymsItems = '"{}{}{}'.format(eachSynonymItem.strip().encode('cp1252'),'"',sFinalComma)
            iIndex = iIndex + 1
        sSynonymsFooter = ']\n}'
        sFinalItem = sValue + sSynonymsHead + sSynonymsItems + sSynonymsFooter
        arAllSynonyms.append(sFinalItem)

    for eachTM1Item in arTM1Info:
        sValue = '      {\n "value": "' + eachTM1Item.PEP.strip().encode('cp1252') + '",'
        sSynonymsHead = '       \n"synonyms":["{}{}'.format(eachTM1Item.Fornecedor.replace('"','').strip().encode('cp1252'),'"]\n}')
        sFinalItem = sValue + sSynonymsHead
        arAllSynonyms.append(sFinalItem)

    iIndexAllSynonyms = 0
    iIndexTotalSynonyms = len(arAllSynonyms)

    sAllSynonyms = ''

    for eachSynonymItem in arAllSynonyms:
        if iIndexAllSynonyms <> (iIndexTotalSynonyms - 1):
            sAllSynonyms = sAllSynonyms + eachSynonymItem.decode('cp1252') + ',\n'
        else:
            sAllSynonyms = sAllSynonyms + eachSynonymItem.decode('cp1252')
        iIndexAllSynonyms = iIndexAllSynonyms + 1

    sSynonymsToSave = sCabecalhoJSON + sAllSynonyms + ']\n}'

    with open('Dados/Sinonimos.json', 'w') as JSONfile:
        JSONfile.write(sSynonymsToSave.encode('cp1252'))
        JSONfile.close()