import os

from conans import ConanFile, CMake

username = os.getenv('CONAN_USERNAME', 'jason2506')
channel = os.getenv('CONAN_CHANNEL', 'testing')


class PyBind11TestConan(ConanFile):

    name = 'pybind11-test'
    requires = (
        'pybind11/0.1.0@{username}/{channel}'.format(
            username=username,
            channel=channel,
        ),
    )

    settings = ('os', 'compiler', 'build_type', 'arch')
    generators = ('cmake', 'txt', 'env')

    options = {
        'python_exec_path': 'ANY',
    }
    default_options = (
        'python_exec_path=None',
    )

    def build(self):
        extra_opts = []
        if self.options.python_exec_path:
            extra_opts.append('-DPYTHON_EXECUTABLE:FILEPATH="{}"'.format(
                self.options.python_exec_path,
            ))

        cmake = CMake(self.settings)
        self.run('cmake "{src_dir}" {opts} {extra_opts}'.format(
            src_dir=self.conanfile_directory,
            opts=cmake.command_line,
            extra_opts=' '.join(extra_opts),
        ))
        self.run('cmake --build . {}'.format(cmake.build_config))

    def test(self):
        self.run('python -c "import example; print(example.add(1, 2))"')
