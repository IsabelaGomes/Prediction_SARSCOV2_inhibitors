import re
import sys
import os

prefix = "complex"
top = "topol"

############################################ 
# simulation MD, production run

inmd = "in.SIM.mdp"
inmd_h = open(inmd, 'w')
content = """; RUN CONTROL PARAMETERS
integrator               = md
dt                       = 0.002
nsteps                   = 5000000

; OUTPUT CONTROL OPTIONS
nstxout         = 0
nstvout         = 0
nstenergy       = 2500
nstlog          = 2500
nstxtcout       = 2500
xtc-precision   = 1000
energygrps      = System

; NEIGHBORSEARCHING PARAMETERS
nstlist                  = 20
ns-type                  = Grid
pbc                      = xyz
rlist                    = 1.2

; OPTIONS FOR ELECTROSTATICS AND VDW
coulombtype              = PME
pme_order                = 4    ; cubic interpolation
fourierspacing           = 0.12 ; grid spacing for FFT
rcoulomb                 = 1.2
vdw-type                 = cutoff
rvdw                     = 1.2

; Temperature coupling
tcoupl		= V-rescale	; modified Berendsen thermostat
tc-grps		= Protein Non-Protein	; two coupling groups - more accurate
tau_t		= 0.1	0.1	; time constant, in ps
ref_t		= 300   300	; reference temperature, one for each group, in K

;  Dispersion correction
DispCorr                 = EnerPres ; account for vdw cut-off

; Pressure coupling
Pcoupl                   = Parrinello-Rahman
Pcoupltype               = Isotropic
tau_p                    = 2.0
compressibility          = 4.5e-5
ref_p                    = 1.0

; GENERATE VELOCITIES FOR STARTUP RUN
gen_vel                 = no

; OPTIONS FOR BONDS
constraints             = h-bonds
continuation            = yes
constraint_algorithm    = lincs
lincs_iter              = 1
lincs_order             = 4
  """
inmd_h.write(content)
inmd_h.close()

if not os.path.exists(prefix + ".SIM.done"):
	if not os.path.exists(prefix + ".SIM.cpt"):
		# generate input files for simulation

		gromppcommand = "gmx grompp -f in.SIM.mdp -c " + prefix + ".equ6.gro -p " + top + ".top -o " + prefix + ".SIM.tpr -t " + prefix + ".equ6.cpt -po " + prefix + ".SIM.mdout.mdp"
		os.system(gromppcommand)

		# start the simulation for the first time
		mdruncommand = "gmx mdrun -deffnm " + prefix + ".SIM -v -nt 12"
		os.system(mdruncommand)

		mvcommand = "mv " + prefix + ".SIM.gro " + prefix + ".SIM.done"
		os.system(mvcommand)


	else:
		# restart the simulation
		mdruncommand = "gmx mdrun -deffnm " + prefix + ".SIM -append -cpi " + prefix + ".SIM.cpt -v -nt 12"
		os.system(mdruncommand)

		mvcommand = "mv " + prefix + ".SIM.gro " + prefix + ".SIM.done"
		os.system(mvcommand)

else:
	print "Uhuuuuuul!! This simulation is COMPLETE!"
