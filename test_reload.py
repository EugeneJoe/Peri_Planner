#!/usr/bin/python3
import models
from models.user import User


objs = models.storage.all()
for obj_id in objs.keys():
    print(objs[obj_id])
    print("\n----------------------\n")
