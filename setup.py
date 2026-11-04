from glob import glob

from setuptools import setup

package_name = 'breadcrumb'

setup(
    name=package_name,
    version='0.3.1',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', glob('launch/*.py')),
        ('share/' + package_name + '/config', glob('config/*.yaml')),
        ('share/' + package_name + '/urdf', glob('urdf/*.urdf')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    description='Drop-and-follow waypoint trails for ROS 2 mobile robots',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'breadcrumb_node = breadcrumb.trail_node:main',
        ],
    },
)
