from copy import deepcopy
from typing import Optional
import pandas as pd


tournament_data = pd.read_excel("C:\\Users\\user\\Desktop\\afdssfd 2024-02-19.xlsx", sheet_name="Основная таблица")
print(tournament_data[tournament_data.columns[1]].tolist())
