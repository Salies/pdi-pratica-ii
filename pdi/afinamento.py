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

from pdi.zhang_suen import zhang_suen
from PIL import Image
from numpy import array as nparray
    
# Abrindo como imagem binária
# na pillow:
#   False   :   pixel preto
#   True    :   pixel branco
im = Image.open("imagens/teste.bmp").convert('1')
Image.fromarray(zhang_suen(nparray(im))).show()