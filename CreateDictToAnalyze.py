
# MONTAR LISTA UNICA DE PALAVRAS POR PEP TM1 PARA MELHORAR O DICIONARIO

def SepareteTM1Dict(arTM1Info):

    arUNIQUE_TM1PEPs = CreateTM1Set_UniqueValues(arTM1Info)
    arTotalWords_x_UNIQUE_PEP = RetriaveWords_TM1PEPs(arTM1Info,arUNIQUE_TM1PEPs)

    return arTotalWords_x_UNIQUE_PEP

def CreateTM1Set_UniqueValues(arTM1Info):

    arTM1PEPs = []

    for eachTM1Info in arTM1Info:
        sTM1PEPCompleta = eachTM1Info.PEP.strip().upper()

        sTM1PEP = sTM1PEPCompleta.split('.')[0].strip().upper()
        arTM1PEPs.append(sTM1PEP)

    arUniqueSET_TM1_PEP = set(arTM1PEPs)

    return arUniqueSET_TM1_PEP

def RetriaveWords_TM1PEPs(arTM1Info,arUNIQUE_TM1PEPs):

    class WORDS_PEP:
        sUNIQUE_TM1PEP = ''
        arWORDS = []
    arTOTAL_TM1_PEPs = []
    for eachUniquePEP in arUNIQUE_TM1PEPs:
        #Para cada PEP unica, percorrer todas as informacoes TM1 e juntar as palavras unicas
        sUNIQUE_PEP = eachUniquePEP
        # if sUNIQUE_PEP == 'PB1353':
        #      print 'Teste'
        arResultSet = []
        arCurrentDescriptionWords = []
        objWORDS = WORDS_PEP()
        iContCalculatedPEPs = 0
        for eachTM1GlobalInfo in arTM1Info:
            sGlobalPEP = eachTM1GlobalInfo.PEP.split('.')[0].strip().upper()
            sGlobalDescription = eachTM1GlobalInfo.Descricao.upper()
            try:
                if sUNIQUE_PEP == sGlobalPEP:
                    arCurrentDescriptionWords = sGlobalDescription.split(' ')
                    for eachCurrentWord in arCurrentDescriptionWords:
                        if (eachCurrentWord.strip().upper() <> '-') or (len(eachCurrentWord) > 1) or (sUNIQUE_PEP.upper() not in eachCurrentWord):
                            arResultSet.append(eachCurrentWord.strip().upper())
                    iContCalculatedPEPs = iContCalculatedPEPs +1
            except:
                print 'Erro!!'
        print 'Numero de PEPs Encontradas {} para a PEP {}'.format(iContCalculatedPEPs,sUNIQUE_PEP.upper())
        if len(arResultSet) > 0:
            objWORDS.arWORDS = set(arResultSet)
            objWORDS.sUNIQUE_TM1PEP = sUNIQUE_PEP.upper()
            arTOTAL_TM1_PEPs.append(objWORDS)

    return  arTOTAL_TM1_PEPs


# MONTAR LISTA UNICA DE PALAVRAS POR PEP SAP PARA MELHORAR O DICIONARIO

def SepareteSAPDict(arSAPInfo):

    arUNIQUE_SAPPEPs = CreateSAPSet_UniqueValues(arSAPInfo)
    arTotalWords_x_UNIQUE_PEP = RetriaveWords_SAPPEPs(arSAPInfo,arUNIQUE_SAPPEPs)

    return arTotalWords_x_UNIQUE_PEP

def CreateSAPSet_UniqueValues(arSAPInfo):

    arSAPPEPs = []

    for eachSAPInfo in arSAPInfo:
        sSAPPEPCompleta = eachSAPInfo.Descricao

        sSAPPEP = sSAPPEPCompleta.split('.')[0].strip()
        arSAPPEPs.append(sSAPPEP)

    arUniqueSET_SAP_PEP = set(arSAPPEPs)

    return arUniqueSET_SAP_PEP

def RetriaveWords_SAPPEPs(arSAPInfo,arUNIQUE_SAPPEPs):

    class WORDS_PEP:
        sUNIQUE_SAP_PEP = ''
        arWORDS = []
    arTOTAL_SAP_PEPs = []
    for eachUniquePEP in arUNIQUE_SAPPEPs:
        #Para cada PEP unica, percorrer todas as informacoes TM1 e juntar as palavras unicas
        sUNIQUE_PEP = eachUniquePEP
        # if sUNIQUE_PEP == 'PB1353':
        #      print 'Teste'
        arResultSet = []
        arCurrentDescriptionWords = []
        objWORDS = WORDS_PEP()
        iContCalculatedPEPs = 0
        for eachSAPGlobalInfo in arSAPInfo:
            sGlobalPEP = eachSAPGlobalInfo.Descricao.split('-')[0].strip().split('.')[0].strip()
            sGlobalDescription = eachSAPGlobalInfo.Descricao
            try:
                if sUNIQUE_PEP == sGlobalPEP:
                    arCurrentDescriptionWords = sGlobalDescription.split(' ')
                    for eachCurrentWord in arCurrentDescriptionWords:
                        if (eachCurrentWord.strip() <> '-') and (len(eachCurrentWord) > 1) and (sUNIQUE_PEP not in eachCurrentWord):
                            arResultSet.append(eachCurrentWord.strip())
                    iContCalculatedPEPs = iContCalculatedPEPs +1
            except:
                print 'Erro!!'
        print 'Numero de PEPs Encontradas {} para a PEP {}'.format(iContCalculatedPEPs,sUNIQUE_PEP)
        if len(arResultSet) > 0:
            objWORDS.arWORDS = set(arResultSet)
            objWORDS.sUNIQUE_SAP_PEP = sUNIQUE_PEP
            arTOTAL_SAP_PEPs.append(objWORDS)

    return  arTOTAL_SAP_PEPs
