cmake_minimum_required(VERSION 2.6.0)

set_source_files_properties(checktype.c PROPERTIES COMPILE_FLAGS "-fPIC")

add_library(checktype STATIC checktype.c)

add_executable(millistamp millistamp.c)

target_link_libraries(millistamp checktype)

install(TARGETS millistamp RUNTIME DESTINATION bin)
