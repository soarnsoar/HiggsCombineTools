### under ../Datacard_M$$

ARR_DIR=($(ls -d Datacard_M*/))



for DIR in ${ARR_DIR[@]};do
    MASS=${DIR%\/}
    MASS=${MASS#Datacard_M}
    YEAR=${PWD#*Datacards_}
    echo "Get Expected Limit of M${MASS}"
    combine -M AsymptoticLimits --bypassFrequentistFit --run blind Datacard_M${MASS}/combine_M${MASS}.txt &> ExpectedLimit_combine_M${MASS}.txt
    combine -M AsymptoticLimits --bypassFrequentistFit --run blind Datacard_M${MASS}/BoostedSR${YEAR}/CleanFatJetPassMBoostedSR_HlnFat_mass/datacard.txt &> ExpectedLimit_BoostedSR_M${MASS}.txt
    combine -M AsymptoticLimits --bypassFrequentistFit --run blind Datacard_M${MASS}/ResolvedSR${YEAR}/LnJJ_mass/datacard.txt &> ExpectedLimit_ResolvedSR_M${MASS}.txt

done
