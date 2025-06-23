from setuptools import setup, find_packages

setup(
    name='transparency_service',
    version='0.2',
    packages=find_packages(),  # Automatically find sub-packages
    install_requires=[  # Specify dependencies
        # 'scikit-learn',
        'PyGithub',
        'openai',
        'PyPDF2',
        'pandas',
        'matplotlib',
        'markdown',
        'shap',
        # 'opencv-python',
        'ipython',
        'gdown',
        # 'kagglehub',
        'plotly',
        # 'lxml',
        'transformers',
        'accelerate>=0.26.0',
        'validators',
        'datasets',
        'torch',
        'torchmetrics',
        'eco2ai',
        'ydata-profiling',

    ],
    description='The description.',  # Short description
    author='CERTH',  # Replace with your name
    author_email='gnikoul@gmail.com',  # Replace with your email
    url='https://github.com/gnikoul/Model-Card',  # Add your project's URL
    classifiers=[  # Classifiers to give users more information
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Development Status :: 3 - Alpha',
    ],
    python_requires='>=3.6',  # Minimum Python version
)
