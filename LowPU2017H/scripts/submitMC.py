import os
import sys
import optparse

def main():

    if not os.environ.get('CMSSW_BASE'):
      print('ERROR: CMSSW not set')
      sys.exit(0)
    
    cmssw=os.environ['CMSSW_BASE']

    #configuration
    usage = 'usage: %prog [options]'
    parser = optparse.OptionParser(usage)
    parser.add_option('-c', '--card',    dest='card',    help='input card',        default=cmssw+'/src/data/cards/dijet_Pt100_TuneCP5_13TeV', type='string')
    parser.add_option('-o', '--out',     dest='output',  help='output directory',  default='/eos/home-m/mpitt/LowMu/MC/nanoAOD', type='string')
    parser.add_option('-n', '--nevents', dest='Nevents', help='number of events to generate',  default=100, type='int')
    parser.add_option('-j', '--njobs',   dest='Njobs',   help='number of jobs',    default=500, type='int')
    parser.add_option('-s', '--submit',  dest='submit',  help='submit jobs',       action='store_true')
    (opt, args) = parser.parse_args()


    #check if user started a proxy
    proxy='{}/src/PPSTools/LowPU2017H/data/voms_proxy.txt'.format(cmssw)
    if not os.path.isfile(proxy):
      print('ERROR: no valid proxy under {},\nplease start one with'.format(proxy))
      print('voms-proxy-init --voms cms')
      print('cp `voms-proxy-info -p` {}'.format(proxy))
      sys.exit(0)
    print('INFO: using proxy under {}'.format(proxy))
        
    #prepare output
    card=opt.card.split('/')[-1]
    output=opt.output+'/'+card
    os.system('mkdir -p {}'.format(output))

    #print a condor file
    condor_script='{}_condor.sub'.format( card )
    scripts_dir='{}/src/PPSTools/LowPU2017H/scripts'.format(cmssw)
    with open (condor_script,'w') as condor:
        condor.write('Proxy_path = {}\n'.format(proxy))
        condor.write('executable = {}/gen_worker.sh\n'.format(scripts_dir))
        condor.write('output     = jobs$(ClusterId).out\n')
        condor.write('error      = jobs$(ClusterId).err\n')
        condor.write('log        = jobs$(ClusterId).log\n')
        condor.write('+JobFlavour = "testmatch"\n') #testmatch tomorrow workday
        for i in range(opt.Njobs):
            condor.write('arguments   = $(Proxy_path) %s %d %s %s %d\n'%(opt.card,i,output,cmssw,opt.Nevents))
            condor.write('queue 1\n')
        condor.write('\n')

    #submit to condor
    if opt.submit:
        os.system('condor_submit {}'.format(condor_script))
    else:
        print('condor_submit {}'.format(condor_script))



if __name__ == "__main__":
    sys.exit(main())
