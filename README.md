# HiggsCombineTools
1) Combine cards
ARR_MASS=(200 210 250 300 350 400 500 550 600 650 700 750 800 900 1500 2000 2500 3000 4000 5000)

for MASS in ${ARR_MASS[@]};do
    combineCards.py -S MuonChggfBoostedSR=Datacard_M${MASS}/MuonChggfBoostedSR/CleanFatJetPassMBoostedSR_HlnFat_mass/datacard.txt ElectronChggfBoostedSR=Datacard_M${MASS}/ElectronChggfBoostedSR/CleanFatJetPassMBoostedSR_HlnFat_mass/datacard.txt MuonChggfResolvedSR=Datacard_M${MASS}/MuonChggfResolvedSR/LnJJ_mass/datacard.txt ElectronChggfResolvedSR=Datacard_M${MASS}/ElectronChggfResolvedSR/LnJJ_mass/datacard.txt &> combine_M${MASS}.txt

done


2)Get limit

combine -M AsymptoticLimits --bypassFrequentistFit Datacards/Datacard_M200/ResolvedSR/LnJJ_mass/datacard.txt
