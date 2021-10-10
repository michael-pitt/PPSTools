import os
import sys
import optparse
import shutil

#analysis channels
channels=["mu", "el", "mj"]

def buildCondorFile(opt,FarmDirectory):

    """ builds the condor file to submit the MC production """

    cmssw=os.environ['CMSSW_BASE']

    cards=opt.cards.split(',')
    if(len(cards)<2): print('INFO: Simulate %s'%(cards[0]))
    else: print('INFO: Simulation for the following %d cards:\n%s'%(len(cards),cards))

    #condor submission file
    condorFile='%s/condor_generator.sub'%(FarmDirectory)
    print '\nWrites: ',condorFile
    with open (condorFile,'w') as condor:
        condor.write('executable = {0}/worker.sh\n'.format(FarmDirectory))
        condor.write('output     = {0}/output$(ClusterId).out\n'.format(FarmDirectory))
        condor.write('error      = {0}/output$(ClusterId).err\n'.format(FarmDirectory))
        condor.write('log        = {0}/output$(ClusterId).log\n'.format(FarmDirectory))
        condor.write('+JobFlavour = "testmatch"\n')
        OpSysAndVer = str(os.system('cat /etc/redhat-release'))
        if 'SLC' in OpSysAndVer:
            OpSysAndVer = "SLCern6"
        else:
            OpSysAndVer = "CentOS7"
        condor.write('requirements = (OpSysAndVer =?= "{0}")\n'.format(OpSysAndVer))

        for i in range(len(cards)):
            card=cards[i]
            cardname=card.split('/')[-1]
            output=opt.output+'/'+cardname
            for ch in channels:
              os.system('mkdir -vp %s_%s'%(output,ch))
            for j in range(opt.Njobs):
              condor.write('arguments = %s %d\n'%(card,j))
              condor.write('queue 1\n')

    workerFile='%s/worker.sh'%(FarmDirectory)
    with open(workerFile,'w') as worker:
        worker.write('#!/bin/bash\n')
        worker.write('startMsg="Job started on "`date`\n')
        worker.write('echo $startMsg\n')
        worker.write('export HOME=%s\n'%os.environ['HOME']) #otherwise, 'dasgoclient' won't work on condor
        worker.write('export X509_USER_PROXY=%s\n'%os.environ['X509_USER_PROXY'])
        worker.write('########### INPUT SETTINGS ###########\n')
        worker.write('cardname=`echo ${1} | rev | cut -d"/" -f1 | rev`\n')
        worker.write('idx=$(printf "%03d" `expr ${2} + 0`)\n')
        worker.write('######################################\n')
        worker.write('WORKDIR=`pwd`/${cardname}_${idx}; mkdir -pv $WORKDIR\n')
        worker.write('echo "Working directory is ${WORKDIR}"\n')
        worker.write('cd %s\n'%cmssw)
        worker.write('eval `scram r -sh`\n')
        worker.write('cd ${WORKDIR}\n')
        worker.write('echo "Produce miniAOD"\n')
        worker.write('$CMSSW_BASE/src/PPSTools/LowPU2017H/scripts/gen_miniaod.sh $1 $2 %d\n'%opt.Nevents)
        worker.write('echo "run proton reco"\n')
        worker.write('cmsRun $CMSSW_BASE/src/PPSTools/NanoTools/test/addProtons_miniaod.py inputFiles=file:miniAOD.root instance=""\n')
        worker.write('echo "MINIAOD-NANOAOD starting"\n')
        worker.write('cmsRun $CMSSW_BASE/src/PPSTools/NanoTools/test/produceNANO.py inputFiles=file:miniAOD_withProtons.root instance=""\n')
        worker.write('echo "Analysis starting"\n')
        for channel in channels:
          worker.write('$CMSSW_BASE/src/PhysicsTools/NanoAODTools/scripts/nano_postproc.py $PWD output_nano.root --bi $CMSSW_BASE/src/PPSTools/LowPU2017H/scripts/keep_and_drop_in.txt --bo $CMSSW_BASE/src/PPSTools/LowPU2017H/scripts/keep_and_drop_out.txt -I PPSTools.LowPU2017H.LowPU_analysis analysis_%s\n'%channel)
          worker.write('cp output_nano_Skim.root %s/${cardname}_%s/skim_events_${idx}.root\n'%(opt.output,channel))
        worker.write('\necho clean output\ncd ../\nrm -rf ${WORKDIR}\n')
        worker.write('echo $startMsg\n')
        worker.write('echo job finished on `date`\n')
    os.system('chmod u+x %s'%(workerFile))

    return condorFile

def main():

    if not os.environ.get('CMSSW_BASE'):
      print('ERROR: CMSSW not set')
      sys.exit(0)
    
    cmssw=os.environ['CMSSW_BASE']

    #configuration
    usage = 'usage: %prog [options]'
    parser = optparse.OptionParser(usage)
    parser.add_option('-c', '--cards',   dest='cards',   help='input card',        default=cmssw+'/src/PPSTools/LowPU2017H/data/cards/dijet_Pt100_TuneCP5_13TeV', type='string')
    parser.add_option('-o', '--out',     dest='output',  help='output directory',  default='/eos/home-m/mpitt/LowMu/MC/nanoAOD', type='string')
    parser.add_option('-n', '--nevents', dest='Nevents', help='number of events to generate',  default=500, type='int')
    parser.add_option('-j', '--njobs',   dest='Njobs',   help='number of jobs',    default=1000, type='int')
    parser.add_option('-s', '--submit',  dest='submit',  help='submit jobs',       action='store_true')
    (opt, args) = parser.parse_args()
     
    #prepare directory with scripts
    FarmDirectory=os.environ['PWD']+'/FarmLocalNtuple'
    if not os.path.exists(FarmDirectory):  os.system('mkdir -vp '+FarmDirectory)
    print('\nINFO: IMPORTANT MESSAGE: RUN THE FOLLOWING SEQUENCE:')
    print('voms-proxy-init --voms cms --out %s/myproxy509\n'%FarmDirectory)
    os.environ['X509_USER_PROXY']='%s/myproxy509'%FarmDirectory

    #build condor submission script and launch jobs
    condor_script=buildCondorFile(opt,FarmDirectory)

    #submit to condor
    if opt.submit:
        os.system('condor_submit {}'.format(condor_script))
    else:
        print('condor_submit {}\n'.format(condor_script))
		

if __name__ == "__main__":
    sys.exit(main())
