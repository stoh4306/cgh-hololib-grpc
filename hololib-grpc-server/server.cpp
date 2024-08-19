#include <random>
#include <vector>
#include <algorithm>
#include <chrono>
#include <sstream>

#include <map>
#include <fstream>
#include <thread>

#include "absl/flags/flag.h"
#include "absl/flags/parse.h"
#include "absl/strings/str_format.h"

#include <grpcpp/ext/proto_server_reflection_plugin.h>
#include <grpcpp/grpcpp.h>
#include <grpcpp/health_check_service_interface.h>

#include "./protos/hololib.grpc.pb.h"   //".hololib.grpc.pb.h"

//#include "mesh.h"
#include "scene.h"
#include "cghgenmodule.h"

using grpc::Server;
using grpc::ServerBuilder;
using grpc::ServerContext;
using grpc::Status;
using namespace hololibgrpc;
using hololibgrpc::HelloRequest;
using hololibgrpc::HelloReply;
using hololibgrpc::HologramRequest;
using hololibgrpc::HologramReply;

ABSL_FLAG(uint16_t, port, 50051, "Server port for the service");

class HololibServiceImpl final : public Greeter::Service {
public:
    Status SayHello(ServerContext* context, const HelloRequest* request, HelloReply* reply) override {
        std::string name = request->name();
        reply->set_message("Hello, " + name);
        return Status::OK;
    }

    Status SayHelloAgain(ServerContext* context, const HelloRequest* request, HelloReply* reply) override {
        std::string name = request->name();
        reply->set_message("Hello again, " + name);
        return Status::OK;
    }
    
Status ComputeHologram(ServerContext* context, const HologramRequest* request, HologramReply* reply) override {
        uint32_t hologramDataSize = request->meshdatasize();
        uint32_t reconstDataSize = request->texturedatasize();
        reply->set_hologramdatasize(hologramDataSize);
        reply->set_reconstdatasize(reconstDataSize);

        std::cout << "-Request : \n"
            << "  .mesh : " << request->meshdatasize() << ", " << request->meshdata().substr(0, 10) << "\n"
            << "  .texture: " << request->texturedatasize() << ", " << request->texturedata().substr(0, 10) << "\n"
            << "  .shading: " << request->shadingoption() << "\n"
            << "  .texture: " << request->textureoption() << "\n"
            << "  .wavelength: " << request->wavelengthoption() << "\n"
            << "  .pixelSize: " << request->pixelsizeoption() << "\n"
            << "  .numOfPixels: " << request->numofpixelsoption() << "\n"
            << "  .initPhase: " << request->initialphaseoption() 
            << std::endl;

        //Hol::TriMesh<double> mesh;
        //mesh.setMeshFromObjData(request->meshdata());
        //mesh.setTextureFromData(request->texturedata());

        Hol::GrpcHologramRequest grpcRequest;
        grpcRequest.meshDataSize = request->meshdatasize();
        grpcRequest.meshData = request->meshdata();
        grpcRequest.texDataSize = request->texturedatasize();
        grpcRequest.texData = request->texturedata();

        grpcRequest.shadingOption = request->shadingoption();
        grpcRequest.textureOption = request->textureoption();
        grpcRequest.wavelengthOption = request->wavelengthoption();
        grpcRequest.pixelSizeOption = request->pixelsizeoption();
        grpcRequest.numOfPixelsOption = request->numofpixelsoption();
        grpcRequest.initPhaseOption = request->initialphaseoption();

        Hol::ComplexArray cgh[3];
        std::vector<uchar> holoImagData, reconstImgData;
        Hol::cgh_gen_from_grpc_request_1(grpcRequest, cgh[0], cgh[1], cgh[2], holoImagData, reconstImgData);

        std::string tempHologramData(holoImagData.begin(), holoImagData.end());
        std::cout << "size=" << tempHologramData.size() << std::endl;
        std::cout << tempHologramData.substr(0,20) << std::endl;
        reply->set_hologramdata(tempHologramData);
        reply->set_hologramdatasize(holoImagData.size());
        reply->set_reconstdata(std::string(reconstImgData.begin(), reconstImgData.end()));
        reply->set_reconstdatasize(reconstImgData.size());
            
        return Status::OK;
    }

    static Status sendEmptyCgh(grpc::ServerWriter<HologramReply>* writer, unsigned char* inComputing, HologramReply* empty)
    {
        unsigned int duration = 0;
        unsigned int interval = 2;

        HologramReply emptyHologram = (HologramReply) *empty;

        while(1) {
            std::this_thread::sleep_for(std::chrono::seconds(interval));
            //std::this_thread::sleep_for(std::chrono::milliseconds(10));
            duration += interval;

            if (*inComputing != 0) 
            {
                emptyHologram.set_duration(duration);
                writer->Write(emptyHologram);
                std::cout << "emptyHologram: size=" << emptyHologram.reconstdatasize() << std::endl;
            }
            else
            {
                break;
            }
        }

        return Status::OK;
    }

