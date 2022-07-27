I = imread("imagem-ref.jpg");
level = graythresh(I);
level2 = level * 255;
BW = imbinarize(I, level2 / 255);
%imshow(BW);
imwrite(BW, 'bin_matlab2.png', 'png');