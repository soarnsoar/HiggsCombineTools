#--combined region
python mkExpectedLimitPlot.py --minLogC 0.0001 --inputDir ../Datacards_2016 --userflags exp2016 --lumi 35.9 --prefix ExpectedLimit_combine
python mkExpectedLimitPlot.py --minLogC 0.0001 --inputDir ../Datacards_2017 --userflags exp2017 --lumi 41.5 --prefix ExpectedLimit_combine  
python mkExpectedLimitPlot.py --minLogC 0.0001 --inputDir ../Datacards_2018 --userflags exp2018 --lumi 59.7 --prefix ExpectedLimit_combine
python mkExpectedLimitPlot.py --minLogC 0.0001 --inputDir ../YearCombDatacards_201620172018 --userflags exp_201620172018 --lumi 137 --prefix ExpectedLimit_combine

#--Boosted
python mkExpectedLimitPlot.py --minLogC 0.0001 --inputDir ../Datacards_2016 --userflags exp2016Boosted --lumi 35.9 --prefix ExpectedLimit_BoostedSR
python mkExpectedLimitPlot.py --minLogC 0.0001 --inputDir ../Datacards_2017 --userflags exp2017Boosted --lumi 41.5 --prefix ExpectedLimit_BoostedSR
python mkExpectedLimitPlot.py --minLogC 0.0001 --inputDir ../Datacards_2018 --userflags exp2018Boosted --lumi 59.7 --prefix ExpectedLimit_BoostedSR
python mkExpectedLimitPlot.py --minLogC 0.0001 --inputDir ../YearCombDatacards_201620172018 --userflags exp_201620172018Boosted --lumi 137 --prefix ExpectedLimit_BoostedSR

#--Resolved
python mkExpectedLimitPlot.py --minLogC 0.0001 --inputDir ../Datacards_2016 --userflags exp2016Resolved --lumi 35.9 --prefix ExpectedLimit_ResolvedSR
python mkExpectedLimitPlot.py --minLogC 0.0001 --inputDir ../Datacards_2017 --userflags exp2017Resolved --lumi 41.5 --prefix ExpectedLimit_ResolvedSR
python mkExpectedLimitPlot.py --minLogC 0.0001 --inputDir ../Datacards_2018 --userflags exp2018Resolved --lumi 59.7 --prefix ExpectedLimit_ResolvedSR
python mkExpectedLimitPlot.py --minLogC 0.0001 --inputDir ../YearCombDatacards_201620172018 --userflags exp_201620172018Resolved --lumi 137 --prefix ExpectedLimit_ResolvedSR


#--Comparison
python mkCompareLimitPlot.py
