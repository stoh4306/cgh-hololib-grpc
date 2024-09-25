import sys

import grpc
import hololib_pb2, hololib_pb2_grpc

from PySide6.QtCore import Qt

from PySide6.QtWidgets import (
    QApplication, 
    QMainWindow, 
    QWidget, QPushButton, 
    QHBoxLayout, QVBoxLayout, QGridLayout,
    QFileDialog,
    QLabel, QComboBox
)

from PySide6.QtGui import (
    QPalette, 
    QColor,
    QPixmap,
    QImage
)

class UnaryClient(object):
    def __init__(self):
        self.host = '192.168.0.20'
        self.server_port = 50051

        # instantiate a channel
        self.channel = grpc.insecure_channel(
            '{}:{}'.format(self.host, self.server_port),
            options=[('grpc.max_send_message_length', 100*1024*1024),
                     ('grpc.max_receive_message_length', 100*1024*1024)])

        # bind the client and the server
        self.stub = hololib_pb2_grpc.GreeterStub(self.channel)

        self.sayHello()

    def sayHello(self):
        response = self.stub.SayHello(hololib_pb2.HelloRequest(name="PythonGUI"))
        print("response=", response.message)

    def computeHologram(self, 
                        meshData, texData, texOption, 
                        wavelength, pixelSize, numPixels, initPhaseOption):
        print("mesh data size : ", len(meshData))
        print("texture data size : ", len(texData))
        print("texture option : ", texOption)
        print("wavelength : ", wavelength)
        print("pixel size : ", pixelSize)
        print("num. pixels : ", numPixels)
        print("init. phase : ", initPhaseOption)
        
        reply = self.stub.ComputeHologram(hololib_pb2.HologramRequest(
                                            meshDataSize=len(meshData), 
                                            meshData=meshData,
                                            textureDataSize=len(texData),
                                            textureData=texData,
                                            textureOption=texOption,
                                            wavelengthOption=wavelength,
                                            pixelSizeOption=pixelSize,
                                            numOfPixelsOption=numPixels,
                                            initialPhaseOption=initPhaseOption))
 
        return reply.hologramData, reply.ReconstData


def readFileToByteData(filepath):
        with open(filepath, 'rb') as f:
            strData = f.read()
            print("data size=", len(strData))
            return strData

