from setuptools import setup, find_packages

setup(
    name='llamaindex_project',
    version='0.1.0',
    author= 'Santiago Olivar',
    author_email='contact.bubl.ai@gmail.com',
    description='',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/bubl-ai/llamaindex-project',
    license='MIT',
    classifiers=[
        'Development Status ::Planning',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Operating System :: OS Independent',
    ],
    package_dir={'': 'bubls'} # Need it this way as we are installing it in editable mode
)