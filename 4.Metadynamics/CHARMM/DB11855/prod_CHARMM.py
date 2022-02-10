import os

config0 = "productive0.conf"
config0_h = open(config0, 'w')
content = """
	#############################################################
	## JOB DESCRIPTION                                         ##
	#############################################################

	#Minimização - Mpro e ligante rígidos
	#Restrição harmônica de 2 kcal/mol/A^2

	#############################################################
	## ADJUSTABLE PARAMETERS                                   ##
	#############################################################

	structure          complex_ion.psf
	coordinates        complex_ion.pdb
	set temperature    300
	set outputname     complex_dm_1
	firsttimestep      0
	Binaryoutput       yes

	#############################################################
	## SIMULATION PARAMETERS                                   ##
	#############################################################

	paraTypeCharmm	    on
	parameters          ../par_all36_prot.prm
	parameters          ../toppar_water_ions.str
	parameters	    DB11855.par
	temperature         $temperature

	#Dinâmica com restrição 
	constraints         on
	consexp             2
	consref             rest0.pdb
	conskfile           rest0.pdb
	conskcol            B #coluna de b-factor

	# Force-Field Parameters
	exclude             scaled1-4
	1-4scaling          1.0
	cutoff              12.
	switching           on
	switchdist          10.
	pairlistdist        13.5

	# Integrator Parameters
	timestep            2.0  ;# 2.0 fs/step
	rigidBonds          all  ;# needed for 2fs steps
	nonbondedFreq       1
	fullElectFrequency  2  
	stepspercycle       10

	# Constant Temperature Control
	langevin            on    ;# do langevin dynamics
	langevinDamping     2     ;# damping coefficient (gamma) of 2/ps
	langevinTemp        $temperature
	langevinHydrogen    off    ;# don't couple langevin bath to hydrogens

	# Periodic Boundary Conditions
	cellBasisVector1   64.    0.   0. 
	cellBasisVector2    0.  104.   0.
	cellBasisVector3    0.    0.  76.
	cellOrigin         1.4842796325683594 -2.407818555831909 -1.7820888757705688
	wrapAll             on

	# PME (for full-system periodic electrostatics)
	PME                 yes
	PMEGridSpacing      1.0
	PMEGridSizeX        81  #3
	PMEGridSizeY        128 #2
	PMEGridSizeZ        81  #3

	# Constant Pressure Control (variable volume)
	useGroupPressure      yes ;# needed for rigidBonds
	useFlexibleCell       no
	useConstantArea       no
	langevinPiston        on
	langevinPistonTarget  1.01325 ;#  in bar -> 1 atm
	langevinPistonPeriod  100.
	langevinPistonDecay   50.
	langevinPistonTemp    $temperature

	# Output
	outputName          $outputname
	restartfreq         1000     ;# 1000steps = every 2 ps
	dcdfreq             2000
	outputEnergies      1000

	#############################################################
	## EXECUTION SCRIPT                                        ##
	#############################################################

	# Minimization
	minimize            250000 ;#500 ps

"""
config0_h.write(content)
config0_h.close()

namdcommand = "charmrun namd2 ++local +p${NCPUS} productive0.conf"
os.system(namdcommand)

print("Minimização - Mpro e ligante rígidos - finalizada")

#############################################################