class MainWindow(QMainWindow):

    def input_mesh_button_clicked(self):
        print("\"Mesh\" button clicked!")
        self.inputMeshPath = QFileDialog.getOpenFileName(self, "Open file", ".\\data")
        self.inputMeshData = readFileToByteData(self.inputMeshPath[0])
        print(self.inputMeshPath[0])

        self.meshPathLable.setText(self.inputMeshPath[0])

    def input_texture_button_clicked(self):
        print("\"Texture\" button clicked!")
        self.inputTexturePath = QFileDialog.getOpenFileName(self, "Open file", ".\\data")
        self.inputTextureData = readFileToByteData(self.inputTexturePath[0])
        print(self.inputTexturePath[0])

        self.texturePathLable.setText(self.inputTexturePath[0])

    def compute_hologram_button_clicked(self):
        print("\"ComputeHologram\" button clicked")
        cghData, reconstData = self.client.computeHologram(
                                    self.inputMeshData, 
                                    self.inputTextureData, 
                                    self.textureOptionCombo.currentText(),
                                    self.waveLengthCombo.currentText(),
                                    self.pixelSizeCombo.currentText(), 
                                    self.numPixelsCombo.currentText(),
                                    self.initialPhaseCombo.currentText())
        
        pix1 = QPixmap()
        pix1.loadFromData(cghData)
        pix2 = QPixmap()
        pix2.loadFromData(reconstData)

        self.cghImageLabel.setPixmap(pix1.scaledToWidth(320))
        self.reconstImageLabel.setPixmap(pix2.scaledToWidth(320))

    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("Hologram Generation using Remote Server")
        pageLayout = QVBoxLayout()
        
        # Top layout for loading mesh object and texture image
        meshLayout = QHBoxLayout()
        
        self.inputMeshButton = QPushButton("Mesh")
        self.inputMeshButton.clicked.connect(self.input_mesh_button_clicked)
        self.inputMeshButton.setEnabled(False)
        meshLayout.addWidget(self.inputMeshButton)

        self.meshPathLable = QLabel("Mesh File Path")
        meshLayout.addWidget(self.meshPathLable)

        texLayout = QHBoxLayout()
        self.inputTextureButton = QPushButton("Texture")
        self.inputTextureButton.clicked.connect(self.input_texture_button_clicked)
        self.inputTextureButton.setEnabled(False)
        texLayout.addWidget(self.inputTextureButton)

        self.texturePathLable = QLabel("Texture File Path")
        texLayout.addWidget(self.texturePathLable)

        
        # Bottom layout for hologram generation settings
        optionsLayout = QHBoxLayout()
        
        optionLeftLayout = QVBoxLayout()

        # Shading
        shadingOptionLayout = QHBoxLayout()
        self.shadingOptionLabel = QLabel("Shading")
        self.shadingOptionCombo = QComboBox(self)
        self.shadingOptionCombo.addItem("Flat")
        self.shadingOptionCombo.addItem("Constant")
        self.shadingOptionCombo.addItem("Smooth")
        shadingOptionLayout.addWidget(self.shadingOptionLabel)
        shadingOptionLayout.addWidget(self.shadingOptionCombo)
        optionLeftLayout.addLayout(shadingOptionLayout)

        #Texture
        textureOptionLayout = QHBoxLayout()
        self.textureOptionLabel = QLabel("Texture")
        self.textureOptionCombo = QComboBox(self)
        self.textureOptionCombo.addItem("On")
        self.textureOptionCombo.addItem("Off")
        textureOptionLayout.addWidget(self.textureOptionLabel)
        textureOptionLayout.addWidget(self.textureOptionCombo)
        optionLeftLayout.addLayout(textureOptionLayout)

        #WaveLength
        wavelengthOptionLayout = QHBoxLayout()
        self.waveLengthLabel = QLabel("Wavelength")
        self.waveLengthCombo = QComboBox(self)
        self.waveLengthCombo.addItems(["Red", "Blue", "Green"])
        wavelengthOptionLayout.addWidget(self.waveLengthLabel)
        wavelengthOptionLayout.addWidget(self.waveLengthCombo)
        optionLeftLayout.addLayout(wavelengthOptionLayout)
        
        
        optionRightLayout = QVBoxLayout()
        # pixelSizeOption
        pixelSizeLayout = QHBoxLayout()
        self.pixelSizeLabel = QLabel("Pixel Size")
        self.pixelSizeCombo = QComboBox(self)
        self.pixelSizeCombo.addItem("3.5")
        pixelSizeLayout.addWidget(self.pixelSizeLabel)
        pixelSizeLayout.addWidget(self.pixelSizeCombo)
        optionRightLayout.addLayout(pixelSizeLayout)

        # number of pixels option
        numPixelsLayout = QHBoxLayout()
        self.numPixelsLabel = QLabel("Num. Pixels")
        self.numPixelsCombo = QComboBox(self)
        self.numPixelsCombo.addItems(["1K", "2K", "4K"])
        numPixelsLayout.addWidget(self.numPixelsLabel)
        numPixelsLayout.addWidget(self.numPixelsCombo)
        optionRightLayout.addLayout(numPixelsLayout)

        # initial phase option
        initialPhaseLayout = QHBoxLayout()
        self.initialPhaseLabel = QLabel("Init. Phase")
        self.initialPhaseCombo = QComboBox(self)
        self.initialPhaseCombo.addItems(["Contant", "Random"])
        initialPhaseLayout.addWidget(self.initialPhaseLabel)
        initialPhaseLayout.addWidget(self.initialPhaseCombo)
        optionRightLayout.addLayout(initialPhaseLayout)

        optionsLayout.addLayout(optionLeftLayout)
        optionsLayout.addLayout(optionRightLayout)

        pageLayout.addLayout(meshLayout)
        pageLayout.addLayout(texLayout)
        pageLayout.addLayout(optionsLayout)
        
        # Compute hologram button
        self.computeHologramButton = QPushButton("Compute Hologram!")
        self.computeHologramButton.clicked.connect(self.compute_hologram_button_clicked)
        self.computeHologramButton.setEnabled(False)
        pageLayout.addWidget(self.computeHologramButton)

        gridLayout = QGridLayout()
        self.cghImageLabel = QLabel()
        self.reconstImageLabel = QLabel()
        gridLayout.addWidget(self.cghImageLabel, 0, 0)
        gridLayout.addWidget(self.reconstImageLabel, 0, 1)
        pageLayout.addLayout(gridLayout)

        widget = QWidget()
        widget.setLayout(pageLayout)
        self.setCentralWidget(widget)

        self.client = UnaryClient()
        self.inputMeshButton.setEnabled(True)
        self.inputTextureButton.setEnabled(True)
        self.computeHologramButton.setEnabled(True)

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()
