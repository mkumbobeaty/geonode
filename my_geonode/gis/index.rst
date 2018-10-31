Pertanto rispetto a Profile di GeoNode, abbiamo in piu:

HQ/RB
GIS Level
Location (geodjango)

Per quanto riguarda la location, si potrebbe pensare di creare un modello Office apposito ed associarlo ad ogni profile.

Ad es:
Model Office
type (HQ/RB/Country Office)
name
location (geodjango)

Il nostro Profile sarà' così:
GeoNode Profile (FK 1-1)
Office (FK n-1)
GIS Level
