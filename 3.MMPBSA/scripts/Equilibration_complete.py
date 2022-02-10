import re
import sys
import os
import numpy as np
import fileinput

prefix = "complex"
top = "topol"

########################################
# equilibration, NVT and NPT 2ns

inequ1 = "in.equ0.mdp"
inequ1_h = open(inequ1, 'w')
content = """; VARIOUS PREPROCESSING OPTIONS
define          = -DPOSRES

; RUN CONTROL PARAMETERS
integrator      = md
dt              = 0.002
nsteps          = 1000000

; OUTPUT CONTROL OPTIONS
nstxout         = 0
nstvout         = 0
nstenergy       = 2500
nstlog          = 2500
nstxtcout       = 2500
xtc-precision   = 1000
energygrps      = System

; NEIGHBORSEARCHING PARAMETERS
nstlist         = 20
ns-type         = Grid
pbc             = xyz
rlist           = 1.2

; OPTIONS FOR ELECTROSTATICS AND VDW
coulombtype     = PME
pme_order       = 4
fourierspacing  = 0.12
rcoulomb        = 1.2
vdw-type        = cutoff
rvdw            = 1.2
vdw-modifier    = Force-switch
rvdw-switch     = 1.0

; Temperature coupling
tcoupl		= V-rescale	; modified Berendsen thermostat
tc-grps		= Protein Non-Protein	; two coupling groups - more accurate
tau_t		= 0.1	0.1	; time constant, in ps
ref_t		= 300   300	; reference temperature, one for each group, in K

; Dispersion correction
DispCorr        = EnerPres

; Pressure coupling
Pcoupl          = Parrinello-Rahman
Pcoupltype      = Isotropic
tau_p           = 2.0
compressibility = 4.5e-5
ref_p           = 1.0
refcoord_scaling = com

; GENERATE VELOCITIES FOR STARTUP RUN
gen_vel                 = yes    ; Assign velocities to particles by taking them randomly from a Maxwell distribution
gen_temp                = 300    ; Temperature to generate corresponding Maxwell distribution
gen_seed                = -1     ; Seed for (semi) random number generation. Different numbers give different sets of velocities

; OPTIONS FOR BONDS
constraints     = h-bonds
continuation    = no
constraint_algorithm    = lincs
lincs_iter      = 1
lincs_order     = 4
"""
inequ1_h.write(content)
inequ1_h.close()



if not os.path.exists(prefix + ".eq0.done"):
	if not os.path.exists(prefix + ".equ0.cpt"):
		# generate input files for simulation

		gromppcommand = "gmx grompp -f in.equ0.mdp -c " + prefix + ".min4.gro -p " + top + ".top -o " + prefix + ".equ0.tpr -po " + prefix + ".equ0.mdout.mdp -r " + prefix + ".min4.gro -maxwarn 10"
		os.system(gromppcommand)

		# start the simulation for the first time
		mdruncommand = "gmx mdrun -deffnm " + prefix + ".equ0 -v -nt 12"
		os.system(mdruncommand)
		os.system("cp " + prefix + ".equ0.gro " + prefix + ".eq0.done")

	else:

		# restart the simulation
		mdruncommand = "gmx mdrun  -deffnm " + prefix + ".equ0 -append -cpi " + prefix + ".equ0.cpt -v -nt 12"
		os.system(mdruncommand)
		os.system("cp " + prefix + ".equ0.gro " + prefix + ".eq0.done")
else:
	print "Equilibration NVT and NPT is COMPLETE"


########################################
# equilibration, all-but-water-restraint 2ns

