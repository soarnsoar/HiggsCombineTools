#source DefineMassBin.sh ##ARR_MASS=(mass1 mass2 ...)

ARR_MASS=( 200 210 230 250 300 350 400 450 500 550 600 650 700 750 800 850 900 1000 1500 2000 2500 3000 4000 5000 )



for MASS in ${ARR_MASS[@]};do
    
    
    #2016
    is2016=`ls ../Datacards_2016/Datacard_M${MASS}/combine_M${MASS}.txt|wc -l`
    is2017=`ls ../Datacards_2016/Datacard_M${MASS}/combine_M${MASS}.txt|wc -l`
    is2018=`ls ../Datacards_2016/Datacard_M${MASS}/combine_M${MASS}.txt|wc -l`
    
    if [ $is2016 -eq 0 ]
    then
	continue
    elif [ $is2017 -eq 0 ]
    then
	continue
    elif [ $is2018 -eq 0 ]
    then
	continue
    fi
    echo $MASS
    mkdir -p Datacard_M${MASS}
    ##2016 cards##
    input2016="MuonChggfBoostedSR2016=../Datacards_2016/Datacard_M${MASS}/MuonChggfBoostedSR/CleanFatJetPassMBoostedSR_HlnFat_mass/datacard.txt ElectronChggfBoostedSR=../Datacards_2016/Datacard_M${MASS}/ElectronChggfBoostedSR/CleanFatJetPassMBoostedSR_HlnFat_mass/datacard.txt MuonChggfResolvedSR=../Datacards_2016/Datacard_M${MASS}/MuonChggfResolvedSR/LnJJ_mass/datacard.txt ElectronChggfResolvedSR=../Datacards_2016/Datacard_M${MASS}/ElectronChggfResolvedSR/LnJJ_mass/datacard.txt"
   input2017="MuonChggfBoostedSR2017=../Datacards_2017/Datacard_M${MASS}/MuonChggfBoostedSR/CleanFatJetPassMBoostedSR_HlnFat_mass/datacard.txt ElectronChggfBoostedSR=../Datacards_2017/Datacard_M${MASS}/ElectronChggfBoostedSR/CleanFatJetPassMBoostedSR_HlnFat_mass/datacard.txt MuonChggfResolvedSR=../Datacards_2017/Datacard_M${MASS}/MuonChggfResolvedSR/LnJJ_mass/datacard.txt ElectronChggfResolvedSR=../Datacards_2017/Datacard_M${MASS}/ElectronChggfResolvedSR/LnJJ_mass/datacard.txt"
   input2018="MuonChggfBoostedSR2018=../Datacards_2018/Datacard_M${MASS}/MuonChggfBoostedSR/CleanFatJetPassMBoostedSR_HlnFat_mass/datacard.txt ElectronChggfBoostedSR=../Datacards_2018/Datacard_M${MASS}/ElectronChggfBoostedSR/CleanFatJetPassMBoostedSR_HlnFat_mass/datacard.txt MuonChggfResolvedSR=../Datacards_2018/Datacard_M${MASS}/MuonChggfResolvedSR/LnJJ_mass/datacard.txt ElectronChggfResolvedSR=../Datacards_2018/Datacard_M${MASS}/ElectronChggfResolvedSR/LnJJ_mass/datacard.txt"
    combineCards.py -S ${input2016} ${input2017} ${input2018} &> Datacard_M${MASS}/combine_M${MASS}.txt
    

done
