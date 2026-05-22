#Create delegates to handle events pertaining to Sunny
from Event_System import GameEvent
#stat-related events
on_hpMax = GameEvent()
on_hp_updated = GameEvent()
on_hpMin = GameEvent()

on_energyMin = GameEvent()
on_energyUpdated = GameEvent()
on_energyMax = GameEvent()
on_energyDebuff = GameEvent()
on_happinessMax = GameEvent()
on_happinessChanged = GameEvent()
on_happinessMin = GameEvent()