inequ1 = "in.equ1.mdp"
inequ1_h = open(inequ1, 'w')
content = """; VARIOUS PREPROCESSING OPTIONS
define          = -DPOSRES_1

; RUN CONTROL PARAMETERS
integrator      = md
dt              = 0.002
nsteps          = 1000000

; OUTPUT CONTROL OPTIONS
nstxout         = 0
nstvout         = 0
nstenergy       = 2500
nstlog          = 2500
nstxtcout       = 2500
xtc-precision   = 1000
energygrps      = System

; NEIGHBORSEARCHING PARAMETERS
nstlist         = 20
ns-type         = Grid
pbc             = xyz
rlist           = 1.2

; OPTIONS FOR ELECTROSTATICS AND VDW
coulombtype     = PME
pme_order       = 4
fourierspacing  = 0.12
rcoulomb        = 1.2
vdw-type        = cutoff
rvdw            = 1.2

; Temperature coupling
tcoupl		= V-rescale	; modified Berendsen thermostat
tc-grps		= Protein Non-Protein	; two coupling groups - more accurate
tau_t		= 0.1	0.1	; time constant, in ps
ref_t		= 300   300	; reference temperature, one for each group, in K

; Dispersion correction
DispCorr        = EnerPres

; Pressure coupling
Pcoupl                   = Parrinello-Rahman
Pcoupltype               = Isotropic
tau_p                    = 2.0
compressibility          = 4.5e-5
ref_p                    = 1.0

refcoord_scaling = com

; GENERATE VELOCITIES FOR STARTUP RUN
gen_vel         = no

; OPTIONS FOR BONDS
constraints     = h-bonds
continuation    = yes
constraint_algorithm    = lincs
lincs_iter      = 1
lincs_order     = 4
"""
inequ1_h.write(content)
inequ1_h.close()


gsel1command = """gmx select -f """ + prefix + """.equ0.gro -s """ + prefix + """.equ0.tpr -select 'group "Protein"' -on 800.ndx"""
os.system(gsel1command)


grestr1command = "gmx genrestr -f " + prefix + ".equ0.gro -n 800.ndx -o 800.itp -fc 800 800 800"
os.system(grestr1command)

with open(top + ".top", "r") as in_file:
	buf = in_file.readlines()
in_file.close()
out_file = open(top + ".top", "w")
for line in buf:
	if line == "; Include Position restraint file\n":
		line = line + """#ifdef POSRES_1\n#include "800.itp"\n#endif\n\n"""
	out_file.write(line)
out_file.close()


if not os.path.exists(prefix + ".eq1.done"):
	if not os.path.exists(prefix + ".equ1.cpt"):
		# generate input files for simulation

		gromppcommand = "gmx grompp -f in.equ1.mdp -c " + prefix + ".equ0.gro -p " + top + ".top -o " + prefix + ".equ1.tpr -t " + prefix + ".equ0.cpt -po " + prefix + ".equ1.mdout.mdp -r " + prefix + ".equ0.gro -maxwarn 10"
		os.system(gromppcommand)

		# start the simulation for the first time
		mdruncommand = "gmx mdrun -deffnm " + prefix + ".equ1 -v -nt 12"
		os.system(mdruncommand)
		os.system("cp " + prefix + ".equ1.gro " + prefix + ".eq1.done")

	else:

		# restart the simulation
		mdruncommand = "gmx mdrun  -deffnm " + prefix + ".equ1 -append -cpi " + prefix + ".equ1.cpt -v -nt 12"
		os.system(mdruncommand)
		os.system("cp " + prefix + ".equ1.gro " + prefix + ".eq1.done")
else:
	print "Equilibration 1 is COMPLETE"


####################################################
# equilibration, main chain and Cbeta restraint 2ns

inequ2 = "in.equ2.mdp"
inequ2_h = open(inequ2, 'w')
content = """; VARIOUS PREPROCESSING OPTIONS
define          = -DPOSRES_2

; RUN CONTROL PARAMETERS
integrator      = md
dt              = 0.002
nsteps          = 1000000

; OUTPUT CONTROL OPTIONS
nstxout         = 0
nstvout         = 0
nstenergy       = 2500
nstlog          = 2500
nstxtcout       = 2500
xtc-precision   = 1000
energygrps      = System

; NEIGHBORSEARCHING PARAMETERS
nstlist         = 20
ns-type         = Grid
pbc             = xyz
rlist           = 1.2

; OPTIONS FOR ELECTROSTATICS AND VDW
coulombtype     = PME
pme_order       = 4
fourierspacing  = 0.12
rcoulomb        = 1.2
vdw-type        = cutoff
rvdw            = 1.2

; Temperature coupling
tcoupl		= V-rescale	; modified Berendsen thermostat
tc-grps		= Protein Non-Protein	; two coupling groups - more accurate
tau_t		= 0.1	0.1	; time constant, in ps
ref_t		= 300   300	; reference temperature, one for each group, in K

; Dispersion correction
DispCorr        = EnerPres

; Pressure coupling
Pcoupl                   = Parrinello-Rahman
Pcoupltype               = Isotropic
tau_p                    = 2.0
compressibility          = 4.5e-5
ref_p                    = 1.0

refcoord_scaling = com

; GENERATE VELOCITIES FOR STARTUP RUN
gen_vel         = no

; OPTIONS FOR BONDS
constraints     = h-bonds
continuation    = yes
constraint_algorithm    = lincs
lincs_iter      = 1
lincs_order     = 4
"""
inequ2_h.write(content)
inequ2_h.close()

