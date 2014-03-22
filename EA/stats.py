import pstats
p = pstats.Stats('resources/restats')
p.strip_dirs().sort_stats('tottime').print_stats()
