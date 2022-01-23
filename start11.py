import sys
from ui.mainWindow import *
from annotator import Annotator
from core import init_model
from PySide2.QtCore import QObject,Signal,Slot


class MainWindow(QMainWindow):
    _signal_saveOption = Signal()
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.mainPath="F:\Python2\卷积\dataset\Berkeley\images"
        self.img_path='test.jpg'
        self.save_path=self.mainPath
        self.if_sis=False
        self.if_cuda=not False
        self.backbone='resnet'
        self.model = init_model('fcanet', 'resnet',
                                './pretrained_model/fcanet-{}.pth'.format(
                                    'resnet'),
                                if_cuda=not False)

        self.ui.p_btm_inputImage.clicked.connect(self.__inputImage)
        self.ui.p_btm_start.clicked.connect(self.__start)
        self.ui.p_btm_ouputImage.clicked.connect(self.__save_path)

    ###槽函数


    def __save_path(self):
        self.save_path=QFileDialog.getExistingDirectory(self,"保存路径",self.mainPath)
        print(self.save_path)

    def __inputImage(self):
        self.img_path = QFileDialog.getOpenFileNames(self,"打开图像文件",self.mainPath,"图像文件(*.jpg)")[0][0]
        print(self.img_path)

    def __init_model(self):
        self.model = init_model('fcanet', 'resnet',
                                './pretrained_model/fcanet-{}.pth'.format(
                                    'resnet'),
                                if_cuda=not False)

    def __start(self):
        #如果默认网络不是resnet,重新初始化model
        if not self.backbone=='resnet':
            self.model = init_model('fcanet', self.backbone,
                                    './pretrained_model/fcanet-{}.pth'.format(
                                        'resnet'),
                                    if_cuda=not False)
        self.anno = Annotator(img_path=self.img_path,
                              model=self.model,
                              if_sis=self.if_sis,
                              if_cuda=self.if_cuda,
                              save_path=self.save_path)

        self.anno.main()
        self.graphic_scene=QGraphicsScene()
        self.graphic_scene.addWidget(self.anno)
        self.ui.graphicsView.setScene(self.graphic_scene)
        self.ui.graphicsView.show()

        self.ui.p_btm_save.clicked.connect(self.__save_with_option)
        #self.ui.pushButton.clicked.connect(self.anno.save_option())

    def __save_with_option(self):
        option = str(self.ui.comboBox_saveOption.currentText())
        self.anno.save_with_option(option)


if __name__ == "__main__":
    app = QApplication([])
    _mainWindow = MainWindow()
    _mainWindow.setWindowTitle("图像识别")
    _mainWindow.show()
    app.exec_()

    # parser = argparse.ArgumentParser(
    #     description="Annotator for FCANet")
    # parser.add_argument('--input', type=str,
    #                     default='test.jpg',
    #                     help='input image')
    # parser.add_argument('--output', type=str,
    #                     default='test_mask.png',
    #                     help='output mask')
    # parser.add_argument('--backbone', type=str,
    #                     default='resnet',
    #                     choices=['resnet', 'res2net'],
    #                     help='backbone name (default: resnet)')
    # parser.add_argument('--sis', action='store_true',
    #                     default=False, help='use sis')
    # parser.add_argument('--cpu', action='store_true',
    #                     default=False,
    #                     help='use cpu (not recommended)')
    # args = parser.parse_args()
    #
    # model = init_model('fcanet', args.backbone,
    #                    './pretrained_model/fcanet-{}.pth'.format(
    #                        args.backbone),
    #                    if_cuda=not args.cpu)

    # anno = Annotator(img_path=args.input, model=model,
    #                  if_sis=args.sis,
    #                  if_cuda=not args.cpu,
    #                  save_path=args.output)