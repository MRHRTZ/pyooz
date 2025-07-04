import os
from setuptools import setup, Extension
from wheel.bdist_wheel import bdist_wheel

ooz_sources = [
    os.path.join('ooz/dep/ooz/', x) for x in [
        "bitknit.cpp",
        "kraken.cpp",
        "lzna.cpp",
        "compress.cpp",
        "compr_kraken.cpp",
        "compr_leviathan.cpp",
        "compr_mermaid.cpp",
        "compr_entropy.cpp",
        "compr_match_finder.cpp",
        "compr_multiarray.cpp",
        "compr_tans.cpp",
    ]
]

extra_compile_args = ['-O2']
if os.environ.get('DEBUG') == '1':
    extra_compile_args = ['-g', '-O0']
    
ext_modules = [
    Extension(
        name='ooz',
        sources=['ooz/ooz_bindings.cpp'] + ooz_sources,
        define_macros=[
            ('OOZ_BUILD_DLL', 1),
            ('Py_LIMITED_API', 0x03080000),
        ],
        include_dirs=['ooz/dep/ooz/simde'],
        extra_compile_args=extra_compile_args,
        py_limited_api=True,
    ),
]

class bdist_wheel_abi3(bdist_wheel):
    def get_tag(self):
        python, abi, plat = super().get_tag()

        if python.startswith("cp"):
            # on CPython, our wheels are abi3 and compatible back to 3.8
            return "cp38", "abi3", plat

        return python, abi, plat

from pathlib import Path
long_description = (Path(__file__).parent / "README.md").read_text()

setup(
    name='pyooz',
    version='0.1.0',
    description="ooz decompression bindings",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Natural Language :: English',
        'Programming Language :: Python :: 3 :: Only',
    ],
    cmdclass={"bdist_wheel": bdist_wheel_abi3},
    ext_modules=ext_modules,
)
