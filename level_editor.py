from Level_Editor.scripts.editor import Editor

def main():
    #Runs the editor
    editor = Editor()
    editor.load('data/levels/world-1/underground1.json')
    editor.main_loop()

main()