gsel1command = """gmx select -f """ + prefix + """.equ0.gro -s """ + prefix + """.equ0.tpr -select 'group "MainChain+Cb"' -on 600.ndx"""
os.system(gsel1command)


grestr1command = "gmx genrestr  -f " + prefix + ".equ0.gro -n 600.ndx -o 600.itp -fc 600 600 600"
os.system(grestr1command)

with open(top + ".top", "r") as in_file:
	buf = in_file.readlines()
in_file.close()
out_file = open(top + ".top", "w")
for line in buf:
	if line == "; Include Position restraint file\n":
		line = line + """#ifdef POSRES_2\n#include "600.itp"\n#endif\n\n"""
	out_file.write(line)
out_file.close()

if not os.path.exists(prefix + ".eq2.done"):
	if not os.path.exists(prefix + ".equ2.cpt"):
		# generate input files for simulation

		gromppcommand = "gmx grompp  -f in.equ2.mdp -c " + prefix + ".equ1.gro -p " + top + ".top -o " + prefix + ".equ2.tpr -t " + prefix + ".equ1.cpt -po " + prefix + ".equ2.mdout.mdp -r " + prefix + ".equ1.gro -maxwarn 10"
		os.system(gromppcommand)

		# start the simulation for the first time
		mdruncommand = "gmx mdrun  -deffnm " + prefix + ".equ2 -v -nt 12"
		os.system(mdruncommand)
		os.system("cp " + prefix + ".equ2.gro " + prefix + ".eq2.done")
	else:

		# restart the simulation
		mdruncommand = "gmx -deffnm " + prefix + ".equ2 -append -cpi " + prefix + ".equ2.cpt -v -nt 12"
		os.system(mdruncommand)
		os.system("cp " + prefix + ".equ2.gro " + prefix + ".eq2.done")
else:
	print "Equilibration 2 is COMPLETE"

################################################
# equilibration, carbon-skeleton restraint 2ns

inequ3 = "in.equ3.mdp"
inequ3_h = open(inequ3, 'w')
content = """; VARIOUS PREPROCESSING OPTIONS
define          = -DPOSRES_3

; RUN CONTROL PARAMETERS
integrator      = md
dt              = 0.002
nsteps          = 1000000

; OUTPUT CONTROL OPTIONS
nstxout         = 0
nstvout         = 0
nstenergy       = 2500
nstlog          = 2500
nstxtcout       = 2500
xtc-precision   = 1000
energygrps      = System

; NEIGHBORSEARCHING PARAMETERS
nstlist         = 20
ns-type         = Grid
pbc             = xyz
rlist           = 1.2

; OPTIONS FOR ELECTROSTATICS AND VDW
coulombtype     = PME
pme_order       = 4
fourierspacing  = 0.12
rcoulomb        = 1.2
vdw-type        = cutoff
rvdw            = 1.2

; Temperature coupling
tcoupl		= V-rescale	; modified Berendsen thermostat
tc-grps		= Protein Non-Protein	; two coupling groups - more accurate
tau_t		= 0.1	0.1	; time constant, in ps
ref_t		= 300   300	; reference temperature, one for each group, in K

; Dispersion correction
DispCorr        = EnerPres

; Pressure coupling
Pcoupl                   = Parrinello-Rahman
Pcoupltype               = Isotropic
tau_p                    = 2.0
compressibility          = 4.5e-5
ref_p                    = 1.0

refcoord_scaling = com

; GENERATE VELOCITIES FOR STARTUP RUN
gen_vel         = no

; OPTIONS FOR BONDS
constraints     = h-bonds
continuation    = yes
constraint_algorithm    = lincs
lincs_iter      = 1
lincs_order     = 4
  """
inequ3_h.write(content)
inequ3_h.close()