config1 = "productive1.conf"
config1_h = open(config1, 'w')
content = """
	#############################################################
	## JOB DESCRIPTION                                         ##
	#############################################################

	#Minimização - Mpro (exceto cadeia lateral) e ligante rígidos
	#Restrição harmônica de 2 kcal/mol/A^2

	#############################################################
	## ADJUSTABLE PARAMETERS                                   ##
	#############################################################

	#Reiniciando a simulação
	bincoordinates     complex_dm_1.coor
	binvelocities      complex_dm_1.vel
	extendedSystem     complex_dm_1.xsc

	structure          complex_ion.psf
	coordinates        complex_ion.pdb
	set temperature    300
	set outputname     complex_dm_2
	firsttimestep      0

	Binaryoutput       yes

	#############################################################
	## SIMULATION PARAMETERS                                   ##
	#############################################################

	paraTypeCharmm	    on
	parameters          ../par_all36_prot.prm
	parameters          ../toppar_water_ions.str
	parameters	    DB11855.par

	#Dinâmica com restrição 
	constraints         on
	consexp             2
	consref             rest1.pdb
	conskfile           rest1.pdb
	conskcol            B #coluna de b-factor

	# Force-Field Parameters
	exclude             scaled1-4
	1-4scaling          1.0
	cutoff              12.
	switching           on
	switchdist          10.
	pairlistdist        13.5

	# Integrator Parameters
	timestep            2.0  ;# 2.0 fs/step
	rigidBonds          all  ;# needed for 2fs steps
	nonbondedFreq       1
	fullElectFrequency  2  
	stepspercycle       10

	# Constant Temperature Control
	langevin            on    ;# do langevin dynamics
	langevinDamping     2     ;# damping coefficient (gamma) of 2/ps
	langevinTemp        $temperature
	langevinHydrogen    off    ;# don't couple langevin bath to hydrogens

	# Periodic Boundary Conditions
	cellBasisVector1   64.    0.   0. 
	cellBasisVector2    0.  104.   0.
	cellBasisVector3    0.    0.  76.
	cellOrigin         1.4842796325683594 -2.407818555831909 -1.7820888757705688
	wrapAll             on

	# PME (for full-system periodic electrostatics)
	PME                 yes
	PMEGridSpacing      1.0
	PMEGridSizeX        81  #3
	PMEGridSizeY        128 #2
	PMEGridSizeZ        81  #3

	# Constant Pressure Control (variable volume)
	useGroupPressure      yes ;# needed for rigidBonds
	useFlexibleCell       no
	useConstantArea       no
	langevinPiston        on
	langevinPistonTarget  1.01325 ;#  in bar -> 1 atm
	langevinPistonPeriod  100.
	langevinPistonDecay   50.
	langevinPistonTemp    $temperature

	# Output
	outputName          $outputname
	restartfreq         1000     ;# 1000steps = every 2 ps
	dcdfreq             2000
	outputEnergies      1000

	#############################################################
	## EXECUTION SCRIPT                                        ##
	#############################################################

	# Minimization
	minimize            250000 ;#500 ps

"""
config1_h.write(content)
config1_h.close()

namdcommand = "charmrun namd2 ++local +p${NCPUS} productive1.conf"
os.system(namdcommand)

print("Minimização - Mpro (exceto cadeia lateral) e ligante rígidos - finalizada")

#############################################################

config2 = "productive2.conf"
config2_h = open(config2, 'w')
content = """
	#############################################################
	## JOB DESCRIPTION                                         ##
	#############################################################

	#Minimização - Mpro (exceto cadeia lateral) rígida
	#Restrição harmônica de 2 kcal/mol/A^2

	#############################################################
	## ADJUSTABLE PARAMETERS                                   ##
	#############################################################

	#Reiniciando a simulação
	bincoordinates     complex_dm_2.coor
	binvelocities      complex_dm_2.vel
	extendedSystem     complex_dm_2.xsc

	structure          complex_ion.psf
	coordinates        complex_ion.pdb
	set temperature    300
	set outputname     complex_dm_3
	firsttimestep      0

	Binaryoutput       yes

	#############################################################
	## SIMULATION PARAMETERS                                   ##
	#############################################################

	paraTypeCharmm	    on
	parameters          ../par_all36_prot.prm
	parameters          ../toppar_water_ions.str
	parameters	    DB11855.par

	#Dinâmica com restrição 
	constraints         on
	consexp             2
	consref             rest2.pdb
	conskfile           rest2.pdb
	conskcol            B #coluna de b-factor

	# Force-Field Parameters
	exclude             scaled1-4
	1-4scaling          1.0
	cutoff              12.
	switching           on
	switchdist          10.
	pairlistdist        13.5

	# Integrator Parameters
	timestep            2.0  ;# 2.0 fs/step
	rigidBonds          all  ;# needed for 2fs steps
	nonbondedFreq       1
	fullElectFrequency  2  
	stepspercycle       10

	# Constant Temperature Control
	langevin            on    ;# do langevin dynamics
	langevinDamping     2     ;# damping coefficient (gamma) of 2/ps
	langevinTemp        $temperature
	langevinHydrogen    off    ;# don't couple langevin bath to hydrogens

	# Periodic Boundary Conditions
	cellBasisVector1   64.    0.   0. 
	cellBasisVector2    0.  104.   0.
	cellBasisVector3    0.    0.  76.
	cellOrigin         1.4842796325683594 -2.407818555831909 -1.7820888757705688
	wrapAll             on

	# PME (for full-system periodic electrostatics)
	PME                 yes
	PMEGridSpacing      1.0
	PMEGridSizeX        81  #3
	PMEGridSizeY        128 #2
	PMEGridSizeZ        81  #3

	# Constant Pressure Control (variable volume)
	useGroupPressure      yes ;# needed for rigidBonds
	useFlexibleCell       no
	useConstantArea       no
	langevinPiston        on
	langevinPistonTarget  1.01325 ;#  in bar -> 1 atm
	langevinPistonPeriod  100.
	langevinPistonDecay   50.
	langevinPistonTemp    $temperature

	# Output
	outputName          $outputname
	restartfreq         1000     ;# 1000steps = every 2 ps
	dcdfreq             2000
	outputEnergies      1000

	#############################################################
	## EXECUTION SCRIPT                                        ##
	#############################################################

	# Minimization
	minimize            250000 ;#500 ps

"""
config2_h.write(content)
config2_h.close()

