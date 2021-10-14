#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Importing necessary packages
import yasara
from yasara import *
import os
import xlsxwriter
import sys


# In[2]:


# Using the text mode
info.mode = "txt"

# Turning the yasara console off
Console("Off")


# In[3]:


# Defining the constants

AVOCONST = 6.02214085700000e+23

JTOUNIT = 6.02214085700000e+20


# In[4]:


# Mapping the three-letter amino acid too one-letter amino-acid
amino_dict = {'C':'Cys', 'D':'Asp', 'S':'Ser', 'Q':'Gln', 'K':'Lys',
     'I':'Ile', 'P':'Pro', 'T':'Thr', 'F':'Phe', 'N':'Asn', 
     'G':'Gly', 'H':'His', 'L':'Leu', 'R':'Arg', 'W':'Trp',
     'A':'Ala', 'V':'Val', 'E':'Glu', 'Y':'Tyr', 'M':'Met'}


# In[5]:


# Defining the list for storing filenames
res_filename = []

# Flag for calling the energy calculation function
call_func = 0


# In[6]:


def Calc_Energy():
    
    print("\nCalculating the energies of all the structures")
    
    # Setting the absolute path of the output structures accepted from the command prompt
    output_path = sys.argv[4]
    
    # Defining the list for storing the energy of the structures
    res_energy = []
    
    #Calculating the energy of the structure
    
    for i in range(len(res_filename)):
        
        # Loading the target
        Load(format='pdb', filename = output_path + "/" + res_filename[i])
        
        # Calculating the solute energy, including solvation energy (=interaction with explicit solvent)
        e = EnergyObj(1, component="All")

        e = sum(e)
        
        # Adding the energy value to the list
        res_energy.append(e)
        
        # Deleting the loaded structures
        DelObj("All")
    
    
    # Creating the result table in excel
    
    # Defining the workbook of the excel
    workbook = xlsxwriter.Workbook(output_path + "/Swap_Minimize.xlsx")
    
    # Defining the worksheet of the results workbook
    worksheet = workbook.add_worksheet('Energy.xlsx')
    
    # Setting the columns of the headers
    worksheet.set_column('A:B', 25)

    # Defining the cell formatting
    cell_fmt = workbook.add_format({'align': 'center','valign': 'vcenter', 'border': 1, 'num_format': '0.00000'})
    cell_fmt2 = workbook.add_format({'align': 'center','valign': 'vcenter', 'border': 1, 'bold': True})
        
    # Writing the cell headers
    worksheet.write("A1","Filename", cell_fmt2)
    worksheet.write("B1","Energy", cell_fmt2)
    
    # Writing the results
    for i in range(0,len(res_filename)):
                
        worksheet.write(i+1,0,res_filename[i],cell_fmt)
        worksheet.write(i+1,1,res_energy[i],cell_fmt)
       
    # Closing the workbook
    workbook.close()
    
    print("\nExiting the program....")
    # Exiting the Yasara
    Exit()


# In[7]:


