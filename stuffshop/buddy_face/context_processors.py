from buddy_face.models import ChineeseBuddy
import random


def show_buddyface(request):
    buddy = ChineeseBuddy.objects.get(id=random.randint(1,ChineeseBuddy.objects.count()))
    return {
        'buddy':buddy,
    }



