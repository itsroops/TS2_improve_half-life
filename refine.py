#!/usr/bin/env python
# coding: utf-8

# In[3]:


# Importing necessary packages
import yasara
from yasara import *
import os
import xlsxwriter


# In[4]:


# Using the text mode
info.mode = "txt"

# Turning the yasara console off
Console("Off")


# In[7]:


def Refine():
    
    # Setting the structure path that is accepted from the command prompt
    struct_path = sys.argv[1]
    
    # Setting the output path that is accepted from the command prompt
    output_path = sys.argv[2]
    
    # Setting up the target file
    target = struct_path.split(".")[0]
    
    # Setting the pH at which the simulation should be run, by default physiological pH 7.4.
    ph = float(sys.argv[3]) # Default: 7.4
 
    # Setting the simulation temperature
    temperature= sys.argv[4] # Defaukt: '298K'
    
    # Water density in [g/ml], should match the temperature set above
    density=float(sys.argv[5]) # Default: 0.997
    
    # Extension of the cell on each side around the solute in [A]
    extension=7.5
    
    # Defining the forcefield
    if info.stage=="Structure":
        ForceField("YASARA2",setpar="Yes")
    
    else:
        ForceField("YAMBER3",setpar="Yes")
    
    # Setting timestep
    timestep=[2,1.0]
    
    # Setting the savesteps for the snapshots
    savesteps=int(sys.argv[6]) # Default: 12500
    
    # Setting number of snapshots to 20, for 20*25 = 500 ps simulation 
    snapshots=int(sys.argv[7]) # Default: 20
    
    # Correction of the cis-peptide bonds
    CorrectCis("Off")
    
    # Correction of the wrong isomers
    CorrectIso("Off")
    
    # Keeping the solute from diffusing around and crossing periodic boundaries
    CorrectDrift("On")

     # Loading the initial structure into Yasara environment
    LoadPDB(target)
 
    # Aligning object with major axes to minimize cell size
    NiceOriAll()
    
    # Cleaning the structure
    CleanAll()
   
    # Creating the simulation cell with the defined values
    CellAuto(extension=extension)
    
    # Fill the cell with water including pKa prediction and protonation state assignment
    ExperimentNeutralization(waterdensity=density,ph=ph,pkafile=target+".pka",speed='fast')
    Experiment("On")
    Wait("ExpEnd")
         
    # Saving the scene with water
    SaveSce(target+"_water.sce")
    
    # Setting the final simulation parameters
    Temp(temperature)
    TimeStep(timestep[0],timestep[1])
    
    # Starting the simulation
    
    # Checking if already there is a snapshot
    i="00001"
    
    filename = target + "_snapshot" + i + ".sim"
    running = FileSize(filename)
    
    # The simulation was not running before
    if not running:
        
        # Performing energy minimization experiment
        print("\nPerforming energy minimization experiment")
        Experiment("Minimization")
        Experiment("On")
        Wait("ExpEnd")
        
        # Starting the real simulation
        Temp(temperature)
        
        print("\nStarting the simulation")
        Sim("On")
    
    # Simulation has been running before
    else:
        
        # Finding and loading the last sim snapshot
        
        while True:
            i='{0:05d}'.format(int(i)+1)
            found = FileSize(target + "_snapshot" + i + ".sim")
            
            if not found:
                break
        
        # Loading the last simulation snapshot
        LoadSim(target + "_snapshot" +  '{0:05d}'.format(int(i)-1))
             
        
    # Setting the temperature and pressure control
    TempCtrl("Rescale")
    PressureCtrl("SolventProbe",name="HOH",density=density)  
        
    # Waiting for 500ps and saving 20 snapshots
    SaveSim(target + "_snapshot00000",savesteps)
    SimSteps(20,10)  
        
    while True:
        
        t = Time()
        ps = snapshots*25
        Wait(10)
        
        if t > ps*1000:
            break
    
    # Stopping the simulation
    Sim("Off")
    
           
    # Checking YASARA structure
    strchecklist =['  Dihedrals','  Packing1D','  Packing3D']
    strchecks=len(strchecklist)
    
    # Checking WHATIF in the twinset
    wifchecklist =['     PhiPsi','   Backbone','   Packing1']
    wifchecks=len(wifchecklist)
    
    # Defining the check structure resultlist
    resultlist = []
    
    # Creating the list for storing the snapshot number
    snapshot = []
    
    # Creating the list for storing the energy of the object    
    energy = []
    
    # Creating the list for storing the resultlist values
    reslist = []
    
    # Creating the list for storing the mean values of the resultlist
    scorelist = []
    
    # Loading the snapshots, energy minimizing each snapshot and remembering the best ones
    energymin=9e99
    energyminss=-1
    scoremax=-9e99
    scoremaxss=-1
    
    for i in range(0,snapshots):
        filename=target + "_snapshot" + '{0:05d}'.format(int(i) +1)
        
        # Adding the snapshot number to the list
        snapshot.append(i)
        

        # Loading the snapshot
        LoadSim(filename)
        
        Wait(2000,"Femtoseconds")
        TempCtrl("Anneal")
        
        # Saving the pdb
        SavePDB(1,filename)
        
        # Calculating the solute energy, including solvation energy (=interaction with explicit solvent)
        e = EnergyObj(1, component="All")

        e = sum(e)
        
        # Adding the energy value to the list
        energy.append(e)
        
               
        if e<energymin:
            energymin=e
            energyminss=i
            
        if info.stage=="Structure":
            
            # Creating a temporary list to store the check object results
            temp = []
            
            for j in range(strchecks):
                resultlist.append(CheckObj(1,strchecklist[j])[0])
                temp.append(CheckObj(1,strchecklist[j])[0])
            
            reslist.append(temp)
        
        if info.stage=="Twinset":
            
            # Creating a temporary list to store the check object results
            temp = []
            
            for j in range(wifchecks):
                resultlist.append(CheckObj(1,wifchecklist[j])[0])
                temp.append(CheckObj(1,wifchecklist[j])[0])
            
            reslist.append(temp)
                
        if info.stage=="Structure" or info.stage=="Twinset":
            score = sum(resultlist) / len(resultlist)
            
            # Adding the score to the list
            scorelist.append(score)
        
            
            if score > scoremax:
                scoremax = score
                scoremaxss = i
    
   
     
    # Creating the result table in excel
    
    # Defining the workbook of the excel
    workbook = xlsxwriter.Workbook(output_path + '/Results.xlsx')
    
    # Defining the worksheet of the results workbook
    worksheet = workbook.add_worksheet('Sim Results.xlsx')
    
    # Setting the columns of the headers
    worksheet.set_column('A:F', 25)

    # Defining the cell formatting
    cell_fmt = workbook.add_format({'align': 'center','valign': 'vcenter', 'border': 1, 'num_format': '0.00000'})
    cell_fmt2 = workbook.add_format({'align': 'center','valign': 'vcenter', 'border': 1, 'bold': True})
    cell_fmt3 = workbook.add_format({'align': 'left','valign': 'vcenter', 'border': 1, 'bold': True,'num_format': '0.00000'})
    
    # Writing the cell headers
    worksheet.write("A1","Snapshot", cell_fmt2)
    worksheet.write("B1","Energy", cell_fmt2)
    worksheet.write("C1","Dihydrals", cell_fmt2)
    worksheet.write("D1","Packing1D", cell_fmt2)
    worksheet.write("E1","Packing3D", cell_fmt2)
    worksheet.write("F1","Average Score", cell_fmt2)
    
    # Writing the results into the excel
    for i in range(0,snapshots):
        
        worksheet.write(i+1,0,snapshot[i]+1,cell_fmt)
        worksheet.write(i+1,1,energy[i],cell_fmt)
        worksheet.write(i+1,2,reslist[i][0],cell_fmt)
        worksheet.write(i+1,3,reslist[i][1],cell_fmt)
        worksheet.write(i+1,4,reslist[i][2],cell_fmt)
        worksheet.write(i+1,5,scorelist[i],cell_fmt)
       
    # Selecting the cell for displaying the minimum energy
    select_cell = "A" + str(snapshots + 5) + ":C" + str(snapshots + 5) 
    
    # Writing the snapshot with minimum energy
    worksheet.merge_range(select_cell, "Snapshot " + str(energyminss+1) + " has a minimum energy of " + str(0.0 + energymin), cell_fmt3)

       
    if info.stage=="Structure" or info.stage=="Twinset":
            
        # Selecting the cell for displaying the maximum quality
        select_cell = "A" + str(snapshots + 8) + ":C" + str(snapshots + 8) 
        
        # Writing the snapshot with maximum quality
        worksheet.merge_range(select_cell,"Snapshot " + str(scoremaxss+1) + " has a maximum quality score of " + str(0.0 + scoremax), cell_fmt3)

    
    # Closing the workbook
    workbook.close()
   
    # Exiting the Yasara
    Exit()


# In[8]:


if __name__ == "__main__":
    Refine()


# In[ ]:




