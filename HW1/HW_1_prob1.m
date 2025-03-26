% HW1: Problem 1

N = 19;                  % filter length 
k = 9;                   % \frac{N-1}{2} = 9
W_p = 1;                 % weighting function for passband
W_s = 0.6;               % weighting function for stopband

% Normalized freqency for stop / transition / pass band
Sb_l = 0;                % Lower bound of the stopband, 0 / 8000 = 0
Sb_h = 0.25;             % Upper bound of the stopband, 2000 / 8000 = 0.25
TB_l = 0.25;             % Lower bound of the transition band, 2000 / 8000 = 0.25
TB_h = 0.3;              % Upper bound of the transition band, 2400 / 8000 = 0.3
Pb_l = 0.275;            % Lower bound of the passband, 2200 / 8000 = 0.275

fs = 8000;               % Sampling frequency in Hz

% Create a frequency vector from 0 to 0.5 with a step of 0.0001 (5001 points)
F_all = 0:0.0001:0.5;
% For the frequency vector F_all, initialize the weight vector W_all and the desired filter response vector Hd_all
W_all = zeros(size(F_all));      
% Desired filter response H_d[F_m] for the 5001 points (0 in stopband, 1 in passband)
Hd_all = double(F_all >= Pb_l); % Check if the frequency is in the passband, and convert the boolean to double

for i = 1:length(F_all)
    if F_all(i) <= Sb_h        % if t is in the stopband
        W_all(i) = W_s;        % set the corresponding weight to W_s (stopband weight)
    elseif F_all(i) >= TB_h && F_all(i) >= Pb_l
        W_all(i) = W_p;        % set the corresponding weight to W_p (passband weight)
    else
        W_all(i) = 0;          % the error in transition band is ignored, so set to 0
    end
end

% Initialization for step 2 (p.58-59)
E_1 = inf;               % set the previous error of the first iteration to infinity
E_0 = 1000;              % set a large value for error of the current iteration
delta = 0.0001;          % Convergence threshold

% Matrix initialization (defined as in p.59)
A_ext = zeros(k+2,k+2);      % Matrix A_ext (\in \mathbb{R}^{(k+2) \times (k+2)})
S = zeros(k+2,1);            % Vector S (\in \mathbb{R}^{(k+2) \times 1})

% Randomly choose the initial values for k+2 = 11 extreme points in [0, 0.5] (should not in transition band to guarantee convergence)
F_ext = [0.1;0.13;0.15;0.17;0.2;0.23;0.35;0.37;0.4;0.43;0.45]; 
Hd_ext = double(F_ext >= Pb_l);          % Vector H with k+2 elements, each \in {0, 1}, representing the desired filter response at the extreme points
P = F_ext;                          % Initialize the local maxmial / minimal points by F_ext
W_ext = zeros(size(F_ext));         % Initialize the weight vector for the extreme points

for i = 1:length(F_ext)
    if F_ext(i) <= Sb_h         
        W_ext(i) = W_s;        
    elseif F_ext(i) >= TB_h && F_ext(i) >= Pb_l
        W_ext(i) = W_p;        
    else
        W_ext(i) = 0;          
    end
end


