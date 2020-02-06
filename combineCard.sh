#source DefineMassBin.sh ##ARR_MASS=(mass1 mass2 ...)
#Datacard_M200/BoostedSR2017

ARR_CARDDIR_YEAR=($(ls -d Datacards_*/))

for CARDDIR in ${ARR_CARDDIR_YEAR[@]};do

    YEAR=${CARDDIR%\/}
    YEAR=${YEAR#Datacards_}
    echo "YEAR="$YEAR
    
  
    pushd ${CARDDIR}


    ARR_DIR=($(ls -d Datacard_M*/))
    for DIR in ${ARR_DIR[@]};do
	MASS=${DIR%\/}
	MASS=${MASS#Datacard_M}
	echo $MASS
	
	combineCards.py -S MuonChggfBoostedSR=Datacard_M${MASS}/MuonChggfBoostedSR${YEAR}/CleanFatJetPassMBoostedSR_HlnFat_mass/datacard.txt ElectronChggfBoostedSR=Datacard_M${MASS}/ElectronChggfBoostedSR${YEAR}/CleanFatJetPassMBoostedSR_HlnFat_mass/datacard.txt MuonChggfResolvedSR=Datacard_M${MASS}/MuonChggfResolvedSR${YEAR}/LnJJ_mass/datacard.txt ElectronChggfResolvedSR=Datacard_M${MASS}/ElectronChggfResolvedSR${YEAR}/LnJJ_mass/datacard.txt &> Datacard_M${MASS}/combine_M${MASS}.txt
	
    done

    popd

done
