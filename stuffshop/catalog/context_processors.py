from catalog.models import MenuNode

def show_navigation(request):
    return {
        'nodes':MenuNode.tree.all(),
    }



