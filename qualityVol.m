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
    aveThresholdPlus = Vref + (Vref * 0.04);
    aveThresholdMinus = Vref - (Vref * 0.025);

    % voltageRequirementCheck has cells containing the occurance vectors. 
    % For this specific example, the first 18 columns contain RMS checks,
    % and the last 6 columns contain the AC three-phase average check.     
    voltageRequirementCheck = cell(1, size(Voltages, 2) * 4 / 3);

    % Loop through each flight phase. 
    for i = 1:length(dataframes)
        % Obtain the current flight frame
        % Create an array of cells to hold an occurance matrix of each column. 
        currentFrame = dataframes{i};
        phaseStartTime = Phaseframe(i, 1);
        occ_frame = cell(1, size(currentFrame, 2) * 4 / 3);
        occurance = 0;
        
        % Iterate through every column in the current frame.
        for j = 1:size(currentFrame, 2)    
            timeIndex = (phaseStartTime / Ts + 1) - Phaseframe(i, 1);
            time = Phaseframe(i, 1) + Ts;
            phaseEndTime = Phaseframe(i, 2);
            
            % Create two empty vectors, holding the index of each
            % exceeding; The vectors will be cleared as soon as the
            % continuity is stopped. 
            rmsExceedingsVector = [];
            aveExceedingsVector = [];
            
            % Create another two vectors, holding the information of the
            % exceedings.
            % 1st column: number of occurance
            % 2nd column: T_start
            % 3rd column: T_end
            % 4th column: duration        
            rms_occ_vec = NaN(length(currentFrame), 4);
            ave_occ_vec = NaN(length(currentFrame), 4);
            
            % Iterate through every row in the current column.
            while time <= phaseEndTime
                %% Initialize Flags for range check.
                % Set a flag to see if the three phase average needs to be
                % calculated. 
                % The average value will be calculated when the column
                % being investigated is the 3rd phase.
                threePhaseAverage = 0;
                if mod(j, 3) ~= 0
                    calculateThreePhaseVoltage = false;                    
                else
                    calculateThreePhaseVoltage = true;
                end
                
                %% Record the exceedings if any is detected. 
                if currentFrame(timeIndex, j) > rmsThresholdMinus && ...
                        currentFrame(timeIndex, j) < rmsThresholdPlus
                    rmsExceedingFlag = false;
                else
                    rmsExceedingFlag = true;
                end
                
                if calculateThreePhaseVoltage
                    threePhaseAverage = (currentFrame(timeIndex, j - 2) +...
                        currentFrame(timeIndex, j - 1) +...
                        currentFrame(timeIndex, j)) / 3;
                    if threePhaseAverage > aveThresholdMinus && ...
                            threePhaseAverage < aveThresholdPlus
                        aveExceedingFlag = false;
                    else
                        aveExceedingFlag = true;
                    end
                end
                
                %% Perform the RMS Value check. 
                if rmsExceedingFlag
                    % An exceeding of the RMS value is detected.
                    % Add the index to the occurance vector.
                    rmsExceedingsVector(end + 1) = timeIndex;
                    
                    if time == phaseEndTime
                        duration = length(rmsExceedingsVector) / Ts;
                        occurance = occurance + 1;
                        rmsStartTime = rmsExceedingsVector(1) / Ts;
                        rmsEndTime = rmsExceedingsVector(end) / Ts;

                        rms_occ_vec(occurance, 1) = occurance;
                        rms_occ_vec(occurance, 2) = rmsStartTime;
                        rms_occ_vec(occurance, 3) = rmsEndTime;
                        rms_occ_vec(occurance, 4) = duration;

                        rmsExceedingsVector = [];
                    end
                    
                    timeIndex = timeIndex + 1;
                    time = time + Ts;
                elseif (~rmsExceedingFlag && ~isempty(rmsExceedingsVector))
                    % Exceeding is not detected, but the vector has values.
                    % Record information extracted from the vector, 
                    % and clear the vector. 
                    duration = length(rmsExceedingsVector) / Ts;
                    occurance = occurance + 1;
                    rmsStartTime = rmsExceedingsVector(1) / Ts;
                    rmsEndTime = rmsExceedingsVector(end) / Ts;
                    
                    rms_occ_vec(occurance, 1) = occurance;
                    rms_occ_vec(occurance, 2) = rmsStartTime;
                    rms_occ_vec(occurance, 3) = rmsEndTime;
                    rms_occ_vec(occurance, 4) = duration;
                    
                    rmsExceedingsVector = [];
                else
                    % No exceeding detected, previous exceedings have all
                    % been recorded, if any. Increment the counters. 
                    timeIndex = timeIndex + 1;
                    time = time + Ts;
                end
                
                %% Perform the average value check. 
                if calculateThreePhaseVoltage && aveExceedingFlag
                    % An exceeding of the average value is detected
                    % Add the index to the occurance vector. 
                    aveExceedingsVector(end + 1) = timeIndex;
            end
            
            rms_occ_vec = rms_occ_vec(all(~isnan(rms_occ_vec),2),:);
            occ_frame{j} = rms_occ_vec;
        end
        
        voltageRequirementCheck{i} = occ_frame;
    end
    
    return
end