# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class RubyNarrayFfi(RubyPackage):
    """Ruby narray ffi interface"""

    homepage = "https://github.com/Nanosim-LIG/narray-ffi"
    url = "https://rubygems.org/downloads/narray_ffi-1.4.4.gem"

    version("1.4.4", sha256="26621b4cea463635867aa8305ad863e67c5bb8321df74e5d3fc95c6425b6197b", expand=False)

    depends_on("ruby", type=("build", "run"))
    depends_on("ruby-narray-old", type=("build", "run"))
    depends_on("ruby-ffi", type=("build", "run"))

    def setup_build_environment(self, env):
        # RubyGems builds native C extensions by invoking `make`. Spack exports a
        # GNU Make 4.4 jobserver via MAKEFLAGS (`--jobserver-auth=fifo:...`) that
        # the make used by RubyGems can reject with:
        #   make: *** internal error: invalid --jobserver-auth string 'fifo:...'
        # Drop MAKEFLAGS so the extension build runs without the jobserver.
        env.unset("MAKEFLAGS")
