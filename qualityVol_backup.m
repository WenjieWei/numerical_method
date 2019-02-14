function voltageRequirementCheck = qualityVol(Voltages, Vref, Phaseframe, Ts)
% QUALITYVOL: 
% This function finds the points where the voltage of either VFSG, 
% Ext Power, BAPU GEN, or RAT GEN are exceeding the requirements specified 
% in file "ECM BA-OPAL-018_MESIS POWER QUALITY ANALYSIS REQUIREMENTS SCOPE_REV.PDF".
% 
% For the 3-phase voltage average, this function assumes that EVERY ADJACENT
% THREE COLUMNS CONTAIN DATA FOR A 3-PHASE SOURCE. 
% E.G.: Columns 1~3 represent the three phases of the 1st source; 4~6
% represent the three phases of the 2nd source, etc. 
% 
% Voltage requirements:
% * For Individual phase nominal voltage RMS: +/- 6% (L-N)
% * For three phase average: Nominal voltage RMS: -2.5% (L-N), or +4% (L-N)
% Input Arguments:
% * Voltages: Voltage vector containing three phase voltage information;
% * Phaseframe: Time interval of each flight phase;
% * Vref: The reference voltage
% * Ts: Time step.
% Retvalues:
    
%% Re-format each column of the voltage data to match with the phase frame.
    % First check if the input voltage matrix is a set of three-phase
    % voltage data.
    if mod(size(Voltages, 2), 3) ~= 0
        disp('Check if the input are all three phase voltages.')
        return
    end
    
    % Create a array of cells to contain all the data according to the
    % phase frame.
    
    % Create array of cells to store the phase frames.
    % Size of the array varies according to the number of phases provided. 
    dataframes = cell(1, size(Phaseframe, 1));
    
    for i = 1:length(Phaseframe)
        % Loop through the phaseframe, 
        % and create 7 matrices if there are 7 phase frames existing. 
        phaseStartTime = Phaseframe(i, 1) + Ts;
        phaseEndTime = Phaseframe(i, 2);
        phaseDuration = phaseEndTime - phaseStartTime + Ts;
        currentFrame = NaN(phaseDuration, size(Voltages, 2));
        
        % Transfer data points from the matrix to a buffer which contains
        % the data for the specified phase.
        time = phaseStartTime;
        timeIndex = phaseStartTime / Ts;
        while time <= phaseEndTime
            for k = 1:size(Voltages, 2)
                currentFrame(timeIndex - (Phaseframe(i, 1) / Ts), k) = Voltages(timeIndex, k);
            end
            timeIndex = timeIndex + 1;
            time = time + Ts;
        end
        
        % Store the buffer to the frame cell.
        dataframes{i} = currentFrame;
    end
%% Find the points where the voltages exceeds the requirements. 
    % Create thresholds for the voltages.
    rmsThresholdPlus = Vref + (Vref * 0.06);
    rmsThresholdMinus = Vref - (Vref * 0.06);
    averageThresholdPlus = Vref + (Vref * 0.04);
    averageThresholdMinus = Vref - (Vref * 0.025);

    % voltageRequirementCheck has cells containing the occurance vectors. 
    % For this specific example, the first 18 columns contain RMS checks,
    % and the last 6 columns contain the AC three-phase average check.     
    voltageRequirementCheck = cell(1, size(Voltages, 2) * 4 / 3);

    % Loop through each flight phase. 
    for i = 1:length(dataframes)
        % Obtain the current flight frame
        % Create an array of cells to hold a vector of each column. 
        currentFrame = dataframes{i};
        phaseStartTime = Phaseframe(i, 1);
        occ_frame = cell(1, size(currentFrame, 2) * 4 / 3);
        occurance = 0;
        
        % Iterate through every column in the current frame.
        for j = 1:size(currentFrame, 2)
            % Create a vector to hold exceeding occurances.
            % 1st column: number of occurance
            % 2nd column: T_start
            % 3rd column: T_end
            % 4th column: duration            
            rms_occ_vec = NaN(length(currentFrame), 4);
            ave_occ_vec = NaN(length(currentFrame), 4);
            timeIndex = (phaseStartTime / Ts + 1) - Phaseframe(i, 1);
            time = Phaseframe(i, 1) + Ts;
            phaseEndTime = Phaseframe(i, 2);
            
            % Iterate through every row in the current column.
            while time <= phaseEndTime
                if currentFrame(timeIndex, j) > rmsThresholdPlus || ...
                        currentFrame(timeIndex, j) < rmsThresholdMinus
                    % Voltage is not within expected range
                    startTime = time;
                    finishDetected = false;
                    occurance = occurance + 1;
                    
                    rms_occ_vec(occurance, 1) = occurance;
                    rms_occ_vec(occurance, 2) = time;
                    
                    % Start new iteration starting from the current point;
                    % Increment duration for every loop until a finish is
                    % detected.
                    while ~finishDetected
                        if time >= phaseEndTime
                            % An exceeding of requirement has not finished when the
                            % current flight phase is finished.
                            % Record the stop time as the finish time of the phase.
                            stopTime = phaseEndTime;
                            %occ_vec(occurance, 4) = duration;
                            finishDetected = true;
                        elseif rmsThresholdMinus < currentFrame(timeIndex, j) ...
                                && currentFrame(timeIndex, j)< rmsThresholdPlus
                            % The voltage level has returned back to
                            % normal. 
                            time = time - Ts;
                            stopTime = time;
                            timeIndex = timeIndex - 1;
                            finishDetected = true;                            
                        else
                            timeIndex = timeIndex + 1;
                            time = time + Ts;
                        end
                    end
                    
                    % The exceeding is detected to have finished.
                    % Record the stop time and duration to the result
                    % vector and reset duration.
                    duration = (stopTime - startTime) / Ts + 1;
                    
                    rms_occ_vec(occurance, 3) = stopTime;
                    rms_occ_vec(occurance, 4) = duration;
                end
                
                timeIndex = timeIndex + 1;
                time = time + Ts;
            end
            
            rms_occ_vec = rms_occ_vec(all(~isnan(rms_occ_vec),2),:);
            occ_frame{j} = rms_occ_vec;
        end
        
        voltageRequirementCheck{i} = occ_frame;
    end
    
    return
end