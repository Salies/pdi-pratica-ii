parBoxCox = 0.15;
data = imread('bebe.bmp');
dataTrans = (1+(abs(dct2(rgb2gray(data))))).^parBoxCox;
dataTrans = floor(dataTrans*255/max(dataTrans(:)));
imagesc(dataTrans);colormap gray