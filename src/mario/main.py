from FGAme import conf
import FGAme
conf.set_backend('pygame')
print(FGAme.__version__)
print(FGAme.__file__)
from mario.levels import Level1

def main(): 
    world = Level1()
    world.run()

if __name__ == '__main__':
    main()
