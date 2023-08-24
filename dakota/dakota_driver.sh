# Dakota change the parameters in this file
# ------------------------------------------------------------------------------
dprepro $1 dakotaParameter.orig dakotaParameter

# Run simulation with new parameter set
# ------------------------------------------------------------------------------
    #---------------------------------------------------------------------------
    H=`head -5 dakotaParameter | tail -1 | cut -d'=' -f2`
    D=`head -6 dakotaParameter | tail -1 | cut -d'=' -f2`
    a=`head -7 dakotaParameter | tail -1 | cut -d'=' -f2`
	a2=`head -8 dakotaParameter | tail -1 | cut -d'=' -f2`
	n=`head -9 dakotaParameter | tail -1 | cut -d'=' -f2`
    loopNumber=`cat ../../.optimizationLoop`

    #---------------------------------------------------------------------------
    H=`echo $H | sed -e 's/[eE]+*/\*10\^/'`
    D=`echo $D | sed -e 's/[eE]+*/\*10\^/'`
    a=`echo $a | sed -e 's/[eE]+*/\*10\^/'`
	a2=`echo $a2 | sed -e 's/[eE]+*/\*10\^/'`
	n=`echo $n | sed -e 's/[eE]+*/\*10\^/'`

    #---------------------------------------------------------------------------
    H=`echo "scale=4; $H" | bc`
    D=`echo "scale=4; $D" | bc`
    a=`echo "scale=4; $a" | bc`
	a2=`echo "scale=4; $a2" | bc`
    n=`echo "scale=4; $n" | bc`

    #---------------------------------------------------------------------------
    >&2 echo -e "   ++++ Evaluate sample $loopNumber"
    >&2 echo -e "   |"
    >&2 echo -e "   |--> Stirrer position = $H [mm]"
    >&2 echo -e "   |--> Stirrer diameter = $D [mm]"
    >&2 echo -e "   |--> Pitch angle = $a [°]"
	>&2 echo -e "   |--> Blade angle = $a2 [°]"
    >&2 echo -e "   |--> Stirrer speed = $n [rad/s]"

	echo "omega $n;" > ./constant/omega
	echo "#inputMode merge;" >> ./constant/omega
	
    python3 geometry.py $D $a $a2
	surfaceTransformPoints "scale=(1 1 1), translate=(0 0 $H),  Rx=0" stirrer.stl ./constant/geometry/stirrer.stl
	>&2 echo -e "   |--> Stirrer created"
	python3 mrf.py $D
	surfaceTransformPoints "scale=(1 1 1), translate=(0 0 $H),  Rx=0" mrf.stl ./constant/geometry/rotating.stl
	>&2 echo -e "   |--> MRF created"
   
    # Mesh the case with new parameters
    #---------------------------------------------------------------------------
    >&2 echo "   |--> Start new meshing"
	
	res=$(sbatch run_of.sh)
	echo $res

	id_job=${res##* }
	
        echo "Started  ... "
        echo $id_job
	ST="PENDING"
	while [[ "$ST" != "COMPLETED" && "$ST" != "FAILED" ]] ; do
            ST=$(sacct -j $id_job -o state | awk 'END {print $1}')                  
            sleep 10
                                            
	done
	echo "...Ended"

	#results.npy
	echo "H \t $H" > ./results.txt
	echo "D \t $D" >> ./results.txt
	echo "a \t $a" >> ./results.txt
	echo "a2 \t $a2" >> ./results.txt
	echo "n \t $n" >> ./results.txt
	cat temp.txt > .dakotaInput.dak

#------------------------------------------------------------------------------
cp .dakotaInput.dak ./$2
sleep 3
#------------------------------------------------------------------------------