    static Status computeCgh(const HologramRequest* request, grpc::ServerWriter<HologramReply>* writer, unsigned char* inComputing)
    {
        //uint32_t hologramDataSize = request->meshdatasize();
        //uint32_t reconstDataSize = request->texturedatasize();

        //reply->set_hologramdatasize(hologramDataSize);
        //reply->set_reconstdatasize(reconstDataSize);

        std::cout << "-Request : \n"
            << "  .mesh : " << request->meshdatasize() << ", " << request->meshdata().substr(0, 10) << "\n"
            << "  .texture: " << request->texturedatasize() << ", " << request->texturedata().substr(0, 10) << "\n"
            << "  .shading: " << request->shadingoption() << "\n"
            << "  .texture: " << request->textureoption() << "\n"
            << "  .wavelength: " << request->wavelengthoption() << "\n"
            << "  .pixelSize: " << request->pixelsizeoption() << "\n"
            << "  .numOfPixels: " << request->numofpixelsoption() << "\n"
            << "  .initPhase: " << request->initialphaseoption() 
            << std::endl;

        //Hol::TriMesh<double> mesh;
        //mesh.setMeshFromObjData(request->meshdata());
        //mesh.setTextureFromData(request->texturedata());

        Hol::GrpcHologramRequest grpcRequest;
        grpcRequest.meshDataSize = request->meshdatasize();
        grpcRequest.meshData = request->meshdata();
        grpcRequest.texDataSize = request->texturedatasize();
        grpcRequest.texData = request->texturedata();

        grpcRequest.shadingOption = request->shadingoption();
        grpcRequest.textureOption = request->textureoption();
        grpcRequest.wavelengthOption = request->wavelengthoption();
        grpcRequest.pixelSizeOption = request->pixelsizeoption();
        grpcRequest.numOfPixelsOption = request->numofpixelsoption();
        grpcRequest.initPhaseOption = request->initialphaseoption();

        auto startTime = std::chrono::high_resolution_clock::now();
        Hol::ComplexArray cgh[3];
        std::vector<uchar> holoImagData, reconstImgData;
        Hol::cgh_gen_from_grpc_request_1(grpcRequest, cgh[0], cgh[1], cgh[2], holoImagData, reconstImgData);

        auto finishTime = std::chrono::high_resolution_clock::now();
        std::chrono::duration<double> timeDuration = std::chrono::duration_cast<std::chrono::duration<double>>(finishTime-startTime);
        std::string tempHologramData(holoImagData.begin(), holoImagData.end());
        std::cout << "size=" << tempHologramData.size() << std::endl;
        std::cout << tempHologramData.substr(0,20) << std::endl;

        HologramReply hologram;
        hologram.set_duration(timeDuration.count());
        hologram.set_hologramdata(tempHologramData);
        hologram.set_hologramdatasize(holoImagData.size());
        hologram.set_reconstdata(std::string(reconstImgData.begin(), reconstImgData.end()));
        hologram.set_reconstdatasize(reconstImgData.size());

        writer->Write(hologram);

        *inComputing = 0;

        return Status::OK;
    }

    Status ComputeHologram_stream(ServerContext* context, const HologramRequest* request, grpc::ServerWriter<HologramReply>* writer)  override {
        inComputing_ = 1;
        std::thread t1(computeCgh, request, writer, &inComputing_);
        //std::thread t2(sendEmptyCgh, writer, &inComputing_, &empty_);

        t1.join();
        //t2.join();

        return Status::OK;
    }
    
  
    void setEmptyHologram()
    {
        cv::Mat whiteImg = cv::imread("white-256.png", -1);
        std::vector<uchar> byteData;
        cv::imencode(".png", whiteImg, byteData);

        empty_.set_duration(0);
        empty_.set_hologramdatasize(byteData.size());
        empty_.set_hologramdata(std::string(byteData.begin(), byteData.end()));
        empty_.set_reconstdatasize(byteData.size());
        empty_.set_reconstdata(std::string(byteData.begin(), byteData.end()));
    }

    HololibServiceImpl() {
        inComputing_ = 0;
        //duration_ = 0;

        setEmptyHologram();
    }

public:
    unsigned char inComputing_;
    //unsigned int duration_;

    HologramReply empty_;
};

void RunServer2(uint16_t port) {
  std::string server_address = absl::StrFormat("0.0.0.0:%d", port);
  HololibServiceImpl service;

  grpc::EnableDefaultHealthCheckService(true);
  grpc::reflection::InitProtoReflectionServerBuilderPlugin();
  ServerBuilder builder;
  // Listen on the given address without any authentication mechanism.
  builder.AddListeningPort(server_address, grpc::InsecureServerCredentials());
  // Register "service" as the instance through which we'll communicate with
  // clients. In this case it corresponds to an *synchronous* service.
  builder.RegisterService(&service);
  // Finally assemble the server.
  std::unique_ptr<Server> server(builder.BuildAndStart());
  std::cout << "Server listening on " << server_address << std::endl;

  // Wait for the server to shutdown. Note that some other thread must be
  // responsible for shutting down the server for this call to ever return.
  server->Wait();
}

int main(int argc, char** argv) {

    RunServer2(absl::GetFlag(FLAGS_port));

    return 0;
}