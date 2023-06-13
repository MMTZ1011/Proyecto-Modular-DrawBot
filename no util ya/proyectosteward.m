clear all
close all hidden
clc


%% variables
%{
poner primero webcamlist a ver cual está habilitada
después poner el número de la deseada en esta variable
%}
webcamlist
numero_de_camara = 2 ;
camara = webcam(numero_de_camara) ;


%configuracion
camara.ExposureMode = 'manual' ;
camara.Exposure= -7 ;
camara.Brightness = 190 ;
%fin configuración 



iteraciones = 100 ;
Pixel = 70/256 ;
hacer_roipoly = false ;


ploteo = false ; 
filtro = false ; 

resolucion_x = 1280 ;
resolucion_y = 720 ;
ratio = 4 ;

%% paracontrolador
if ploteo == true
    Kp = 0.05 ; %listo
    
    Kd = 0.05 ;
    Ki = 0.05 ;
else
    Kp = 0.025 ; %la proporcional
    
    Kd = 0.05 ; %la derivativa
    Ki = 0.0075 ;%0.015 ; %integral
end







%%

disp("Resolución:")
disp(camara.Resolution)



% preview(camara)
if hacer_roipoly == true 
    fotografia = snapshot(camara) ;

    imshow(fotografia) ;
    seleccion = roipoly ;

    img = im2double(fotografia) ;
    imshow(seleccion) ;


    seleccionR = img(:, :, 1).*seleccion ;
    seleccionG = img(:, :, 2).*seleccion ;
    seleccionB = img(:, :, 3).*seleccion ;

    R = sum(seleccionR(:)) / sum(seleccion(:)) ;
    G = sum(seleccionG(:)) / sum(seleccion(:)) ;
    B = sum(seleccionB(:)) / sum(seleccion(:)) ;

else

    %{
        R = 0.05 ;    
        G = 0.05 ;
        B = 0.05 ;
    %}
    R = 255/255 ;    
    G = 150/255 ;
    B = 0/255 ;
end
    
disp('en valores de uint8:')
disp(uint8(R*255))
disp(uint8(G*255))
disp(uint8(B*255))


% hace for



%a = arduino();

a = arduino('COM11', 'Uno', 'Libraries', 'Servo');


%para el motor de abajo
s1 = servo(a, 'D8') ;
% para el motor de arriba
s2 = servo(a, 'D4') ;

%% establece las posiciones iniciales

writePosition(s1, 0.5)
writePosition(s2, 0.3)


writeDigitalPin(a, 'D11',0) ;





%% centroimagen
centro_x = resolucion_x/8 ;
centro_y = resolucion_y/8 ;


preview(camara)

if ploteo == true
    figure()
end



m = resolucion_y/4 ;
n = resolucion_x/4 ;
c = 3 ;
% ruido
ruido = 0.2*rand(m, n, c); %Ruido
H = zeros(m,n);




Kp = 0.05 ; %la proporcional
    
Kd = 0.0015 ; %la derivativa
Ki = 0.01%0.0005 ;%0.015 ; %integral

previousTime = 0 ;
X_cumError = 0 ;
Y_cumError = 0 ;
X_lastError = 0 ;
Y_lastError = 0 ;
tic % marca el inicio para ir registrando cosas

save_error_X = zeros(iteraciones,1) ;
save_error_Y = zeros(iteraciones,1) ;




for idx = 1:iteraciones
    X = snapshot(camara) ;
    X = X(1 : ratio : end, 1 : ratio : end, :) ;
    X = im2double(X) ;
    
    if filtro ==true 
       X = X+ruido ;
       %Fouriel
       Xf=fftshift(fftn(X, [m n o]));
       
