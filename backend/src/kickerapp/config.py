# Mu = starting mean rating
# Default: 1000
MU = 1000

# Sigma = starting standard deviation
# Default: MU / 3
SIGMA = MU / 3

# Beta = score difference which indicates a 80% win chance between two players
# Default: SIGMA / 2
BETA = SIGMA / 2

# Tau = volatility of mu (higher = more volatility)
# Default: SIGMA / 100
TAU = SIGMA / 50

# Draw_prob = probability of a draw in a match
# Default: 0.01
DRAW_PROB = 0.01

# Exploitation Factor: The lower this value, the more random the matches are balanced
# Higher values give more weight to the calculated match balances
# Default: 100
EXPLOITATION_FACTOR = 100
