#!/usr/bin/env python
# coding: utf-8

# In[66]:


# Importing necessary packages
import yasara
from yasara import *
import os
import xlsxwriter


# In[68]:


# Using the text mode
info.mode = "txt"

# Turning the yasara console off
Console("Off")


# In[69]:


# Defining the list for storing filenames
res_filename = []

# Initializing lists for the calculation of energies 
energy = []
en_obj_bond = []
en_obj_angle = []
en_obj_dihedral = []
en_obj_planarity = []
en_obj_coulomb = []
en_obj_vdw = []
en_obj_tot = []


# In[71]:


def Analyze():
    
      
    # Initializing list for the snapshot number
    snap_obj = [*range(0, len(res_filename), 1)]

    # Initializing list for the calculation of mass
    mass_obj = []

    # Initializing list for the calculation of dipole
    dipole_obj = []

    # Initializing list for the calculation of charge
    charge = []

    # Initializing lists for the calculation of volumes 
    vol_obj_vdw = []
    vol_obj_molecular = []
    vol_obj_accessible = []


    # Initializing lists for the calculation of radius from the center of mass
    rad_obj_nuclear_mass = []
    rad_obj_vdw_mass = []
    rad_obj_gyration_mass = []
    
    
    # Initializing lists for the calculation of radius from the geometric center
    rad_obj_nuclear_geometric = []
    rad_obj_vdw_geometric = []
    rad_obj_gyration_geometric = []

    # Initializing lists for the calculation of surface 
    surf_obj_vdw = []
    surf_obj_ms = []
    surf_obj_sas = []

    # Initializing lists for the calculation of secondary structure contents 
    ss_obj_helix = []
    ss_obj_sheet = []
    ss_obj_turn = []
    ss_obj_coil = []
    ss_obj_3_10_helix = []
    ss_obj_pi_helix = [] 
    
    # Loading one target object for commnon count calculations
    Load(format='pdb', filename = res_filename[0])
    
    # Calculating the mass of the object
    mass_obj = MassObj(1)
       
    # Calculating the charge of the object
    charge = ChargeObj(1)
    
    # Deleting the loaded structure
    DelObj("All")
    
    # Initializing the counter for energy calculations
    c = 0
    
    for i in res_filename:
        
        # Loading the target
        Load(format='pdb', filename = i)
        
        # Calculating the dipole moment of the object
        dipole_obj.append(DipoleObj(1))
         
        
        # Adding the bond energy value to the list
        en_obj_bond.append(energy[c][0])

        # Adding the angle energy value to the list
        en_obj_angle.append(energy[c][1])

        # Adding the dihedral energy value to the list
        en_obj_dihedral.append(energy[c][2])

        # Adding the planarity energy value to the list
        en_obj_planarity.append(energy[c][3])

        # Adding the coulomb energy value to the list
        en_obj_coulomb.append(energy[c][4])

        # Adding the vdw energy value to the list
        en_obj_vdw.append(energy[c][5])

        # Adding the total energy value to the list
        en_obj_tot.append(sum(energy[c]))
        
        c = c+1
        
        # Calculating the volume of the object
        v = VolumeObj(1)
        
        # Adding the volume for the surface type Van der Waals surface
        vol_obj_vdw.append(v[0])
        
        # Adding the volume for the surface type molecular surface
        vol_obj_molecular.append(v[1])
        
        # Adding the volume for the surface type accesibility surface
        vol_obj_accessible.append(v[2])
        
        # Calculating and adding the nuclear radius from the center of mass
        rad_obj_nuclear_mass.append(RadiusObj(1, center="mass", Type="nuclear"))

        # Calculating and adding the Van der Waals radius from the center of mass
        rad_obj_vdw_mass.append(RadiusObj(1, center="mass", Type="vdw"))

        # Calculating and adding the radius of gyration from the center of mass
        rad_obj_gyration_mass.append(RadiusObj(1, center="mass", Type="gyration"))

        # Calculating and adding the nuclear radius from the geometric center
        rad_obj_nuclear_geometric.append(RadiusObj(1, center="geometric", Type="nuclear"))

        # Calculating and adding the Van der Waals radius from the geometric center
        rad_obj_vdw_geometric.append(RadiusObj(1, center="geometric", Type="vdw"))

        # Calculating and adding the radius of gyration from the geometric center
        rad_obj_gyration_geometric.append(RadiusObj(1, center="geometric", Type="gyration"))
        
        # Calculating the volume of the object
        s = SurfObj(1)
        
        # Adding the Van der Waals surface value to the list
        surf_obj_vdw.append(s[0])

        # Adding the molecular surface value to the list
        surf_obj_ms.append(s[1])

        # Adding the solvent accessible surface value to the list
        surf_obj_sas.append(s[2])
        
        # Calculating the secondary structure content
        ss=SecStrObj(1)

        # Adding the alpha helix content value to the list
        ss_obj_helix.append(ss[0])

        # Adding the beta sheet content value to the list
        ss_obj_sheet.append(ss[1])

        # Adding the turn content value to the list
        ss_obj_turn.append(ss[2])

        # Adding the coil content value to the list
        ss_obj_coil.append(ss[3])

        # Adding the 3-10 helix content value to the list
        ss_obj_3_10_helix.append(ss[4])

        # Adding the pi content value to the list
        ss_obj_pi_helix.append(ss[5])
        
        # Deleting the loaded structures
        DelObj("All")
    

    # Creating the result table in excel

    # Defining the workbook of the excel
    workbook = xlsxwriter.Workbook('Analysis.xlsx')

    # Defining the worksheet for the basic counts
    #worksheet = workbook.add_worksheet('Basic Counts.xlsx')

    # Defining the worksheet for the energy components
    worksheet2 = workbook.add_worksheet('Energies.xlsx')

    # Defining the worksheet for the volume components
    worksheet3 = workbook.add_worksheet('Volumes.xlsx')
    
    # Defining the worksheet for the radius components
    worksheet4 = workbook.add_worksheet('Radius.xlsx')
    
    # Defining the worksheet for the surface components
    worksheet5 = workbook.add_worksheet('Surfaces.xlsx')

    # Defining the worksheet for the secondary structure components
    worksheet6 = workbook.add_worksheet('Seconday Structures.xlsx')

    # Defining the worksheet for the rmsd values
    #worksheet7 = workbook.add_worksheet('RMSD.xlsx')

    
    # Defining the cell formatting
    cell_fmt = workbook.add_format({'align': 'center','valign': 'vcenter', 'border': 1, 'num_format': '0.00000'})
    cell_fmt2 = workbook.add_format({'align': 'center','valign': 'vcenter', 'border': 1, 'bold': True})
    cell_fmt3 = workbook.add_format({'align': 'left','valign': 'vcenter', 'border': 1, 'bold': True,'num_format': '0.00000'})

    # Setting the columns of the headers for the energy worksheet
    worksheet2.set_column('A:H', 25)
    
    # Writing the cell headers
    worksheet2.write("A1","Snapshot", cell_fmt2)
    worksheet2.write("B1","Bond Energy", cell_fmt2)
    worksheet2.write("C1","Angle Energy", cell_fmt2)
    worksheet2.write("D1","Dihedral Energy", cell_fmt2)
    worksheet2.write("E1","Planarity Energy", cell_fmt2)
    worksheet2.write("F1","Coulomb Energy", cell_fmt2)
    worksheet2.write("G1","Vdw Energy", cell_fmt2)
    worksheet2.write("H1","Total Energy", cell_fmt2)
    
  
    
    # Writing the energy results into the excel
    for i in range(0,len(snap_obj)):
        
        worksheet2.write(i+1,0,snap_obj[i],cell_fmt)
        worksheet2.write(i+1,1,en_obj_bond[i],cell_fmt)
        worksheet2.write(i+1,2,en_obj_angle[i],cell_fmt)
        worksheet2.write(i+1,3,en_obj_dihedral[i],cell_fmt)
        worksheet2.write(i+1,4,en_obj_planarity[i],cell_fmt)
        worksheet2.write(i+1,5,en_obj_coulomb[i],cell_fmt)
        worksheet2.write(i+1,6,en_obj_vdw[i],cell_fmt)
        worksheet2.write(i+1,7,en_obj_tot[i],cell_fmt)


    # Setting the columns of the headers for the volume worksheet
    worksheet3.set_column('A:D', 25)

    # Writing the cell headers
    worksheet3.write("A1","Snapshot", cell_fmt2)
    worksheet3.write("B1","Volume for VDW", cell_fmt2)
    worksheet3.write("C1","Volume for Molecular Surface", cell_fmt2)
    worksheet3.write("D1","Volume for Accessibility Surface", cell_fmt2)

    # Writing the volume results into the excel
    for i in range(0,len(snap_obj)):
        
        worksheet3.write(i+1,0,snap_obj[i],cell_fmt)
        worksheet3.write(i+1,1,vol_obj_vdw[i],cell_fmt)
        worksheet3.write(i+1,2,vol_obj_molecular[i],cell_fmt)
        worksheet3.write(i+1,3,vol_obj_accessible[i],cell_fmt)

        
    # Setting the columns of the headers for the radius worksheet
    worksheet4.set_column('A:G', 25)
        
    # Writing the cell headers
    worksheet4.write("A1","Snapshot", cell_fmt2)
    worksheet4.write("B1","Nuclear Radius from center of mass", cell_fmt2)
    worksheet4.write("C1","Van der Waals Radius from center of mass", cell_fmt2)
    worksheet4.write("D1","Radius of gyration from center of mass", cell_fmt2)
    worksheet4.write("E1","Nuclear Radius from geometric center", cell_fmt2)
    worksheet4.write("F1","Van der Waals Radius from geometric center", cell_fmt2)
    worksheet4.write("G1","Radius of gyration from geometric center", cell_fmt2)
    
    # Writing the radius results into the excel
    for i in range(0,len(snap_obj)):
        
        worksheet4.write(i+1,0,snap_obj[i],cell_fmt)
        worksheet4.write(i+1,1,rad_obj_nuclear_mass[i][0],cell_fmt)
        worksheet4.write(i+1,2,rad_obj_vdw_mass[i][0],cell_fmt)
        worksheet4.write(i+1,3,rad_obj_gyration_mass[i][0],cell_fmt)
        worksheet4.write(i+1,4,rad_obj_nuclear_geometric[i][0],cell_fmt)
        worksheet4.write(i+1,5,rad_obj_vdw_geometric[i][0],cell_fmt)
        worksheet4.write(i+1,6,rad_obj_gyration_geometric[i][0],cell_fmt)
        
    
    # Setting the columns of the headers for the surfaces worksheet
    worksheet5.set_column('A:D', 25)
        
    # Writing the cell headers
    worksheet5.write("A1","Snapshot", cell_fmt2)
    worksheet5.write("B1","Van der Waals surface", cell_fmt2)
    worksheet5.write("C1","Molecular surface", cell_fmt2)
    worksheet5.write("D1","Solvent Accesibility surface", cell_fmt2)  
        
    # Writing the secosndary structure results into the excel
    for i in range(0,len(snap_obj)):
        
        worksheet5.write(i+1,0,snap_obj[i],cell_fmt)
        worksheet5.write(i+1,1,surf_obj_vdw[i],cell_fmt)
        worksheet5.write(i+1,2,surf_obj_ms[i],cell_fmt)
        worksheet5.write(i+1,3,surf_obj_sas[i],cell_fmt)    
        
        
    
    # Setting the columns of the headers for the secondary sructures worksheet
    worksheet6.set_column('A:G', 25)
        
    # Writing the cell headers
    worksheet6.write("A1","Snapshot", cell_fmt2)
    worksheet6.write("B1","Alpha helix content", cell_fmt2)
    worksheet6.write("C1","Beta sheet content", cell_fmt2)
    worksheet6.write("D1","Turn content", cell_fmt2)
    worksheet6.write("E1","Coil content", cell_fmt2)
    worksheet6.write("F1","3_10 helix content", cell_fmt2)
    worksheet6.write("G1","Pi helix content", cell_fmt2)
    
    # Writing the secosndary structure results into the excel
    for i in range(0,len(snap_obj)):
        
        worksheet6.write(i+1,0,snap_obj[i],cell_fmt)
        worksheet6.write(i+1,1,ss_obj_helix[i],cell_fmt)
        worksheet6.write(i+1,2,ss_obj_sheet[i],cell_fmt)
        worksheet6.write(i+1,3,ss_obj_turn[i],cell_fmt)
        worksheet6.write(i+1,4,ss_obj_coil[i],cell_fmt)
        worksheet6.write(i+1,5,ss_obj_3_10_helix[i],cell_fmt)
        worksheet6.write(i+1,6,ss_obj_pi_helix[i],cell_fmt)
                     
    
    
    # Closing the workbook
    workbook.close()
   
    print(mass_obj)
    print(charge)
    print(dipole_obj)
    # Exiting the Yasara
    Exit()                 
       


