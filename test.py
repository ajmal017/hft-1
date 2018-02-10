import pandas as pd
import numpy as np

df = pd.read_csv('prices.csv', names=['id', '_ts', 'price', 'pair', 'exchange', 'previous_price'])
df