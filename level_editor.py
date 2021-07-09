from Level_Editor.scripts.editor import Editor

def main():
    #Runs the editor
    editor = Editor()
    editor.load('data/levels/world-2/3.json')
    editor.main_loop()


main()