def Minimize(path,ff):
    
    # Loading the target
    Load(format='pdb', filename=path)
    
   
    print("\nRunning energy minimizing for the structure: " + path.split("/")[-1] + ".pdb")
    
   
    # Cleaning and preparing for minimization
    CleanAll()
    
    # Optimize the hydrogen-bonding network
    OptHydAll(method='YASARA')
    
    # checking if the cell already has a simulation cell
    cellfound = CountObj('SimCell')
    
    # If the simulation cell is not present, then a cell is created with Periodic Boundary Condition
    if cellfound == 0:
        CellAuto(extension=8)
        Boundary('Periodic')
        
    # Selecting the force field
    ForceField (name=ff,setpar="Yes")
    
    # Checking that atleast one atom is free to move
    fixed_atoms = CountAtom('Fixed')
    all_atoms=info.atoms
    
    if fixed_atoms==all_atoms :
        print("Either no atom is present or all the atoms are fixed. Hence, energy minimization is not possible for this structure.")
        return 1      

       
    # Correction of the cis-peptide bonds which are newly formed
    CorrectCis("On",old="No")
    
    # Correction of the wrong isomers which are newly formed 
    CorrectIso("On", old="No")
    
    # If the forcefield is not equal to NOVA
    if ff!='NOVA':
        
        # Counting number of water residues
        waters = CountRes('Water')
        
        # Counting the solvent accessible surface area of the object other than water
        surfres = SurfRes('!Water', Type="Accessible")
        
        # Creating water shell
        if not waters or surfres[0]/waters > 15:
            
            # Setting the neutralization experiment with the usual parameters
            ExperimentNeutralization(waterdensity=0.997, nacl=0.9, ph=7.4, speed='Fast')
            
            # Running the neutralization experiment
            Experiment('On')
          
            Wait("ExpEnd")
            DelRes("Water with distance>6 from !Water")
        
        else:
        
            # Storing the atoms which are fixed
            FixedList = ListAtom('Fixed')

            # Fix all the atoms in the soup
            FixAll()

            # Free all the atoms of the water
            FreeRes('Water')

            # Setting the energy minimization only for the water molecules
            ExperimentMinimization(convergence=0.1)

            # Performing energy minimization only for the water molecules
            Experiment('On')
            Wait("ExpEnd")

            # Freeing all the atoms
            FreeAll()

            # Checking if the structure had fixed atoms 
            if len(FixedList) > 0:

                # Fixing the atoms which were initially fixed
                for i in FixedList:
                    FixRes(i)
                    
    # Running the main energy minimization
    
    #Converging as soon as the energy improves by less than 0.05 kJ/mol = 50 J/mol per atom during 200 steps
    ExperimentMinimization(convergence=(50.0*JTOUNIT)/AVOCONST)

    # Starting the experiment
    Experiment('On')
    Wait("ExpEnd")
      
    # Checking if the minimization introduce any error

    wronghands = CheckAll(Type="Isomers")
    cisbonds = CheckAll(Type="PepBonds")
    
   
    #if wronghands[0]!=0 or cisbonds[0]!=0:
        #print("\n**WARNING** Number of wrong isomers = " + str(int(wronghands[0])))
        #print("\n**WARNING** Number of cis-peptide bonds = " + str(int(cisbonds[0])))
        
    
    k = path.split(".")[0]+"_min.pdb"
    print("\nSaving the minimized structure as: " + k.split("/")[-1])
    print("\n*************************")
    
    # Saving the minimized structure
    SavePDB(path.split("/")[-1].split(".")[0], filename=path.split(".")[0]+"_min", format="PDB",transform="Yes")
    
   
    
    # Adding the minimized filename to the result list
    res_filename.append(path.split("/")[-1]+"_min.pdb")
    
    
     # Clearing the loaded structures
    DelObj("All")
    
    # Check if the minimization is complete and if energy calculation is possible
    
    if call_func ==1:
        
              
        # Calling the calculate energy function
        Calc_Energy()
    
    
  


# In[123]:


def Swap():
    
    # Setting the loci values accepted from the command prompt
    loci = sys.argv[1]
    
    # Setting the force field value acceptedfrom the command prompt
    ff = sys.argv[2]
    
    # Setting the absolute path of the initial structure accepted from the command prompt
    struct_path = sys.argv[3]
    
    # Setting the absolute path of the output structures accepted from the command prompt
    output_path = sys.argv[4]
    
    # Converting the loci values into list
    loci = list(loci.split(" "))
          
    # Loading the initial structure into Yasara environment
    LoadPDB(struct_path)
  
    
    # Renaming the object
    NameObj(1,"in")
    
    # Saving the structure in the output path with a predefined name
    SavePDB (1,output_path + "/" + "in",format="PDB",transform="Yes")
    
    # Adding the filename to the result list
    res_filename.append("in.pdb")
   
    
    # Clearing the loaded structure
    DelObj("All")


    # Setting the filename and file path for the initial structure
    file_name = "in.pdb"
    file_path = output_path
    
  
    # Keeping track of the index of the loci
    c=0
    
    # Repeating for all loci
    for i in loci:
         
        global call_func
        
        if i==loci[-1]:
            call_func = 1
            
        else:
            call_func = 0
         
        # Selecting the name of the input pdb for loading into Yasara
        name = file_path + str("/") + file_name
        
        print("\nLoading structure for mutation: " + file_name)
               
        # Loading the structure into Yasara environment
        LoadPDB(name)
        
         
        # Selecting the force field
        ForceField(name=ff,setpar="Yes")
        
        # Finding the residue name
        res_no = i
        res_name=SequenceRes(res_no)
        res_name = amino_dict[res_name[0]]
        
        # Swapping the residue to D configuration
        SwapRes(selection1=res_name+" " +str(res_no),new=res_name,isomer="D")
        
        # Saving the new filename of the mutated pdb
        new_name = output_path + "/" + "in_m_" + str(loci[c])
        
        print("\nSaving the mutated structure as: " + new_name.split("/")[-1] + ".pdb")
        
        file_name = "in_m_" + str(loci[c]) + "_min.pdb"
       
  
        # Storing the name of the mutated structure for the first locus
        if c==0:
            old_file_name = "in"
                     
        
        # Storing the name of the mutated structure for the loci other than the first loci
        else:
            old_file_name = "in_m_" + str(loci[c-1]) + "_min"
            
     
        
        # Updating the index of the loci
        c = c + 1
        
           
        # Saving the mutated pdb structure                                                             
        SavePDB (old_file_name,new_name,format="PDB",transform="Yes")
        
       
        # Adding the mutated filename to the result list
        res_filename.append(new_name.split("/")[-1] + ".pdb")
        
                
        # Clearing the loaded structure
        DelObj("All")
        
        # Running energy minimization function on the mutated structure
        Minimize(new_name,ff)



# In[124]:


if __name__ == "__main__":
    Swap()


# In[ ]:




