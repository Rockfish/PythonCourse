import os

def get_timestamps():
    timestamps = {'Music': {'mac':{'name': 'Music_Mac_Install_3.2.102.dmg'},
                                'win' :{'name': 'Music_Win_Install_3.2.102.exe'}},
                  'Firmware': {'name': 'mfw name'}
                  }

    root, dirs, files = next(os.walk('distribution/Music'))

    for name in files:
        if name.startswith('Music_Mac'):
            timestamps['Music']['mac']['name'] = name
        if name.startswith('Music_Win'):
            timestamps['Music']['win']['name'] = name

    root, dirs, files = next(os.walk('distribution/Firmware'))

    for name in files:
        if name.startswith('MusicZ_Firmware'):
            timestamps['Firmware']['name'] = name

    return timestamps


                          