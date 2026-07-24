# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class RubyBabeltrace(RubyPackage):
    """Ruby libbabeltrace ffi bindings"""

    homepage = "https://github.com/argonne-lcf/babeltrace-ruby"
    url = "https://rubygems.org/downloads/babeltrace-0.1.3.gem"

    version("0.1.3", sha256="bce6133637c18d503efb6b88ebffcbbdef8561310366b5c5d32751f6ae4b055c", expand=False)

    depends_on("ruby@2.3.0:", type=("build", "run"))
    depends_on("ruby-walk", type=("build", "run"))
    depends_on("ruby-ffi", type=("build", "run"))
    depends_on("babeltrace@1.5.8:", type=("build", "link", "run"))

    def setup_run_environment(self, env):
        super().setup_run_environment(env)
        env.prepend_path("LD_LIBRARY_PATH", self.spec["babeltrace"].prefix.lib)

    def setup_dependent_build_environment(self, env, dependent_spec):
        super().setup_dependent_build_environment(env, dependent_spec)
        env.prepend_path("LD_LIBRARY_PATH", self.spec["babeltrace"].prefix.lib)

    def setup_build_environment(self, env):
        # RubyGems builds native C extensions by invoking `make`. Spack exports a
        # GNU Make 4.4 jobserver via MAKEFLAGS (`--jobserver-auth=fifo:...`) that
        # the make used by RubyGems can reject with:
        #   make: *** internal error: invalid --jobserver-auth string 'fifo:...'
        # Drop MAKEFLAGS so the extension build runs without the jobserver.
        env.unset("MAKEFLAGS")