gsel1command = """gmx select -f """ + prefix + """.equ0.gro -s """ + prefix + """.equ0.tpr -select 'group "MainChain"' -on 400.ndx"""
os.system(gsel1command)


grestr1command = "gmx genrestr  -f " + prefix + ".equ0.gro -n 400.ndx -o 400.itp -fc 400 400 400"
os.system(grestr1command)

with open(top + ".top", "r") as in_file:
	buf = in_file.readlines()
in_file.close()
out_file = open(top + ".top", "w")
for line in buf:
	if line == "; Include Position restraint file\n":
		line = line + """#ifdef POSRES_3\n#include "400.itp"\n#endif\n\n"""
	out_file.write(line)
out_file.close()


if not os.path.exists(prefix + ".eq3.done"):
	if not os.path.exists(prefix + ".equ3.cpt"):
		# generate input files for simulation

		gromppcommand = "gmx grompp  -f in.equ3.mdp -c " + prefix + ".equ2.gro -p " + top + ".top -o " + prefix + ".equ3.tpr -t " + prefix + ".equ2.cpt -po " + prefix + ".equ3.mdout.mdp -r " + prefix + ".equ2.gro -maxwarn 10"
		os.system(gromppcommand)

		# start the simulation for the first time
		mdruncommand = "gmx mdrun  -deffnm " + prefix + ".equ3 -v -nt 12"
		os.system(mdruncommand)
		os.system("cp " + prefix + ".equ3.gro " + prefix + ".eq3.done")
	else:

		# restart the simulation
		mdruncommand = "gmx mdrun   -deffnm " + prefix + ".equ3 -append -cpi " + prefix + ".equ3.cpt -v -nt 12"
		os.system(mdruncommand)
		os.system("cp " + prefix + ".equ3.gro " + prefix + ".eq3.done")
else:
	print "Equilibration 3 is COMPLETE"

#################################################
# equilibration, carbon skeleton restraint 2 ns

inequ4 = "in.equ4.mdp"
inequ4_h = open(inequ4, 'w')
content = """; VARIOUS PREPROCESSING OPTIONS
define          = -DPOSRES_4

; RUN CONTROL PARAMETERS
integrator      = md
dt              = 0.002
nsteps          = 1000000

; OUTPUT CONTROL OPTIONS
nstxout         = 0
nstvout         = 0
nstenergy       = 2500
nstlog          = 2500
nstxtcout       = 2500
xtc-precision   = 1000
energygrps      = System

; NEIGHBORSEARCHING PARAMETERS
nstlist         = 20
ns-type         = Grid
pbc             = xyz
rlist           = 1.2

; OPTIONS FOR ELECTROSTATICS AND VDW
coulombtype     = PME
pme_order       = 4
fourierspacing  = 0.12
rcoulomb        = 1.2
vdw-type        = cutoff
rvdw            = 1.2

; Temperature coupling
tcoupl		= V-rescale	; modified Berendsen thermostat
tc-grps		= Protein Non-Protein	; two coupling groups - more accurate
tau_t		= 0.1	0.1	; time constant, in ps
ref_t		= 300   300	; reference temperature, one for each group, in K

; Dispersion correction
DispCorr        = EnerPres

; Pressure coupling
Pcoupl                   = Parrinello-Rahman
Pcoupltype               = Isotropic
tau_p                    = 2.0
compressibility          = 4.5e-5
ref_p                    = 1.0

refcoord_scaling = com

; GENERATE VELOCITIES FOR STARTUP RUN
gen_vel         = no

; OPTIONS FOR BONDS
constraints     = h-bonds
continuation    = yes
constraint_algorithm    = lincs
lincs_iter      = 1
lincs_order     = 4
  """
inequ4_h.write(content)
inequ4_h.close()

gsel1command = """gmx select -f """ + prefix + """.equ0.gro -s """ + prefix + """.equ0.tpr -select 'group "Backbone"' -on 200.ndx"""
os.system(gsel1command)


grestr1command = "gmx genrestr  -f " + prefix + ".equ0.gro -n 200.ndx -o 200.itp -fc 200 200 200"
os.system(grestr1command)

with open(top + ".top", "r") as in_file:
	buf = in_file.readlines()
in_file.close()
out_file = open(top + ".top", "w")
for line in buf:
	if line == "; Include Position restraint file\n":
		line = line + """#ifdef POSRES_4\n#include "200.itp"\n#endif\n\n"""
	out_file.write(line)
