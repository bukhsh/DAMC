import oats
from oats.run import atc, fbmc

CaseStudy_atc  = '/home/waqquas/DAMC/case studies/example_atc.xlsx'
CaseStudy_fmbc = '/home/waqquas/DAMC/case studies/example_fmbc.xlsx'


# atc(neos=False, solver='cplex', tc=CaseStudy_atc)
fbmc(neos=False, solver='cplex', tc=CaseStudy_fmbc)
