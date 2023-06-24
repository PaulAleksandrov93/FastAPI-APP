# import datetime
# import pydantic_models
# import models
import bit

wallet = bit.Key()  # наш кошелек готов и содержится в переменной wallet 
print(wallet.get_balance())