import io
from difflib import SequenceMatcher

def ImportHistoricalFile(sPath,sRefMonth):
    print (sPath)
    class LineToAnalyze:
        sTM1Line = ''
        sSAPLine = ''
        sLineType = ''
        sMonth = ''
    arAnalyzedRelations = []
    arToAnalyzeSAPValues = []
    bTitle = True
    with io.open(sPath, 'r') as HistFile:
        print HistFile
        sData = HistFile.readlines()
        for eachLine in sData:
            if bTitle == False:
                objLineToAnalyze = LineToAnalyze()
                arEachLine = eachLine.split(',')
                if len(arEachLine) > 0:
                    sFileMonth = arEachLine[0][1:5].strip().replace('"','')
                    sSAPValue = arEachLine[0][6:].strip().replace('"','')
                    sTM1Value = arEachLine[1].strip().replace('"', '')
                    if sFileMonth == unicode(sRefMonth) and sTM1Value == '':
                        #Esta linha nao deve ter relacionamento
                        #Incluir em um Vetor para fazer o relacionamento depois;
                        objLineToAnalyze.sSAPLine = sSAPValue
                        objLineToAnalyze.sTM1Line = sTM1Value
                        objLineToAnalyze.sMonth = sFileMonth
                        objLineToAnalyze.sLineType = 'TO_ANALYZE'
                        arToAnalyzeSAPValues.append(objLineToAnalyze)
                    else:
                        if sFileMonth == unicode(sRefMonth) and sTM1Value <> '':
                            print 'Teste'
                        #Linha ja possui um relacionamento revisado;
                        objLineToAnalyze.sMonth = sFileMonth
                        objLineToAnalyze.sSAPLine = sSAPValue
                        objLineToAnalyze.sTM1Line = sTM1Value
                        objLineToAnalyze.sLineType = 'ANALYZED'
                        arAnalyzedRelations.append(objLineToAnalyze)
            else:
                print 'Reading Title'
                bTitle = False

    HistFile.close()
    return arToAnalyzeSAPValues, arAnalyzedRelations

def SearchForDefinedRelationship(arToAnalyzeSAPValues, arAnalyzedRelations):

    arNewRelations = []
    arValuesWithoutMatch = []
    bMatchExists = False
    for eachToAnalyzeLine in arToAnalyzeSAPValues:
        sSAPValue = eachToAnalyzeLine.sSAPLine.strip()
        bMatchExists = False
        for eachAnalyzedRelations in arAnalyzedRelations:
            sSAPAnalyzedValue  = eachAnalyzedRelations.sSAPLine.strip()
            sCodPEPSAPValue = sSAPValue.split('-')[0].strip()
            sCodSAPAnalyzedValue = sSAPAnalyzedValue.split('-')[0].strip()
            if sCodPEPSAPValue == sCodSAPAnalyzedValue:
                if SequenceMatcher(None, sSAPValue, sSAPAnalyzedValue).ratio() > 0.90:
                    bMatchExists = True
                #if sSAPValue == sSAPAnalyzedValue:
                    #Relacao ja realizada anteriormente.
                    eachToAnalyzeLine.sTM1Line = eachAnalyzedRelations.sTM1Line
                    eachToAnalyzeLine.sLineType = 'ANALYZED'
                    arNewRelations.append(eachToAnalyzeLine)
                    print (sSAPValue + '---' + sSAPAnalyzedValue)
                    break
        if not bMatchExists:
            arValuesWithoutMatch.append(eachToAnalyzeLine)
    return arNewRelations, arValuesWithoutMatch

