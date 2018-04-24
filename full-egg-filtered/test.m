I = imread('egg_model.jpg');
I = imcrop(I);
I1 = I(:,:,1);
I2 = I(:,:,2);
I3 = I(:,:,3);