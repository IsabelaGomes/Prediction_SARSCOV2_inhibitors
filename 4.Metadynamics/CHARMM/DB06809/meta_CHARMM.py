import os
 
parm1 = "metadin1.in"
parm1_h = open(parm1, 'w')
content = """
colvarsTrajFrequency 250
colvarsRestartFrequency 1000

analysis on      #analysis 
colvar {
	name dist
	lowerBoundary 0.0
	upperBoundary  30.0
	
	expandBoundaries  off   	 # Allow biases to expand the two boundaries
	lowerWall       -5.0		 #  Position of the lower wall, It is a good idea to set this value a little higher than lowerBoundary
	lowerWallConstant  50.0		 # Lower wall force constant (kcal/mol)
	upperWall        35.0	     # Similar to lowerWall
	upperWallConstant   50.0	 # Similar to lowerWallConstant
	
	width  1 #tamanho da gride
	distance {
		group1 { atomNumbersRange 2234-2244 }   #CYS 145
		group2 { atomNumbers 4646 4647 4648 4649 4650 4651 4652 4656 4660 4661 4662 4671 4672 4673 4688 4689 4690 4691 4692 4693 4694 4695 4696 4697 4714 4715 4716 4717 4718 4719 }   #ligante próximos a CYS145
	}
}

colvar {
	name ang
	lowerBoundary  0.0
	upperBoundary  180.0
	
	expandBoundaries  off   	 # Allow biases to expand the two boundaries
	lowerWall       -10.0		 #  Position of the lower wall, It is a good idea to set this value a little higher than lowerBoundary
	lowerWallConstant  50.0		 # Lower wall force constant (kcal/mol)
	upperWall        190.0	     # Similar to lowerWall
	upperWallConstant   50.0	 # Similar to lowerWallConstant
	
	width  10 #10 em 10 graus
	angle {
		group1 { atomNumbersRange 2234-2244 }    #CYS 145
		group2 { atomNumbersRange 4646-4735 }    #ligante
		group3 { atomNumbersRange 1-4645 }       #M-pro toda (podia ser somente o domínio 
		#CYS145 - CG lig - CGpro
	}
}

#META MD SECTION
metadynamics {
	name metadin1
	colvars dist ang
	hillWeight 0.02                   # Height of each hill (kcal/mol) , default 0.01 - larger numbers = faster
	newHillFrequency  100             # Default is 100 - lower numbers = faster
	hillWidth       1.77              # Relative width of the hills, Default Value:  sqrt(2pi/2
	useGrids   on                     #
	gridsUpdateFrequency   100        # Frequency of update of the grids , default the same as newHillFrequency
	writeFreeEnergyFile on             # Periodically save the PMF
	keepFreeEnergyFiles on             # Keep all the PMF files Activating this option can be useful to follow more closely the convergence of the simulation, by comparing PMFs with small time
	rebinGrids     off                # Recompute the grids when reading a state file
	keepHills      off                # Write each individual hill to the state file
	multipleReplicas off              # Note: This option cannot be used in conjunction with useGrids.
	# replicaID  namexx               # if multipleReplicas is on
	# replicaUpdateFrequency  steps   # if multipleReplicas is on
	writeHillsTrajectory  on          # logfile is written by the metadynamics bias

}
histogram {
	colvars dist ang     		  # betagamma
	outputFreq      100           # the Frequency for in timesteps at which the histogram file is refreshed
}

"""
parm1_h.write(content)
parm1_h.close()

config1 = "metadin1.conf"
config1_h = open(config1, 'w')
content = """
	#############################################################
	## JOB DESCRIPTION                                         ##
	#############################################################

	#Metadinâmica

	#############################################################
	## ADJUSTABLE PARAMETERS                                   ##
	#############################################################

	#Reiniciando a simulação
	bincoordinates     ../complex_dm_8.coor
	#binvelocities      ../complex_dm_8.vel
	extendedSystem     ../complex_dm_8.xsc

	structure          ../complex_ion.psf
	coordinates        ../complex_ion.pdb
	set temperature    300
	set outputname     complex_metadin1
	firsttimestep      0

	Binaryoutput       yes
	
	#############################################################
	## SIMULATION PARAMETERS                                   ##
	#############################################################

	paraTypeCharmm	    on
	parameters          ../../par_all36_prot.prm
	parameters          ../../toppar_water_ions.str
	parameters	    	../DB06809.par
	temperature         $temperature

	#Dinâmica com restrição 
	constraints         on
	consexp             2
	consref             ../rest3.pdb
	conskfile           ../rest3.pdb
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
	cellOrigin         1.4824976921081543 -2.4227981567382813 -1.7144038677215576
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

	# META MD or any biasing method SECTION
	colvars              on
	colvarsConfig        metadin1.in 
	run 3500000 ; #7 ns

"""
config1_h.write(content)
config1_h.close()

namdcommand = "charmrun namd2 ++local +p${NCPUS} metadin1.conf"
os.system(namdcommand)

print("Finalizada CV1")

