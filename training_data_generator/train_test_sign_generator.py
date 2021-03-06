import pandas as pd
import random as ran
import numpy as np
import re
import time
import itertools
ran.seed(time.time())

class Sign_Maker(object):

	def __init__(self, auto=True):
		if auto == True or auto == False:
			self.auto = auto
		else:
			self.auto = True

		self.sign_name_list = ['steal','take','swing','bunt','hit-and-run','squeeze','power','contact','ice','fake steal']
		self.sign_prefix1 = ['l','r','m']
		self.sign_prefix2 = ['u','l','m']
		self.sign_mid = ['v','h','t','g','p']
		self.sign_suffix = ['a','h','n','l','e','b','h','c','f','c','t']
		self.sign_alts = ['#','*']

		self.signs = self._define_signs()

	def _define_signs(self):
		'''
		if auto = False, let's user name signs and define the rules for said signs. If false, signs are auto-generated.
		Default: auto = True
		'''
		n_signs = 10
		signs = {}
		
		if self.auto == False:
			n_signs_input = input('How many signs would you like to define?')
			n_signs = int(n_signs_input)

			for i in range(0,n_signs):
				sign_name = input('Enter the name of your sign: ')
				sign_rule = input('''Enter the rules of your signs. Separate sign actions by spaces.

Legends: *=random sign, #=any number of random signs,
Prefix1 (H-Location): l=left, r=right, m=mid
Prefix2 (V-Location): u=upper, l=lower, m=mid
Middle (Action): v=vertical swipe, h=horizontal swipe, t=tap, g=grab, p=point
Suffix (Bodypart): a=arm, h=hand, n=nose, l=lip, e=ear, b=brim, h=hat crown, f=face, c=chest, t=leg

Example: # mmtn * lmva * mmhl # (randoms, tap mid nose, random, v-swipe left arm, random, h-swipe lip, randoms)
: ''')

				signs[sign_name] = sign_rule

		else:
			sign_names = self.sign_name_list[:]
			for i in range(0,n_signs):
				sign_name = ran.choice(sign_names)
				sign_names.remove(sign_name)

				sign_length = ran.randint(1,5)
				
				sign = []
				for j in range(0,sign_length):
					sign_type = ran.randint(1,12)
					if sign_type < 9:
						sign_action = self._create_random_signs(False)
						sign.append(sign_action)
					else:
						sign_alt_choice = ran.randint(1,10)
						if sign_alt_choice < 8:
							sign_action = '*'
						else:
							sign_action = '#'

						sign.append(sign_action)

				sign.insert(0,'#')
				sign.append('#')

				sign = [i for i,j in itertools.groupby(sign)]

				str_sign = ' '.join(sign)

				if re.search('[a-zA-Z]', str_sign) == None:
					str_sign += ' '+self._create_random_signs(False)+' #'
				signs[sign_name] = str_sign
		
		return signs

	def create_train_data(self, n_rows=100000):
		'''
		Takes list of signs and creates training data of both signs and no signs.
		'''
		train_set = []
		for i in range(0,n_rows):
			train_set.append([i, self._create_random_signs(True, ran.randint(1,10)), 'none'])
		for i in range(0, int(n_rows * .8)):
			name, sign = ran.choice(list(self.signs.items()))

			train_set[i] = [i, self._update_special_characters(sign), name]

		np_train_set = np.array(train_set)

		np.random.shuffle(np_train_set)

		return np_train_set

	def _update_special_characters(self, sign):
		'''
		Function that employs simple regex's to replace the special sign characters with random signs.
		'''
		new_sign = re.sub(r'\*', self._create_random_signs(False), sign)
		new_sign2 = re.sub(r'\#+', self._create_random_signs(True, ran.randint(1,3)), new_sign)

		return new_sign2

	def _create_random_signs(self, is_multiple=False, multiple_range=None):
		'''
		Function to create the random code to indicate the sign being given.
		'''
		if is_multiple == False:
			random_sign = ''.join([ran.choice(self.sign_prefix1),ran.choice(self.sign_prefix2),ran.choice(self.sign_mid),ran.choice(self.sign_suffix)])
			return random_sign
		else:
			random_sign = []
			for i in range(0,multiple_range):
				sign = ''.join([ran.choice(self.sign_prefix1),ran.choice(self.sign_prefix2),ran.choice(self.sign_mid),ran.choice(self.sign_suffix)])
				random_sign.append(sign)
			random_signs = ' '.join(random_sign)
			
			return random_signs

	def _dedupe_adjacent(self, sign):
		for i in xrange(len(sign)-1, 0, -1):
			if sign[i] == sign[i-1]:
				del sign[i]