while (E_1 - E_0 > delta || E_1 - E_0 < 0) 
    disp(['E_1 = ', num2str(E_1), ', E_0 = ', num2str(E_0)]);
    disp(['F_ext size: ', num2str(size(F_ext))]);
    
    E_1 = E_0;                                                  % set the previous error to the current error
    
    % STEP 2
    for row = 1:k+2                                             % build the matrix A_ext
        for col = 1:k+2
            if col == 1                                         % set the first column of A_ext to 1
                A_ext(row, col) = 1;
            elseif col == k+2                                   % set the last column of A_ext to \frac{(-1)^{row-1}}{W(F_{row-1})}
                A_ext(row, col) = (-1)^(row-1) / W_ext(row);
            else                                                % set the other columns of A_ext to cos(2 \pi n F_{row-1})
                % Debug print before accessing F_ext
                if row > length(F_ext)
                    disp(['ERROR: Trying to access F_ext(', num2str(row), ') but F_ext only has ', num2str(length(F_ext)), ' elements']);
                    break;
                end
                A_ext(row, col) = cos(2 * pi * (col-1) * F_ext(row));
            end
        end
    end

    S = A_ext \ Hd_ext;                                                % S = A_ext^{-1} H

    % STEP 3
    % R(F) = \sum_{n=0}^k s[n] cos(2 \pi n F)   (p.49)
    % Initialize RF as a vector of zeros with the same size as F_all
    RF = zeros(size(F_all));
    % Calculate RF for each frequency point
    for n = 0:k
        RF = RF + S(n+1) * cos(2 * pi * n * F_all);
    end
    
    % err(F) = [R(F) - H_d(F)]W(F)              (p.60)
    % calculate the error of the 5001 points
    err = (RF - Hd_all) .* W_all;

    % STEP 4
    count = 0;          % count the number of the extreme points
    err_ext = [];       % store the error of the extreme points
    location_ext = [];  % store the location of the extreme points
    
    % Pre-allocate arrays with correct size to ensure consistency
    F_ext = zeros(k+2, 1);      % Reset F_ext to ensure it has exactly k+2 elements
    err_ext = zeros(1, k+2);    % Make err_ext a row vector with k+2 elements
    location_ext = zeros(1, k+2); % Make location_ext a row vector with k+2 elements
    
    for i = 1:length(F_all)
        % leftmost point
        if i == 1
            if err(i) > err(i+1) && err(i) > 0  % local maximum
                count = count + 1;
                F_ext(count) = F_all(i);
                err_ext(count) = abs(err(i));
                location_ext(count) = i;
            elseif err(i) < err(i+1) && err(i) < 0  % local minimum
                count = count + 1;
                F_ext(count) = F_all(i);
                err_ext(count) = abs(err(i));
                location_ext(count) = i;
            end
        % rightmost point
        elseif i == length(F_all)
            if err(i) > err(i-1) && err(i) > 0  % local maximum
                count = count + 1;
                F_ext(count) = F_all(i);
                err_ext(count) = abs(err(i));
                location_ext(count) = i;
            elseif err(i) < err(i-1) && err(i) < 0  % local minimum
                count = count + 1;
                F_ext(count) = F_all(i);
                err_ext(count) = abs(err(i));
                location_ext(count) = i;
            end
        else
            if err(i) > err(i-1) && err(i) > err(i+1)   % local maximal
                count = count + 1;
                F_ext(count) = F_all(i);
                err_ext(count) = abs(err(i));
                location_ext(count) = i;
            elseif err(i) < err(i-1) && err(i) < err(i+1)   % local minimal
                count = count + 1;
                F_ext(count) = F_all(i);
                err_ext(count) = abs(err(i));
                location_ext(count) = i;
            end
        end
    end

    disp(['Found ', num2str(count), ' extreme points']);
    disp('F_ext values:');
    disp(F_ext');  % Transpose to display as row for readability
    
    disp('err_ext values:');
    disp(err_ext);
    
    disp('location_ext values:');
    disp(location_ext);
    
    % if more than k+2 extreme points:
    % 1. choose the nonboundary ones
    % 2. if there are still more than k+2, sort and choose the k+2 ones with the largest |error value|
    if count >= (k+2) + 2       % if we have >= two more than required
        disp(['Too many (', num2str(count), ') extreme points, selecting subset']);
        % Discard the first and last elements
        err_ext(1) = [];
        F_ext(1) = [];
        location_ext(1) = [];
        err_ext(end) = [];
        F_ext(end) = [];
        location_ext(end) = [];
        if length(err_ext) > k+2
            % if still more than k+2 after removing the boundaries, sort and choose the k+2 ones with the largest |error value|
            [err_ext, idx] = sort(err_ext, 'descend');
            F_ext = F_ext(idx);                         % reorder F_ext by the order of the sorted err_ext
            location_ext = location_ext(idx);           % reorder location_ext by the order of the sorted err_ext
            err_ext = err_ext(1:k+2);                   % preserve the k+2 largest ones by truncating since this list if sorted
            F_ext = F_ext(1:k+2);
            location_ext = location_ext(1:k+2);
        else
            % if we have exactly k+2 extreme points, sort
            [err_ext, idx] = sort(err_ext, 'descend');
            F_ext = F_ext(idx);
            location_ext = location_ext(idx);
        end
    elseif count == (k+2) + 1   % if we have one more than required
        disp('One extra extreme point, removing one');
        if err_ext(1) > err_ext(k+2)  
            % Discard the last element
            err_ext(end) = [];
            F_ext(end) = [];
            location_ext(end) = [];
        else
            % Discard the first element
            err_ext(1) = [];
            F_ext(1) = [];
            location_ext(1) = [];
        end
        [err_ext, idx] = sort(err_ext, 'descend');
        F_ext = F_ext(idx);
        location_ext = location_ext(idx);
    else                        % if we have exactly k+2 extreme points, sort
        disp('Exactly k+2 extreme points, sort');
        [err_ext, idx] = sort(err_ext, 'descend');
        F_ext = F_ext(idx);
        location_ext = location_ext(idx);
    end
    disp(['F_ext size after processing: ', num2str(size(F_ext))]);
    disp ('F_ext:');
    disp (F_ext);
    disp ('err_ext:');
    disp (err_ext);
    disp ('location_ext:');
    disp (location_ext);
    
    % STEP 5
    % E_0 = max(|err(F)|)                       (p.61)   
    E_0 = max(err_ext);
    disp(['New E_0 (current error): ', num2str(E_0)]);
    if E_1 - E_0 > delta || E_1 - E_0 < 0
        % if the error is not in the convergence threshold, continue from step 2
        % update the weight vector W_ext 
        W_ext = zeros(size(F_ext));
        for i = 1:length(F_ext)
            if F_ext(i) <= Sb_h                              % if the frequency is in the stopband
                W_ext(i) = W_s;
            elseif F_ext(i) >= TB_h && F_ext(i) >= Pb_l      % if the frequency is in the passband
                W_ext(i) = W_p;
            else                                             % if the frequency is in the transition band
                W_ext(i) = 0;
            end
        end
        % update the desired filter response vector Hd_ext
        Hd_ext = double(F_ext >= Pb_l);
    else
        % if the error is in the convergence threshold, stop the iteration
        break;
    end
end

% STEP 6
h(k+1,1) = S(1);                % h[k] = s[0]
for n = 1:k
    h(k+n+1,1) = S(n+1,1)/2;    % h[k+n] = s[n]/2
    h(k-n+1,1) = S(n+1,1)/2;    % h[k-n] = s[n]/2
end

% Plot the results
figure(1);
% Plot Frequency Response
subplot(211)
plot(F_all, RF, 'r', F_ext, Hd_ext, 'b')
title('Frequency Response $R(F)$', 'Interpreter', 'latex');
xlabel('Normalized Frequency');
ylabel('$R(F)$', 'Interpreter', 'latex');
xlim([0 0.5])
grid on;

% Plot Impulse Response
subplot(212)
n = 0:1:N-1;
stem(n, h)      % stem plot
title('Impulse Response $h[n]$', 'Interpreter', 'latex');
xlabel('n');
ylabel('$h[n]$', 'Interpreter', 'latex');
grid on;

drawnow;
shg;
