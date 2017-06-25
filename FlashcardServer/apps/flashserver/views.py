from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import Deck, Card

# Create your views here.
def index(req):
    all_decks = Deck.objects.all()
    all_cards = Card.objects.all()
    return render(req, 'flashserver/index.html', {"decks":all_decks, "cards":all_cards})

@csrf_exempt
def deck_index(req):
    if req.method == 'GET':
        all_decks = Deck.objects.all()
        return JsonResponse({"decks":[{"name":deck.name, "id":deck.id, "created_at":deck.created_at, "updated_at":deck.updated_at, "num_cards":deck.cards.count()} for deck in all_decks]}, safe=True)
    elif req.method == 'POST':
        new_deck = Deck.objects.validate(req.POST)
        if new_deck["success"]:
            return redirect(deck_target, id=new_deck["data"].id)
        else:
            return JsonResponse({"debug_name":"deck_index", "debug_method":"post", "data":new_deck["errors"].values()}, safe=True)

@csrf_exempt
def deck_target(req, id):
    if req.method == 'GET':
        try:
            deck = Deck.objects.get(id=id)
            return JsonResponse({"name":deck.name, "id":deck.id, "created_at":deck.created_at, "updated_at":deck.updated_at, "cards":list(deck.cards.all())}, safe=False)
        except Deck.DoesNotExist:
            return JsonResponse({"error":"Deck not found"})
    elif req.method == 'PUT':
        # TODO
        return JsonResponse({"debug_name":"deck_target", "id":id, "debug_method":"put"}, safe=True)
    elif req.method == 'DELETE':
        # TODO
        return JsonResponse({"debug_name":"deck_target", "id":id, "debug_method":"delete"}, safe=True)
    else:
        return JsonResponse({"debug_name":"deck_target", "id":id, "debug_method":"unknown"}, safe=True)


@csrf_exempt
def card_index(req):
    if req.method == 'GET':
        all_cards = Card.objects.all()
        return JsonResponse({"cards":[{"side1":card.side1, "side2":card.side2, "id":card.id, "created_at":card.created_at, "updated_at":card.updated_at, "deck_id":card.deck.id, "deck_name":card.deck.name} for card in all_cards]}, safe=True)
    elif req.method == 'POST':
        new_card = Card.objects.validate(req.POST)
        if new_card["success"]:
            #return redirect(card_target, id=new_card["data"].id)
            return redirect(index)
        else:
            return JsonResponse({"debug_name":"card_index", "debug_method":"post", "data":new_card["errors"].values()}, safe=True)

@csrf_exempt
def card_target(req, id):
    if req.method == 'GET':
        try:
            card = Card.objects.get(id=id)
            return JsonResponse({"side1":card.side1, "side2":card.side2, "id":card.id, "created_at":card.created_at, "updated_at":card.updated_at, "deck_id":card.deck.id, "deck_name":card.deck.name}, safe=False)
        except Card.DoesNotExist:
            return JsonResponse({"error":"Card not found"})
    elif req.method == 'PUT':
        # TODO
        return JsonResponse({"debug_name":"card_target", "id":id, "debug_method":"put"}, safe=True)
    elif req.method == 'DELETE':
        # TODO
        return JsonResponse({"debug_name":"card_target", "id":id, "debug_method":"delete"}, safe=True)
    else:
        return JsonResponse({"debug_name":"card_target", "id":id, "debug_method":"unknown"}, safe=True)
