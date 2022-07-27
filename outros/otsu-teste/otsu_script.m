% FCT-UNESP -- Processamento Digital de Imagens -- 2022
% Daniel Henrique Serezane Pereira
% rodar na pasta onde está o script
I = imread("imagem-ref.jpg");
level = graythresh(I);
BW = imbinarize(I, level);
imwrite(BW, 'bin_matlab.png', 'png');