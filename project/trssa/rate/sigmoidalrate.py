class SigmoidalRate:
	def __init__(self, base, divisor, exponentialCoefficient):
		self.base = base
		self.divisor = divisor
		self.exponentialCoefficient = exponentialCoefficient

	def integrate(self, currentTime, delta):
		rate = self.evaluate(currentTime)
		return rate * delta

	def solve(self, currentTime, rhs):
		rate = evaluate(currentTime)
		return rhs / rate

	def evaluate(self, currentTime):
		power = (currentTime / self.divisor)**self.exponentialCoefficient
		return self.base / (1 + power)

	def getRateBound(self, currentTime, nextTime):
		return [evaluate(nextTime), evaluate(currentTime)]
