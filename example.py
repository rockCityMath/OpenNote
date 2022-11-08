
from models.Page import Page
from models.Notebook import Notebook
from models.DragItem import DragItem

def main():
    # nb = Notebook()
    # for i in range(3):
    #     nb.pages.append(Page('a'))
    
    # for i in range(3):
    #     page = nb.pages[i]
    #     page.items.add(DragItem((50,0)))
    # nb.title="somenameimadeuplol"
    # nb.pages[1].title="anotherone"

    # nb.save()
    


    test = Page('Page1')
    test.items.add(DragItem((20,10)))
    test.items.add(DragItem((30,40)))
    test.items.add(DragItem((30,40)))
    test2 = Page('Page2')
    test2.items.add(DragItem((230,10)))
    test2.items.add(DragItem((130,40)))
    
    nb = Notebook('Notebook')
    nb.pages.append(test)
    nb.pages.append(test2)
    nb.location="lefile.on"
    nb.save()
    note = Notebook()
    note.load('lefile.on')
    print(note.title)
    print(note.pages[0].title)
 
if __name__=="__main__":
	main()