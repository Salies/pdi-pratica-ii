A = imread("teste.bmp");
B = [0 1 0; 1 1 1; 0 1 0];
A2 = imdilate(A, B);
imwrite(A2, "2_m.png");
A3 = imerode(A, B);
imwrite(A3, "0_m.png")
