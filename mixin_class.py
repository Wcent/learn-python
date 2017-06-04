#! /usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'cent'

'''
a mixin-class sample shows how to use multiple inheritance
note: super().init works only when all base classes calling super().init
'''

class Animal(object):
    def __init__(self, type='animal'):
        super(Animal, self).__init__()
        print('init in Animal...')
        self.__type = type

    @property
    def type(self):
        return self.__type

    def speak(self):
        print('yoyo, I am an %s' % self.__type)

class RunnableMixin(object):
    def __init__(self):
        super(RunnableMixin, self).__init__()
        print('init in RunnableMixin...')

    def run(self):
        print('I can run.')

class FlyableMixin(object):
    def __init__(self):
        super(FlyableMixin, self).__init__()
        print('init in FlyableMixin')

    def fly(self):
        print('I can fly.')

class Dog(Animal, RunnableMixin):
    def __init__(self):
        super(Dog, self).__init__(type='dog')
        print('init in Dog...')

    def speak(self):
        print('haha, I am a %s, speak wang wang' % self.type)

class Cat(Animal, RunnableMixin):
    def __init__(self):
        super(Cat, self).__init__(type='cat')
        print('init in Cat...')

    def speak(self):
        print('haha, I am a %s, speak miao miao' % self.type)

class Bird(Animal, RunnableMixin, FlyableMixin):
    def __init__(self):
        super(Bird, self).__init__(type='bird')
        print('init in Bird...')

    def speak(self):
        print('haha, I am a %s, sings song' % self.type)

def speak(Animal):
    Animal.speak()

# testing
if __name__ == '__main__':
    ani = Animal()
    dog = Dog()
    cat = Cat()
    bird = Bird()

    animal_list = []
    animal_list.append(ani)
    animal_list.append(dog)
    animal_list.append(cat)
    animal_list.append(bird)
    for animal in animal_list:
        speak(animal)
        if isinstance(animal, RunnableMixin):
            animal.run()
        if isinstance(animal, FlyableMixin):
            animal.fly()