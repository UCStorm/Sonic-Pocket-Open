import pygame, sys, numpy, json, math, configparser, os


def extract_timer_frame_oldanimation(animation, timer__frame__old):
	if type(timer__frame__old) is list:
		old_animation 	= timer__frame__old[2]

		if old_animation == animation:
			frame = int(timer__frame__old[1])
			timer = timer__frame__old[0]
		else:
			frame = 0
			timer = 0
	else: 
		frame = 0
		timer = 0
		old_animation = ""

	return timer, frame, old_animation

class SpriteAnimations:
	def update(sprites, animation, timer__frame__old):
		# verification
		timer, frame, old_animation = extract_timer_frame_oldanimation(animation, timer__frame__old)

		# reset Frame
		try: sprites[animation]["FRAME"][frame]
		except: frame = sprites[animation]["LOOP"]

		# timer update
		timer += sprites[animation]["SPEED"]

		if timer > sprites[animation]["DURATION"][frame]:
			timer -= sprites[animation]["DURATION"][frame]
			frame += 1

		# second reset Frame
		try: sprites[animation]["FRAME"][frame]
		except: frame = sprites[animation]["LOOP"]

		return [timer, frame, animation]


	def Advanced_update(sprites, animation, timer__frame__old):
		# verification
		timer, frame, old_animation = extract_timer_frame_oldanimation(animation, timer__frame__old)
		end_animation = False

		# reset Frame
		try: sprites[animation]["FRAME"][frame]
		except: frame = sprites[animation]["LOOP"]

		# timer update
		timer += sprites[animation]["SPEED"]

		if timer > sprites[animation]["DURATION"][frame]:
			timer -= sprites[animation]["DURATION"][frame]
			frame += 1

		# second reset Frame
		try: sprites[animation]["FRAME"][frame]
		except: 
			frame = sprites[animation]["LOOP"]
			end_animation = True

		return [timer, frame, animation], end_animation


	def get_length(sprites, animation) -> int:
		return len(sprites[animation]["FRAME"])

	def get_rotation_id(sprites, animation):
		return sprites[animation]["ROTATION"]
	
	def BaseOn(spritelist, complement_spritelist):
		for complement_sprite in complement_spritelist:
			spritelist[complement_sprite] = complement_spritelist[complement_sprite]
		return spritelist
	

	def load(link_bin, OG_size=[]):
		size = 16
		def negative_number(n):
			if n > 32767: n -= 65536
			return n

		lists = {}

		with open(link_bin, mode='rb') as file: # b is important -> binary
			fileContent = file.read()
			image_list = []
			HitBox_numbers = 0
			Animation_numbers = 0

			line = 8

			N_Texture = int(fileContent[line])
			line += 1
			for n in range(N_Texture):
				lenght_Link = int(fileContent[line])
				line += 1
				Link = str(fileContent[line : line+lenght_Link].decode())
				line += lenght_Link
				list = Link.split("/")
				image_list.append(
					pygame.image.load(f"{os.path.dirname(file.name)}/{list[(len(list) - 1)]}").convert(8))

			HitBox_numbers = int(fileContent[line])
			line += 1

			for n in range(HitBox_numbers): line +=  int(fileContent[line])+1
			Animation_numbers = int(fileContent[line]) + (int(fileContent[line+1])*256)
			line += 2

			for i in range(Animation_numbers):
				len_name = int(fileContent[line])
				line += 1
				name = str(fileContent[line : line+len_name].decode()).replace("\x00", "")
				line += len_name

				Frame_number = int(fileContent[line])
				line += 2
				Speed = int(fileContent[line]) + (int(fileContent[line+1])*256)
				line += 2
				Loop = int(fileContent[line])
				line += 1
				RotationID = int(fileContent[line])
				line += 1
				frames = []
				FrameDuration = []
				Pivots = []
				SIZES = []

				

				for i in range(Frame_number):

					image:pygame.Surface = image_list[int(fileContent[line])]
					COORD = [0, 0]
					SIZE = [0, 0]
					PIVOT = [0, 0]

					line += 1

					FrameDuration.append(int(fileContent[line]) + (int(fileContent[line+1])*256))
					line += 2
					#ID = int(fileContent[line]) + (int(fileContent[line+1])*256)
					line += 2

					COORD[0] = int(fileContent[line]) + (int(fileContent[line+1])*256)
					line += 2
					COORD[1] = int(fileContent[line]) + (int(fileContent[line+1])*256)
					line += 2
					SIZE[0] = int(fileContent[line]) + (int(fileContent[line+1])*256)
					line += 2
					SIZE[1] = int(fileContent[line]) + (int(fileContent[line+1])*256)
					line += 2
					SIZES.append(SIZE)

					PIVOT[0] = negative_number(int(fileContent[line]) + (int(fileContent[line+1])*256))
					line += 2
					PIVOT[1] = negative_number(int(fileContent[line]) + (int(fileContent[line+1])*256))
					Pivots.append(PIVOT)
					line += 2
					line += 4*HitBox_numbers*2

					if SIZE[0] == 0 or SIZE[1] == 0:
						surface = image.subsurface(0, 0, 1, 1).convert(8)
						surface.fill(surface.get_palette_at(0))
					else:
						surface = image.subsurface(COORD[0], COORD[1], SIZE[0], SIZE[1]).convert(8)
					Surfarray = pygame.surfarray.array2d(surface)
					frames.append(Surfarray)

				lists[name] = {
						"SPEED": Speed, "LOOP": Loop, "FRAME": frames, "DURATION": FrameDuration, 
						"PIVOT": Pivots, "ROTATION":RotationID+1, "SIZES": SIZES}

		return lists
