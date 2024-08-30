from setuptools import setup, find_packages

setup(
    name='LLMChatLinker',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'sqlalchemy',
        'psycopg2-binary',
        'pika',
    ],
    entry_points={
        'console_scripts': [
            'llmchatlinker = llmchatlinker.main:main',
        ],
    },
)