import sys
import numpy as np
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QFileDialog,QMessageBox

import cv2

class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 button - pythonspot.com'
        self.left = 500
        self.top = 400
        self.width = 320
        self.height = 200
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.button = QPushButton('Select Image', self)
        self.button.setToolTip('This is an example button')
        self.button.move(100, 70)
        self.button.clicked.connect(self.select_image)

        self.show()

    def select_image(self):
        filepath_starmap = QFileDialog.getOpenFileName(self, "Select Image","c\\",'Image files (*.jpg *.png)')
        starmap_name = filepath_starmap[0].split("/")[-1]
        starmap = cv2.imread(starmap_name)
        filepath_template = QFileDialog.getOpenFileName(self, "Select Template","c\\",'Image files (*.jpg *.png)')
        template_name = filepath_template[0].split("/")[-1]
        small_area = cv2.imread(template_name, 0)

        self.matching(starmap,small_area)

    def matching(self,starmap,small_area):
        img_gray = cv2.cvtColor(starmap, cv2.COLOR_BGR2GRAY)
        w, h = small_area.shape[::-1]

        res = cv2.matchTemplate(img_gray, small_area, cv2.TM_CCOEFF_NORMED)
        threshold = 0.8
        loc = np.where(res >= threshold)

        if (len(loc[0]) != 0):
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

            top_left = max_loc
            bottom_right = (top_left[0] + w, top_left[1] + h)

            cv2.rectangle(starmap, top_left, bottom_right, (151, 151, 0), 2)
            print('sol ust:',top_left)
            print('sag ust:',(top_left[0]+w, top_left[1]))
            print('sol alt:',(top_left[0], top_left[1]+h ))
            print('sag alt:',(top_left[0]+w, top_left[1]+h ))
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("Sol Üst:" + str(top_left) + '\n' + "Sağ Üst:" + str((top_left[0]+w, top_left[1])) + '\n' +
                        "Sol Alt:" + str((top_left[0], top_left[1]+h )) + '\n' +
                        "Sol Üst:" + str((top_left[0]+w, top_left[1]+h )))


            msg.exec_()

            cv2.imwrite('detected.jpg', starmap)
        else:
            print('Eşleşme bulunamadı.')
            small_area = cv2.rotate(small_area, cv2.ROTATE_90_COUNTERCLOCKWISE)
            self.matching(starmap, small_area)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())

