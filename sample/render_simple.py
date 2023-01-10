import mitsuba as mi

mi.set_variant('scalar_rgb')
MITSUBA_DIR = '/home/udemegane/workspace/mitsuba3'
RESOURCE_DIR = MITSUBA_DIR+'/resources/data/scenes/cbox/'

scene: mi.Scene = mi.load_file(
    RESOURCE_DIR+'cbox-rgb.xml')
params = mi.traverse(scene)
print(params)
image = mi.render(scene, spp=50)

mi.util.write_bitmap('cbox-rgb.png', image)
