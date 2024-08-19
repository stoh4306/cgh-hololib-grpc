import grpc
import hololib_pb2, hololib_pb2_grpc

def run():
    channel = grpc.insecure_channel("192.168.0.20:50051")
    stub = hololib_pb2_grpc.GreeterStub(channel)
    response = stub.SayHello(hololib_pb2.HelloRequest(name="you"))
    print("Greeter client received: " + response.message)

if __name__ == "__main__":
    run()