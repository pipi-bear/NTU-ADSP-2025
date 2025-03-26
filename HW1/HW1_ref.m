% adsp hw1
% b08505006 

iteration = 0;
k = 8;            %(17-1)/2=8
TBd = 0.2;        % 1200/6000 = 0.2
TBu  =0.25 ;      % 1500/6000 = 0.25
delta = 0.0001;
Fs = 6000;
F =[0.03;0.06;0.09;0.15;0.19;0.28;0.31;0.39;0.45;0.46]; 
M = zeros(k+2,k+2);
E1 = 1000;        % max(error) last time
E = zeros(10,1);    %local maximums
Ws = 0.6;       % weight function for F[n]
Wp = 1;
H = [1;1;1;1;1;0;0;0;0;0];      % perfect filter for F[n]
S = zeros(10,1);        
h = zeros(2*k-1,1);     %impulse response
f = 0:0.0001:0.5;


for l = 1:5001
    if l <=2001
        hd(l) = 1;      % perfect filter
        w(l) = Wp;      % weight function
    elseif l>=2501
        hd(l) = 0;
        w(l) = Ws; 
    else
        w(l) = 0;
     
    end
end

while (E1-max(E)< 0 || E1-max(E)> delta || iteration == 0)
    
    iteration = iteration+1;
    E1 = max(E);
    for i = 1:k+2  % bilding M 
        for j = 2:k+2
            if j == k+2
                if F(i)<=TBd
                    M(i,j) = (-1)^(i+1) /Wp ;
                else
                    M(i,j) = (-1)^(i+1) /Ws ;
                end
    
            else 
                M(i,1) = 1;
                M(i,j)=cos(2*pi*(j-1)*F(i));
            end       
        end
    end
   
    S = M \ H; %solving s[n]

    % solving r           
    r = S(1)+S(2)*cos(2*pi*f)+S(3)*cos(4*pi*f)+S(4)*cos(6*pi*f)+S(5)*cos(8*pi*f)+...
        S(6)*cos(10*pi*f)+S(7)*cos(12*pi*f)+S(8)*cos(14*pi*f)+S(9)*cos(16*pi*f);

    % calculatin error
    err = (r-hd).* w;
    
    a=1;
    A = [];
    for x = 1:5001  %find local maximums
        if x==1 
            if abs(err(x+1)) < abs(err(x))
                E(a) = abs(err(x));
                A(a) = f(x);
                a=a+1;                                    
            end

        elseif  x== 5001 
          
            if (abs(err(x-1)) < abs(err(x) ) )
                E(a) = abs(err(x));
                A(a) = f(x);
                a=a+1;
            end

        elseif  (abs(err(x-1)) < abs(err(x)) && abs(err(x+1)) < abs(err(x)))
            E(a) = abs(err(x));
            A(a) = f(x);
            a=a+1;
        end
    end
    if a==13  %if there are k+4 extreme points choosing the nonboundary ones
        for g = 1:10
            F(g) = A(g+1);
            E(g) = E(g+1);
        end
        E(11)=[];
        E(12)=[];
       
    elseif a==12 %if there are k+3 extreme points choosing the bigger |err| boundary one
        if E(11)<E(1) 
            for g = 1:10
            F(g) = A(g);
            end
           E(11)=[];
         
        else
            for g = 1:10
            F(g) = A(g+1);
            E(g) = E(g+1);
            end
            E(11)=[];
          
        end
    elseif a == 11 
        for g = 1:10
            F(g) = A(g);
          
        end
    elseif a==9
        
    end
fprintf('\niteration =')    
disp(iteration) 
fprintf('max(E) =')
disp(max(E))

 
end

h(k+1,1) = S(1);  %transform s to impulse response
for n=1:k
    h(k+1+n,1) = S(n+1,1)/2;
    h(k+1-n,1) = S(n+1,1)/2;
end
n=1:2*k+1;
subplot(2,1,1) 
bar(n,h);
xlabel('n')
ylabel('h[n]')
title('impulse response')
subplot(2,1,2)
hold on
plot(Fs*f,r);
plot (Fs*f,hd);
xlabel('frequency(hz)')
ylabel('R(f)')
title('frequency response')
hold off


