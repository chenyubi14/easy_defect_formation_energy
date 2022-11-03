
# In[1]:

# Go to a folder that stores all jobs about one material, like BeO, BN, ZnO. Let's call this folder 'folder_working'. All jobs need to be a subfolder of this 'folder_working'
# Run 'python /PATH-TO-FILE/energyf.native.specialKPOINT.py' at 'folder_working'
# Need the freysoldt correction energy stored in a file called 'DEFECT' for a defect folder. This energy should be a line 'FREYCORRALL=0.28'

# In[2]:
import numpy as np
import sys
import os
import matplotlib.pyplot as plt
from class96_formationenergy import chemical_potential, defectinfo, readformationenergy
from class1_read import read_file_values
folder_working = os.environ['PWD'] + '/'

# In[3]:

# (0) perfect supercell as bulk reference
######################################################## check for changes
folder_perfect ='wurtzite_01_super_perfect/perfect_run_aexx0.405.specialKPOINT'+'/' # the folder of perfect bulk structure, will be used to read total energy of a perfect supercell: E_tot(bulk)
folder_bandgap = 'wurtzite_00_unit/unit.AEXX0.405'+'/' # read bandgap from this unitcell folder through reading VBM and VBM. folder_bandgap may not be the same as folder_perfect, which may not have the correct KPOINT sampling to read bandgap. For example, a special KPOINT calculation cannot give the VBM and CBM located at Gamma/other points.
folder_VBM = 'wurtzite_01_super_perfect/perfect_run_aexx0.405'+'/' # read VBM from this supercell folder. folder_VBM may not be the same as folder_perfect, because VBM may be located at Gamma point or a different point.
########################################################



# (1) defect information: type, formula, directories, charges
######################################################## check for changes
defecttype='$\mathit{V}_\mathrm{O}$' # this is the label of oxygen vacancy written on the formation energy curves.
defect_formula = {'Be':0, 'O':-1}# n>0 adding, n<0 removing. Oxygen vacancy removed one O atom.
defect_2ndclass_folder = 'wurtzite_11_vO'+'/' # defect_folder. Will generate folder_working/wurtzite_11_vO. The '/' is necessary.
defect_3rdclass_folder = ['defect0e.special'+'/','defect-1e.special'+'/'] # the charge defect folders as subfolders of defect_folder. Can include all charged defects by extending this list.
defect_charge = [0,-1] # charges of charge defect folders. Should follow the order of the list 'defect_3rdclass_folder'. This charge is positive when removing electrons. E.g. charge=-1 when adding one electron.
# generate a class (defectinfo) that stores these defect information
defect_3rdclass_folder = [ folder_working+defect_2ndclass_folder+ff for ff in defect_3rdclass_folder] # add pre-folder to get ['wurtzite_11_vO/defect0e.special/', 'wurtzite_11_vO/defect-1e.special/']
vo = defectinfo(defecttype,charge=defect_charge, indiv_folder=defect_3rdclass_folder,formula=defect_formula) # remove an O atom
# vo is a class to store these information

defecttype='$\mathrm{H}_\mathit{i}$' # this is the label of hydrogen interstitial written on the formation energy curves.
defect_formula = {'Be':0, 'O':0, 'H':1}# n>0 adding, n<0 removing. Hydrogen interstitial inserted one H atom.
defect_2ndclass_folder = 'wurtzite_81_iH'+'/' # defect_folder. Will generate folder_working/wurtzite_81_Hi
defect_3rdclass_folder = ['defect-1e'+'/','defect1e'+'/'] # the charge defect folders as subfolders of defect_folder. Can include all charged defects by extending this list.
defect_charge = [-1,1] # charges of charge defect folders. Should follow the order of the list 'defect_3rdclass_folder'. This charge is positive when removing electrons. E.g. charge=-1 when adding one electron.
# generate a class (defectinfo) that stores these defect information
defect_3rdclass_folder = [ folder_working+defect_2ndclass_folder+ff for ff in defect_3rdclass_folder] # add pre-folder to get ['wurtzite_81_Hi/defect-1e/', 'wurtzite_81_Hi/defect1e/']
hi = defectinfo(defecttype,charge=defect_charge, indiv_folder=defect_3rdclass_folder,formula=defect_formula) # insert a H atom
# hi is a class to store these information

### you can add more defects by copying the above templates and put the information of other defects
######################################################## 


