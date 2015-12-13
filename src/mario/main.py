from FGAme import conf
conf.set_backend('pygame')
from mario.levels import Level1


def main():
    world = Level1()
    world.run()

if __name__ == "__main__":
    main()
