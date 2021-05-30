import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from classes.Maps import Map


def test_world_creation():
    print('Map 1')
    world_map = Map(100, 100, amplitudes=[3, 6, 12, 24], zoomed=True)
    world_map.export_map('./images/map-test.png')
    world_map.export_map('./images/map-test-3d.png', view3d=True)
    print('Map 2')
    world_map.transform_elevation(0.58)  # lots of mountains, not much water
    world_map.export_map('./images/map-test2.png')
    world_map.export_map('./images/map-test2-3d.png', view3d=True)
    print('Map 3')
    world_map.transform_elevation(1.21)
    world_map.export_map('./images/map-test3.png')
    world_map.export_map('./images/map-test3-3d.png', view3d=True)


def test_dungeon_creation():
    print('Dungeon 1')
    dungeon = Map(100, 100, amplitudes=[3, 6, 12, 24])  # good for dungeons (zoomed=False)
    dungeon.transform_dungeon()
    dungeon.export_map('./images/dungeon-test.png', colormap='dungeon')
    dungeon.export_map('./images/dungeon-test-3d.png', view3d=True, colormap='dungeon')


def test_all():
    # test_world_creation()
    test_dungeon_creation()


test_all()