# (2) 
######################################################## check for changes
# defects to be plotted should be put in this list: list_defect
list_defect= [vo,hi] # If a class of defect information is not in this list. It will not show up in the formation energy diagram
condition = 'O-rich' # calculate chemical potentials (delta miu) under this condition. Need to be this format: O-rich / Be-rich / Zn-rich.
comment = 'native.special.test' # this comment is used in the filename of saved figure.
#The figure filename is condition_comment_formation-energy.jpeg
######################################################## 



# In[4]:
# (3) chemical potentials from formation enthalpy
######################################################## check for changes
elements_name = ['Be', 'O', 'H', 'F', 'Li'] # all elements occurred in the defects. Will read their bulk energies, The order of impurity elements is no important.
folder_unit='wurtzite_00_unit/unit.AEXX0.405'+'/' # folder_unit is the folder that stores elemental phases Will generate folder_working/folder_unit. The '/' is necessary.
folder_elements = ['energyf_Be/'+'/', 'energyf_O'+'/','energyf_H'+'/', 'energyf_F'+'/','energyf_Li'+'/'] #Will read bulk energies of these elements. Should follow the order of 'elements_name'. These folders should be subfolders of 'folder_unit'
impurity_atomnames=elements_name[2:] # remove the first two elements that are in the host. It will become ['H','F','Li']. 
########################################################


## read delta miu
read_fil = read_file_values(folder_working+folder_unit)
dict_delta_miu=read_fil.read_delta_miu4energyf(condition,impurity_atomnames=impurity_atomnames)

# (4) chemical potential including delta_miu
folder_elements = [folder_working+folder_unit+ff for ff in folder_elements]
# dict_elementformula is the formula of compound like {'Be':2, 'O':2}
dict_miu = chemical_potential(elements_name, folder_elements, dict_delta_miu) #  {'Be': miu_Be, 'O': miu_O}
dict_miu['condition'] = condition # dict_miu={'Be':miu_Be, 'O':miu_O, 'condition': O_rich}
print('miu_dict=%s\n\n\n'%(dict_miu)) # print chemical potential


######################################################### check for changes
# define dict_miu by hand if the code can not automatically handle your problem
#dict_miu={'Be':miu_Be, 'O':miu_O, 'condition': O_rich}
#########################################################


# In[5]:
myread=readformationenergy(folder_working, folder_perfect,list_defect, dict_miu, comment=comment,folder_bandgap=folder_bandgap) # initialize class
myread.readperfect(folder_VBM=folder_working+folder_VBM) #read perfect supercell folder # obtain E_perfect, BG, vbm

# plotting information
######################################################### check for changes
plot_charge_labels_segment=False #Usually False. False: don't plot charges labels. True: plot charges in the middle of each segment
lower_bound_plot=True # Usually true. Plot the charge defect with the lowest formation energy (lower bound) 
xlimits=[0, 11.3] # the x limits in plot
ylimits=[-20, 25] # the y limits in plot
# Set the position of defect label for each condition.
if condition == 'O-rich':
    # defectlabeltextposition is a dictionary with elements like {defect:[int,float1,float2]}; int (integer) is index of transition_level with location (x0,y0). The defect label will be placed close to int1_th transition level at location (x0,y0); float1 (dx) is to shift the position of label horizontally; float (dy) is to shift the position of label verically; As a result, the location of the label is (x0+dx,y0+dy)]} 
    defectlabeltextposition={vo:[2,0.,0.],hi:[1,0.,0.]} 
# For example: float=0 for no shift; float1(dx)=-1 move label to the left by 1eV; float2(dy)= 1 move label upward by 1eV;
elif condition == 'Be-rich': 
    defectlabeltextposition={vo:[2,0.,0.],hi:[0,0.,0.]} 
else:
    print('Error! need to specify where to put defect labels')
    sys.exit()
#########################################################

if not os.path.isdir(folder_working+'graphdata'):
    os.mkdir(folder_working+'graphdata')

fig=plt.figure()
fig.set_size_inches(8, fig.get_figheight(), forward=True)
fig.set_size_inches(10, fig.get_figwidth(), forward=True)
ax=fig.add_subplot(1,1,1)
# calculate formation energy and plot
savename = myread.myplot(ax,plot_charge_labels_segment,lower_bound_plot=lower_bound_plot,defectlabeltextposition=defectlabeltextposition,xlimits=xlimits,ylimits=ylimits)

#########################################################
# There is some default  figure setup, but you may want to make changes
# plt is returned, use it to make any changes you want. For example:
#plt.legend()
#########################################################

plt.savefig(savename, format='jpeg', dpi=300, bbox_inches='tight')