namdcommand = "charmrun namd2 ++local +p${NCPUS} productive2.conf"
os.system(namdcommand)

print("Minimização - Mpro (exceto cadeia lateral) rígida - finalizada")

#############################################################

config3 = "productive3.conf"
config3_h = open(config3, 'w')
content = """
	#############################################################
	## JOB DESCRIPTION                                         ##
	#############################################################

	#Minimização - sistema livre
	#Restrição harmônica de 2 kcal/mol/A^2

	#############################################################
	## ADJUSTABLE PARAMETERS                                   ##
	#############################################################

	#Reiniciando a simulação
	bincoordinates     complex_dm_3.coor
	binvelocities      complex_dm_3.vel
	extendedSystem     complex_dm_3.xsc

	structure          complex_ion.psf
	coordinates        complex_ion.pdb
	set temperature    300
	set outputname     complex_dm_4
	firsttimestep      0

	Binaryoutput       yes

	#############################################################
	## SIMULATION PARAMETERS                                   ##
	#############################################################

	paraTypeCharmm	    on
	parameters          ../par_all36_prot.prm
	parameters          ../toppar_water_ions.str
	parameters	    DB11855.par

	# Force-Field Parameters
	exclude             scaled1-4
	1-4scaling          1.0
	cutoff              12.
	switching           on
	switchdist          10.
	pairlistdist        13.5

	# Integrator Parameters
	timestep            2.0  ;# 2.0 fs/step
	rigidBonds          all  ;# needed for 2fs steps
	nonbondedFreq       1
	fullElectFrequency  2  
	stepspercycle       10

	# Constant Temperature Control
	langevin            on    ;# do langevin dynamics
	langevinDamping     2     ;# damping coefficient (gamma) of 2/ps
	langevinTemp        $temperature
	langevinHydrogen    off    ;# don't couple langevin bath to hydrogens

	# Periodic Boundary Conditions
	cellBasisVector1   64.    0.   0. 
	cellBasisVector2    0.  104.   0.
	cellBasisVector3    0.    0.  76.
	cellOrigin         1.4842796325683594 -2.407818555831909 -1.7820888757705688
	wrapAll             on

	# PME (for full-system periodic electrostatics)
	PME                 yes
	PMEGridSpacing      1.0
	PMEGridSizeX        81  #3
	PMEGridSizeY        128 #2
	PMEGridSizeZ        81  #3

	# Constant Pressure Control (variable volume)
	useGroupPressure      yes ;# needed for rigidBonds
	useFlexibleCell       no
	useConstantArea       no
	langevinPiston        on
	langevinPistonTarget  1.01325 ;#  in bar -> 1 atm
	langevinPistonPeriod  100.
	langevinPistonDecay   50.
	langevinPistonTemp    $temperature

	# Output
	outputName          $outputname
	restartfreq         1000     ;# 1000steps = every 2 ps
	dcdfreq             2000
	outputEnergies      1000

	#############################################################
	## EXECUTION SCRIPT                                        ##
	#############################################################

	# Minimization
	minimize            250000 ;#500 ps

"""
config3_h.write(content)
config3_h.close()

namdcommand = "charmrun namd2 ++local +p${NCPUS} productive3.conf"
os.system(namdcommand)

