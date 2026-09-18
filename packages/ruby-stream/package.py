# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class RubyStream(RubyPackage):
    """Stream - Extended External Iterators. Runtime dependency of ruby-rgl."""

    homepage = "https://github.com/monora/stream"
    url = "https://rubygems.org/downloads/stream-0.5.6.gem"

    version("0.5.6", sha256="2733607ce840d60c72eb181714d45f0a7b077ee62fec0a94510a29c39175610f", expand=False)

    # Pure Ruby: the gemspec declares `extensions: []`, so unlike the sibling
    # ruby-* recipes here there is nothing for make to build and no gmake dep.
    depends_on("ruby", type=("build", "run"))
