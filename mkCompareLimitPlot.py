import ROOT
import copy
import glob
from SM_ggHWW_XSEC import *

ROOT.gROOT.SetBatch()

def GetLimit(dirpath,txtname):
    #exp2016/200/exp.txt
    #tgr_cls_exp     = ROOT.TGraph(Nmass)
    massdir_list=glob.glob(dirpath+'/*/')
    #print massdir_list
    mass_list=[]
    dic={}
    for massdir in massdir_list:
        #massdir=exp2016/900/
        mass=massdir.replace(dirpath+'/','').rstrip('/')
        #print mass
        f=open(massdir+'/'+txtname,'r')
        limit=float(f.readline())
        dic[float(mass)]=limit
        f.close()
    return dic

def TestGetLimit():
    
    dic_limit2016=GetLimit('exp2016','exp.txt')
    dic_explimit2016=copy.deepcopy(dic_limit2016)

    dic_limit2017=GetLimit('exp2017','exp.txt')
    dic_explimit2017=copy.deepcopy(dic_limit2017)

    dic_limit2018=GetLimit('exp2018','exp.txt')
    dic_explimit2018=copy.deepcopy(dic_limit2018)
    

    #print dic_explimit2016
    #print dic_explimit2017
    #print dic_explimit2018
    
    ggH_Theory=GetggHWWXsec()
    ggH_Theory=copy.deepcopy(ggH_Theory)

def GetLimitGraph(dic_limit):

    this_dic_limit=copy.deepcopy(dic_limit)
    Nmass=len(dic_limit)
    tgr     = ROOT.TGraph(Nmass)
    tgr.SetLineWidth(4)
    idx=0
    for mass,value in sorted(this_dic_limit.items()):
        tgr.SetPoint(idx,mass,value)
        idx+=1
    return tgr

def GetMinMaxFromDic(dic):
    miny=dic.values()[0]
    maxy=dic.values()[0]
    for a in dic.values():
        if a > maxy:maxy=a
        if a < miny:miny=a
    return miny, maxy
    
def CompareExpLimitsEachYear(dirname_prefix,tag=''):
    import tdrStyle as tdrStyle
    tdrStyle.setTDRStyle()

    tcanvas = ROOT.TCanvas( 'tcanvas'+tag, 'distro'+tag,800,600)
    tcanvas.cd()
    tcanvas.SetLogy()
    tcanvas.SetGrid()
    dic_limit=GetLimit(dirname_prefix+'2016'+tag,'exp.txt')
    tgr_2016exp=GetLimitGraph(dic_limit)
    dic_2016exp=copy.deepcopy(dic_limit)
    
    dic_limit=GetLimit(dirname_prefix+'2017'+tag,'exp.txt')
    tgr_2017exp=GetLimitGraph(dic_limit)
    dic_2017exp=copy.deepcopy(dic_limit)
    
    dic_limit=GetLimit(dirname_prefix+'2018'+tag,'exp.txt')
    tgr_2018exp=GetLimitGraph(dic_limit)
    dic_2018exp=copy.deepcopy(dic_limit)
    
    dic_limit=GetLimit(dirname_prefix+'_201620172018'+tag,'exp.txt')
    tgr_201620172018exp=GetLimitGraph(dic_limit)
    dic_201620172018exp=copy.deepcopy(dic_limit)

    dic_limit=GetggHWWXsec()
    tgr_theory=GetLimitGraph(dic_limit)
    dic_theory=copy.deepcopy(dic_limit)
    
    dic_3yr=copy.deepcopy(dic_2016exp)
    dic_3yr.update(dic_2017exp)
    dic_3yr.update(dic_2018exp)
    dic_3yr.update(dic_201620172018exp)
    dic_3yr.update(dic_theory)
    miny,maxy=GetMinMaxFromDic(dic_3yr)

    tgr_2016exp.SetLineStyle(2)
    tgr_2017exp.SetLineStyle(2)
    tgr_2018exp.SetLineStyle(2)
    tgr_201620172018exp.SetLineStyle(2)

    tgr_2016exp.SetLineColor(ROOT.kBlue)
    tgr_2017exp.SetLineColor(ROOT.kGreen)
    tgr_2018exp.SetLineColor(ROOT.kOrange)
    tgr_201620172018exp.SetLineColor(ROOT.kBlack)
    tgr_theory.SetLineColor(ROOT.kRed)



    masses=[200,210,230,250,270,300,350,400,450,500,550,600,650,700,750,800,850,900,1000,1500,2000,2500,3000,4000,5000]
    Nmass=len(masses)
    frame = ROOT.TH2F("frame","",Nmass,min(masses),max(masses),100,miny*0.1,maxy*10)
    frame.SetYTitle("Limit 95% CL_{s} on #sigma_{X#rightarrowWW} [pb]")
    frame.GetYaxis().SetTitleSize(0.05)
    frame.GetYaxis().SetLabelSize(0.03)
    frame.SetXTitle("m_{X} (GeV)")
    frame.GetXaxis().SetTitleSize(0.035)
    frame.GetXaxis().SetLabelSize(0.03)
    frame.GetXaxis().SetTitleOffset(1.5)
    frame.Draw()
    
    tgr_2016exp.Draw('l same')
    tgr_2017exp.Draw('l same')
    tgr_2018exp.Draw('l same')
    tgr_201620172018exp.Draw('l same')
    tgr_theory.Draw('l same')



    
    import CMS_lumi as CMS_lumi
    CMS_lumi.lumi_13TeV='137 fb^{-1}'
    CMS_lumi.writeExtraText=1
    CMS_lumi.extraText="Preliminary"
    CMS_lumi.relPosX = 0.12
    CMS_lumi.lumi_sqrtS = '13 TeV'
    iPeriod = 4
    iPos  = 0
    CMS_lumi.CMS_lumi(tcanvas, iPeriod, iPos)
    #x1 y1 x2 y2
    leg= ROOT.TLegend(0.5,0.75,0.95,0.94)
    leg.SetFillColor(0)
    leg.SetBorderSize(1)
    leg.SetTextFont(8)
    leg.SetTextSize(20)
    if not tag=='': tag = ' '+tag
    leg.AddEntry(tgr_2016exp,     "Expected Limit 2016"+tag,"l")
    leg.AddEntry(tgr_2017exp,     "Expected Limit 2017"+tag,"l")
    leg.AddEntry(tgr_2018exp,     "Expected Limit 2018"+tag,"l")
    leg.AddEntry(tgr_201620172018exp,     "3yrs combined"+tag,"l")
    leg.AddEntry(tgr_theory,      "SM-like scenario, f_{vbf}=0",'l')
    
    leg.Draw("same")
    tag=tag.replace(' ','_')
    tcanvas.SaveAs('compare'+tag+'.png')

