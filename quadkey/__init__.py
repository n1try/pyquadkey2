from util import precondition
from tile_system import TileSystem, valid_key

class QuadKey:

	@precondition(lambda c, key: valid_key(key))
	def __init__(self, key):
		"""
		A quadkey must be between 1 and 23 digits and can only contain digit[0-3]
		"""
		self.key = key 
		self.level = len(key)
		
	def children(self):
		if self.level >= 23:
			return []
		return [QuadKey(self.key + str(k)) for k in [0, 1, 2, 3]]

	def parent(self):
		return QuadKey(self.key[:-1])

	def nearby(self):
		tile, level = TileSystem.quadkey_to_tile(self.key)
		perms = [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]
		tiles = set(map(lambda perm: (abs(tile[0]+perm[0]), abs(tile[1]+perm[1])), perms))
		return [TileSystem.tile_to_quadkey(tile, level) for tile in tiles]

	def is_ancestor(self, node):
		"""
			If node is ancestor of self
			Get the difference in level
			If not, None
		"""
		if self.level <= node.level or self.key[:len(node.key)] != node.key: 
			return None
		return self.level - node.level

	def is_descendent(self, node):
		"""
			If node is descendent of self
			Get the difference in level
			If not, None
		"""
		return node.is_ancestor(self)

	def area(self):
		size = TileSystem.map_size(self.level)
		LAT = 0
		res = TileSystem.ground_resolution(LAT, self.level)
		side = (size / 2) * res
		return side*side

	def __eq__(self, other):
		return self.key == other.key

	def __ne__(self, other):
		return not self.__eq__(other)

	def __str__(self):
		return self.key

	def __repr__(self):
		return self.key

	@staticmethod
	def from_geo(geo, level):	
		"""
		Constucts a quadkey representation from geo and level
		geo => (lat, lon)
		If lat or lon are outside of bounds, they will be clipped
		If level is outside of bounds, an AssertionError is raised
		
		"""
		pixel = TileSystem.geo_to_pixel(geo, level)
		tile = TileSystem.pixel_to_tile(pixel)
		key = TileSystem.tile_to_quadkey(tile, level)
		return QuadKey(key) 
