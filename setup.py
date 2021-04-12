import setuptools

setuptools.setup(
    name = 'yagv',
    version = '0.5.0',
    description = 'Yet another Gcode viewer (3D Printing Format)',
    packages = setuptools.find_packages(),
    package_dir = {"":'.'},
    package_data = {'': [ "data/hana_swimsuit_fv_solid_v1.gcode" ] },
    classifiers = [
      "Environment :: Console",
      "Topic :: Multimedia :: Graphics :: 3D Rendering",
      "Topic :: Multimedia :: Graphics :: Presentation",
      "Topic :: Multimedia :: Graphics :: Viewers"
    ],
    include_package_data = True,
    py_modules = ['gcodeParser'],
    scripts = ['yagv'],
    python_requires='>3.6',
    install_requires=[
        'setuptools',
        'pyglet>=1.4.10, <2'
    ]
)
