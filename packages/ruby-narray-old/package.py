# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RubyNarrayOld(RubyPackage):
    """Numerical N-dimensional Array class"""

    homepage = "http://masa16.github.io/narray/"
    url = "https://rubygems.org/downloads/narray-0.6.1.2.gem"

    version("0.6.1.2", sha256="73bf101929a1570e8034058e1296fec58d6c3386c26bf26810d33f70dd4236b7", expand=False)

    depends_on("ruby", type=("build", "run"))

    def setup_build_environment(self, env):
        # RubyGems builds native C extensions by invoking `make`. Spack exports a
        # GNU Make 4.4 jobserver via MAKEFLAGS (`--jobserver-auth=fifo:...`) that
        # the make used by RubyGems can reject with:
        #   make: *** internal error: invalid --jobserver-auth string 'fifo:...'
        # Drop MAKEFLAGS so the extension build runs without the jobserver.
        env.unset("MAKEFLAGS")
