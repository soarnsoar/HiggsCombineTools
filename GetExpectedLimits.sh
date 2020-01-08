### under ../Datacard_M$$

source DefineMassBin.sh ##ARR_MAss=(mass1 mass2 ...)




for MASS in ${ARR_MASS[@]};do
    echo "Get Expected Limit of M${MASS}"
    combine -M AsymptoticLimits --bypassFrequentistFit --run blind Datacard_M${MASS}/combine_M${MASS}.txt &> ExpectedLimit_M${MASS}.txt

done
