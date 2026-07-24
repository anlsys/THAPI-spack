# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class RubyFfi(RubyPackage):
    """Ruby-FFI is a gem for programmatically loading dynamically-linked native
    libraries, binding functions within them, and calling those functions
    from Ruby code."""

    homepage = "https://github.com/ffi/ffi/wiki"
    url = "https://rubygems.org/downloads/ffi-1.15.4.gem"

    version("1.17.2", sha256="297235842e5947cc3036ebe64077584bff583cd7a4e94e9a02fdec399ef46da6", expand=False)
    version("1.16.3", sha256="6d3242ff10c87271b0675c58d68d3f10148fabc2ad6da52a18123f06078871fb", expand=False)
    version("1.15.4", sha256="56cfca5261ead48688241236adfefb07a000a6d17184d7a4eed48d55b9675d6b", expand=False)

    depends_on("ruby@2.3.0:", type=("build", "run"))

    def setup_build_environment(self, env):
        # RubyGems builds native C extensions by invoking `make`. Spack exports a
        # GNU Make 4.4 jobserver via MAKEFLAGS (`--jobserver-auth=fifo:...`) that
        # the make used by RubyGems can reject with:
        #   make: *** internal error: invalid --jobserver-auth string 'fifo:...'
        # Drop MAKEFLAGS so the extension build runs without the jobserver.
        env.unset("MAKEFLAGS")
