cmake_minimum_required(VERSION 3.8)

project(grpc-hololib)

find_package(Threads REQUIRED)

find_package(Protobuf CONFIG REQUIRED)
message(STATUS "Using protobuf ${Protobuf_VERSION}")
set(_PROTOBUF_LIBPROTOBUF protobuf::libprotobuf)
set(_REFLECTION gRPC::grpc++_reflection)
set(_PROTOBUF_PROTOC $<TARGET_FILE:protobuf::protoc>)

find_package(gRPC CONFIG REQUIRED)
message(STATUS "Using gRPC ${gRPC_VERSION}")
set(_GRPC_GRPCPP gRPC::grpc++)
set(_GRPC_CPP_PLUGIN_EXECUTABLE $<TARGET_FILE:gRPC::grpc_cpp_plugin>)

find_package(OpenMP REQUIRED)
find_package(CUDAToolkit REQUIRED)
message(STATUS "CUDA Libs dir : ${CUDA_TOOLKIT_ROOT_DIR}")
find_package(OpenCV REQUIRED)
message(STATUS "OpenCV include dir : ${OpenCV_INCLUDE_DIRS}")
#find_package(faiss REQUIRED)
#find_package(SQLite3 REQUIRED)
#find_package(MKL REQUIRED)

message("- CMAKE_CURRENT_BINARY_DIR = " ${CMAKE_CURRENT_BINARY_DIR})
message("- _PROTOBUF_PROTOC = " ${_PROTOBUF_PROTOC})
message("- _GRPC_CPP_PLUGIN_EXECUTABLE = " ${_GRPC_CPP_PLUGIN_EXECUTABLE})
message("- GRPC_LIBRARIES = " ${GRPC_LIBS})

#Proto file
get_filename_component(hololib_proto "${CMAKE_CURRENT_BINARY_DIR}/../protos/hololib.proto" ABSOLUTE)
get_filename_component(hololib_proto_path "${hololib_proto}" PATH)
message("- proto-file = " ${hololib_proto})
message("- proto-path = " ${hololib_proto_path})

# Generated sources
set(hololib_proto_srcs "${CMAKE_CURRENT_BINARY_DIR}/../protos/hololib.pb.cc")
set(hololib_proto_hdrs "${CMAKE_CURRENT_BINARY_DIR}/../protos/hololib.pb.h")
set(hololib_grpc_srcs  "${CMAKE_CURRENT_BINARY_DIR}/../protos/hololib.grpc.pb.cc")
set(hololib_grpc_hdrs  "${CMAKE_CURRENT_BINARY_DIR}/../protos/hololib.grpc.pb.h")

add_custom_command(
      OUTPUT "${hololib_proto_srcs}" "${hololib_proto_hdrs}" "${hololib_grpc_srcs}" "${hololib_grpc_hdrs}"
      COMMAND ${_PROTOBUF_PROTOC} #/usr/local/bin/protoc
      ARGS --grpc_out "${hololib_proto_path}"
        --cpp_out "${hololib_proto_path}"
        -I "${hololib_proto_path}"
        --plugin=protoc-gen-grpc=${_GRPC_CPP_PLUGIN_EXECUTABLE}#"/usr/local/bin/grpc_cpp_plugin"
        "${hololib_proto}"
      DEPENDS "${hololib_proto}")

# Include generated *.pb.h files
include_directories(#"${hololib_proto_path}" 
    #/usr/local/include
    "${CMAKE_CURRENT_BINARY_DIR}/../proto"
    "${CMAKE_CURRENT_BINARY_DIR}/../../hololib/include"
    ${OpenCV_INCLUDE_DIRS}
    )

link_directories(
    /usr/local/cuda/lib64
    "${CMAKE_CURRENT_BINARY_DIR}/../../hololib/build"
    )

# hw_grpc_proto
add_library(hololib_grpc_proto
  ${hololib_grpc_srcs}
  ${hololib_grpc_hdrs}
  ${hololib_proto_srcs}
  ${hololib_proto_hdrs})
target_link_libraries(hololib_grpc_proto #gRPC::grpc++)
  ${_REFLECTION}
  ${_GRPC_GRPCPP}
  ${_PROTOBUF_LIBPROTOBUF} )

# Project target
add_executable(server server.cpp)
target_link_libraries(server
    hololib_grpc_proto
    #gRPC::grpc++ gRPC::grpc++_reflection gRPC::grpc++_alts
    absl::flags absl::flags_parse 
    #absl_log_internal_check_op absl_log_internal_conditions absl_log_internal_format absl_log_internal_globals absl_log_internal_log_sink_set 
    #absl_log_internal_message absl_log_internal_nullguard absl_log_internal_proto absl_log_severity absl_log_sink #grpc++_reflection grpc++ grpc #grpc++_reflection 
    ${_REFLECTION}
    ${_GRPC_GRPCPP}
    ${_PROTOBUF_LIBPROTOBUF}
    ${OpenCV_LIBS}
    OpenMP::OpenMP_CXX
    hololib
    cudart
    cufft
    fftw3
    #faiss sqlite3
    #mkl_intel_lp64 mkl_intel_thread mkl_core iomp5
)

#add_executable(client client.cpp)
#target_link_libraries(client 
#    vecsearch_grpc_proto
#    ${GRPC_LIB_FILES})
