# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class RubyPairingHeap(RubyPackage):
    """Performant priority queue in pure Ruby with support for changing
    priority. Runtime dependency of ruby-rgl."""

    homepage = "https://github.com/mhib/pairing_heap"
    url = "https://rubygems.org/downloads/pairing_heap-3.1.1.gem"

    version("3.1.1", sha256="c71a74ecdf9d6accc7545b38075b2f4e8d98b550aabe0f0758a587ee12e93588", expand=False)

    # Pure Ruby: the gemspec declares `extensions: []`, so unlike the sibling
    # ruby-* recipes here there is nothing for make to build and no gmake dep.
    depends_on("ruby@2.3.0:", type=("build", "run"))
