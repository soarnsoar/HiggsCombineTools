#!/usr/bin/env python
import glob

import os, sys
sys.path.insert(0,'./')
import ROOT
import logging
import argparse
from collections import OrderedDict
from SM_ggHWW_XSEC import *


class CombiPlot:
  def __init__(self,opt):
    self.Userflags = opt.Userflags
    self.outputDirPlots = opt.outputDirPlots
    #self.scaleToPlot = opt.scaleToPlot
    self.minLogC = opt.minLogC
    self.maxLogC = opt.maxLogC
    self.inputDir = opt.inputDir
    self.lumi = opt.lumi
    self.sqrtS = opt.sqrtS
    self.prefix=opt.prefix
  def defineStyle(self):

    import tdrStyle as tdrStyle
    tdrStyle.setTDRStyle()

    ROOT.TGaxis.SetExponentOffset(-0.08, 0.00,"y")

  def GetMaxMinY(self,values):
    #values[i_value][i_mass]
    maximum=-1e309 ##init
    minimum=1e309
    #print "values[0]=",values[0]
    for i_value in values:
      #print 'i_value=',i_value
      if i_value==0:continue
      for limit in values[i_value]:
        if limit > maximum : maximum=limit
        if limit < minimum : minimum=limit
    #print 'max=',maximum
    #print 'min=',minimum
    return maximum, minimum

  def SetValues(self,masses,Scales):
    isCLsb = False
    Nmass = len(masses)
    print "Nmass", Nmass
    values =dict( (i, []) for i in range(7) ) #mass, obs, expp2, expp1, exp, expm1, expm2 7 items
    for mass in masses:
      Scale=1
      if mass in Scales: ## if there's y value(xsec OR BR) scaler for that mass
        Scale=Scales[mass]

      #ExpectedLimit_combine_M200
      fileName=self.inputDir+'/'+self.prefix+'_M'+str(mass)+'.txt'
      #print fileName
      f = open(fileName,"r")
      fL = f.readlines()
      
      #row = 1
      valid=False ## no calculated limit
      for x in fL:
        #print x
        if 'CLsb'  in x:
          isCLsb = True
        #if 'BR' in x:
        #  # Observed Limit: BR < 0.3334
        #  print float(x.split("BR <")[-1])
        #  values[row].append( float(x.split("BR <")[-1]) )
        #  row +=1
        if 'Expected' in x:
          valid=True
          if'2.5%' in x: ##Expected  2.5%: r < 4.0104
            #print "Find 2.5%"
            values[2].append(float(x.split('<')[-1])*Scale)
          elif '16.0%' in x:
            #print "Find 16.0%"
            values[3].append(float(x.split('<')[-1])*Scale)
          elif '50.0%' in x:
            #print "Find 50.0%"
            values[4].append(float(x.split('<')[-1])*Scale)
            values[1].append(float(x.split('<')[-1])*Scale) ##obs=exp
          elif '84.0%' in x:
            #print "Find 84.0%"
            values[5].append(float(x.split('<')[-1])*Scale)
          elif '97.5%' in x:
            #print "Find 97.5%"
            values[6].append(float(x.split('<')[-1])*Scale)
      if valid:
        values[0].append(mass)
      
     #i     # 0       1      2     3    4      5       6
    print 'mass, ,obs    expm2, expm1, exp, expp1, expp2'
    
    
    for j in range(len(values[0])):
      print (''.join(str(values[i][j])+' ' for i in range(7) ) )
    return values


  def GetTheoryValue(self):
    #https://twiki.cern.ch/twiki/bin/view/LHCPhysics/CERNYellowReportPageBSMAt13TeV
    #https://twiki.cern.ch/twiki/bin/view/LHCPhysics/CERNYellowReportPageBR2010
    #BR=0.1086*3*0.6741
    Xsec={}
    return Xsecs

      


  def mkAsymptoticPlot(self,masses,Scales):
    Nmass = len(masses)
    self.defineStyle()

    massbin=masses
    values=self.SetValues(masses,Scales)
    masses=values[0]
    Nmass=len(masses)
    #values[j][i]= ith mass,
    #j = 0    1     2    3    4    5     6
    #   mass obs expm2 expm1 exp expp1 expp2
    tcanvas = ROOT.TCanvas( 'tcanvas', 'distro',800,600)
    tcanvas.cd()
    tcanvas.SetLogy()
    tcanvas.SetGrid()


    # Making tgraphs for each items
    tgr_cls_obs     = ROOT.TGraph(Nmass)
    tgr_cls_exp     = ROOT.TGraph(Nmass)
    
    tgr_cls_exp_pm1 = ROOT.TGraphAsymmErrors(Nmass)
    tgr_cls_exp_pm2 = ROOT.TGraphAsymmErrors(Nmass)
    tgr_cls_obs.SetLineWidth(2)
    tgr_cls_exp.SetLineWidth(4)
    tgr_cls_exp_pm1.SetLineWidth(2)
    tgr_cls_exp_pm2.SetLineWidth(2)


    tgr_cls_exp.SetLineStyle(2)

    tgr_cls_exp.SetLineColor(ROOT.kBlack)
    tgr_cls_exp_pm1.SetLineColor(ROOT.kGreen)
    tgr_cls_exp_pm2.SetLineColor(ROOT.kYellow)
    tgr_cls_exp_pm1.SetFillColor(ROOT.kGreen)
    tgr_cls_exp_pm2.SetFillColor(ROOT.kYellow)

    ##Theroy graph
    #Xsecs=self.GetTheoryValue()
    Xsecs=GetggHWWXsec()
    tgr_theory  = ROOT.TGraph(len(Xsecs))
    tgr_theory.SetFillColor(ROOT.kRed)
    tgr_theory.SetLineColor(ROOT.kRed)
    tgr_theory.SetLineWidth(2)

    idx=0
    for mass, xsec in sorted(Xsecs.items()):
      #print 'idx=',idx
      #print 'mass=',mass
      
      tgr_theory.SetPoint(idx,mass,xsec)
      
      idx+=1


    for i in range(Nmass):

      tgr_cls_obs.SetPoint(i,values[0][i], values[1][i])
      tgr_cls_exp.SetPoint(i,values[0][i], values[4][i])
      tgr_cls_exp_pm1.SetPoint(i,values[0][i], values[4][i])
      tgr_cls_exp_pm2.SetPoint(i,values[0][i], values[4][i])

      tgr_cls_exp_pm1.SetPointError(i, 0, 0, values[4][i]-values[3][i], values[5][i]-values[4][i])
      tgr_cls_exp_pm2.SetPointError(i, 0, 0, values[4][i]-values[2][i], values[6][i]-values[4][i])

    maxy, miny=self.GetMaxMinY(values)
    if self.minLogC != None:
      miny = float(self.minLogC)
    if self.maxLogC != None:
      maxy = float(self.maxLogC)

    frame = ROOT.TH2F("frame","",len(massbin),min(massbin),max(massbin),100,miny*0.1,maxy*10)
    
    frame.SetYTitle("Limit 95% CL_{s} on #sigma_{X#rightarrowWW} [pb]")
    frame.GetYaxis().SetTitleSize(0.05)
    frame.GetYaxis().SetLabelSize(0.03)
    frame.SetXTitle("m_{X} (GeV)")
    frame.GetXaxis().SetTitleSize(0.035)
    frame.GetXaxis().SetLabelSize(0.03)
    frame.GetXaxis().SetTitleOffset(1.5)
    #tgr_cls_exp_pm2.GetHistogram().SetYTitle("Limit on B(t #rightarrow H^{+}b) with B(H^{+}#rightarrow c#bar{b}) = 1");
    frame.Draw()
    tgr_cls_exp_pm2.Draw("3 same")
    #tgr_cls_exp_pm2.Draw("a3 same")
    tgr_cls_exp_pm1.Draw("3 same")
    tgr_cls_exp.Draw("l same")
    tgr_theory.Draw("l same")
    #tgr_cls_obs.Draw("pl same")

    import CMS_lumi as CMS_lumi
    
    CMS_lumi.lumi_13TeV=self.lumi+' fb^{-1}'
    CMS_lumi.writeExtraText=1
    CMS_lumi.extraText="Preliminary"
    CMS_lumi.relPosX = 0.12
    CMS_lumi.lumi_sqrtS = self.sqrtS
    iPeriod = 4
    iPos  = 0
    CMS_lumi.CMS_lumi(tcanvas, iPeriod, iPos)

    #leg= ROOT.TLegend(0.65,0.65,0.9,0.84)
    leg= ROOT.TLegend(0.5,0.75,0.95,0.94)
    leg.SetFillColor(0)
    leg.SetBorderSize(1)
    leg.SetTextFont(8)
    leg.SetTextSize(20)
    leg.AddEntry(tgr_cls_exp,     "Expected Limit","l")
    leg.AddEntry(tgr_cls_exp_pm1, "Expected #pm 1#sigma","f");
    leg.AddEntry(tgr_cls_exp_pm2, "Expected #pm 2#sigma","f");
    leg.AddEntry(tgr_theory,      "SM-like scenario, f_{vbf}=0",'l')
    leg.Draw("same")

    tcanvas.SaveAs(self.outputDirPlots+'/'+self.Userflags+'.png')

    ##export values
    #values[j][i]= ith mass
    for i in range(Nmass):
      dirmass=self.Userflags+'/'+str(values[0][i])
      os.system('mkdir -p '+dirmass)
      
      list_alias=['mass','obs','expm2','expm1','exp','expp1','expp2']
      for j in range(1,7):
        
        f=open(dirmass+'/'+list_alias[j]+'.txt','w')
        f.write(str(values[j][i]))
        f.close()

      
      #     #i     # 0       1      2     3    4      5       6 
      #    print 'mass, ,obs    expm2, expm1, exp, expp1, expp2'

    
    

