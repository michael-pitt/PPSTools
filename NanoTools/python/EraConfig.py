def getEraConfiguration(era,isData):
    
    """ defines global tags, depending on the era """

    globalTags = {
        'era2016preVFP':('106X_mcRun2_asymptotic_preVFP_v11',    '106X_dataRun2_v35'),
        'era2016':('106X_mcRun2_asymptotic_v17',                 '106X_dataRun2_v35'),
        'era2017':('106X_mc2017_realistic_v9',                   '106X_dataRun2_v35'),
        'era2018':('106X_upgrade2018_realistic_v16_L1v1',        '106X_dataRun2_v35')
        }
    ppsFiles   = {
        'era2017_B':('Validation.CTPPS.simu_config.year_2017_preTS2_cff'),
        'era2017_C':('Validation.CTPPS.simu_config.year_2017_preTS2_cff'),
        'era2017_C1':('Validation.CTPPS.simu_config.year_2017_preTS2_cff'),
        'era2017_C2':('Validation.CTPPS.simu_config.year_2017_preTS2_cff'),
        'era2017_D':('Validation.CTPPS.simu_config.year_2017_preTS2_cff'),
        'era2017_E':('Validation.CTPPS.simu_config.year_2017_postTS2_cff'),
        'era2017_F':('Validation.CTPPS.simu_config.year_2017_postTS2_cff'),
        'era2017_F1':('Validation.CTPPS.simu_config.year_2017_postTS2_cff'),
        'era2017_F2':('Validation.CTPPS.simu_config.year_2017_postTS2_cff'),
        'era2017_F3':('Validation.CTPPS.simu_config.year_2017_postTS2_cff'),
        'era2017_H':('Validation.CTPPS.simu_config.year_2017_postTS2_cff'),
        'era2017':('Validation.CTPPS.simu_config.year_2017_cff'),                           
        }    
    
    era_full=era
    era=era_full.split('_')[0]                
    globalTag = globalTags[era][isData]
    ppsFile    = ppsFiles[era_full]

    return globalTag, ppsFile

    