print("Minimização - sistema livre - finalizada")

#############################################################

config4 = "productive4.conf"
config4_h = open(config4, 'w')
content = """
	#############################################################
	## JOB DESCRIPTION                                         ##
	#############################################################

	#Equilibração
	#Restrição harmônica de 2 kcal/mol/A^2

	#############################################################
	## ADJUSTABLE PARAMETERS                                   ##
	#############################################################

	#Reiniciando a simulação
	bincoordinates     complex_dm_4.coor
	#binvelocities      complex_dm_4.vel
	extendedSystem     complex_dm_4.xsc

	structure          complex_ion.psf
	coordinates        complex_ion.pdb
	set temperature    300
	set outputname     complex_dm_5
	firsttimestep      0

	Binaryoutput       yes

	#############################################################
	## SIMULATION PARAMETERS                                   ##
	#############################################################

	paraTypeCharmm	    on
	parameters          ../par_all36_prot.prm
	parameters          ../toppar_water_ions.str
	parameters	    	DB11855.par
	
	temperature         $temperature

	# Force-Field Parameters
	exclude             scaled1-4
	1-4scaling          1.0
	cutoff              12.
	switching           on
	switchdist          10.
	pairlistdist        13.5

	# Integrator Parameters
	timestep            2.0  ;# 2.0 fs/step
	rigidBonds          all  ;# needed for 2fs steps
	nonbondedFreq       1
	fullElectFrequency  2  
	stepspercycle       10

	# Constant Temperature Control
	langevin            on    ;# do langevin dynamics
	langevinDamping     2     ;# damping coefficient (gamma) of 2/ps
	langevinTemp        $temperature
	langevinHydrogen    off    ;# don't couple langevin bath to hydrogens

	# Periodic Boundary Conditions
	cellBasisVector1   64.    0.   0. 
	cellBasisVector2    0.  104.   0.
	cellBasisVector3    0.    0.  76.
	cellOrigin         1.4842796325683594 -2.407818555831909 -1.7820888757705688
	wrapAll             on

	# PME (for full-system periodic electrostatics)
	PME                 yes
	PMEGridSpacing      1.0
	PMEGridSizeX        81  #3
	PMEGridSizeY        128 #2
	PMEGridSizeZ        81  #3

	# Constant Pressure Control (variable volume)
	useGroupPressure      yes ;# needed for rigidBonds
	useFlexibleCell       no
	useConstantArea       no
	langevinPiston        on
	langevinPistonTarget  1.01325 ;#  in bar -> 1 atm
	langevinPistonPeriod  100.
	langevinPistonDecay   50.
	langevinPistonTemp    $temperature

	# Output
	outputName          $outputname
	restartfreq         1000     ;# 1000steps = every 2 ps
	dcdfreq             2000
	outputEnergies      1000

	#############################################################
	## EXECUTION SCRIPT                                        ##
	#############################################################

	# Simulation
	reinitvels          $temperature
	run 4000000 ; #8 ns

"""
config4_h.write(content)
config4_h.close()

namdcommand = "charmrun namd2 ++local +p${NCPUS} productive4.conf"
os.system(namdcommand)

print("Equilibração finalizada")

#############################################################

