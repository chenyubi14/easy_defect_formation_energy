# easy_defect_formation_energy 
This is a python based script, specific to plot defect formation energies as a function of Fermi level for defects in semiconductors and insulators.

Here is a brief introduction to the files.

energyf.native.specialKPOINT.py is the python file that stores the folder information.

class0_functional1.py, class1_read.py, and class96_formationenergy.py are functions/class that are used to draw the diagram.

You only need to edit the information of this file energyf.native.specialKPOINT.py. Inside energyf.native.specialKPOINT.py, don't change codes outside this pattern; only need to edit the lines in between
######################################################## check for changes
########################################################


## Run
To run this python script, go to folder_working, and run `python /PATH-TO-FILE/energyf.native.specialKPOINT.py`. 


## data structure
Need the following structure of folders to process the data reading

Go to a folder that stores all jobs about one host material, like BeO, BN, ZnO. Let's call this folder "folder_working". All jobs need to be subfolders of "folder_working". 

When you specify folders, it will assume the folders are under "folder_working". Do not give a full path to a job folder, because "folder_working" will be automatically added to every path you specify.

Need to put defect_folders/unit_folders/perfect_folders as subfolders of folder_working. For example, 
	'folder_working/wurtzite_81_iH' is a defect folder about hydrogen interstitial; 
	'folder_working/wurtzite_00_unit' is a folder with unit cell jobs; 
	'folder_working/wurtzite_01_super_perfect' is a folder about perfect supercells 

Furthermore, the charge defects should be stored as subfolders of a defect folder. For example,
	'folder_working/wurtizite_81_iH/defect-1e' and 'folder_working/wurtizite_81_iH/defect1e' are hydrogen interstitial defects with charges -1e/1e

Need the freysoldt correction energy stored in a file called 'DEFECT' for a charge folder. E.g. in the file 'folder_working/wurtizite_81_iH/defect-1e/DEFECT', this energy should be saved as a line 'FREYCORRALL=0.28'

## chemical potential automation needs a special care

chemical potential calculation needs a special structure

To calculate the chemical potential, the jobs need a special structure.

Suppose 'folder_unit'='folder_working/wurtzite_01_unit/unit_aexx0.25' is a unit cell calculation of ZnO. The jobs of elemental phases, like Zn and O, need to be named as 'energyf_Zn' and 'energyf_O', and put as subfolders of folder_unit. 

Formation enthalpy of ZnO will be calculated using energy of ZnO in 'folder_unit', energy of Zn in 'folder_unit/energyf_Zn' and energy of O in 'folder_unit/energyf_O'. It is crutial that the folders are named starting 'energyf_' and as subfolders of 'folder_unit'. 

Chemical potentials will be calculated given the condition like 'Zn-rich'/'O-rich'. The code cannot resolve other conditions. If you want a different condition like intermediate chemical potentials, you can give numerical values to this variable 'dict_miu' in 'energyf_*.py' file. 'dict_miu' is a python dictionary like dict_miu={'Zn':float_miu_Zn, 'O':float_miu_O, 'condition': 'intermediate'}.


## chemical potential for impurity calculation
For an impurity calculation, like Cu in ZnO, the jobs also need to follow a special structure to automatically calculate chemical potentials.

You need to specify the impurity elements in this variable 'elements_name' of file 'energyf_*.py'.

The elemental phase of Cu should be saved as 'energyf_Cu' as a subfolder of 'folder_unit'. The compound CuO should be saved as 'energyf_Cu_O_${COMMENTS}', as a subfolder of 'folder_unit'.

For each impurity on ZnO, like H, the code will find the folders of names starting with 'energyf_H_'. It may find 'energyf_H_O_H2O', 'energyf_H_Zn_Zn2H', 'energyf_H_O_H2O2', etc. The formation enthalpy of these compound will be calculated, each giving one constrain on delta miu. There will be multiple calculated values of delta miu of H. The smallest value will be picked, and this value is guaranteed to be no larger than 0.

So far, my code can only handle a material with two different elements like CuO, Cu2O, H2O. Other compound like ZnCuO2 cannot be propertly calculated. You may calculate chemical potentials by hand and define the variable 'dict_miu' directly in the file 'energyf_*.py'. 


## edit 
Edit the information in energyf.native.specialKPOINT.py. Run `python /PATH-TO-FILE/energyf.native.specialKPOINT.py` at folder_working to draw the diagram.

For a different formation energy diagram. Copy energyf.native.specialKPOINT.py to a different file, and change the information.


