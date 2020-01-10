ARR_DIR=($(ls -d Datacard_M*/))



for DIR in ${ARR_DIR[@]};do
    MASS=${DIR%\/}
    MASS=${MASS#Datacard_M}
    echo $MASS

    echo "Get Expected Limit of M${MASS}"
    combine -M AsymptoticLimits --bypassFrequentistFit --run blind Datacard_M${MASS}/combine_M${MASS}.txt &> ExpectedLimit_M${MASS}.txt

done