def CompareExpLimitsEachRegion(dirname_prefix):
    import tdrStyle as tdrStyle
    tdrStyle.setTDRStyle()

    tcanvas = ROOT.TCanvas( 'tcanvas_each_r', 'distro_each_r',800,600)
    tcanvas.cd()
    tcanvas.SetLogy()
    tcanvas.SetGrid()

        
    dic_limit=GetLimit(dirname_prefix+'_201620172018Boosted','exp.txt')
    tgr_201620172018expBoosted=GetLimitGraph(dic_limit)
    dic_201620172018expBoosted=copy.deepcopy(dic_limit)

    dic_limit=GetLimit(dirname_prefix+'_201620172018Resolved','exp.txt')
    tgr_201620172018expResolved=GetLimitGraph(dic_limit)
    dic_201620172018expResolved=copy.deepcopy(dic_limit)

    dic_limit=GetLimit(dirname_prefix+'_201620172018','exp.txt')
    tgr_201620172018exp=GetLimitGraph(dic_limit)
    dic_201620172018exp=copy.deepcopy(dic_limit)
    
    dic_limit=GetggHWWXsec()
    tgr_theory=GetLimitGraph(dic_limit)
    dic_theory=copy.deepcopy(dic_limit)
    
    dic_total=copy.deepcopy(dic_201620172018expBoosted)
    dic_total.update(dic_201620172018expResolved)
    dic_total.update(dic_theory)
    miny,maxy=GetMinMaxFromDic(dic_total)
    
    tgr_201620172018expBoosted.SetLineStyle(2)
    tgr_201620172018expBoosted.SetLineColor(ROOT.kBlue)

    tgr_201620172018expResolved.SetLineStyle(2)
    tgr_201620172018expResolved.SetLineColor(ROOT.kGreen)

    tgr_201620172018exp.SetLineStyle(2)
    tgr_201620172018exp.SetLineColor(ROOT.kBlack)
    

    tgr_theory.SetLineColor(ROOT.kRed)
    
    
    masses=[200,210,230,250,270,300,350,400,450,500,550,600,650,700,750,800,850,900,1000,1500,2000,2500,3000,4000,5000]
    Nmass=len(masses)
    frame = ROOT.TH2F("frame","",Nmass,min(masses),max(masses),100,miny*0.1,maxy*10)
    frame.SetYTitle("Limit 95% CL_{s} on #sigma_{X#rightarrowWW} [pb]")
    frame.GetYaxis().SetTitleSize(0.05)
    frame.GetYaxis().SetLabelSize(0.03)
    frame.SetXTitle("m_{X} (GeV)")
    frame.GetXaxis().SetTitleSize(0.035)
    frame.GetXaxis().SetLabelSize(0.03)
    frame.GetXaxis().SetTitleOffset(1.5)
    frame.Draw()
    
    tgr_201620172018expBoosted.Draw('l same')
    tgr_201620172018expResolved.Draw('l same')
    tgr_201620172018exp.Draw('l same')
    tgr_theory.Draw('l same')



    
    import CMS_lumi as CMS_lumi
    CMS_lumi.lumi_13TeV='137 fb^{-1}'
    CMS_lumi.writeExtraText=1
    CMS_lumi.extraText="Preliminary"
    CMS_lumi.relPosX = 0.12
    CMS_lumi.lumi_sqrtS = '13 TeV'
    iPeriod = 4
    iPos  = 0
    CMS_lumi.CMS_lumi(tcanvas, iPeriod, iPos)
    #x1 y1 x2 y2
    leg= ROOT.TLegend(0.5,0.75,0.95,0.94)
    leg.SetFillColor(0)
    leg.SetBorderSize(1)
    leg.SetTextFont(8)
    leg.SetTextSize(20)
    
    leg.AddEntry(tgr_201620172018expBoosted,     "Expected Limit, Boosted","l")
    leg.AddEntry(tgr_201620172018expResolved,     "Expected Limit, Resolved","l")
    leg.AddEntry(tgr_201620172018exp,     "Expected Limit combined, ","l")
    leg.AddEntry(tgr_theory,      "SM-like scenario, f_{vbf}=0",'l')
    
    leg.Draw("same")
    
    tcanvas.SaveAs('compare_region.png')


if __name__ == '__main__':
    CompareExpLimitsEachYear('exp','') ## Combine Boosted+Resolved
    CompareExpLimitsEachYear('exp','Boosted') ## Combine Boosted only
    CompareExpLimitsEachYear('exp','Resolved') ## Combine Resolved only


    CompareExpLimitsEachRegion('exp')