out_file.close()


if not os.path.exists(prefix + ".eq4.done"):
	if not os.path.exists(prefix + ".equ4.cpt"):
		# generate input files for simulation

		gromppcommand = "gmx grompp  -f in.equ4.mdp -c " + prefix + ".equ3.gro -p " + top + ".top -o " + prefix + ".equ4.tpr -t " + prefix + ".equ3.cpt -po " + prefix + ".equ4.mdout.mdp -r " + prefix + ".equ3.gro -maxwarn 10"
		os.system(gromppcommand)

		# start the simulation for the first time
		mdruncommand = "gmx mdrun  -deffnm " + prefix + ".equ4 -v -nt 12"
		os.system(mdruncommand)
		os.system("cp " + prefix + ".equ4.gro " + prefix + ".eq4.done")
	else:

		# restart the simulation
		mdruncommand = "gmx mdrun  -deffnm " + prefix + ".equ4 -append -cpi " + prefix + ".equ4.cpt -v -nt 12"
		os.system(mdruncommand)
		os.system("cp " + prefix + ".equ4.gro " + prefix + ".eq4.done")
else:
	print "Equilibration 4 is COMPLETE"

############################################
# equilibration, alpha carbon restraint 3ns

inequ5 = "in.equ5.mdp"
inequ5_h = open(inequ5, 'w')
content = """; VARIOUS PREPROCESSING OPTIONS
define          = -DPOSRES_5

; RUN CONTROL PARAMETERS
integrator      = md
dt              = 0.002
nsteps          = 1500000

; OUTPUT CONTROL OPTIONS
nstxout         = 0
nstvout         = 0
nstenergy       = 2500
nstlog          = 2500
nstxtcout       = 2500
xtc-precision   = 1000
energygrps      = System

; NEIGHBORSEARCHING PARAMETERS
nstlist         = 20
ns-type         = Grid
pbc             = xyz
rlist           = 1.2

; OPTIONS FOR ELECTROSTATICS AND VDW
coulombtype     = PME
pme_order       = 4
fourierspacing  = 0.12
rcoulomb        = 1.2
vdw-type        = cutoff
rvdw            = 1.2

; Temperature coupling
tcoupl		= V-rescale	; modified Berendsen thermostat
tc-grps		= Protein Non-Protein	; two coupling groups - more accurate
tau_t		= 0.1	0.1	; time constant, in ps
ref_t		= 300   300	; reference temperature, one for each group, in K

; Dispersion correction
DispCorr        = EnerPres

; Pressure coupling
Pcoupl                   = Parrinello-Rahman
Pcoupltype               = Isotropic
tau_p                    = 2.0
compressibility          = 4.5e-5
ref_p                    = 1.0

refcoord_scaling = com

; GENERATE VELOCITIES FOR STARTUP RUN
gen_vel         = no

; OPTIONS FOR BONDS
constraints     = h-bonds
continuation    = yes
constraint_algorithm    = lincs
lincs_iter      = 1
lincs_order     = 4
    """
inequ5_h.write(content)
inequ5_h.close()

gsel1command = """gmx select -f """ + prefix + """.equ0.gro -s """ + prefix + """.equ0.tpr -select 'CA' -on 100.ndx"""
os.system(gsel1command)


grestr4command = "gmx genrestr  -f " + prefix + ".equ0.gro -n 100.ndx -o 100.itp -fc 100 100 100"
os.system(grestr4command)

with open(top + ".top", "r") as in_file:
	buf = in_file.readlines()
in_file.close()
out_file = open(top + ".top", "w")
for line in buf:
	if line == "; Include Position restraint file\n":
		line = line + """#ifdef POSRES_5\n#include "100.itp"\n#endif\n\n"""
	out_file.write(line)
out_file.close()