config5 = "productive5.conf"
config5_h = open(config5, 'w')
content = """
	#############################################################
	## JOB DESCRIPTION                                         ##
	#############################################################

	#Preparação para metadinâmica - Mpro (exceto cadeia lateral) rígida
	#Restrição harmônica de 2 kcal/mol/A^2

	#############################################################
	## ADJUSTABLE PARAMETERS                                   ##
	#############################################################

	#Reiniciando a simulação
	bincoordinates     complex_dm_5.coor
	binvelocities      complex_dm_5.vel
	extendedSystem     complex_dm_5.xsc

	structure          complex_ion.psf
	coordinates        complex_ion.pdb
	set temperature    300
	set outputname     complex_dm_6
	firsttimestep      0

	Binaryoutput       yes

	#############################################################
	## SIMULATION PARAMETERS                                   ##
	#############################################################

	paraTypeCharmm	    on
	parameters          ../par_all36_prot.prm
	parameters          ../toppar_water_ions.str
	parameters	    DB11855.par

	#Dinâmica com restrição 
	constraints         on
	consexp             2
	consref             rest2.pdb
	conskfile           rest2.pdb
	conskcol            B #coluna de b-factor

	# Force-Field Parameters
	exclude             scaled1-4
	1-4scaling          1.0
	cutoff              12.
	switching           on
	switchdist          10.
	pairlistdist        13.5

	# Integrator Parameters
	timestep            2.0  ;# 2.0 fs/step
	rigidBonds          all  ;# needed for 2fs steps
	nonbondedFreq       1
	fullElectFrequency  2  
	stepspercycle       10

	# Constant Temperature Control
	langevin            on    ;# do langevin dynamics
	langevinDamping     2     ;# damping coefficient (gamma) of 2/ps
	langevinTemp        $temperature
	langevinHydrogen    off    ;# don't couple langevin bath to hydrogens

	# Periodic Boundary Conditions
	cellBasisVector1   64.    0.   0. 
	cellBasisVector2    0.  104.   0.
	cellBasisVector3    0.    0.  76.
	cellOrigin         1.4842796325683594 -2.407818555831909 -1.7820888757705688
	wrapAll             on

	# PME (for full-system periodic electrostatics)
	PME                 yes
	PMEGridSpacing      1.0
	PMEGridSizeX        81  #3
	PMEGridSizeY        128 #2
	PMEGridSizeZ        81  #3

	# Constant Pressure Control (variable volume)
	useGroupPressure      yes ;# needed for rigidBonds
	useFlexibleCell       no
	useConstantArea       no
	langevinPiston        on
	langevinPistonTarget  1.01325 ;#  in bar -> 1 atm
	langevinPistonPeriod  100.
	langevinPistonDecay   50.
	langevinPistonTemp    $temperature

	# Output
	outputName          $outputname
	restartfreq         1000     ;# 1000steps = every 2 ps
	dcdfreq             2000
	outputEnergies      1000

	#############################################################
	## EXECUTION SCRIPT                                        ##
	#############################################################

	# Minimization
	minimize            250000 ;#500 ps

"""
config5_h.write(content)
config5_h.close()

namdcommand = "charmrun namd2 ++local +p${NCPUS} productive5.conf"
os.system(namdcommand)

print("Preparação para metadinâmica - Mpro (exceto cadeia lateral) rígida - finalizada")

#############################################################

config6 = "productive6.conf"
config6_h = open(config6, 'w')
content = """
	#############################################################
	## JOB DESCRIPTION                                         ##
	#############################################################

	#Preparação para metadinâmica - Mpro rígida
	#Restrição harmônica de 2 kcal/mol/A^2

	#############################################################
	## ADJUSTABLE PARAMETERS                                   ##
	#############################################################

	#Reiniciando a simulação
	bincoordinates     complex_dm_6.coor
	binvelocities      complex_dm_6.vel
	extendedSystem     complex_dm_6.xsc

	structure          complex_ion.psf
	coordinates        complex_ion.pdb
	set temperature    300
	set outputname     complex_dm_7
	firsttimestep      0

	Binaryoutput       yes

	#############################################################
	## SIMULATION PARAMETERS                                   ##
	#############################################################

	paraTypeCharmm	    on
	parameters          ../par_all36_prot.prm
	parameters          ../toppar_water_ions.str
	parameters	    DB11855.par

	#Dinâmica com restrição 
	constraints         on
	consexp             2
	consref             rest3.pdb
	conskfile           rest3.pdb
	conskcol            B #coluna de b-factor

	# Force-Field Parameters
	exclude             scaled1-4
	1-4scaling          1.0
	cutoff              12.
	switching           on
	switchdist          10.
	pairlistdist        13.5

	# Integrator Parameters
	timestep            2.0  ;# 2.0 fs/step
	rigidBonds          all  ;# needed for 2fs steps
	nonbondedFreq       1
	fullElectFrequency  2  
	stepspercycle       10

	# Constant Temperature Control
	langevin            on    ;# do langevin dynamics
	langevinDamping     2     ;# damping coefficient (gamma) of 2/ps
	langevinTemp        $temperature
	langevinHydrogen    off    ;# don't couple langevin bath to hydrogens

	# Periodic Boundary Conditions
	cellBasisVector1   64.    0.   0. 
	cellBasisVector2    0.  104.   0.
	cellBasisVector3    0.    0.  76.
	cellOrigin         1.4842796325683594 -2.407818555831909 -1.7820888757705688
	wrapAll             on

	# PME (for full-system periodic electrostatics)
	PME                 yes
	PMEGridSpacing      1.0
	PMEGridSizeX        81  #3
	PMEGridSizeY        128 #2
	PMEGridSizeZ        81  #3

	# Constant Pressure Control (variable volume)
	useGroupPressure      yes ;# needed for rigidBonds
	useFlexibleCell       no
	useConstantArea       no
	langevinPiston        on
	langevinPistonTarget  1.01325 ;#  in bar -> 1 atm
	langevinPistonPeriod  100.
	langevinPistonDecay   50.
	langevinPistonTemp    $temperature

	# Output
	outputName          $outputname
	restartfreq         1000     ;# 1000steps = every 2 ps
	dcdfreq             2000
	outputEnergies      1000

	#############################################################
	## EXECUTION SCRIPT                                        ##
	#############################################################

	# Minimization
	minimize            250000 ;#500 ps

"""
config6_h.write(content)
config6_h.close()

