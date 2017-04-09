import os
import sys

from conans import ConanFile, CMake, tools


class PyBind11Conan(ConanFile):

    name = 'pybind11'
    version = '0.1.0'
    url = 'https://github.com/jason2506/conan-pybind11'
    license = 'BSD-3-Clause'

    settings = ('os', 'compiler', 'build_type', 'arch')
    generators = ('cmake', 'txt', 'env')
    build_policy = 'always'
    options = {
        'version': (
            '2.1.1', '2.1.0',
            '2.0.1', '2.0.0',
        ),
    }
    default_options = (
        'version={last_version}'.format(last_version=options['version'][0]),
    )

    exports = (
        'CMakeLists.txt',
    )

    def source(self):
        ext = 'zip' if sys.platform == 'win32' else 'tar.gz'
        filename = 'v{ver}.{ext}'.format(ver=self.options.version, ext=ext)
        url = 'https://github.com/pybind/pybind11/archive/{}'.format(filename)

        self.output.info('Downloading {}...'.format(url))
        tools.download(url, filename)
        tools.unzip(filename, '.')
        os.unlink(filename)

    def build(self):
        extra_opts = []
        extra_opts.append('-DCMAKE_INSTALL_PREFIX="{}"'.format(
            self.package_folder,
        ))

        extra_opts.append('-DPYBIND11_INSTALL=ON')
        extra_opts.append('-DPYBIND11_TEST=OFF')

        folder = 'pybind11-{}'.format(self.options.version)
        src_dir = os.path.join(self.conanfile_directory, folder)

        cmake = CMake(self.settings)
        self.run('cmake "{src_dir}" {opts} {extra_opts}'.format(
            src_dir=src_dir,
            opts=cmake.command_line,
            extra_opts=' '.join(extra_opts),
        ))
        self.run('cmake --build . {}'.format(cmake.build_config))

    def package(self):
        self.run('cmake --build . --target install')
