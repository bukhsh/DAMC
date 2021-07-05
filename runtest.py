import oats
from oats.run import fbmc

CaseStudy = '/home/waqquas/FBMC/case studies/example10.xlsx'
fbmc(neos=False, solver='cplex', tc=CaseStudy)
