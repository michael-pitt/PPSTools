class ObjectSelector:
    def __init__(self, _year = "None" ):
        self.year = _year


class ProtonSelector(ObjectSelector):
    def __init__(self, _era = "2017H"):

        self.era = _era
        self.apperture = [8*[0], 8*[0]]
        self.xmin={}
        self.ymin={}
        self.xmax={}
        self.ymax={}

        #Aperture cuts (https://twiki.cern.ch/twiki/bin/view/CMS/TaggedProtonsFiducialCuts)
        #-ThXMax = ([0]*Xangle+[1])+((xi<([2]*Xangle+[3]))*([4]*Xangle+[5])+(xi<([2]*Xangle+[3]))*([6]*Xangle+[7]))*(xi-([2]*Xangle+[3]))
        if self.era=='2017B' or self.era=='2017C1' or self.era=='2017C2' or self.era=='2017D':
                self.apperture[0][0]=-8.71198E-07
                self.apperture[0][1]=0.000134726
                self.apperture[0][2]=0.000264704
                self.apperture[0][3]=0.081951
                self.apperture[0][4]=-4.32065E-05
                self.apperture[0][5]=0.0130746
                self.apperture[0][6]=-0.000183472
                self.apperture[0][7]=0.0395241
                self.apperture[1][0]=0.0
                self.apperture[1][1]=3.43116E-05
                self.apperture[1][2]=0.000626936
                self.apperture[1][3]=0.061324
                self.apperture[1][4]=0.0
                self.apperture[1][5]=0.00654394
                self.apperture[1][6]=-0.000145164
                self.apperture[1][7]=0.0272919
        elif self.era=='2017E' or self.era=='2017F1' or self.era=='2017F2' or self.era=='2017F3' or self.era=='2017H':
                self.apperture[0][0]=-8.92079E-07
                self.apperture[0][1]=0.000150214
                self.apperture[0][2]=0.000278622
                self.apperture[0][3]=0.0964383
                self.apperture[0][4]=-3.9541e-05
                self.apperture[0][5]=0.0115104
                self.apperture[0][6]=-0.000108249
                self.apperture[0][7]=0.0249303
                self.apperture[1][0]=0.0
                self.apperture[1][1]=4.56961E-05
                self.apperture[1][2]=0.00075625
                self.apperture[1][3]=0.0643361
                self.apperture[1][4]=-3.01107e-05
                self.apperture[1][5]=0.00985126
                self.apperture[1][6]=-8.95437e-05
                self.apperture[1][7]=0.0169474
        elif '2018' in self.era:
                self.apperture[0][0]=-8.44219E-07
                self.apperture[0][1]=0.000100957
                self.apperture[0][2]=0.000247185
                self.apperture[0][3]=0.101599
                self.apperture[0][4]=-1.40289E-05
                self.apperture[0][5]=0.00727237
                self.apperture[0][6]=-0.000107811
                self.apperture[0][7]=0.0261867
                self.apperture[1][0]=4.74758E-07
                self.apperture[1][1]=-3.0881E-05
                self.apperture[1][2]=0.000727859
                self.apperture[1][3]=0.0722653
                self.apperture[1][4]=-2.43968E-05
                self.apperture[1][5]=0.0085461
                self.apperture[1][6]=-7.19216E-05
                self.apperture[1][7]=0.0148267
                                
        #Pixel Fiducial cuts (https://twiki.cern.ch/twiki/bin/viewauth/CMS/TaggedProtonsPixelEfficiencies)
        if self.era=='2017B':
                self.xmin[(0,0)]=-100
                self.xmax[(0,0)]=100
                self.ymin[(0,0)]=-100
                self.ymax[(0,0)]=100
                self.xmin[(0,2)]=1.995
                self.xmax[(0,2)]=24.479
                self.ymin[(0,2)]=-11.098
                self.ymax[(0,2)]=4.298
                self.xmin[(1,0)]=-100
                self.xmax[(1,0)]=100
                self.ymin[(1,0)]=-100
                self.ymax[(1,0)]=100
                self.xmin[(1,2)]=2.422
                self.xmax[(1,2)]=24.62
                self.ymin[(1,2)]=-10.698
                self.ymax[(1,2)]=4.698
        elif self.era=='2017C1':
                self.xmin[(0,0)]=-100
                self.xmax[(0,0)]=100
                self.ymin[(0,0)]=-100
                self.ymax[(0,0)]=100
                self.xmin[(0,2)]=1.86
                self.xmax[(0,2)]=24.334
                self.ymin[(0,2)]=-11.098
                self.ymax[(0,2)]=4.298
                self.xmin[(1,0)]=-100
                self.xmax[(1,0)]=100
                self.ymin[(1,0)]=-100
                self.ymax[(1,0)]=100
                self.xmin[(1,2)]=2.422
                self.xmax[(1,2)]=24.62
                self.ymin[(1,2)]=-10.698
                self.ymax[(1,2)]=4.698
        elif self.era=='2017C2':
                self.xmin[(0,0)]=-100
                self.xmax[(0,0)]=100
                self.ymin[(0,0)]=-100
                self.ymax[(0,0)]=100
                self.xmin[(0,2)]=1.86
                self.xmax[(0,2)]=24.334
                self.ymin[(0,2)]=-11.098
                self.ymax[(0,2)]=4.298
                self.xmin[(1,0)]=-100
                self.xmax[(1,0)]=100
                self.ymin[(1,0)]=-100
                self.ymax[(1,0)]=100
                self.xmin[(1,2)]=2.422
                self.xmax[(1,2)]=24.62
                self.ymin[(1,2)]=-10.698
                self.ymax[(1,2)]=4.698
        elif self.era=='2017D':
                self.xmin[(0,0)]=-100
                self.xmax[(0,0)]=100
                self.ymin[(0,0)]=-100
                self.ymax[(0,0)]=100
                self.xmin[(0,2)]=1.86
                self.xmax[(0,2)]=24.334
                self.ymin[(0,2)]=-11.098
                self.ymax[(0,2)]=4.298
                self.xmin[(1,0)]=-100
                self.xmax[(1,0)]=100
                self.ymin[(1,0)]=-100
                self.ymax[(1,0)]=100
                self.xmin[(1,2)]=2.422
                self.xmax[(1,2)]=24.62
                self.ymin[(1,2)]=-10.698
                self.ymax[(1,2)]=4.698
        elif self.era=='2017E':
                self.xmin[(0,0)]=-100
                self.xmax[(0,0)]=100
                self.ymin[(0,0)]=-100
                self.ymax[(0,0)]=100
                self.xmin[(0,2)]=1.995
                self.xmax[(0,2)]=24.479
                self.ymin[(0,2)]=-10.098
                self.ymax[(0,2)]=4.998
                self.xmin[(1,0)]=-100
                self.xmax[(1,0)]=100
                self.ymin[(1,0)]=-100
                self.ymax[(1,0)]=100
                self.xmin[(1,2)]=2.422
                self.xmax[(1,2)]=24.62
                self.ymin[(1,2)]=-9.698
                self.ymax[(1,2)]=5.398
        elif self.era=='2017F1':
                self.xmin[(0,0)]=-100
                self.xmax[(0,0)]=100
                self.ymin[(0,0)]=-100
                self.ymax[(0,0)]=100
                self.xmin[(0,2)]=1.995
                self.xmax[(0,2)]=24.479
                self.ymin[(0,2)]=-10.098
                self.ymax[(0,2)]=4.998
                self.xmin[(1,0)]=-100
                self.xmax[(1,0)]=100
                self.ymin[(1,0)]=-100
                self.ymax[(1,0)]=100
                self.xmin[(1,2)]=2.422
                self.xmax[(1,2)]=24.62
                self.ymin[(1,2)]=-9.698
                self.ymax[(1,2)]=5.398
        elif self.era=='2017F2':
                self.xmin[(0,0)]=-100
                self.xmax[(0,0)]=100
                self.ymin[(0,0)]=-100
                self.ymax[(0,0)]=100
                self.xmin[(0,2)]=1.995
                self.xmax[(0,2)]=24.479
                self.ymin[(0,2)]=-10.098
                self.ymax[(0,2)]=4.998
                self.xmin[(1,0)]=-100
                self.xmax[(1,0)]=100
                self.ymin[(1,0)]=-100
                self.ymax[(1,0)]=100
                self.xmin[(1,2)]=2.422
                self.xmax[(1,2)]=24.62
                self.ymin[(1,2)]=-9.698
                self.ymax[(1,2)]=5.398
        elif self.era=='2017F3':
                self.xmin[(0,0)]=-100
                self.xmax[(0,0)]=100
                self.ymin[(0,0)]=-100
                self.ymax[(0,0)]=100
                self.xmin[(0,2)]=1.995
                self.xmax[(0,2)]=24.479
                self.ymin[(0,2)]=-10.098
                self.ymax[(0,2)]=4.998
                self.xmin[(1,0)]=-100
                self.xmax[(1,0)]=100
                self.ymin[(1,0)]=-100
                self.ymax[(1,0)]=100
                self.xmin[(1,2)]=2.422
                self.xmax[(1,2)]=24.62
                self.ymin[(1,2)]=-9.698
                self.ymax[(1,2)]=5.398
        elif self.era=='2017H':
                self.xmin[(0,0)]=-100
                self.xmax[(0,0)]=100
                self.ymin[(0,0)]=-100
                self.ymax[(0,0)]=100
                self.xmin[(0,2)]=1.995
                self.xmax[(0,2)]=24.479
                self.ymin[(0,2)]=-10.098
                self.ymax[(0,2)]=4.998
                self.xmin[(1,0)]=-100
                self.xmax[(1,0)]=100
                self.ymin[(1,0)]=-100
                self.ymax[(1,0)]=100
                self.xmin[(1,2)]=2.422
                self.xmax[(1,2)]=24.62
                self.ymin[(1,2)]=-9.698
                self.ymax[(1,2)]=5.398
        elif self.era=='2018A':
                self.xmin[(0,0)]=2.71
                self.xmax[(0,0)]=17.927
                self.ymin[(0,0)]=-11.598
                self.ymax[(0,0)]=3.698
                self.xmin[(0,2)]=2.278
                self.xmax[(0,2)]=24.62
                self.ymin[(0,2)]=-10.898
                self.ymax[(0,2)]=4.398
                self.xmin[(1,0)]=3
                self.xmax[(1,0)]=18.498
                self.ymin[(1,0)]=-11.298
                self.ymax[(1,0)]=4.098
                self.xmin[(1,2)]=2.42
                self.xmax[(1,2)]=20.045
                self.ymin[(1,2)]=-10.398
                self.ymax[(1,2)]=5.098
        elif self.era=='2018B1':
                self.xmin[(0,0)]=2.85
                self.xmax[(0,0)]=17.927
                self.ymin[(0,0)]=-11.598
                self.ymax[(0,0)]=3.698
                self.xmin[(0,2)]=2.42
                self.xmax[(0,2)]=24.62
                self.ymin[(0,2)]=-10.798
                self.ymax[(0,2)]=4.298
                self.xmin[(1,0)]=3
                self.xmax[(1,0)]=18.07
                self.ymin[(1,0)]=-11.198
                self.ymax[(1,0)]=4.098
                self.xmin[(1,2)]=2.42
                self.xmax[(1,2)]=25.045
                self.ymin[(1,2)]=-10.398
                self.ymax[(1,2)]=5.098
        elif self.era=='2018B2':
                self.xmin[(0,0)]=2.562
                self.xmax[(0,0)]=17.64
                self.ymin[(0,0)]=-11.098
                self.ymax[(0,0)]=4.198
                self.xmin[(0,2)]=2.135
                self.xmax[(0,2)]=24.62
                self.ymin[(0,2)]=-11.398
                self.ymax[(0,2)]=3.798
                self.xmin[(1,0)]=3
                self.xmax[(1,0)]=17.931
                self.ymin[(1,0)]=-10.498
                self.ymax[(1,0)]=4.698
                self.xmin[(1,2)]=2.279
                self.xmax[(1,2)]=24.76
                self.ymin[(1,2)]=-10.598
                self.ymax[(1,2)]=4.498
        elif self.era=='2018C':
                self.xmin[(0,0)]=2.564
                self.xmax[(0,0)]=17.93
                self.ymin[(0,0)]=-11.098
                self.ymax[(0,0)]=4.198
                self.xmin[(0,2)]=2.278
                self.xmax[(0,2)]=24.62
                self.ymin[(0,2)]=-11.398
                self.ymax[(0,2)]=3.698
                self.xmin[(1,0)]=3
                self.xmax[(1,0)]=17.931
                self.ymin[(1,0)]=-10.498
                self.ymax[(1,0)]=4.698
                self.xmin[(1,2)]=2.279
                self.xmax[(1,2)]=24.76
                self.ymin[(1,2)]=-10.598
                self.ymax[(1,2)]=4.398
        elif self.era=='2018D1':
                self.xmin[(0,0)]=2.847
                self.xmax[(0,0)]=17.93
                self.ymin[(0,0)]=-11.098
                self.ymax[(0,0)]=4.098
                self.xmin[(0,2)]=2.278
                self.xmax[(0,2)]=24.62
                self.ymin[(0,2)]=-11.398
                self.ymax[(0,2)]=3.698
                self.xmin[(1,0)]=3
                self.xmax[(1,0)]=17.931
                self.ymin[(1,0)]=-10.498
                self.ymax[(1,0)]=4.698
                self.xmin[(1,2)]=2.279
                self.xmax[(1,2)]=24.76
                self.ymin[(1,2)]=-10.598
                self.ymax[(1,2)]=4.398
        elif self.era=='2018D2':
                self.xmin[(0,0)]=2.847
                self.xmax[(0,0)]=17.931
                self.ymin[(0,0)]=-10.598
                self.ymax[(0,0)]=4.498
                self.xmin[(0,2)]=2.278
                self.xmax[(0,2)]=24.62
                self.ymin[(0,2)]=-11.598
                self.ymax[(0,2)]=3.398
                self.xmin[(1,0)]=3
                self.xmax[(1,0)]=17.931
                self.ymin[(1,0)]=-10.498
                self.ymax[(1,0)]=4.698
                self.xmin[(1,2)]=2.279
                self.xmax[(1,2)]=24.76
                self.ymin[(1,2)]=-10.598
                self.ymax[(1,2)]=3.898

                      
    def evalProton(self, proton, xangle = 150.0 ):
        
        arm = proton.arm
        
        # check aperture cuts in (xi,ThX) plane
        x = self.apperture[arm]
        xi_cut = x[2]*xangle+x[3]
        thXmax = (x[0]*xangle+x[1]) + ((x[4]*xangle+x[5]) if (proton.xi<xi_cut) else  (x[6]*xangle+x[7])) * (proton.xi - xi_cut)
        if proton.thetaX > -thXmax: return False
        
        #check pixel track fiducial cuts
        x, y = proton.xfar, proton.yfar; rp=(arm,2)
        if (x<self.xmin[rp] or y<self.ymin[rp] or x>self.xmax[rp] or y>self.ymax[rp]): return False
        if '2017' in self.era: return True
        x, y= proton.xnear, proton.ynear; rp=(arm,0)
        if (x<self.xmin[rp] or y<self.ymin[rp] or x>self.xmax[rp] or y>self.ymax[rp]): return False
        
        return True


class ElectronSelector(ObjectSelector):
    def __init__(self, _minPt = 25):
        self.minPt = _minPt

    def evalElectron(self, el):
        
        isEBEE = True if abs(el.eta)>1.4442 and abs(el.eta)<1.5660 else False
        
        if isEBEE: return False
        if el.pt < self.minPt: return False
        if abs(el.eta) > 2.4: return False
        #if abs(el.dxy) > 0.05 or abs(el.dz) > 0.2: return False
        #if not el.mvaFall17V2noIso_WP80: return False
        if el.cutBased<3: return False

        return True
        
class MuonSelector(ObjectSelector):
    def __init__(self, _minPt = 25, _id = 'medium'):
        self.minPt = _minPt
        self.id = _id

    def evalMuon(self, mu):

        if mu.pt < self.minPt: return False
        if abs(mu.eta) > 2.4: return False
        if mu.pfRelIso04_all>0.4: return False
        #if abs(mu.dxybs) > 0.05 or abs(mu.dz) > 1.0: return False
        if abs(mu.dxybs) > 0.05: return False
        if self.id == 'tight' and not mu.tightId: return False
        elif self.id == 'medium' and not mu.mediumId: return False
        elif self.id == 'loose' and not mu.looseId: return False
        return True
        