if not os.path.exists(prefix + ".eq5.done"):
	if not os.path.exists(prefix + ".equ5.cpt"):
		# generate input files for simulation

		gromppcommand = "gmx grompp  -f in.equ5.mdp -c " + prefix + ".equ4.gro -p " + top + ".top -o " + prefix + ".equ5.tpr -t " + prefix + ".equ4.cpt -po " + prefix + ".equ5.mdout.mdp -r " + prefix + ".equ4.gro -maxwarn 10"
		os.system(gromppcommand)

		# start the simulation for the first time
		mdruncommand = "gmx mdrun  -deffnm " + prefix + ".equ5 -v -nt 12"
		os.system(mdruncommand)
		os.system("cp " + prefix + ".equ5.gro " + prefix + ".eq5.done")
	else:

		# restart the simulation
		mdruncommand = "gmx mdrun  -deffnm " + prefix + ".equ5 -append -cpi " + prefix + ".equ5.cpt -v -nt 12"
		os.system(mdruncommand)
		os.system("cp " + prefix + ".equ5.gro " + prefix + ".eq5.done")
else:
  print "Equilibration 5 is COMPLETE"

############################################
# equilibration, alpha carbon restraint 3ns

inequ6 = "in.equ6.mdp"
inequ6_h = open(inequ6, 'w')
content = """; VARIOUS PREPROCESSING OPTIONS
define          = -DPOSRES_6

; RUN CONTROL PARAMETERS
integrator      = md
dt              = 0.002
nsteps          = 1500000

; OUTPUT CONTROL OPTIONS
nstxout         = 0
nstvout         = 0
nstenergy       = 2500
nstlog          = 2500
nstxtcout       = 2500
xtc-precision   = 1000
energygrps      = System

; NEIGHBORSEARCHING PARAMETERS
nstlist         = 20
ns-type         = Grid
pbc             = xyz
rlist           = 1.2

; OPTIONS FOR ELECTROSTATICS AND VDW
coulombtype     = PME
pme_order       = 4
fourierspacing  = 0.12
rcoulomb        = 1.2
vdw-type        = cutoff
rvdw            = 1.2

; Temperature coupling
tcoupl		= V-rescale	; modified Berendsen thermostat
tc-grps		= Protein Non-Protein	; two coupling groups - more accurate
tau_t		= 0.1	0.1	; time constant, in ps
ref_t		= 300   300	; reference temperature, one for each group, in K

; Dispersion correction
DispCorr        = EnerPres

; Pressure coupling
Pcoupl                   = Parrinello-Rahman
Pcoupltype               = Isotropic
tau_p                    = 2.0
compressibility          = 4.5e-5
ref_p                    = 1.0

refcoord_scaling = com

; GENERATE VELOCITIES FOR STARTUP RUN
gen_vel         = no

; OPTIONS FOR BONDS
constraints     = h-bonds
continuation    = yes
constraint_algorithm    = lincs
lincs_iter      = 1
lincs_order     = 4
    """
inequ6_h.write(content)
inequ6_h.close()

grestr5command = "gmx genrestr  -f " + prefix + ".equ0.gro -n 100.ndx -o 50.itp -fc 50 50 50"
os.system(grestr5command)

with open(top + ".top", "r") as in_file:
	buf = in_file.readlines()
in_file.close()
out_file = open(top + ".top", "w")
for line in buf:
	if line == "; Include Position restraint file\n":
		line = line + """\n#ifdef POSRES_6\n#include "50.itp"\n#endif\n\n"""
	out_file.write(line)
out_file.close()

if not os.path.exists(prefix + ".eq6.done"):
	if not os.path.exists(prefix + ".equ6.cpt"):
		# generate input files for simulation

		gromppcommand = "gmx grompp  -f in.equ6.mdp -c " + prefix + ".equ5.gro -p " + top + ".top -o " + prefix + ".equ6.tpr -t " + prefix + ".equ5.cpt -po " + prefix + ".equ6.mdout.mdp -r " + prefix + ".equ5.gro -maxwarn 10"
		os.system(gromppcommand)

		# start the simulation for the first time
		mdruncommand = "gmx mdrun  -deffnm " + prefix + ".equ6 -v -nt 12"
		os.system(mdruncommand)
		os.system("cp " + prefix + ".equ6.gro " + prefix + ".eq6.done")
	else:

		# restart the simulation
		mdruncommand = "gmx mdrun  -deffnm " + prefix + ".equ6 -append -cpi " + prefix + ".equ6.cpt -v -nt 12"
		os.system(mdruncommand)
		os.system("cp " + prefix + ".equ6.gro " + prefix + ".eq6.done")
else:
	print "Equilibration 6 is COMPLETE"
	sys.exit("\n>>>All equilibrations are completed! Moving to next phase...\n")