%     mesh(real(Xf));
%     imshow(real(Xf))
        %Filtro pasa bajas
        
        for im=1:m
            for in=1:n  %creamos circunferencia para filtrado
               if (im-a)^2 + (in-b)^2 < r^2
                   H(im,in,:)=1;
               end
            end
        end
        yf = Xf.*H;
        X = abs(ifftn(ifftshift(yf)));
    end
    
    CapaR = (X(:, :, 1) > (R-Pixel)) & (X(:,:, 1) < (R+Pixel)) ;
    CapaG = (X(:, :, 2) > (G-Pixel)) & (X(:,:, 2) < (G+Pixel)) ;
    CapaB = (X(:, :, 3) > (B-Pixel)) & (X(:,:, 3) < (B+Pixel)) ;
    
    BusqColor = CapaR.*CapaG.*CapaB ;

    [XColor, YColor] = find(BusqColor==1) ;
    
    CX = sum(XColor(:)) / sum(BusqColor(:)) ;
    CY = sum(YColor(:)) / sum(BusqColor(:)) ;
    
    if ploteo == true 
        imshow(BusqColor)
        hold on
        plot(CY, CX, '*r', 'LineWidth',10) ;%centroide
        plot(centro_x, centro_y, '*c', 'LineWidth',2) ; %centro global
        plot([centro_x, CY],[centro_y, CX], ':r', 'LineWidth',2)%linea de distancia
        title(idx)
    else
        disp(idx) 
    end
    %% PID tiempo
    currentTime = toc ;
    elapsedTime = currentTime - previousTime ;
       
    
    %% si no es 0
    if isnan(CX)==0 && isnan(CY) == 0
       % prende led
       writeDigitalPin(a, 'D11', 1);
       
        
       X_error = CY - centro_x ; %horizontal
       Y_error = CX - centro_y ; %vertical
       
       
       save_error_X(idx) = X_error ;
       save_error_Y(idx) = Y_error ;
       
       
       if ploteo == true 
           str = {'x_e:=', X_error,'y_e=', Y_error};
           text(0, 0, str, 'Color','black','FontSize',11,'BackgroundColor','yellow','VerticalAlignment','top') ;
       end
       
       %% controlador
       pos_x = readPosition(s1) ;
       pos_y = readPosition(s2) ;
       
       %% valores del tiempo para PID
        
        X_cumError = X_cumError+( X_error * elapsedTime) ;
        Y_cumError = Y_cumError+( Y_error * elapsedTime) ;
        
       X_rateError = (X_error - X_lastError)/elapsedTime ;
       Y_rateError = (Y_error - Y_lastError)/elapsedTime ;
        
       %% entradas de grados
       %entrada_X = -(X_error*Kp)/180 ; 
       %entrada_Y =  (Y_error*Kp)/180 ; 
       
       entrada_X = -(Kp*X_error  + Kd*X_rateError + Ki*X_cumError  )/180   ; 
       entrada_Y =  (Kp*Y_error + Kd*Y_rateError + Ki*Y_cumError )/180 ; 
       
       %% ve que no sea el mínimo
       if abs(entrada_X) < 0.0056 % 1/180 osea un grado
           entrada_X = sign(entrada_X)*0.0056 ; % obtenemos el signo y el 0.005 según fue el caso
       end
       if abs(entrada_Y) < 0.0056 % 1/180 osea un grado
           entrada_Y = sign(entrada_Y) *0.0056 ; % obtenemos el signo y el 0.005 según fue el caso
       end
       
       %% calculo write de step motor
       nueva_pos_x = pos_x+entrada_X ;
       if nueva_pos_x <0.05 %si es menor
           nueva_pos_x = 0.05 ;
       elseif nueva_pos_x > 1 
           nueva_pos_x = 1 ;
       end
       
       nueva_pos_y = pos_y+entrada_Y ;
       if nueva_pos_y <0.05 %si es menor
           nueva_pos_y = 0.05 ;
       elseif nueva_pos_y > 1 
           nueva_pos_y = 1 ;
       end
              
       %% establecemos los servos
       writePosition(s1, nueva_pos_x) ;
       writePosition(s2, nueva_pos_y) ;  

         %% guarda datos para el PID
           X_lastError = X_error ;
           Y_lastError = Y_error ; 
           previousTime = currentTime;
       %% plotea
       if ploteo == true
            str = {'i_x:=', entrada_X, 'i_y:=', entrada_Y };
            text(0, 100, str, 'Color','black','FontSize',10,'BackgroundColor','magenta','VerticalAlignment','top') ;
            text(0, resolucion_y, str, 'Color','black','FontSize',10,'BackgroundColor','magenta','VerticalAlignment','top') ;
       end
    else
         %% guarda datos para el PID
           X_lastError = 0 ;
           Y_lastError = 0 ; 
           X_cumError = 0 ;
           Y_cumError = 0 ;
           previousTime = currentTime;
          % desprende led
            writeDigitalPin(a, 'D11', 0);
        disp("No hayó objeto")
    end
    if ploteo ==true
        drawnow
    end
end


if ploteo == false 
    imshow(BusqColor)
    hold on
    plot(CY, CX, '*r', 'LineWidth',10) ;%centroide
    plot(centro_x, centro_y, '*c', 'LineWidth',2) ; %centro global
    plot([centro_x, CY],[centro_y, CX], ':r', 'LineWidth',2)%linea de distancia
end


figure()
plot(save_error_X, save_error_Y)