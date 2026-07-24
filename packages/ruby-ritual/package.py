# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class RubyRitual(RubyPackage):
    """Adds tasks and helpers to your Rakefile to manage releases in a lightweight manner."""

    homepage = "https://github.com/oggy/ritual"
    url = "https://rubygems.org/downloads/ritual-0.5.1.gem"

    version("0.5.1", sha256="9c1a574b23a98c0139fa87d1c30ea85094e14fe194d11bfa975e58248788770b", expand=False)

    depends_on("ruby@2.3.0:", type=("build", "run"))
    depends_on("ruby-thor", type=("build", "run"))
    depends_on("ruby-rake", type=("build", "run"))

    def setup_build_environment(self, env):
        # RubyGems builds native C extensions by invoking `make`. Spack exports a
        # GNU Make 4.4 jobserver via MAKEFLAGS (`--jobserver-auth=fifo:...`) that
        # the make used by RubyGems can reject with:
        #   make: *** internal error: invalid --jobserver-auth string 'fifo:...'
        # Drop MAKEFLAGS so the extension build runs without the jobserver.
        env.unset("MAKEFLAGS")
