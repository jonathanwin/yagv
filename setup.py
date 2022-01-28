import setuptools

setuptools.setup(
    name = 'yagv',
    version = '0.5.8',        # -- check ./yagv & Makefile too
    description = 'Yet Another Gcode Viewer (3D Printing Format)',
    packages = setuptools.find_packages(),
    package_dir = {'':'.'},
    # package_data = {'': [ "icon.png", "data/hana_swimsuit_fv_solid_v1.gcode" ] },
    # include_package_data = True,
    classifiers = [
      "Environment :: Console",
      "Topic :: Multimedia :: Graphics :: 3D Rendering",
      "Topic :: Multimedia :: Graphics :: Presentation",
      "Topic :: Multimedia :: Graphics :: Viewers"
    ],
    data_files = [ ( 'data', ['data/hana_swimsuit_fv_solid_v1.gcode'] ), ('icons', ['icon.png']) ],
    py_modules = ['gcodeParser'],
    scripts = ['yagv'],
    python_requires='>3.6',
    install_requires=[
        'setuptools',
        'pyglet>=1.4.10, <2'
    ]
)
