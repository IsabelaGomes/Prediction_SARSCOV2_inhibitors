import os

prefix = "complex"
top = "topol"

############################################ 
# simulation MD, fix time

convertcommand = "gmx convert-tpr -s " + prefix + ".SIM20.tpr -extend 80000 -o " + prefix + ".SIM100.tpr" 
os.system(convertcommand)

mdruncommand = "gmx mdrun -deffnm " + prefix + ".SIM100 -append -cpi " + prefix + ".SIM20.cpt -v -nt 24"
os.system(mdruncommand)