#############################################################
 
parm2 = "metadin2.in"
parm2_h = open(parm2, 'w')
content = """
colvarsTrajFrequency 250
colvarsRestartFrequency 1000

analysis on      #analysis 
colvar {
	name dist
	lowerBoundary 0.0
	upperBoundary  30.0
	
	expandBoundaries  off   	 # Allow biases to expand the two boundaries
	lowerWall       -5.0		 #  Position of the lower wall, It is a good idea to set this value a little higher than lowerBoundary
	lowerWallConstant  50.0		 # Lower wall force constant (kcal/mol)
	upperWall        35.0	     # Similar to lowerWall
	upperWallConstant   50.0	 # Similar to lowerWallConstant
	
	width  1 #tamanho da gride
	distance {
		group1 { atomNumbersRange 2234-2244 }   #CYS 145
		group2 { atomNumbers 4646 4647 4648 4649 4650 4651 4652 4656 4660 4661 4662 4671 4672 4673 4688 4689 4690 4691 4692 4693 4694 4695 4696 4697 4714 4715 4716 4717 4718 4719 }   #ligante próximos a CYS145
	}
}

colvar {
	name ang
	lowerBoundary  0.0
	upperBoundary  180.0
	
	expandBoundaries  off   	 # Allow biases to expand the two boundaries
	lowerWall       -10.0		 #  Position of the lower wall, It is a good idea to set this value a little higher than lowerBoundary
	lowerWallConstant  50.0		 # Lower wall force constant (kcal/mol)
	upperWall        190.0	     # Similar to lowerWall
	upperWallConstant   50.0	 # Similar to lowerWallConstant
	
	width  10 #10 em 10 graus
	angle {
		group1 { atomNumbersRange 2234-2244 }    #CYS 145
		group2 { atomNumbers 4656 4657 4658 4659 4672 4673 4674 4675 4676 4677 4678 4679 4680 4681}   #anel dentro
		group3 { atomNumbers 4652 4653 4654 4655 4661 4662 4663 4664 4665 4666 4667 4668 4669 4670 }    #anel fora
		#CYS145 - anel dentro - anel fora
	}
}4723 4646

#META MD SECTION
metadynamics {
	name metadin1
	colvars dist ang
	hillWeight 0.02                   # Height of each hill (kcal/mol) , default 0.01 - larger numbers = faster
	newHillFrequency  100             # Default is 100 - lower numbers = faster
	hillWidth       1.77              # Relative width of the hills, Default Value:  sqrt(2pi/2
	useGrids   on                     #
	gridsUpdateFrequency   100        # Frequency of update of the grids , default the same as newHillFrequency
	writeFreeEnergyFile on             # Periodically save the PMF
	keepFreeEnergyFiles on             # Keep all the PMF files Activating this option can be useful to follow more closely the convergence of the simulation, by comparing PMFs with small time
	rebinGrids     off                # Recompute the grids when reading a state file
	keepHills      off                # Write each individual hill to the state file
	multipleReplicas off              # Note: This option cannot be used in conjunction with useGrids.
	# replicaID  namexx               # if multipleReplicas is on
	# replicaUpdateFrequency  steps   # if multipleReplicas is on
	writeHillsTrajectory  on          # logfile is written by the metadynamics bias

}
histogram {
	colvars dist ang     		  # betagamma
	outputFreq      100           # the Frequency for in timesteps at which the histogram file is refreshed
}

"""
parm2_h.write(content)
parm2_h.close()

config2 = "metadin2.conf"
config2_h = open(config2, 'w')
content = """

	#############################################################
	## JOB DESCRIPTION                                         ##
	#############################################################

	#Metadinâmica

	#############################################################
	## ADJUSTABLE PARAMETERS                                   ##
	#############################################################

	#Reiniciando a simulação
	bincoordinates     ../complex_dm_8.coor
	#binvelocities      ../complex_dm_8.vel
	extendedSystem     ../complex_dm_8.xsc

	structure          ../complex_ion.psf
	coordinates        ../complex_ion.pdb
	set temperature    300
	set outputname     complex_metadin2
	firsttimestep      0

	Binaryoutput       yes
	
	#############################################################
	## SIMULATION PARAMETERS                                   ##
	#############################################################

	paraTypeCharmm	    on
	parameters          ../../par_all36_prot.prm
	parameters          ../../toppar_water_ions.str
	parameters	    	../DB06809.par
	temperature         $temperature

	#Dinâmica com restrição 
	constraints         on
	consexp             2
	consref             ../rest3.pdb
	conskfile           ../rest3.pdb
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
	cellOrigin         1.4824976921081543 -2.4227981567382813 -1.7144038677215576
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

	# META MD or any biasing method SECTION
	colvars              on
	colvarsConfig        metadin2.in 
	run 3500000 ; #7 ns
	
"""
config2_h.write(content)
config2_h.close()

namdcommand = "charmrun namd2 ++local +p${NCPUS} metadin2.conf"
os.system(namdcommand)

print("Finalizada CV2")
