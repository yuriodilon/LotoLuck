from django import template

register = template.Library()

@register.filter
def get_bola(jogo, bola_num):
    """
    Retorna o valor da bola correspondente (e.g., bola1, bola2, ...).
    """
    return getattr(jogo, f"bola{bola_num}", None)
