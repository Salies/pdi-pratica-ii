''' 
Este programa é parte dos trabalhos práticos do segundo bimestre 
da disciplina de Processamento Digital de Imagens,
ministrada na FCT-UNESP em 2022.

Autores:
Carlos Eduardo Fernandes de Santana
Daniel Henrique Serezane Pereira

///

Aula 11
Trabalho Prático
Implementar o afinamento de objetos, para a obtenção de Esqueletos de imagens binárias usando o algoritmo de Zhang e Suen. 
Usar a imagem teste.bmp para demonstrar observe que esta imagem tem objeto branco e fundo preto.
O algoritmo deve ser aplicado apenas nos pontos de borda, entretanto, pode ser aplicado em todos os pontos  da imagem, gerando um processamento maior 
o resultado obtido com este algoritmo será comparado com o resultado obtido pela operação de erosão, visto na próxima aula
'''

from numba import njit

@njit
def vizinhos(i, j, img):
    return [
            img[i - 1, j], # p[2] -- 0
            img[i - 1, j + 1], # p[3] -- 1
            img[i, j + 1], # p[4] -- 2
            img[i + 1, j + 1], # p[5] -- 3
            img[i + 1, j], # p[6] -- 4
            img[i + 1, j - 1], # p[7] -- 5
            img[i, j - 1], # p[8] -- 6
            img[i - 1, j - 1] # p[9] -- 7
    ]

@njit
def S(p):
    p.append(p[0]) # coloca o p2 no final
    s = 0
    for k in range(len(p) - 1):
        if (p[k], p[k + 1]) == (False, True):
            s += 1
    return s

# loop do zhang_suen -- para reutlizar código
@njit
def zs_loop(out, idx):
    mar = []
    # Ignora pixels na borda da imagem
    for i in range(1, out.shape[0] - 1):
        for j in range(1, out.shape[1] - 1):
            if(out[i, j] == False): # pixels pretos não podem ser de borda
                continue
            p = vizinhos(i, j, out)
            if(sum(p) == 8): # se tem 8 vizinhos brancos não é pixel de borda
                continue
            # Se batarem as condições, marcar para eliminação
            if ((2 <= sum(p) <= 6) and (S(p) == 1) and (p[idx[0]] * p[idx[1]] * p[idx[2]] == 0) and (p[idx[3]] * p[idx[4]] * p[idx[5]] == 0)):
                # Marca para eliminar -- por que não elimina de uma vez? Porque senão buga a "busca" por pixels de borda.
                mar.append((i, j))
    # Elimina os pixels
    for i, j in mar:
        out[i, j] = False
    return len(mar), out

@njit
def zhang_suen(img):
    out = img.copy()
    # qtd. de pixels marcados para remoção, passo 1 (p1) e passo 2 (p2)
    # não há do while em Python, por isso o valor inicial, a ser redefinido
    mar_p1 = 1
    mar_p2 = 1
    # loopa enquanto houverem pixels marcados em cada um dos passos
    while mar_p1 != 0 or mar_p2 != 0:
        # Passo 1
        # O segundo parâmetro são os índices dos vizinhos que o passo tem que pegar
        # É uma otimização simples, visto que é só isso que muda entre os passos do algoritmo (Zhang-Suen)
        mar_p1, out = zs_loop(out, [0, 2, 4, 2, 4, 6])
        # Passo 2 -- mesma coisa, só mudam os vizinhos das condições c) e d)
        mar_p2, out = zs_loop(out, [0, 2, 6, 0, 4, 6])
    return out