def GetXsecScale():
  
  BR=0.1086*3*0.6741 ## to W->l nu 3 flavour , W->qq
  Scales = {
    200:2.7568/BR, ## 200GeV : shape's xsec/BR to lnqq
    210:2.4136/BR,
    230:1.9234/BR,
    250:1.5703/BR,
    270:1.3027/BR,
    300:1.0015/BR,
    350:0.6651/BR,
    400:0.4039/BR,
    450:0.2783/BR,
    500:0.2049/BR,
    550:0.1567/BR,
    600:0.1227/BR,
    650:0.0977/BR,
    700:0.0786/BR,
    750:0.0639/BR,
    800:0.0524/BR,
    900:0.0359/BR,
    1000:0.0252/BR,
    1500:0.00503/BR,
    2000:0.00131/BR,
    2500:0.000394/BR,
    3000:0.000128/BR,
    4000:0.0000115/BR,
    5000:0.0000019/BR,
  }
  return Scales


if __name__ == "__main__":

  print '''
  -----------------------------------------------------------------------------------------
                                                           
    _____  _       _     __  __       _               _    _       _           _           
   |  __ \| |     | |   |  \/  |     | |             | |  | |     | |         | |          
   | |__) | | ___ | |_  | \  / | __ _| | _____ _ __  | |__| | __ _| |__   __ _| |__   __ _ 
   |  ___/| |/ _ \| __| | |\/| |/ _` | |/ / _ \ '__| |  __  |/ _` | '_ \ / _` | '_ \ / _` |
   | |    | | (_) | |_  | |  | | (_| |   <  __/ |    | |  | | (_| | | | | (_| | | | | (_| |
   |_|    |_|\___/ \__| |_|  |_|\__,_|_|\_\___|_|    |_|  |_|\__,_|_| |_|\__,_|_| |_|\__,_|
  	                                                                                          
  -----------------------------------------------------------------------------------------
  
  '''
  
  
  parser = argparse.ArgumentParser(description='JudgementDay')
  parser.add_argument('--userflags', dest='Userflags', default="test")
  parser.add_argument('--prefix', dest='prefix',help='limit txt file name', default="ExpectedLimit_combine")
  parser.add_argument('--debug', dest='debug', default=0, type=int)
  #parser.add_argument('--scaleToPlot'    , dest='scaleToPlot'    , help='scale of maxY to maxHistoY'                 , default=2.0  ,    type=float   )
  parser.add_argument('--minLogC'        , dest='minLogC'        , help='min Y in log plots'                         , default=None  ,    type=float   )
  parser.add_argument('--maxLogC'        , dest='maxLogC'        , help='max Y in log plots'                         , default=None   ,    type=float   )
  parser.add_argument('--maxLinearScale' , dest='maxLinearScale' , help='scale factor for max Y in linear plots (1.45 magic number as default)'     , default=1.45   ,    type=float   )
  parser.add_argument('--outputDirPlots' , dest='outputDirPlots' , help='output directory'                           , default='./')
  
  parser.add_argument('--inputDir', dest='inputDir', help='input dir path', default='/')
  parser.add_argument('--sqrtS', dest='sqrtS', help='sqrts', default='13 TeV')
  parser.add_argument('--lumi', dest='lumi', help='total integrated lumi', default='100')
  
  
  
  
  ROOT.gROOT.SetBatch()
  
  opt = parser.parse_args()
  
  
  print ""
  print "                   Userflags =", opt.Userflags
  print "              outputDirPlots =", opt.outputDirPlots
  #print "                 scaleToPlot =", opt.scaleToPlot
  print "                     minLogC =", opt.minLogC
  print "                     maxLogC =", opt.maxLogC
  print "                    inputDir =", opt.inputDir
  
  
  #opt.scaleToPlot = opt.scaleToPlot
  #opt.minLogC = opt.minLogC
  #opt.maxLogC = opt.maxLogC
  
  
  
  if not opt.debug:
    pass
  elif opt.debug == 2:
    print 'Logging level set to DEBUG (%d)' % opt.debug
    logging.basicConfig( level=logging.DEBUG )
  elif opt.debug == 1:
    print 'Logging level set to INFO (%d)' % opt.debug
    logging.basicConfig( level=logging.INFO )
  
  Userflags = []
  if opt.Userflags != "":
    Userflags = (opt.Userflags).split(',')
  
  IsFirstFlag = True
  tag=''
  for flag in Userflags:
    if IsFirstFlag:
      tag = flag
    else:
      tag += '_'+flag 
  print tag
  
  com = CombiPlot(opt)
  #masses = [200,210,250,300,350,400,500,550,600,650,700,750,800,900,1500,2000,2500,3000,4000,5000]
  ##Take masses
  LIST_MASSDIR=glob.glob(opt.inputDir+'/Datacard_M*')
  masses=[]
  for MASSDIR in LIST_MASSDIR:
    #MASSDIR=../Datacards_2016/Datacard_M350
    MASS=MASSDIR.split('/')[-1].split('M')[-1]
    print MASS
    masses.append(int(MASS))
  masses.sort()

  

  #Scales =  GetggHWWXsec()
  Scales =  GetXsecScale()
  com.mkAsymptoticPlot(masses,Scales)
  
  
  
  
  
  print 'Now closing......, Bye!'


