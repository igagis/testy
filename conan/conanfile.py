import os
from conan import ConanFile
from conan.tools.scm import Git
from conan.tools.files import load, update_conandata, copy
from conan.tools.layout import basic_layout

class TstConan(ConanFile):
	name = "tst"
	license = "MIT"
	author = "Ivan Gagis <igagis@gmail.com>"
	url = "http://github.com/cppfw/" + name
	description = "xUnit-like testig framework for C++"
	topics = ("C++", "cross-platform")
	settings = "os", "compiler", "build_type", "arch"
	package_type = "library"
	options = {"shared": [True, False], "fPIC": [True, False]}
	default_options = {"shared": False, "fPIC": True}
	generators = "AutotoolsDeps" # this will set CXXFLAGS etc. env vars

	def requirements(self):
		self.requires("utki/[>=1.1.202]@cppfw/main", transitive_headers=True, transitive_libs=True)
		self.requires("clargs/[>=0.2.47]@cppfw/main", transitive_headers=True, transitive_libs=True)
		self.requires("nitki/[>=0.0.0]@cppfw/main", transitive_headers=True, transitive_libs=True)

	def config_options(self):
		if self.settings.os == "Windows":
			del self.options.fPIC

	# save commit and remote URL to conandata.yml for packaging
	def export(self):
		git = Git(self, self.recipe_folder)
		scm_url = git.get_remote_url()
		scm_commit = git.get_commit()
		update_conandata(self, {"sources": {"commit": scm_commit, "url": scm_url}})

	def source(self):
		git = Git(self)
		sources = self.conan_data["sources"]
		# shallow fetch commit
		git.fetch_commit(url=sources["url"], commit=sources['commit'])
		# shallow clone submodules
		git.run("submodule update --init --remote --depth 1")

	def build(self):
		self.run("make lint=off")
		self.run("make lint=off test")

	def package(self):
		src_dir = os.path.join(self.build_folder, "src")
		src_rel_dir = os.path.join(self.build_folder, "src/out/rel")
		dst_include_dir = os.path.join(self.package_folder, "include")
		dst_lib_dir = os.path.join(self.package_folder, "lib")
		dst_bin_dir = os.path.join(self.package_folder, "bin")
		
		copy(conanfile=self, pattern="*.h",                    dst=dst_include_dir, src=src_dir,     keep_path=True)
		copy(conanfile=self, pattern="*.hpp",                  dst=dst_include_dir, src=src_dir,     keep_path=True)

		if self.options.shared:
			copy(conanfile=self, pattern="*" + self.name + ".lib", dst=dst_lib_dir,     src="",          keep_path=False)
			copy(conanfile=self, pattern="*.dll",                  dst=dst_bin_dir,     src=src_rel_dir, keep_path=False)
			copy(conanfile=self, pattern="*.so",                   dst=dst_lib_dir,     src=src_rel_dir, keep_path=False)
			copy(conanfile=self, pattern="*.so.*",                 dst=dst_lib_dir,     src=src_rel_dir, keep_path=False)
			copy(conanfile=self, pattern="*.dylib",                dst=dst_lib_dir,     src=src_rel_dir, keep_path=False)
		else:
			copy(conanfile=self, pattern="*" + self.name + ".lib", dst=dst_lib_dir,     src="",          keep_path=False)
			copy(conanfile=self, pattern="*.a",                    dst=dst_lib_dir,     src=src_rel_dir, keep_path=False)

	def package_info(self):
		self.cpp_info.libs = [self.name]

	def package_id(self):

		# change package id only when minor or major version changes, i.e. when ABI breaks
		self.info.requires.minor_mode()