# In[93]:


def Run():
    
    struct_path = sys.argv[1]
     
    # Setting up the target file
    target = struct_path.split(".")[0]
    
    # Setting the pH at which the simulation should be run, by default physiological pH 7.4.
    ph = float(sys.argv[2]) # Default 7.4
    
    # Setting the NaCl concentration
    nacl = float(sys.argv[3]) # Default: 0.9
    
    # Setting the simulation temperature
    temperature = sys.argv[4] # Default: '298K'
    
    # Water density in [g/ml], should match the temperature set above
    density = float(sys.argv[5]) # Default: 0.997

      
    # Setting the format of the simulation files
    format = sys.argv[6] # Default: 'sim'

    # Duration of the simulation in [picoseconds]
    duration = int(sys.argv[7]) # Default: 250
    
    # Extension of the cell on each side around the solute in [A]
    extension = int(sys.argv[8]) # Default: 10
    
    # Shape of the simulation cell
    cellshape = sys.argv[9] # Default:'Cube'
    
    # Defining the speed of the simulation
    speed = sys.argv[10] # Default: "fast"
    
    # Defining the force field
    ff = sys.argv[11]
    
    # Defining the cutoff for the non-bonded interactions
    co = int(sys.argv[12]) # Default: 8
        
    # Setting the saveinterval with respect to the speed
    if speed=='fast':
        saveinterval=250000
    
    else:
        saveinterval=100000
        
    # Setting the forcefield
    ForceField(ff)
    
    # Defining the cutoff for the non-bonded interactions
    Cutoff(co)

    bnd = sys.argv[13] # Default: "Periodic"
    
    # Defining the cell boundary
    Boundary(bnd)
    
    # Use longrange coulomb forces (particle-mesh Ewald)
    Longrange("Coulomb")
    
    # Keeping the solute from diffusing around and crossing periodic boundaries
    CorrectDrift("On")
    
    # Loading the initial structure into Yasara environment
    LoadPDB(struct_path)
 
    # Aligning object with major axes to minimize cell size
    NiceOriAll()
    
    # Deleting long peptide bonds that bridge gaps in the structure
    DelBond("N","C",lenmin=5)
    
    # Deleting waters that are not involved in metal binding, to help the calculation of binding energies
    DelRes("Water with 0 arrows to all")
    
    # Preparing the structure for simulation at the chosen pH
    CleanAll()
    pH(ph)
         
    if info.stage=="Structure":
        
        # Optimizing the hydrogen-bonding network
        OptHydAll(method='YASARA')
    
    # Creating the simulation cell with the defined values
    CellAuto(extension=extension,shape=cellshape)
    
    # Saving the scene
    SaveSce(target)
    
     
    if ph!='None':
        
        # Checking if bounday is 'Wall'
        if bnd=='Wall':
            
            # Filling cell with water for 'Wall' boundary
            FillCellWater()
            
        else:
            
            # Fill the cell with water including pKa prediction and protonation state assignment
            ExperimentNeutralization(waterdensity=density,ph=ph,pkafile=target+".pka",speed='fast')
            Experiment("On")
            Wait("ExpEnd")
         
   
    # Saving the scene with water
    SaveSce(target+"_water.sce")
    
    # Choosing timestep and activating contraints
    
    # For fast simulation speed
    if speed=='fast':
                     
        # Constraining bonds to hydrogens
        FixBond("all","Element H")
        
        # Constraining certain bond angles involving hydrogens
        FixHydAngle("all")
        
        # Choosing a multiple timestep of 2*2.5 = 5 fs
        tslist=[2,2.5]
        
    # For normal or slow speed
    else:
        # Removing any constraints
        FreeBond("all","all")
        FreeAngle("all","all","all")
        
        # For slow speed
        if speed=='slow':
            # Choosing a multiple timestep of 2*1.00 = 2.0 fs
            tslist=[2,1.0]
        
        else:
            
            # Choosing a multiple timestep of 2*1.25 = 2.5 fs
            print("Choosing a multiple timestep of 2*1.25 = 2.5 fs")
            tslist=[2,1.25]
            
            # Slowing down atoms moving faster than 13000 m/s for rare circumstances
            Brake(13000)
    
    # Updating the pairlist every 10 (CPU) or 25 (GPU) steps
    
    processorlist=Processors()
    
    if processorlist[3]:
        SimSteps(screen=25,pairlist=25)
    
    else:
        SimSteps(screen=10,pairlist=10)
        
    #Calculating the total timestep
    ts=tslist[1]*tslist[0]
    
      
    # Setting the savesteps for the snapshots
    savesteps=saveinterval/ts
    
       
    # Setting the final simulation parameters
    TimeStep(tslist[0],tslist[1])
    Temp(temperature)
    
    # Checking if the user has accidentally fixed some atoms
    fixed_atoms = CountAtom('Fixed')
    
    # If there fixed atoms then they would be freed
    if fixed_atoms > 0:
        FreeAll()
  
        
    # Checking if already there is a snapshot
    i = "00000"

    # Checking if the format is 'sim' 
    if format=='sim':
        trajectfilename= target + i + '.sim'
        
    else:
        restartfilename=target + '.sim'
        trajectfilename=target + '.' + format
        
        # Backwards compatibility: Starting with YASARA version 12.8.1, XTC trajectories no longer contain a number in the filename
    
        old = FileSize(target + i + '.xtc')
        
        if old > 0:
            RenameFile(target + i + '.xtc',trajectfilename)
    
    running = FileSize(trajectfilename)
    
    # The simulation was not running before
    if not running:
            
        # Performing energy minimization experiment
        
        print("\nPerforming energy minimization experiment\n")
        Experiment("Minimization")
        Experiment("On")
        Wait("ExpEnd")
        
        # Starting the real simulation
        Sim("On")
    
    # The simulation was running before
    else:
        
        print("\nThe simulation has been running before\n")
        if format=='sim':
            
            # Finding and loading the last sim snapshot
            while True:
                
                found = FileSize(target + i + '.sim')
                if not found:
                    break
                    
                else:
                    LoadSim(target + i)
                    
                    i='{0:05d}'.format(int(i)+1)
                    
                    # Calculating the solute energy, including solvation energy (=interaction with explicit solvent)
                    e = EnergyObj(1, component="All")
                    energy.append(e)
     
            i='{0:05d}'.format(int(i)-1)
            
            # Loading the last simulation snapshot
            LoadSim(target + i)
            
            # Adjusting savesteps to save snapshots in the same interval as previously
            
            if int(i)>0:
                t = Time()
                savesteps=0+t/(ts*int(i))
            
        else:
            # Checking if there is a restart file with atom velocities
            found = FileSize(restartfilename)
            
            if found > 0:
                last,t = Load(format,trajectfilename),1
                
                if not last:
                    last,t = Load(format,trajectfilename),2
                    savesteps=0+t/ts
                    
                # Loading the restart file
                LoadSim(restartfilename)
            
            # No restart file found. Loading the last snapshot in the XTC/MDCrd trajectory
            else:
                
                while True:
                    i='{0:05d}'.format(int(i)+1)
                    last,t = Load(format,trajectfilename),int(i)
                    Sim("Pause")
                    Wait(1)
                    
                    if last:
                        break
                        
                savesteps=0+t/(ts*(int(i)-1))
                Sim("Continue")
                
    
    # Set temperature and pressure control
    TempCtrl("Rescale")
    PressureCtrl("SolventProbe",name="HOH",density=density) 
       
     
    # Saving the future snapshots
    SaveSim(trajectfilename,int(savesteps))
    
    
 
    if format!='sim':
        # Saving a single SIM restart file with velocities
        SaveSim(restartfilename,savesteps,Number=no)
            
      
    # Checking the duration of the simulation
    if duration == 'forever':
        Wait('forever')
    
    # Checking if the similation has finished
    else:
        while True:
            Wait(10)
            t = Time()
            print("\nSimulation running at time: " + str(int(t)) + " in femtoseconds")
             
            if int(t)%saveinterval == 0:
                            
                
                # Calculating the solute energy, including solvation energy (=interaction with explicit solvent)
                e = EnergyObj(1, component="All")
                energy.append(e)
    
            
            if t > 1000.0 * duration + 1:
                break  
      
        # Finishing the simulation
        Sim("Off")
        
           
         
        if format=='sim':
            
            i="00000"
            
            # Finding and loading the last sim snapshot
            while True:
                
                found = FileSize(target + i + '.sim')
                
                
                if not found:
                    
                    Analyze()
                    break
                            
                        
                # Recording the filename of the snapshot
                filename=target + '{0:05d}'.format(int(i))
                
                i='{0:05d}'.format(int(i)+1)
                
                # Loading the snapshot
                LoadSim(filename)

                # Saving the pdb
                SavePDB(1,filename)
                
                res_filename.append(filename + ".pdb")
                
    
        # Exiting Yasara
        Exit()
        
    


# In[73]:


if __name__ == "__main__":
    Run()


# In[ ]:




