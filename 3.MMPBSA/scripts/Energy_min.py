import os

prefix = "complex"
top = "topol"

##########################
# preparation for MD: box

inmin0 = "in.min0.mdp"
inmin0_h = open(inmin0, 'w')
content = """

; Define can be used to control processes
define          = -DFLEXIBLE    ; Use flexible water model

; Parameters describing what to do, when to stop and what to save
integrator      = steep
emtol           = 100.0
nsteps          = -1
nstenergy       = 1
energygrps      = System

; Parameters describing how to find the neighbors of each atom and how to calculate the interactions
cutoff-scheme   = Verlet
nstlist         = 20
ns_type         = grid
coulombtype     = PME
vdw-type        = cutoff
vdw-modifier    = force-switch
rlist           = 1.2
rcoulomb        = 1.2
rvdw            = 1.2
rvdw-switch     = 1.0
constraints     = none
pbc             = xyz

"""
inmin0_h.write(content)
inmin0_h.close()

editconfcommand = "gmx editconf -f " + prefix + ".gro -c -bt dodecahedron -d 1.4 -o " + prefix + ".pbc.gro"
os.system(editconfcommand)

gromppcommand = "gmx grompp -f in.min0.mdp -c " + prefix + ".pbc.gro -p " + top + ".top -o " + prefix + ".pbc.min0.tpr -maxwarn 10"
os.system(gromppcommand)

mdruncommand = "gmx mdrun -deffnm " + prefix + ".pbc.min0 -v -nt 12"
os.system(mdruncommand)		

print "The box is created!" 

###################################
# preparation for MD: solvatation

inmin1 = "in.min1.mdp"
inmin1_h = open(inmin1, 'w')
content = """

; Define can be used to control processes

; Parameters describing what to do, when to stop and what to save
integrator      = steep
emtol           = 100.0
nsteps          = -1
nstenergy       = 1
energygrps      = System

; Parameters describing how to find the neighbors of each atom and how to calculate the interactions
cutoff-scheme   = Verlet
nstlist         = 20
ns_type         = grid
coulombtype     = PME
vdw-type        = cutoff
vdw-modifier    = force-switch
rlist           = 1.2
rcoulomb        = 1.2
rvdw            = 1.2
rvdw-switch     = 1.0
constraints     = none
pbc             = xyz

"""
inmin1_h.write(content)
inmin1_h.close()

solvatecommand = "gmx solvate -cp " + prefix + ".pbc.min0.gro -cs spc216.gro -p " + top + ".top -o " + prefix + ".wat.gro"
os.system(solvatecommand)

gromppcommand = "gmx grompp -f in.min1.mdp -c " + prefix + ".wat.gro -p " + top + ".top -o " + prefix + ".wat.min1.tpr -maxwarn 10"
os.system(gromppcommand)

mdruncommand = "gmx mdrun -deffnm " + prefix + ".wat.min1 -v -nt 12"
os.system(mdruncommand)		

print "The sistem is solvated!"


#####################################
# preparation for MD: neutralization

inmin2 = "in.min2.mdp"
inmin2_h = open(inmin2, 'w')
content = """

; Define can be used to control processes
define          = -DFLEXIBLE  

; Parameters describing what to do, when to stop and what to save
integrator      = steep
emtol           = 1.0
nsteps          = -1
nstenergy       = 1
energygrps      = System

; Parameters describing how to find the neighbors of each atom and how to calculate the interactions
cutoff-scheme   = Verlet
nstlist         = 1
ns_type         = grid
coulombtype     = PME
vdw-type        = cutoff
vdw-modifier    = force-switch
rlist           = 1.2
rcoulomb        = 1.2
rvdw            = 1.2
rvdw-switch     = 1.0
constraints     = none
pbc             = xyz

"""
inmin2_h.write(content)
inmin2_h.close()

gromppcommand = "gmx grompp -f in.min2.mdp -c " + prefix + ".ion.gro -p " + top + ".top -o " + prefix + ".ion.min2.tpr -maxwarn 10"
os.system(gromppcommand)

mdruncommand = "gmx mdrun -deffnm " + prefix + ".ion.min2 -v -nt 12"
os.system(mdruncommand)		

print "The sistem is neutralized!"


#########################################
# preparation for MD: final minimization

inmin3 = "in.min3.mdp"
inmin3_h = open(inmin3, 'w')
content = """

; Define can be used to control processes
define          = -DFLEXIBLE  

; Parameters describing what to do, when to stop and what to save
integrator      = steep
emtol           = 1.0
nsteps          = -1
nstenergy       = 1
energygrps      = System

; Parameters describing how to find the neighbors of each atom and how to calculate the interactions
cutoff-scheme   = Verlet
nstlist         = 1
ns_type         = grid
coulombtype     = PME
vdw-type        = cutoff
vdw-modifier    = force-switch
rlist           = 1.2
rcoulomb        = 1.2
rvdw            = 1.2
rvdw-switch     = 1.0
constraints     = none
pbc             = xyz

"""
inmin3_h.write(content)
inmin3_h.close()

#steepest descent
gromppcommand = "gmx grompp -f in.min3.mdp -c " + prefix + ".ion.min2.gro -p " + top + ".top -o " + prefix + ".min3.tpr -maxwarn 10"
os.system(gromppcommand)

mdruncommand = "gmx mdrun -deffnm " + prefix + ".min3 -v -nt 12"
os.system(mdruncommand)	

inmin4 = "in.min4.mdp"
inmin4_h = open(inmin4, 'w')
content = """

; Define can be used to control processes
define          = -DFLEXIBLE    

; Parameters describing what to do, when to stop and what to save
integrator      = cg
emtol           = 1.0
nsteps          = -1
nstenergy       = 1
energygrps      = System

; Parameters describing how to find the neighbors of each atom and how to calculate the interactions
cutoff-scheme   = Verlet
nstlist         = 1
ns_type         = grid
coulombtype     = PME
vdw-type        = cutoff
vdw-modifier    = force-switch
rlist           = 1.2
rcoulomb        = 1.2
rvdw            = 1.2
rvdw-switch     = 1.0
constraints     = none
pbc             = xyz

"""
inmin4_h.write(content)
inmin4_h.close()

#conjugate gradient
gromppcommand = "gmx grompp -f in.min4.mdp -c " + prefix + ".min3.gro -p " + top + ".top -o " + prefix + ".min4.tpr -maxwarn 10"
os.system(gromppcommand)

mdruncommand = "gmx mdrun -deffnm " + prefix + ".min4 -v -nt 12"
os.system(mdruncommand)	

print "The energy is minimized!"