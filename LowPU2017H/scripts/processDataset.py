import os
import sys
import optparse

def main():

    #configuration
    usage = 'usage: %prog [options]'
    parser = optparse.OptionParser(usage)
    parser.add_option('-i', '--in',     dest='input',  help='input dataset',    default='/SingleMuon/Run2017H-UL2017_MiniAODv1_NanoAODv2-v1/NANOAOD', type='string')
    parser.add_option('-o', '--out',    dest='output', help='output directory', default='/eos/user/p/psilva/data/sdanalysis/SingleMuon/Chunks', type='string')
    parser.add_option('--dry',          dest='dry',    help='don\'t submit', action='store_true')
    (opt, args) = parser.parse_args()

    cmssw=os.environ['CMSSW_BASE']

    #start a proxy
    proxy='{}/src/PPSTools/LowPU2017H/data/voms_proxy.txt'.format(cmssw)
    print('Warning: assuming you have a valid proxy under {}'.format(proxy))
    print('If not the case, before submitting to condor, please start one with')
    print('voms-proxy-init --voms cms --valid 172:00 --out {}'.format(proxy))
        
    #get list of files
    file_list=os.popen('dasgoclient --query=\"file dataset={} status=*\"'.format(opt.input)).read().split()

    #prepare output
    os.system('mkdir -p {}'.format(opt.output))

    #print a condor file
    condor_script='{}_condor.sub'.format( opt.input.replace('/','_')[1:] )
    scripts_dir='{}/src/PPSTools/LowPU2017H/scripts'.format(cmssw)
    with open (condor_script,'w') as condor:
        condor.write('executable = {}/lowpu_worker.sh\n'.format(scripts_dir))
        condor.write('output     = condor/jobs$(ClusterId).out\n')
        condor.write('error      = condor/jobs$(ClusterId).err\n')
        condor.write('log        = condor/jobs$(ClusterId).log\n')
        condor.write('+JobFlavour = "testmatch"\n')
        condor.write('arguments = $(input) {} {}\n'.format(opt.output,cmssw))
        condor.write('queue input from (\n')
        for f in file_list:
            condor.write('\troot://cms-xrd-global.cern.ch/{}\n'.format(f.strip()))
        condor.write(')\n')

    #submit to condor
    if not opt.dry:
        os.system('condor_submit {}'.format(condor_script))



if __name__ == "__main__":
    sys.exit(main())
