from magnitude import *

specs = {
    'entities':{
        'inlet': {'inflow': MagTwo, 'd': MagThree},
        'container':{'volume': MagThree, 'd': DThree},
        'outlet':{'outflow': MagThree, 'd': DThree}
    },
    'init_state':{
        'inlet': {'inflow': MagTwo.ZERO, 'd': MagThree.ZERO},
        'container':{'volume': MagThree.ZERO, 'd': DThree.ZERO},
        'outlet':{'outflow': MagThree.ZERO, 'd': DThree.ZERO}
    },
    'relations':[
        {
            'ty':'I+',
            'args':None,
            'from':'inlet',
            'to':'container'
        },
        {
            'ty':'I-',
            'args':None,
            'from':'outlet',
            'to':'container'
        },
        {
            'ty':'P+',
            'args':None,
            'from':'container',
            'to':'outlet'
        },
        {
            'ty':'VC',
            'args':[MagThree.MAX, MagThree.MAX],
            'from':'outflow',
            'to':'container'
        },
        {
            'ty':'VC',
            'args':[MagThree.ZERO, MagThree.ZERO],
            'from':'outflow',
            'to':'container'
        }
    ]
}
