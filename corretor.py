import nltk
# no console: nltk.download('punkt')


LETRAS = 'abcdefghijklmnopqrstuvwxyzáâàãéêèíîìóôòõúûùüç'


class Corpus:

    def __init__(self, caminho: str):
        self.__caminho = caminho
        self.__texto = self.__ler_txt()
        self.__tokens = nltk.tokenize.word_tokenize(self.__texto)
        self.__vocabulario, self.__total_vocabulario, self.__palavras, self.__total_palavras = self.__separa_palavras()
        self.__frequencia_palavras = nltk.FreqDist(self.__palavras)

    @property
    def vocabulario(self):
        return self.__vocabulario

    @property
    def total_vocabulario(self):
        return self.__total_vocabulario

    @property
    def palavras(self):
        return self.__palavras

    @property
    def total_palavras(self):
        return self.__total_palavras

    @property
    def frequencia_palavras(self):
        return self.__frequencia_palavras

    def __ler_txt(self):
        with open(self.__caminho, 'r', encoding='utf8') as arquivo:
            texto = arquivo.read()
        return texto

    def __separa_palavras(self):
        palavras = [token.lower() for token in self.__tokens if token.isalpha()]
        palavras_sem_repeticao = list(set(palavras))
        return palavras_sem_repeticao, len(palavras_sem_repeticao), palavras, len(palavras)


class Corretor:

    def __init__(self, corpus: str):
        self.__corpus = Corpus(corpus)

    @property
    def corpus(self):
        return self.__corpus

    def verifica(self, palavra: str):
        palavra = palavra.lower()
        palavras_geradas = self.__gerador_de_palavras(palavra)
        palavra_correta = max(palavras_geradas, key=self.__probabilidade)
        return palavra_correta

    def avaliador(self, nome_arquivo: str):
        lista_palavras_teste = []
        arquivo = open(nome_arquivo, encoding='utf8')
        for linha in arquivo:
            correta, errada = linha.split()
            lista_palavras_teste.append((correta, errada))
        arquivo.close()

        qtd_acertos = 0
        qtd_desconhecidas = 0
        numero_palavras = len(lista_palavras_teste)
        for correta, errada in lista_palavras_teste:
            palavra_candidata = self.verifica(errada)
            if palavra_candidata == correta:
                qtd_acertos += 1
            qtd_desconhecidas += (correta not in self.corpus.vocabulario)

        taxa_acerto = qtd_acertos / numero_palavras
        taxa_desconhecidas = qtd_desconhecidas / numero_palavras
        print(f'Em um total de {numero_palavras} palavras:\n' +
              f'Taxa de palavras corrigidas em {taxa_acerto * 100:.2f}%\n' +
              f'Taxa de palavras desconhecidas em {taxa_desconhecidas * 100:.2f}%')

    def __probabilidade(self, palavra_gerada: str):
        return self.corpus.frequencia_palavras[palavra_gerada] / self.corpus.total_palavras

    def __insere_letras(self, fatias:list):
        novas_palavras = []
        for esquerda, direita in fatias:
            for letra in LETRAS:
                novas_palavras.append(esquerda + letra + direita)
        return novas_palavras

    def __deletando_caractere(self, fatias: list):
        novas_palavras = []
        for esquerda, direita in fatias:
            novas_palavras.append(esquerda + direita[1:])
        return novas_palavras

    def __substitui_letra(self, fatias: list):
        novas_palavras = []
        for esquerda, direita in fatias:
            for letra in LETRAS:
                novas_palavras.append(esquerda + letra + direita[1:])
        return novas_palavras

    def __inverte_letra(self, fatias: list):
        novas_palavras = []
        for esquerda, direita in fatias:
            if len(direita) > 1:
                novas_palavras.append(esquerda + direita[1] + direita[0] + direita[2:])
        return novas_palavras

    def __gerador_de_palavras(self, palavra: str):
        fatias = []
        for i in range(len(palavra) + 1):
            fatias.append((palavra[:i], palavra[i:]))
        palavras_geradas = self.__insere_letras(fatias)
        palavras_geradas += self.__deletando_caractere(fatias)
        palavras_geradas += self.__substitui_letra(fatias)
        palavras_geradas += self.__inverte_letra(fatias)
        return palavras_geradas


if __name__ == '__main__':
    corretor = Corretor(corpus='dados/artigos.txt')
    print(corretor.verifica('lóigica'), end='\n\n')
    corretor.avaliador('dados/palavras.txt')