import os, sys, re
import array
import ROOT
from ROOT import TCanvas, TFile, TH1F, TH2F
# import printer

def zeroBinRemover(histo1D,tdirOut,tdirIn,hName,isVerbose):
    nx=histo1D.GetXaxis().GetNbins()
    #hName = histo1D.GetName()
    histo=TH1F(hName,hName,nx,0,nx)
    l=0
    if "__CMS" in hName:
    	hNominalName=hName[:hName.find("__CMS")]
    elif "_CMS" in hName:
        hNominalName=hName[:hName.find("_CMS")]
    elif "_THU" in hName:
        hNominalName=hName[:hName.find("_THU")]
    elif "_JHU" in hName:
        hNominalName=hName[:hName.find("_JHU")]
    elif "_Jet" in hName:
        hNominalName=hName[:hName.find("_Jet")]
    elif "_JER" in hName:
        hNominalName=hName[:hName.find("_JER")]
    elif "_muES" in hName:
        hNominalName=hName[:hName.find("_muES")]
    elif "_Reco" in hName:
        hNominalName=hName[:hName.find("_Reco")]
    elif "_Rivet" in hName:
        hNominalName=hName[:hName.find("_Rivet")]
    elif "_QCD" in hName:
        hNominalName=hName[:hName.find("_QCD")]
    else:
    	hNominalName=hName[:hName.find("CMS")]
    hNominal=tdirIn.Get(hNominalName)
    if isVerbose is True and hNominal:
        strFormat = '%-25s%-80s%-10s%-20s\n'
        strOut = strFormat % (tdirOut.GetName(), hName,'nominal:',hNominalName)
        print(strOut)
        #printgray(hName+"\t nominal:\t"+hNominalName)
        
    for j in range(1,nx+1):
        l=l+1
        if isVerbose is True and hNominal:
            print(str(hNominal.GetBinContent(l))+"\t"+ str(histo1D.GetBinContent(l)))
        if histo1D.GetBinContent(l)<0.0: # negative bin
            histo.SetBinContent(l,0.0)
            histo.SetBinError(l,0.0)
            #printorange("!"+str(l)+" "+tdirOut.GetName()+" "+hName)
            # print("Find negative!!! "+str(l)+" "+tdirOut.GetName()+" "+hName)
        elif hNominal and hNominal.GetBinContent(l)<=0.0 and histo1D.GetBinContent(l)!=0.0:
            histo.SetBinContent(l,0.0)#hNominal.GetBinContent(l))
            histo.SetBinError(l,0.0)#hNominal.GetBinError(l))
            if isVerbose is True: print("!!!"+str(l)+"th bin set to zero as nominal is zero(or negative)\t ")
        else:
            histo.SetBinContent(l,histo1D.GetBinContent(l))
            histo.SetBinError(l,histo1D.GetBinError(l))

    #printgray('\t No more negative bin ... '+str(histo.Integral()))

    if "Up" in hName or "Down" in hName:
        # Add small values for empty up/down when nominal is non-zero        
	#print " histo: %s, hNominal: %s"%(hName,hNominalName)
	#print "histo.Integral()=", histo.Integral()
	#print "hNominal.Integral()=", hNominal.Integral()
        if histo.Integral()<=0.0 and hNominal.Integral()!=0.0:
            histo.SetBinContent(1,0.001)
            histo.SetBinError(1,0.0)
            if isVerbose is True:
                if "reweight" in hName: 
                    print("Null shapes set to 0.001\t\t"+tdirOut.GetName()+"\t"+hName+"\t"+str(histo.Integral()))
                else : 
                    print("Null shapes set to 0.001\t\t"+tdirOut.GetName()+"\t"+hName+"\t"+str(histo.Integral()))
    
    tdirOut.cd()
    histo.Write()

    

def main():
    filename = sys.argv[1]
    isVerbose = False
    if len(sys.argv)>2: 
        isVerbose = True
        print("Verbose Mode is on")
    
        
    fIn = TFile(filename, 'READ')
    filenameOut = filename[0:-5]+"_noNegativeBins.root"
    fOut = TFile(filenameOut, 'RECREATE')

    for dir in fIn.GetListOfKeys(): 
        tdirName = dir.GetName() 
        fOut.mkdir(tdirName)
        tdirIn = fIn.Get(tdirName)
        tdirOut = fOut.Get(tdirName)
        if isVerbose:
            print("\n>> "+tdirName)
        else:
            print("\n>> "+tdirName)
        tdir = fIn.Get(tdirName)
        for h in tdir.GetListOfKeys():
            hName = h.GetName()
            if "ttH" in hName: continue
            if "ggZH" in hName: continue
            #if "MINLO" in hName: continue
            if "EWKW" in hName: continue
            #if "hww" in hName: continue
            #if "htt_0PM125_" in hName and "htt_0PM125_CMS" not in hName: continue
            #if "htt_0M125_" in hName and "htt_0M125_CMS" not in hName: continue
            #if "htt_0Mf05ph0125_" in hName and "htt_0Mf05ph0125_CMS" not in hName: continue
            histo1D = tdir.Get(hName)
            #printblue(str(histo1D.Integral()))
            zeroBinRemover(histo1D,tdirOut,tdirIn,hName,isVerbose)
            #printmsg("\t"+hName)
    print("Saving output...\n\t"+filenameOut)
    fIn.Close()
    fOut.Close()

if __name__ == "__main__":
    main()

            
        
