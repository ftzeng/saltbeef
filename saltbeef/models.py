import random
import numpy as np
from hashlib import md5
from saltbeef import db, generate


def gen_id(name):
    return md5(name.encode('utf8')).hexdigest()


class Creature(db.Model):
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String)
    hp = db.Column(db.Integer)
    atk = db.Column(db.Integer)
    dfn = db.Column(db.Integer)
    current_hp = db.Column(db.Integer)
    trainer_id = db.Column(db.String, db.ForeignKey('trainer.id'))

    def __init__(self):
        self.name = generate.name()
        self.id = gen_id(self.name)
        self.hp = np.random.binomial(40, 0.4)
        self.atk = np.random.binomial(20, 0.4)
        self.dfn = np.random.binomial(10, 0.4)
        self.current_hp = self.hp

    def __repr__(self):
        return '{} ({}ATK {}DFN {}/{}HP)'.format(
            self.name,
            self.atk,
            self.dfn,
            self.current_hp,
            self.hp
        )

    def attack(self):
        name = generate.move()
        return name, np.random.binomial(self.atk, 0.8)

    def defend(self, attack):
        defense = np.random.binomial(self.dfn, 0.8)/10
        damage = int(attack * (1 - defense))
        self.current_hp -= damage
        return damage


class Item(db.Model):
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String)
    effect_type = db.Column(db.String)
    effect_str = db.Column(db.Integer)
    trainer_id = db.Column(db.String, db.ForeignKey('trainer.id'))

    def __init__(self):
        self.name = generate.item()
        self.id = gen_id(self.name)
        self.effect_type = random.choice(['hp', 'atk', 'dfn'])
        self.effect_str = np.random.binomial(30, 0.3)

    def __repr__(self):
        if self.effect_type == 'hp':
            return '{} (heals {}HP)'.format(
                self.name,
                self.effect_str
            )
        else:
            return '{} (+{} to {})'.format(self.name, self.effect_str, self.effect_type.upper())


class Trainer(db.Model):
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String)
    wins = db.Column(db.Integer)
    losses = db.Column(db.Integer)
    creatures = db.relationship(Creature, backref='trainer')
    items = db.relationship(Item, backref='trainer')

    def __init__(self, name):
        self.name = name
        self.wins = 0
        self.losses = 0
        self.id = gen_id(self.name)
        self.creatures = [Creature()]
