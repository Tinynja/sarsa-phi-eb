# Built-in libraries
import pickle
import subprocess

# Pypi libraries
from ale_py import ALEInterface
import ale_py.roms as ROMS
import numpy as np
import matplotlib.pyplot as plt


DISPLAY_FORMAT = 'PAL'


def get_color_palette(rom):
	res = subprocess.run(['python_pipenv.cmd', '-c', f'from ale_py import ALEInterface; from ale_py.roms import {rom}; ALEInterface().loadROM({rom})'], capture_output=True)
	return res.stderr.decode().splitlines()[6].strip().split()[-1]


ale = ALEInterface()
unique_colors = np.empty((0,3), dtype=int)

for rom in ROMS._RESOLVED_ROMS:
	try:
		if get_color_palette(rom) == DISPLAY_FORMAT:
			ale.loadROM(getattr(ROMS, rom))
			img = ale.getScreenRGB()
			unique_colors = np.append(unique_colors, img.reshape(-1,3), axis=0)
			unique_colors = np.unique(unique_colors, axis=0)
			nb_unique = unique_colors.shape[0]
			print(f'Found {nb_unique} unique colors so far...')
	except:
		pass

# Print the palette
print('Here is the gathered palette:')
print(unique_colors)

# Save the palette as pickle
with open(f'{DISPLAY_FORMAT}_Palette.pickle', 'wb') as file:
	pickle.dump(unique_colors, file)

# Show the palette
side_size = int(np.ceil(np.sqrt(nb_unique)))
nb_fillblack = side_size**2 - nb_unique

unique_colors = np.append(unique_colors, np.zeros((nb_fillblack, 3), dtype=int), axis=0)
unique_colors = unique_colors.reshape(side_size, side_size, 3)

plt.imshow(unique_colors)
plt.show()
