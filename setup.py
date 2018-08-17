from setuptools import setup, find_packages


requires = [
    'flask',
    'flask-sqlalchemy',
    'flask-jwt',
    'flask-bcrypt',
]

tests_require = [

]

dev_requires = [
    'ipython',
]

setup(
    name='flask_todo',
    version='0.0',
    description='A To-Do List built with Flask',
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Flask',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
    ],
    author='Bahram AGhaei',
    author_email='aghaee.bahram@gmail.com',
    url='',
    keywords='web flask',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    extras_require={
        'testing': tests_require,
        'dev': dev_requires
    },
    install_requires=requires
)
