package main

import (
	"bytes"
	"context"
	"fmt"
	"image/png"
	"log"
	"os"
	"time"

	pb "grpc-cmd-client/protos"

	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials/insecure"
)

func main() {
	// Set up a connection to the server.
	conn, err := grpc.NewClient("192.168.0.20:50051", grpc.WithTransportCredentials(insecure.NewCredentials()))
	if err != nil {
		log.Fatalf("did not connect: %v", err)
	}
	defer conn.Close()

	// Create a client stub
	client := pb.NewGreeterClient(conn)

	// Contact the server and print out its response.
	name := "Seungtaik"
	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Minute)
	defer cancel()

	r, err := client.SayHello(ctx, &pb.HelloRequest{Name: name})
	if err != nil {
		log.Fatalf("could not greet: %v", err)
	}
	log.Printf("Greeting from server: %s", r.GetMessage())

	meshFile := os.Args[1]
	textureFile := os.Args[2]

	meshData, err := readFileToBytes(meshFile)
	if err != nil {
		log.Fatalf("Failed to read mesh file : %v", err)
	}
	//fmt.Println(string(meshData))

	textureData, err := readFileToBytes(textureFile)
	if err != nil {
		log.Fatalf("Failed to read texture file : %v", err)
	}

	var hologramRequest pb.HologramRequest
	hologramRequest.MeshDataSize = uint32(len(meshData))
	hologramRequest.MeshData = meshData
	hologramRequest.TextureDataSize = uint32(len(textureData))
	hologramRequest.TextureData = textureData
	hologramRequest.ShadingOption = "Flat"
	hologramRequest.TextureOption = "Off"
	hologramRequest.WavelengthOption = "Red"
	hologramRequest.PixelSizeOption = "3.5"
	hologramRequest.NumOfPixelsOption = "2K"
	hologramRequest.InitialPhaseOption = "Constant"

	fmt.Println(len(hologramRequest.MeshData), len(hologramRequest.TextureData))

	reply, err := client.ComputeHologram(ctx, &hologramRequest)
	if err != nil {
		log.Fatalf("%v", err)
	}

	if reply == nil {
		log.Fatalf("null reply!")
	}

	fmt.Printf("size=%d\n", reply.ReconstDataSize)

	exportDataToImage(reply.HologramData, "cgh.png")
	exportDataToImage(reply.ReconstData, "reconst.png")
}

func exportDataToImage(data []byte, filepath string) error {
	file, err := os.Create(filepath)
	if err != nil {
		log.Fatalf("Failed to open %v", err)
	}
	defer file.Close()

	imgReader := bytes.NewReader(data)
	img, err := png.Decode(imgReader)
	if err != nil {
		log.Fatalf("Failed to deconde image data")
	}

	err = png.Encode(file, img)
	if err != nil {
		log.Fatalf("Failed to encode image data to export")
	}

	return nil
}

func readFileToBytes(filepath string) ([]byte, error) {
	byteData, err := os.ReadFile(filepath)
	if err != nil {
		return byteData, err
	}
	return byteData, nil
}