namdcommand = "charmrun namd2 ++local +p${NCPUS} productive6.conf"
os.system(namdcommand)

print("Preparação para metadinâmica - Mpro rígida - finalizada")

#############################################################

config7 = "productive7.conf"
config7_h = open(config7, 'w')
content = """
	#############################################################
	## JOB DESCRIPTION                                         ##
	#############################################################

	#Preparação metadinâmica
	#Restrição harmônica de 2 kcal/mol/A^2

	#############################################################
	## ADJUSTABLE PARAMETERS                                   ##
	#############################################################

	#Reiniciando a simulação
	bincoordinates     complex_dm_7.coor
	#binvelocities      complex_dm_7.vel
	extendedSystem     complex_dm_7.xsc

	structure          complex_ion.psf
	coordinates        complex_ion.pdb
	set temperature    300
	set outputname     complex_dm_8
	firsttimestep      0

	Binaryoutput       yes

	#############################################################
	## SIMULATION PARAMETERS                                   ##
	#############################################################

	paraTypeCharmm	    on
	parameters          ../par_all36_prot.prm
	parameters          ../toppar_water_ions.str
	parameters		    DB11855.par
	
	temperature         $temperature

	# Force-Field Parameters
	exclude             scaled1-4
	1-4scaling          1.0
	cutoff              12.
	switching           on
	switchdist          10.
	pairlistdist        13.5

	# Integrator Parameters
	timestep            2.0  ;# 2.0 fs/step
	rigidBonds          all  ;# needed for 2fs steps
	nonbondedFreq       1
	fullElectFrequency  2  
	stepspercycle       10

	# Constant Temperature Control
	langevin            on    ;# do langevin dynamics
	langevinDamping     2     ;# damping coefficient (gamma) of 2/ps
	langevinTemp        $temperature
	langevinHydrogen    off    ;# don't couple langevin bath to hydrogens

	# Periodic Boundary Conditions
	cellBasisVector1   64.    0.   0. 
	cellBasisVector2    0.  104.   0.
	cellBasisVector3    0.    0.  76.
	cellOrigin         1.4842796325683594 -2.407818555831909 -1.7820888757705688
	wrapAll             on

	# PME (for full-system periodic electrostatics)
	PME                 yes
	PMEGridSpacing      1.0
	PMEGridSizeX        81  #3
	PMEGridSizeY        128 #2
	PMEGridSizeZ        81  #3

	# Constant Pressure Control (variable volume)
	useGroupPressure      yes ;# needed for rigidBonds
	useFlexibleCell       no
	useConstantArea       no
	langevinPiston        on
	langevinPistonTarget  1.01325 ;#  in bar -> 1 atm
	langevinPistonPeriod  100.
	langevinPistonDecay   50.
	langevinPistonTemp    $temperature

	# Output
	outputName          $outputname
	restartfreq         1000     ;# 1000steps = every 2 ps
	dcdfreq             2000
	outputEnergies      1000

	#############################################################
	## EXECUTION SCRIPT                                        ##
	#############################################################

	# Simulation
	reinitvels          $temperature
	run 500000 ; #1 ns

"""
config7_h.write(content)
config7_h.close()

namdcommand = "charmrun namd2 ++local +p${NCPUS} productive7.conf"
os.system(namdcommand)

print("Preparação finalizada")

#############################################################
