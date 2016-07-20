import sys
from PyQt5.QtWidgets import QWidget, QLabel, QGridLayout, QApplication, QPushButton

class Home(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        grid = QGridLayout()

        editButton = QPushButton("Edit Ingredients")
        clearButton = QPushButton("Clear Ingredients")
        searchButton = QPushButton("Search")
        selectButton = QPushButton("Select")
        nextButton = QPushButton("Next")

        titleLabel = QLabel("   Title:")
        ingredientsLabel = QLabel("   Ingredients:")

        # Test with sample info
        title = QLabel('''<a href='http://allrecipes.com/Recipe/Chicken-Berry-Salad/Detail.aspx'>Chicken Berry Salad</a>''')
        title.setOpenExternalLinks(True)
        ingredients = QLabel("blueberies, chicken, cider vinegar, orange juice")
        thumbnail = "http://img.recipepuppy.com\/624118.jpg"

        grid.addWidget(editButton, 1, 0)
        grid.addWidget(clearButton, 2, 0)
        grid.addWidget(searchButton, 3, 0)

        grid.addWidget(titleLabel, 1, 1)
        grid.addWidget(ingredientsLabel, 2, 1)

        grid.addWidget(title, 1, 2)
        grid.addWidget(ingredients, 2, 2)

        grid.addWidget(selectButton, 3, 2)
        grid.addWidget(nextButton, 3, 3)

        self.setLayout(grid)

        self.setGeometry(300, 300, 700, 175)
        self.setWindowTitle("College Cooking")
        self.show()

if __name__ == '__main__':

    app = QApplication(sys.argv)
    home = Home()
    sys.exit(app.exec_())
