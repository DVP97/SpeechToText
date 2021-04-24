def procesarTxt(string):
    
    # posible mejora: nltk para stematizar palabras de string
    
    # variables
    stopwords = [["bajo marcha","GD"],["punto muerto","GD"],["bajo primera","GD"],["bajo segunda","GD"],["bajo tercera","GD"],["bajo cuarta","GD"],["bajo quinta","GD"],["subo marcha","GU"],["subo primera","GU"],["subo segunda","GU"],["subo tercera","GU"],["subo cuarta","GU"],["subo quinta","GU"],["subo sexta","GU"],["intermitente izquierdo","LB"],["intermitente derecho","RB"],["embrague","G"],["acelero","T"],["freno","B"],]
    new_text = []

    split = string.split()
    maxNum = len(split)

    #iteramos en busca de coincidencias de palabras, en caso de encontrar insertamos el código
    pos = 0
    buffer = 0
    buffer_word = ""

    for element in split:  # para cada uno de los elementos del string de entrada
        new_text.append(element)
        if buffer == 1:
            new_text.append("<"+buffer_word+">")
            buffer = 0

        for stop in stopwords:
            pal_Buscar = stop[0].split() #separamos las palabras para poder comparar todo el código entero
            len_pal_Buscar = len(pal_Buscar)
            pos_Actual = 0

            if element == pal_Buscar[pos_Actual]: 
                #ha encontrado la primera coincidencia
                if len_pal_Buscar>1 and pos+1<maxNum: #si tiene mas de una palabra el stopword y queda más texto por analizar entra
                    if split[pos+1] == pal_Buscar[pos_Actual+1]:
                        buffer = buffer + 1
                        buffer_word = stop[1]
                else:
                    new_text.append("<"+stop[1]+">")

        pos = pos + 1
        
    #volvemos a juntar la lista para tener un solo string
    reJoin = " ".join(new_text)
    print(reJoin)
    return reJoin