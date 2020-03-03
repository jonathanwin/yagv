import setuptools


setuptools.setup(
    name = 'yagv',
    version = '0.4',
    description = '',
    packages = setuptools.find_packages(),
    package_dir = {"":'.'},
    data_files=[
        ("data", ("data/hana_swimsuit_fv_solid_v1.gcode",))
    ],
    classifiers = [

    ],
    #include_package_data = True,
    py_modules = ['gcodeParser'],
    scripts = ['yagv'],
    python_requies='>3.6'
)
