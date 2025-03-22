import pygame, sys, numpy, json, math, configparser, os


# Copyright (c) 2023-2025 UCSTORM
# Tous droits réservés.


LOOPMAX = 32
OUT_SIDE = 256

class_type = list[pygame.Mask, pygame.Rect, pygame.Rect]

class Mask:

	class_type = class_type
	
	def clear(sensor1):
		sensor1[0].clear()

	def newSensor(rect, center_point) -> class_type: # rect_to_mask
		""" INSIDE: MASK, RECT+CENTER_POINT, ORIGINAL_RECT"""
		mask = pygame.mask.from_surface(pygame.Surface((rect[2], rect[3])))
		return [mask, pygame.Rect(rect[0]+center_point[0], rect[1]+center_point[1], rect[2], rect[3]), rect]

	def surface_to_mask(surface, rect) -> class_type:
		mask = pygame.mask.from_surface(surface)
		return [mask, pygame.Rect(rect[0], rect[1], surface.get_size()[0], surface.get_size()[1]), pygame.Rect(rect[0], rect[1], surface.get_size()[0], surface.get_size()[1])]

	
	def blit(mask_chunk, coord, sensor) -> class_type:
		sensor[0].draw(mask_chunk[0],coord)
		return sensor

	def collide(sensor1, sensor2):
		return sensor1[0].overlap(sensor2[0], [sensor2[1][0]-sensor1[1][0], sensor2[1][1]-sensor1[1][1]])

	def colliderect(sensor1, sensor2):
		return sensor1[1].colliderect(sensor2[1])
	
	def sensor_draw(surface, sensor, color):
		pygame.draw.rect(surface, color, sensor[1])

	def rotation_sensor(sensor, MODE, center_point):
		""" POSSIBILITY: 0 ,1, 2, 3"""
		rect = [0, 0, 0, 0]
		if MODE == 0: rect = [sensor[2][0], sensor[2][1], sensor[2][2], sensor[2][3]]
		elif MODE == 1: rect = [sensor[2][1], -(sensor[2][0] + sensor[2][2]), sensor[2][3], sensor[2][2]]
		elif MODE == 2: rect = [-(sensor[2][0] + sensor[2][2]), -(sensor[2][1] + sensor[2][3]), sensor[2][2], sensor[2][3]]
		elif MODE == 3: rect = [-(sensor[2][1] + sensor[2][3]), sensor[2][0], sensor[2][3], sensor[2][2]]

		return Mask.rect_to_mask(rect, center_point)

	def collide_inside_y(sensor1, sensor2):
		running = True
		LOOP = 0

		while running:
			if sensor1[0].overlap(sensor2[0], [sensor2[1][0] - sensor1[1][0], sensor2[1][1] - (sensor1[1][1]-LOOP)]):
				LOOP += 1
			else: running = False
			if LOOP >= LOOPMAX:
				running = False
		return LOOP

	def collide_outside_y(sensor1, sensor2):
		running = True
		LOOP = 0

		while running:
			if not sensor1[0].overlap(sensor2[0], [sensor2[1][0] - sensor1[1][0], sensor2[1][1] - (sensor1[1][1] + LOOP)]):
				LOOP += 1
			else:running = False
			if LOOP >= LOOPMAX: running = False
		return LOOP

	def collide_inside_x(sensor1, sensor2):
		running = True
		LOOP = 0

		while running:
			if sensor1[0].overlap(sensor2[0], [sensor2[1][0] - (sensor1[1][0]-LOOP), sensor2[1][1] - (sensor1[1][1])]):
				LOOP += 1
			else: running = False
			if LOOP >= LOOPMAX:running = False
		return LOOP


	def collide_outside_x(sensor1, sensor2):
		running = True
		LOOP = 0

		while running:
			if not sensor1[0].overlap(sensor2[0], [sensor2[1][0] - (sensor1[1][0]+ LOOP), sensor2[1][1] - (sensor1[1][1])]):
				LOOP += 1
			else:running = False
			if LOOP >= LOOPMAX: running = False
		return LOOP


	def collide_inside_y_minus(sensor1, sensor2):
		running = True
		LOOP = 0

		while running:
			if sensor1[0].overlap(sensor2[0], [sensor2[1][0] - sensor1[1][0], sensor2[1][1] - (sensor1[1][1]+LOOP)]):
				LOOP += 1
			else: running = False
			if LOOP >= LOOPMAX:running = False
		return -LOOP


	def collide_outside_y_minus(sensor1, sensor2):
		running = True
		LOOP = 0

		while running:
			if not sensor1[0].overlap(sensor2[0], [sensor2[1][0] - sensor1[1][0], sensor2[1][1] - (sensor1[1][1] - LOOP)]):
				LOOP += 1
			else:running = False
			if LOOP >= LOOPMAX: running = False
		return -LOOP


	def collide_inside_x_minus(sensor1, sensor2):
		running = True
		LOOP = 0

		while running:
			if sensor1[0].overlap(sensor2[0], [sensor2[1][0] - (sensor1[1][0]+LOOP), sensor2[1][1] - (sensor1[1][1])]):
				LOOP += 1
			else: running = False
			if LOOP >= LOOPMAX:running = False
		return -LOOP


	def collide_outside_x_minus(sensor1, sensor2):
		running = True
		LOOP = 0

		while running:
			if not sensor1[0].overlap(sensor2[0], [sensor2[1][0] - (sensor1[1][0]- LOOP), sensor2[1][1] - (sensor1[1][1])]):
				LOOP += 1
			else:running = False
			if LOOP >= LOOPMAX: running = False
		return -LOOP
