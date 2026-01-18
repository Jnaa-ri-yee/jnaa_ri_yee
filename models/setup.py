from setuptools import setup, find_packages

setup(
    name="sign-language-training-system",
    version="1.0.0",
    description="Sistema autónomo de entrenamiento para interpretación de señas",
    author="Axel Eduardo Urbina Secundino",
    author_email="jnaariyee@gmail.com",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.8",
    install_requires=[
        "torch>=2.0.0",
        "torchvision>=0.15.0",
        "opencv-python>=4.8.0",
        "mediapipe>=0.10.0",
        "Pillow>=10.0.0",
        "scikit-learn>=1.3.0",
        "matplotlib>=3.7.0",
        "seaborn>=0.12.0",
        "numpy>=1.24.0",
        "pandas>=2.0.0",
        "pyyaml>=6.0",
        "tqdm>=4.65.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
        ],
        "viz": [
            "tensorboard>=2.13.0",
        ],
        "auto": [
            "optuna>=3.3.0",
        ]
    },
    entry_points={
        "console_scripts": [
            "train-sign-model=main:main",
        ],
    },
)