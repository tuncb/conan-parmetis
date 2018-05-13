from conans import ConanFile, CMake, tools
import os

class MetisConan(ConanFile):
    name = "parmetis"
    version = "4.0.3"
    settings = "os", "compiler", "build_type", "arch"
    build_policy = "always"
    options = {
        "remove_rint_fix": [True, False],
        "remove_infinity_fix": [True, False],        
		"REALTYPEWIDTH": ["32", "64"],
		"IDXTYPEWIDTH": ["32", "64"],
    }
    default_options = "remove_rint_fix=True", "remove_infinity_fix=True", "REALTYPEWIDTH=64", "IDXTYPEWIDTH=32"

    def update_cmake_for_mpi(self):
        filename = ".\\parmetis-4.0.3\\CMakeLists.txt"
        lines = []
        with open(filename) as f:
            lines = f.readlines()
        for i in range(12, 17):
            lines[i] = lines[i][1:] 
        with open(filename, 'w') as f:
            f.writelines(lines)

    def source(self):
        archive_filename = "parmetis-4.0.3.tar.gz"
        tools.download("http://glaros.dtc.umn.edu/gkhome/fetch/sw/parmetis/parmetis-4.0.3.tar.gz", archive_filename)
        tools.untargz(archive_filename)

        self.update_cmake_for_mpi()

        if self.options.remove_rint_fix == True:
            tools.replace_in_file(".\\parmetis-4.0.3\\metis\\GKlib\\gk_arch.h", "#define rint(x) ((int)((x)+0.5))", "//#define rint(x) ((int)((x)+0.5))")
        if self.options.remove_infinity_fix == True:
            tools.replace_in_file(".\\parmetis-4.0.3\\metis\\GKlib\\gk_arch.h", "#define INFINITY FLT_MAX", "//#define INFINITY FLT_MAX")        

        tools.replace_in_file(".\\parmetis-4.0.3\\metis\\include\\metis.h", "#define IDXTYPEWIDTH 32", "#define IDXTYPEWIDTH {}".format(self.options.IDXTYPEWIDTH))
        tools.replace_in_file(".\\parmetis-4.0.3\\metis\\include\\metis.h", "#define REALTYPEWIDTH 32", "#define REALTYPEWIDTH {}".format(self.options.REALTYPEWIDTH))        
                    
    def build(self):
        cmake = CMake(self)
        cmake.configure(source_folder="./parmetis-4.0.3")
        cmake.build()    

    def package(self):
        self.copy("*parmetis.h", dst="include", keep_path=False)
        self.copy("*parmetis.lib", dst="lib", keep_path=False)
        self.copy("*metis.h", dst="include", keep_path=False)
        self.copy("*metis.lib", dst="lib", keep_path=False)        
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.dylib", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.includedirs = ['./include']
        self.cpp_info.libs = ["metis", "parmetis"]
