#source DefineMassBin.sh ##ARR_MASS=(mass1 mass2 ...)

ARR_DIR=($(ls -d Datacard_M*/))



for DIR in ${ARR_DIR[@]};do
    MASS=${DIR%\/}
    MASS=${MASS#Datacard_M}
    echo $MASS

    combineCards.py -S MuonChggfBoostedSR=Datacard_M${MASS}/MuonChggfBoostedSR/CleanFatJetPassMBoostedSR_HlnFat_mass/datacard.txt ElectronChggfBoostedSR=Datacard_M${MASS}/ElectronChggfBoostedSR/CleanFatJetPassMBoostedSR_HlnFat_mass/datacard.txt MuonChggfResolvedSR=Datacard_M${MASS}/MuonChggfResolvedSR/LnJJ_mass/datacard.txt ElectronChggfResolvedSR=Datacard_M${MASS}/ElectronChggfResolvedSR/LnJJ_mass/datacard.txt &> Datacard_M${MASS}/combine_M${MASS}.txt

done
